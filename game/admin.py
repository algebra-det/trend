from django.contrib import admin
from .models import Game, Challenge, EventGame, Promotion

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title', 'id']

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'game']
    search_fields = ['title', 'id', 'game']


@admin.register(EventGame)
class EventAdmin(admin.ModelAdmin):
    list_display = ['game', 'id', 'game_id', 'total_participants']
    search_fields = ['game', 'id', 'game_id', 'total_participants']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'game', 'id', 'game_id', 'location_latitude', 'location_longitude']
    search_fields = ['title', 'game', 'id', 'game_id']


