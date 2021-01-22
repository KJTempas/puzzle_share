from django import forms
from .models import Puzzle

class NewPuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ('name',  'company', 'pieces')