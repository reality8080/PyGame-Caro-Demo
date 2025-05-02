from checkWin import checkWin
from MarkSquare import markSquare
from collections import deque


def evaluateBoard(checkBoard, boardRows, boardCols):
    score = 0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col] == 2:  # AI
                score += 10
            elif checkBoard[row][col] == 1:  # Người chơi
                score -= 10
    if checkWin(checkBoard, 2):
        return 1000
    elif checkWin(checkBoard, 1):
        return -1000
    return score


def backtrack(board, boardRows, boardCols, isAI, bestMove=None):
    if checkWin(board, 2):
        return 1000, bestMove
    elif checkWin(board, 1):
        return -1000, bestMove

    validMoves = []
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 0:
                validMoves.append((row, col))

    if not validMoves:
        return 0, bestMove

    maxScore = -float('inf') if isAI else float('inf')
    optimalMove = None

    for move in validMoves:
        row, col = move
        board[row][col] = 2 if isAI else 1
        score, _ = backtrack(board, boardRows, boardCols, not isAI, bestMove)
        board[row][col] = 0

        if isAI and score > maxScore:
            maxScore = score
            optimalMove = move
        elif not isAI and score < maxScore:
            maxScore = score
            optimalMove = move

    return maxScore, optimalMove


def bestMoveBacktracking(board, boardRows, boardCols):
    _, bestMove = backtrack(board, boardRows, boardCols, True)
    if bestMove:
        markSquare(board, bestMove[0], bestMove[1], 2)
        return True
    return False
