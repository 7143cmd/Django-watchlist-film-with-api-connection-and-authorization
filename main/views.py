from django.shortcuts import render
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm

#User = get_user_model()

def home(request):
    return render(request, 'main/index.html')
def register(request):
    form = RegisterForm()

    data = {"form": form}

    return render(request, 'main/register.html', data)
def login(request):
    form = LoginForm()

    data = {"form": form}

    return render(request, 'main/login.html', data)

# Create your views here.
