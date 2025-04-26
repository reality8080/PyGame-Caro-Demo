from checkWin import checkWin
from MarkSquare import markSquare
import numpy as np

def evaluateBoard(checkBoard, boardRows, boardCols):
    score = 0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col] == 2:  # AI
                score += 10
            elif checkBoard[row][col] == 1:  # Người chơi
                score -= 10

    if checkWin(checkBoard, 2, boardRows, boardCols):
        return 1000
    elif checkWin(checkBoard, 1, boardRows, boardCols):
        return -1000

    return score


def ucs(board, player, boardRows, boardCols):
    bestMove = None
    minCost = float('inf')

    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 0:
                board[row][col] = player  # Dùng player truyền vào
                cost = np.count_nonzero(board != 0)
                board[row][col] = 0

                if cost < minCost:
                    minCost = cost
                    bestMove = (row, col)

    if bestMove:
        return bestMove  # Trả về vị trí (row, col)
    return None


