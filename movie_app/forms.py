from django import forms

class ReviewForm(forms.Form):
    username = forms.CharField(label="Your Name", max_length=100, required=True)
    email = forms.EmailField(label="Your Email ID", required=True)
    movie_name = forms.CharField(label="Movie Name", max_length=200, required=True)
    release_year = forms.IntegerField(label="Release Year", required=True)
    genre = forms.ModelChoiceField(label = "genre", required = True)
