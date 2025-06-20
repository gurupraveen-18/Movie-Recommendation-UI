from django.contrib import admin
from django.urls import path
from . import views
from django.shortcuts import render

def show_loader(request):
    return render(request, 'movie_app/loader.html')

urlpatterns = [
    path('', views.index, name='home'),
    path('categories/', views.categories, name='categories'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('review/', views.review, name='review'),
    path('about/', views.about, name='about'),
    path('add-to-watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('clear-watchlist/', views.clear_watchlist, name='clear_watchlist'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path('loader/', show_loader, name='loader'),
]


