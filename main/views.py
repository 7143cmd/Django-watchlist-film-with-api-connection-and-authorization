from django.shortcuts import render

def home(request):
    return render(request, 'main/index.html')
def register(request):
    return render(request, 'main/register.html')
def login(request):
    return render(request, 'main/login.html')

# Create your views here.
