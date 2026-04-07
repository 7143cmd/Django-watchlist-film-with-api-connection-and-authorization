import requests
from random import randint, choice
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

#User = get_user_model()

@login_required(login_url='login')
def home(request):
    return render(request, 'main/index.html')

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

@login_required
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

    return render(request, 'main/search.html', {
        'results': results,
        'query': query
    })
# Create your views here.
