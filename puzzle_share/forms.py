from django import forms
from django.forms import FileInput
from .models import Puzzle

class NewPuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ('name',  'company', 'pieces', 'owner_last_name', 'photo')

class SearchForm(forms.Form):
    search_term = forms.CharField()


class NameForm(forms.Form):
    user_last_name = forms.CharField(label = 'User_last_name', max_length=20)


