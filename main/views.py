import requests
from django.http import JsonResponse
from random import randint, choice, sample
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Watchlist
from .forms import RegisterForm, LoginForm

API_URL = "https://api.imdbapi.dev/titles"

######

def get_titles(params):
    response = requests.get(API_URL, params=params)
    data = response.json().get("titles", [])

    filtered = [
        t for t in data
        if t.get("rating") and t["rating"].get("voteCount", 0) >= 10000
    ]

    return filtered


def get_random(items, cnt=4):
    return sample(items, min(len(items), cnt))

######
@login_required(login_url='login')
def home(request):
    watchlist = Watchlist.objects.filter(user=request.user).order_by('-date_added')[:5]

    movies = []

    for item in watchlist:
        url = f"https://api.imdbapi.dev/titles/{item.movie}"
        response = requests.get(url)
        data = response.json()

        movies.append({
            "id": item.movie,
            "title": data.get("primaryTitle"),
            "image": data.get("primaryImage", {}).get("url")
        })

    return render(request, 'main/index.html', {
        "watchlist": movies,
        "watchlist_ids": [m["id"] for m in movies]
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {"form": form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if not request.POST.get('remember_me'):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)

                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid login or password')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {"form": form})

def rand_movie(request):                       #https://api.imdbapi.dev/titles?startYear=2000&endYear=2010&minVoteCount=1000&minAggregateRating=5&sortBy=SORT_BY_POPULARITY

    start_year = randint(1950, 1990)
    end_year = randint(1991, 2025)
    agregate = randint(0, 7)

    url = f'https://api.imdbapi.dev/titles?startYear={start_year}&endYear={end_year}&minVoteCount=1000&minAggregateRating={agregate}'

    response = requests.get(url)
    data = response.json()

    movies = data.get('titles', [])

    if not movies:
        return redirect('')

    movie = choice(movies)
    imdb_id = movie['id']

    return redirect(f'https://www.imdb.com/title/{imdb_id}')

@login_required(login_url='login')
def search_mov(request, query):
    results = []

    if query:
        url = f"https://api.imdbapi.dev/search/titles?query={query}"

        try:
            response = requests.get(url)
            data = response.json()

            movies = data.get('titles', [])

            for movie in movies:
                rating = movie.get('rating')

                if not rating:
                    continue

                vote_count = rating.get('voteCount')

                if not vote_count or vote_count < 1000:
                    continue

                results.append(movie)

        except Exception:
            results = []

    user_watchlist = Watchlist.objects.filter(user=request.user).values_list('movie', flat=True)

    return render(request, 'main/search.html', {
        'results': results,
        'query': query,
        "watchlist_ids": list(user_watchlist)
    })

@login_required(login_url='login')
def movies(request):

    best = get_titles({
        "minAggregateRating": 8.9,
        "types": "MOVIE",
        "limit": 50
    })

    popular = get_titles({
        "sortBy": "SORT_BY_POPULARITY",
        "types": "MOVIE",
        "limit": 50
    })

    randoms = get_titles({
        "startYear": 2000,
        "endYear": 2010,
        "types": "MOVIE",
        "limit": 50
    })

    user_watchlist = Watchlist.objects.filter(user=request.user).values_list('movie', flat=True)

    return render(request, "main/movies.html", {
        "best": get_random(best),
        "popular": get_random(popular),
        "randoms": get_random(randoms),
        "watchlist_ids": list(user_watchlist)
    })

@login_required(login_url='login')
def series(request):
    best = get_titles({
        "minAggregateRating": 9.2,
        "types": "TV_SERIES",
        "limit": 50
    })

    popular = get_titles({
        "sortBy": "SORT_BY_POPULARITY",
        "types": "TV_SERIES",
        "limit": 50
    })

    randoms = get_titles({
        "startYear": 2010,
        "types": "TV_SERIES",
        "limit": 50
    })

    user_watchlist = Watchlist.objects.filter(user=request.user).values_list('movie', flat=True)

    return render(request, "main/series.html", {
        "best": get_random(best),
        "popular": get_random(popular),
        "randoms": get_random(randoms),
        "watchlist_ids": list(user_watchlist)
    })

@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")

        if not movie_id:
            return JsonResponse({"status": "error"})

        obj = Watchlist.objects.filter(
            user=request.user,
            movie=movie_id
        ).first()

        if obj:
            obj.delete()
            return JsonResponse({"status": "removed"})

        Watchlist.objects.create(
            user=request.user,
            movie=movie_id
        )

        return JsonResponse({"status": "added"})

    return JsonResponse({"status": "error"})

@login_required(login_url='login')
def profile(request):

    watchlist_qs = Watchlist.objects.filter(
        user=request.user
    ).order_by('-date_added')

    movies = []

    for item in watchlist_qs:
        url = f"https://api.imdbapi.dev/titles/{item.movie}"
        response = requests.get(url)
        data = response.json()

        movies.append({
            "id": item.movie,
            "title": data.get("primaryTitle"),
            "image": data.get("primaryImage", {}).get("url")
        })

    content = {
        'user': request.user,
        'watchlist': movies,
        'watchlist_ids': [m["id"] for m in movies]
    }

    return render(request, 'main/profile.html', content)
# Create your views here.
