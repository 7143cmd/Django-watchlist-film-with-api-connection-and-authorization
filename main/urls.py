from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('registration/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('random/', views.rand_movie, name='random'),
    path('search/<str:query>/', views.search_mov, name='search')
]
