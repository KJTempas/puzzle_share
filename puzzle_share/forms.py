from django import forms
from .models import Puzzle

class NewPuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ('name',  'company', 'pieces', 'owner_last_name')

class SearchForm(forms.Form):
    search_term = forms.CharField()