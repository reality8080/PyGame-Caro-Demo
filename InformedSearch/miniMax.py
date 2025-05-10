from Function.checkWin import checkWin
from Function.isFullBoard import isBoardFull
# from MarkSquare import markSquare
from functools import lru_cache
# from copy import deepcopy
import numpy as np
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20

maxDepth = 3

class EvaluatedMiniMax:
    def __init__(self, board, boardRows, boardCols):
        self.board = board
        self.boardRows = boardRows
        self.boardCols = boardCols
        self.evaluator = CaroEvaluator20x20()
    
    def evaluate(self, player):
        opponent = 1 if player == 2 else 2
        score_player = self.evaluator.evaluate(self.board, player, self.boardRows, self.boardCols)
        score_opponent = self.evaluator.evaluate(self.board, opponent, self.boardRows, self.boardCols)
        return score_player - score_opponent

@lru_cache(maxsize=100000)
def evaluatedMiniMax(boardTuple, player, boardRows, boardCols):
    board = [list(row) for row in boardTuple]  # Create a copy
    evaluator = EvaluatedMiniMax(board, boardRows, boardCols)
    score = evaluator.evaluate(player)
    return score/1000

# def getCandidateMoves(board, boardRows, boardCols, distance=1, beamWidth=6, player=2):
#     candidates = set()
#     for row in range(boardRows):
#         for col in range(boardCols):
#             if board[row][col] != 0:
#                 for dr in range(-distance, distance + 1):
#                     for dc in range(-distance, distance + 1):
#                         r, c = row + dr, col + dc
#                         if 0 <= r < boardRows and 0 <= c < boardCols and board[r][c] == 0:
#                             candidates.add((r, c))
#     if not candidates:
#         center_row, center_col = boardRows // 2, boardCols // 2
#         if board[center_row][center_col] == 0:
#             candidates.add((center_row, center_col))
#         else:
#             for r in range(boardRows):
#                 for c in range(boardCols):
#                     if board[r][c] == 0:
#                         candidates.add((r, c))
#                         break
#     beamWidth = min(beamWidth, len(candidates))
#     if not candidates:
#         return []
#     boardTuple = tuple(tuple(row) for row in board)
#     scored = [(r, c, evaluateMove(r, c, boardTuple , player, boardRows, boardCols)) for r, c in candidates]
#     topMoves = sorted(scored, key=lambda x: x[2], reverse=True)[:beamWidth]
#     return [(r, c) for r, c, _ in topMoves]

def getCandidateMoves(board, boardRows, boardCols, distance=1, beamWidth=6, player=2):
    candidates = set()
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] != 0:
                for dr in range(-distance, distance + 1):
                    for dc in range(-distance, distance + 1):
                        r, c = row + dr, col + dc
                        if 0 <= r < boardRows and 0 <= c < boardCols and board[r][c] == 0:
                            candidates.add((r, c))
    
    # Nếu không có ứng viên, lấy tất cả ô trống
    if not candidates:
        for row in range(boardRows):
            for col in range(boardCols):
                if board[row][col] == 0:
                    candidates.add((row, col))
    
    beamWidth = min(beamWidth, len(candidates))
    if not candidates:
        return []
    
    boardTuple = tuple(tuple(row) for row in board)
    scored = [(r, c, evaluateMove(r, c, boardTuple, player, boardRows, boardCols)) for r, c in candidates]
    topMoves = sorted(scored, key=lambda x: x[2], reverse=True)[:beamWidth]
    # print("Candidate moves:", [(r, c, score) for r, c, score in topMoves])
    return [(r, c) for r, c, _ in topMoves]

@lru_cache(maxsize=100000)
def evaluateMove(row, col, boardTuple, player, boardRows, boardCols):
    board = [list(row) for row in boardTuple]  # Create a copy
    boardCopy = [row[:] for row in board]  # Deep copy of board
    boardCopy[row][col] = player
    if checkWin(boardCopy, player, boardRows, boardCols):
        return float('inf')
    score = evaluatedMiniMax(tuple(tuple(row) for row in boardCopy), player, boardRows, boardCols)
    return score

# def miniMax(board, boardRows, boardCols, depth, isMaximizing, alpha, beta,player):
#     if checkWin(board, 2, boardRows, boardCols):
#         return float('inf')
#     elif checkWin(board, 1, boardRows, boardCols):
#         return float('-inf')
#     elif isBoardFull(board, boardRows, boardCols):
#         return 0
    
#     if depth >= maxDepth:
#         return evaluatedMiniMax(tuple(tuple(row) for row in board), player, boardRows, boardCols)
#     moves = getCandidateMoves(board, boardRows, boardCols, player=player)
#     boardTuple = tuple(tuple(row) for row in board)
#     if isMaximizing:
#         bestScore = float('-inf')
#         scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, player, boardRows, boardCols)) for r, c in moves]
#         sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
#         for row, col, _ in sortedMoves:
#             if board[row][col] == 0:
#                 board[row][col] = 2
#                 score = miniMax(board, boardRows, boardCols, depth + 1, False, alpha, beta,player)
#                 board[row][col] = 0
#                 bestScore = max(bestScore, score)
#                 alpha = max(alpha, bestScore)
#                 if beta <= alpha:
#                     break
#         return bestScore
#     else:
#         bestScore = float('inf')
#         opponnent=1 if player==2 else 2
#         scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, opponnent, boardRows, boardCols)) for r, c in moves]
#         sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
#         for row, col, _ in sortedMoves:
#             if board[row][col] == 0:
#                 board[row][col] = opponnent
#                 score = miniMax(board, boardRows, boardCols, depth + 1, True, alpha, beta,player)
#                 board[row][col] = 0
#                 bestScore = min(bestScore, score)
#                 beta = min(beta, bestScore)
#                 if beta <= alpha:
#                     break
#         return bestScore

def miniMax(board, boardRows, boardCols, depth, isMaximizing, alpha, beta, player):
    if checkWin(board, 2, boardRows, boardCols):
        return float('inf')
    elif checkWin(board, 1, boardRows, boardCols):
        return float('-inf')
    elif isBoardFull(board, boardRows, boardCols):
        return 0
    
    if depth >= maxDepth:
        return evaluatedMiniMax(tuple(tuple(row) for row in board), player, boardRows, boardCols)
    
    moves = getCandidateMoves(board, boardRows, boardCols, player=player)
    boardTuple = tuple(tuple(row) for row in board)
    if isMaximizing:
        bestScore = float('-inf')
        scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, player, boardRows, boardCols)) for r, c in moves]
        sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
        for row, col, _ in sortedMoves:
            if board[row][col] == 0:
                board[row][col] = 2
                score = miniMax(board, boardRows, boardCols, depth + 1, False, alpha, beta, player)
                board[row][col] = 0
                assert board[row][col] == 0, f"Failed to reset board at ({row}, {col})"
                bestScore = max(bestScore, score)
                alpha = max(alpha, bestScore)
                if beta <= alpha:
                    break
        return bestScore
    else:
        bestScore = float('inf')
        opponent = 1 if player == 2 else 2
        scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, opponent, boardRows, boardCols)) for r, c in moves]
        sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
        for row, col, _ in sortedMoves:
            if board[row][col] == 0:
                board[row][col] = opponent
                score = miniMax(board, boardRows, boardCols, depth + 1, True, alpha, beta, player)
                board[row][col] = 0
                assert board[row][col] == 0, f"Failed to reset board at ({row}, {col})"
                bestScore = min(bestScore, score)
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break
        return bestScore

def bestMove(board, boardRows, boardCols, player=2):
    bestScore = float('-inf')
    move = None
    opponnent=3-player
    moves = getCandidateMoves(board, boardRows, boardCols, player=player)
    if not moves:
        return None
    
    boardTuple = tuple(tuple(row) for row in board)
    scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, player, boardRows, boardCols)) for r, c in moves]
    sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
    
    for row, col, _ in sortedMoves:
        if board[row][col] != 0:
            continue
        board[row][col] = player
        if checkWin(board, player, boardRows, boardCols):
            board[row][col] = 0
            return (row, col)
        board[row][col] = 0
        
        board[row][col] = opponnent
        if checkWin(board, opponnent, boardRows, boardCols):
            board[row][col] = 0
            return (row, col)
        board[row][col] = 0
        
        board[row][col] = player
        score = miniMax(board, boardRows, boardCols, 0, False, float('-inf'), float('inf'), player)
        board[row][col] = 0
        # assert board[row][col] == 0, f"Failed to reset board at ({row}, {col})"
        # print(f"Evaluated move ({row}, {col}) with score {score}")
        if score > bestScore:
            bestScore = score
            move = (row, col)

    return move