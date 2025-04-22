from checkWin import checkWin
from MarkSquare import markSquare

def heuristic(board, player, rows, cols):
    score = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player:
                score += 10
            elif board[r][c] == 3 - player:
                score -= 10

    if checkWin(player, board):
        return 1000
    elif checkWin(3 - player, board):
        return -1000

    return score

def DeepHillClimbing(board, boardRows, boardCols, player=2):
    best_score = heuristic(board, player, boardRows, boardCols)
    best_move = None

    for r in range(boardRows):
        for c in range(boardCols):
            if board[r][c] == 0:
                board[r][c] = player
                score = heuristic(board, player, boardRows, boardCols)
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                board[r][c] = 0  

    if best_move is not None:
        r, c = best_move
        markSquare(board, r, c, player)
        return True
    else:
        return False
