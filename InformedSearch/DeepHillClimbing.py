from checkWin import checkWin
from MarkSquare import markSquare
import random

def heuristic(board, player, rows, cols):
    score = 0
    opponent = 3 - player

    if checkWin(player, board):
        return 1000
    elif checkWin(opponent, board):
        return -1000

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player:
                score += 10
            elif board[r][c] == opponent:
                score -= 10

    return score

def DeepHillClimbing(board, boardRows, boardCols, player=2):
    current_score = heuristic(board, player, boardRows, boardCols)
    best_score = current_score
    best_moves = []

    for r in range(boardRows):
        for c in range(boardCols):
            if board[r][c] == 0:
                board[r][c] = player
                score = heuristic(board, player, boardRows, boardCols)
                if score > best_score:
                    best_score = score
                    best_moves = [(r, c)]
                elif score == best_score:
                    best_moves.append((r, c))
                board[r][c] = 0

    if best_moves:
        r, c = random.choice(best_moves) 
        markSquare(board, r, c, player)
        return True
    else:
        empty = [(r, c) for r in range(boardRows) for c in range(boardCols) if board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            markSquare(board, r, c, player)
            return True
        return False
