from django.contrib import admin
from django.urls import path
from games.views import home, chess_game, tic_tac_toe, memory_game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('chess/', chess_game, name='chess'),
    path('tictactoe/', tic_tac_toe, name='tictactoe'),
    path('memory/', memory_game, name='memory'),
]