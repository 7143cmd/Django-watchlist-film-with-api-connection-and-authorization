from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('registration/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('random/', views.rand_movie, name='random'),
    path('movies/', views.movies, name='movies'),
    path('series/', views.series, name='series'),
    path('watchlist/add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('search/<str:query>/', views.search_mov, name='search'),
    path('profile', views.profile, name='profile')

]
