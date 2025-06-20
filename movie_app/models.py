from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre)
    languages = models.ManyToManyField(Language)
    rating = models.FloatField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)  # allows optional image upload
    link = models.URLField(default='https://example.com')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class OTTPlatform(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='ott_logos/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ott_links')
    link = models.URLField(default='https://example.com')

    def __str__(self):
        return f"{self.name} - {self.movie.title}"
