from django.contrib import admin

from game.models import MagicBox, Trophy


@admin.register(MagicBox)
class MagicBoxAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title', 'id']


@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title', 'id']