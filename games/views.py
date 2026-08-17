from django.shortcuts import render
import random

# الصفحة الرئيسية
def home(request):
    return render(request, 'home.html')

# 1. لعبة الشطرنج (Chess Board)
def chess_game(request):
    # إعداد رقعة الشطرنج الافتراضية
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
        r = int(request.POST.get('row'))
        c = int(request.POST.get('col'))
        
        if selected is None:
            if board[r][c] != "":
                request.session['selected'] = [r, c]
        else:
            sr, sc = selected
            board[r][c] = board[sr][sc]
            board[sr][sc] = ""
            request.session['selected'] = None
            request.session['chess_board'] = board

    return render(request, 'chess.html', {
        'board': request.session['chess_board'],
        'selected': request.session.get('selected')
    })

# 2. لعبة إكس أو (Tic-Tac-Toe)
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
        if board[move] == "":
            board[move] = "X"
            winner = check_winner(board)
            if winner == "X":
                request.session['status'] = "مبروك! أنت الفائز 🎉"
                request.session['game_over'] = True
            elif winner == "Tie":
                request.session['status'] = "تعادل!"
                request.session['game_over'] = True
            else:
                empty = [i for i, v in enumerate(board) if v == ""]
                if empty:
                    bot_move = random.choice(empty)
                    board[bot_move] = "O"
                    winner = check_winner(board)
                    if winner == "O":
                        request.session['status'] = "الكمبيوتر فاز 💻"
                        request.session['game_over'] = True

            request.session['board'] = board

    return render(request, 'tictactoe.html', {
        'board': request.session['board'],
        'status': request.session['status'],
        'game_over': request.session.get('game_over')
    })

# 3. لعبة مطابقة بطاقات الذاكرة (Memory Game)
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
        if idx not in matched and idx not in flipped:
            if len(flipped) == 2:
                flipped = [idx]
            else:
                flipped.append(idx)
                if len(flipped) == 2:
                    if cards[flipped[0]] == cards[flipped[1]]:
                        matched.extend(flipped)
            request.session['flipped'] = flipped
            request.session['matched'] = matched

    return render(request, 'memory.html', {
        'cards': cards,
        'flipped': flipped,
        'matched': matched,
        'won': len(matched) == len(cards)
    })