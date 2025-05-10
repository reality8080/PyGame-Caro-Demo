from Function.checkWin import checkWin
from Function.MarkSquare import markSquare
import random

def heuristic(board, player, boardRows,boardCols):
    score = 0
    opponent = 3 - player

    if checkWin(board,player,boardRows,boardCols):
        return 1000
    elif checkWin(board,opponent,boardRows,boardCols):
        return -1000

    for r in range(boardRows):
        for c in range(boardCols):
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
        # return True
        return (r,c)
    else:
        empty = [(r, c) for r in range(boardRows) for c in range(boardCols) if board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            return (r,c)
        return None
