from django.contrib import admin
from .models import Game, GameScore

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'game_name', 'result', 'played_at')
    list_filter = ('game_name', 'played_at')