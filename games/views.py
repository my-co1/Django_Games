from django.shortcuts import render
import random
from datetime import datetime
from .models import Game, GameScore

def home(request):
    # جلب الألعاب من قاعدة البيانات، وإن لم توجد يتم إنشاؤها تلقائياً لأول مرة
    if not Game.objects.exists():
        Game.objects.create(title="Chess Board Simulator", category="Strategy", description="Interactive 8x8 chessboard simulator with live piece moving mechanics")
        Game.objects.create(title="Tic Tac Toe", category="Classic", description="Play against the server logic and test your winning moves")
        Game.objects.create(title="Card Memory Match", category="Puzzle", description="Match pairs of hidden cards to test and enhance your memory power")

    games_list = Game.objects.all()
    recent_scores = GameScore.objects.all().order_by('-played_at')[:5]  # آخر 5 نتائج مسجلة

    return render(request, 'home.html', {
        'games': games_list,
        'recent_scores': recent_scores,
        'today': datetime.now(),
        'user_name': request.GET.get('name', 'player')
    })

def chess_game(request):
    initial_board = [
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    ]
    if 'chess_board' not in request.session or request.GET.get('reset'):
        request.session['chess_board'] = initial_board
        request.session['selected'] = None

    board = request.session['chess_board']
    selected = request.session.get('selected')

    if request.method == "POST":
        pos = request.POST.get('pos', '').split(',')
        if len(pos) == 2:
            r, c = int(pos[0]), int(pos[1])
            if selected is None:
                if board[r][c] != "":
                    request.session['selected'] = [r, c]
            else:
                sr, sc = selected
                board[r][c] = board[sr][sc]
                board[sr][sc] = ""
                request.session['selected'] = None
                request.session['chess_board'] = board
                request.session.modified = True

    return render(request, 'chess.html', {
        'board': request.session['chess_board'],
        'selected': request.session.get('selected')
    })

def tic_tac_toe(request):
    if 'board' not in request.session or request.GET.get('reset'):
        request.session['board'] = [""] * 9
        request.session['game_over'] = False
        request.session['status'] = "دورك للعب (X)"

    board = request.session['board']
    game_over = request.session.get('game_over', False)

    def check_winner(b):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for x, y, z in wins:
            if b[x] and b[x] == b[y] == b[z]:
                return b[x]
        if "" not in b:
            return "Tie"
        return None

    if request.method == "POST" and not game_over:
        move = int(request.POST.get('cell'))
        player_name = request.POST.get('player_name', 'Player')
        if board[move] == "":
            board[move] = "X"
            winner = check_winner(board)
            if winner == "X":
                request.session['status'] = "مبروك! أنت الفائز 🎉"
                request.session['game_over'] = True
                # تسجيل الفوز في قاعدة البيانات
                GameScore.objects.create(player_name=player_name, game_name="Tic Tac Toe", result="Win 🎉")
            elif winner == "Tie":
                request.session['status'] = "تعادل!"
                request.session['game_over'] = True
                GameScore.objects.create(player_name=player_name, game_name="Tic Tac Toe", result="Tie 🤝")
            else:
                empty = [i for i, v in enumerate(board) if v == ""]
                if empty:
                    bot_move = random.choice(empty)
                    board[bot_move] = "O"
                    winner = check_winner(board)
                    if winner == "O":
                        request.session['status'] = "الكمبيوتر فاز 💻"
                        request.session['game_over'] = True
                        GameScore.objects.create(player_name=player_name, game_name="Tic Tac Toe", result="Loss 💻")

            request.session['board'] = board
            request.session.modified = True

    return render(request, 'tictactoe.html', {
        'board': request.session['board'],
        'status': request.session['status'],
        'game_over': request.session.get('game_over')
    })

def memory_game(request):
    icons = ['🚀', '🎮', '🐍', '💻', '🔒', '⭐']
    if 'memory_cards' not in request.session or request.GET.get('reset'):
        cards = icons * 2
        random.shuffle(cards)
        request.session['memory_cards'] = cards
        request.session['flipped'] = []
        request.session['matched'] = []

    cards = request.session['memory_cards']
    flipped = request.session.get('flipped', [])
    matched = request.session.get('matched', [])

    if request.method == "POST":
        idx = int(request.POST.get('card_idx'))
        player_name = request.POST.get('player_name', 'Player')
        if idx not in matched and idx not in flipped:
            if len(flipped) == 2:
                flipped = [idx]
            else:
                flipped.append(idx)
                if len(flipped) == 2:
                    if cards[flipped[0]] == cards[flipped[1]]:
                        matched.extend(flipped)
                        if len(matched) == len(cards):
                            # تسجيل إتمام اللعبة في الداتابيز
                            GameScore.objects.create(player_name=player_name, game_name="Memory Match", result="Completed 🏆")
            request.session['flipped'] = flipped
            request.session['matched'] = matched
            request.session.modified = True

    return render(request, 'memory.html', {
        'cards': cards,
        'flipped': flipped,
        'matched': matched,
        'won': len(matched) == len(cards)
    })