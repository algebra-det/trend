from django import forms
from .models import MagicBox, Trophy

from django.core.exceptions import ValidationError

class MagicBoxForm(forms.ModelForm):
    class Meta:
        model = MagicBox
        fields = '__all__'
        exclude = ['created_at','updated_at']
        labels = {
        "title": "Titolo",
        'image': 'Immagine del gioco',
        'points': 'Punti'
        }


class TrophyForm(forms.ModelForm):
    class Meta:
        model = Trophy
        fields = '__all__'
        exclude = ['created_at','updated_at']
        labels = {
        "title": "Titolo",
        'image': 'Immagine del gioco',
        'points': 'Punti'
        }