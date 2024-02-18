from django import forms
from .models import Game, Challenge, Promotion

from django.core.exceptions import ValidationError

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        exclude = ['created_at','updated_at', 'ended', 'joined_players']
        labels = {
        "title": "Titolo",
        'category': 'Tipo di gioco',
        'description': 'Descrizione',
        'location_name': 'Posizione',
        'location_latitude': 'Posizione Latitudine',
        'location_longitude': 'Posizione Longitudine',
        'clue': 'Traccia',
        'brief': 'breve',
        'total_point': 'Punti totali',
        'min_players':  'Partecipanti obbligatori',
        'difficulty': 'Difficoltà',
        'start_date': "Data d'inizio",
        'end_date': "Data di fine",
        'rules_yes': 'Regole del gioco : sì',
        'rules_no': 'Regole del gioco : No',
        'image': 'Immagine del gioco 1',
        'image1': 'Immagine del gioco 2',
        'image2': 'Immagine del gioco 3',
        'image3': 'Immagine del gioco 4',
        'status': 'stato',

        }

    def clean(self):
        cd = super(GameForm, self).clean()
        title = cd['title']
        # if Game.objects.filter(title=title).exists():
        #     raise ValidationError('Gioco con questo nome Esiste già! Per favore scegline un altro')

        category = cd.get('category')
        min_players = cd.get('min_players')
        if category == 'Event' and  (min_players == 0 or min_players == 1):
            raise ValidationError('In caso di eventi, ci devono essere più di 1 giocatore')
        if category == 'Classic' and min_players !=0:
            raise ValidationError('In Case of Classic, non ci possono essere giocatori richiesti, quindi rendilo 0')
        if not cd.get('location_latitude') or not cd.get('location_longitude'):
            raise ValidationError('Si prega di scegliere Nome località dalle Opzioni')

        return cd


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        exclude = ['game', 'created_at', 'updated_at']

    def clean(self):
        cd = super(PromotionForm, self).clean()

        if not cd.get('location_latitude') or not cd.get('location_longitude'):
            raise ValidationError('Si prega di scegliere Nome località dalle Opzioni.')

        return cd

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ChallengeForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['magic_box'].required = True

    def clean(self):
        cd = super(ChallengeForm, self).clean()
        object_type = cd.get('object_type', None)
        if object_type:
            if not cd.get('trophy', None):
                raise ValidationError('Se è selezionato il tipo di oggetto, devi selezionare anche il trofeo.')
        trophy = cd.get('trophy', None)
        if trophy:
            if not cd.get('object_type', None):
                raise ValidationError('Se viene selezionato il trofeo, devi selezionare anche il tipo di oggetto.')

        if not cd.get('location_latitude') or not cd.get('location_longitude'):
            raise ValidationError('Si prega di scegliere Nome località dalle Opzioni')

        return cd