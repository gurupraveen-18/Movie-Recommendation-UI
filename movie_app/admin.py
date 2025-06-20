from django.contrib import admin
from movie_app import models  # Import the whole models module to avoid circular import

class OTTPlatformInline(admin.TabularInline):
    model = models.OTTPlatform
    extra = 1
    fields = ['name', 'logo', 'link']
    verbose_name_plural = "OTT Platforms"

@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'rating']
    search_fields = ['title']
    list_filter = ['release_year', 'genres', 'languages']
    inlines = [OTTPlatformInline]
    filter_horizontal = ['genres', 'languages']

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.OTTPlatform)
class OTTPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'link']
