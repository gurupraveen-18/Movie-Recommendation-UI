from django.shortcuts import render, redirect
from .models import Movie, Genre, Language
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from random import sample
from django.utils.safestring import mark_safe
import json
from django.core.mail import send_mail
from django.conf import settings



def index(request):
    movies = Movie.objects.all()
    return render(request, "movie_app/index.html", {"movies": movies})
  # make sure this import is at the top


def categories(request):
    all_genres = Genre.objects.all()
    movies_by_genre = {}

    selected_genre_id = request.GET.get('genre', '')
    selected_language = request.GET.get('language', '')
    selected_rating = request.GET.get('rating', '')
    search_query = request.GET.get('search', '')

    featured_movie = None
    carousel_movies = []
    filtered_results = []
    filters_applied = any([selected_genre_id, selected_language, selected_rating, search_query])

    for genre in all_genres:
        movies = Movie.objects.filter(genres=genre)

        if selected_language:
            movies = movies.filter(languages__id=selected_language)

        if selected_rating:
            try:
                movies = movies.filter(rating__gte=float(selected_rating))
            except ValueError:
                pass

        if search_query:
            movies = movies.filter(title__icontains=search_query)

        movies = movies.distinct()
        movies_by_genre[genre] = movies

        if not featured_movie and movies.exists():
            featured_movie = movies.first()

        carousel_movies += list(movies[:10])

        # Collect all movies across genres for filtered result grid
        if filters_applied:
            filtered_results += list(movies)

    # Ensure carousel movies are random, unique, and max 3
    carousel_movies = list(set(carousel_movies))
    carousel_movies = sample(carousel_movies, min(3, len(carousel_movies)))

    carousel_data = [
        {
            'title': movie.title,
            'poster': movie.poster.url if movie.poster else ''
        }
        for movie in carousel_movies
    ]

    context = {
        'carousel_json': mark_safe(json.dumps(carousel_data)),
        'movies_by_genre': movies_by_genre,
        'featured_movie': featured_movie,
        'carousel_movies': carousel_movies,
        'genres': all_genres,
        'selected_genre_id': selected_genre_id,
        'selected_language': selected_language,
        'selected_rating': selected_rating,
        'search_query': search_query,
        'languages': Language.objects.all(),

        # ✅ Newly added:
        'filters_applied': filters_applied,
        'filtered_results': filtered_results,
    }

    # Filtered results shown below carousel (deduplicated and filtered correctly)
    filtered_results = Movie.objects.all()

    if selected_genre_id or selected_language or selected_rating or search_query:
        if selected_genre_id:
            filtered_results = filtered_results.filter(genres__id=selected_genre_id)
        if selected_language:
            filtered_results = filtered_results.filter(languages__id=selected_language)
        if selected_rating:
            try:
                filtered_results = filtered_results.filter(rating__gte=float(selected_rating))
            except ValueError:
                pass
        if search_query:
            filtered_results = filtered_results.filter(title__icontains=search_query)

        filtered_results = filtered_results.distinct()

        context["filtered_results"] = filtered_results
    else:
        context["filtered_results"] = None


    return render(request, "movie_app/categories.html", context)




def watchlist(request):
    watchlist = request.session.get('watchlist', [])
    movies = Movie.objects.filter(id__in=watchlist)
    return render(request, "movie_app/watchlist.html", {"movies": movies})



def add_to_watchlist(request, movie_id):
    watchlist = request.session.get('watchlist', [])
    if movie_id not in watchlist:
        watchlist.append(movie_id)
        request.session['watchlist'] = watchlist
        messages.success(request, 'Added to Watchlist ✅')
    else:
        messages.info(request, 'Already in Watchlist ℹ️')
    return redirect('home')

    

def remove_from_watchlist(request, movie_id):
    watchlist = request.session.get('watchlist', [])
    if movie_id in watchlist:
        watchlist.remove(movie_id)
        request.session['watchlist'] = watchlist
    return redirect('watchlist')

def clear_watchlist(request):
    request.session['watchlist'] = []
    return redirect('watchlist')
    


def review(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('usermailid')
        movie_name = request.POST.get('movie_name')
        release_year = request.POST.get('release_year')
        genre = request.POST.get('genre')

        # Email content
        subject = "🎬 New Movie Suggestion from a User"
        message = (
            f"User Name: {name}\n"
            f"User Email: {email}\n"
            f"Movie Name: {movie_name}\n"
            f"Release Year: {release_year}\n"
            f"Genre: {genre}"
        )

        admin_email = settings.ADMIN_EMAIL  # Ensure this is set in settings.py

        # Send email to admin
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])

        messages.success(request, "✅ Your Request Submitted Successfully!")
        return redirect('review')  # or use render with empty fields to reset

    return render(request, 'movie_app/review.html')



def about(request):
    return render(request, "movie_app/about.html")




def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genres=genre)

    context = {
        'genre': genre,
        'movies': movies,
    }
    return render(request, 'movie_app/genre_detail.html', context)
