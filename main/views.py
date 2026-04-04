from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

#User = get_user_model()

def home(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {"form": form})

def login(request):
    form = LoginForm()

    data = {"form": form}

    return render(request, 'main/login.html', data)

# Create your views here.
