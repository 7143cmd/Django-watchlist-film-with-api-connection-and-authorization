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

# Create your views here.
