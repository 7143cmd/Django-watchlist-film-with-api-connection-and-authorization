from django.shortcuts import render
from django.contrib.auth import get_user_model

#User = get_user_model()

def home(request):
    return render(request, 'main/index.html')
def register(request):
    return render(request, 'main/register.html')
def login(request):
    return render(request, 'main/login.html')

# Create your views here.
