from checkWin import checkWin
from isFullBoard import isBoardFull
from MarkSquare import markSquare
from functools import lru_cache
# import hashlib
from copy import deepcopy

# from concurrent.futures import ThreadPoolExecutor
import numpy as np
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20

# # from functools import lru_cache

# # Do sau
maxDepth=3
# # Moi do sau chon ra
# beamWidth=3

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
    
# def evaluatedMiniMax(checkBoard,player, boardRows,boardCols):
#     myEvaluator = EvaluatedMiniMax(checkBoard, boardRows, boardCols)
#     return myEvaluator.evaluate(player)


# def boardToStr(board):
#     return ''.join(str(cell) for row in board for cell in row)

def boardToKey(board):
    return tuple(tuple(row) for row in board)


@lru_cache(maxsize=100000)
def evaluatedMiniMax(boardTuple, player, boardRows, boardCols):
    board=[list(row) for row in boardTuple]  # Tạo bản sao
    evaluator = EvaluatedMiniMax(board, boardRows, boardCols)
    score = evaluator.evaluate(player)
    return score


def getCandidateMoves(board, boardRows, boardCols, distance=1, beamWidth=6,player=2):
    candidates = set()
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] !=0 :
                for dr in range(-distance, distance + 1):
                    for dc in range(-distance, distance + 1):
                        r, c = row + dr, col + dc
                        if 0 <= r < boardRows and 0 <= c < boardCols and board[r][c] == 0:
                            candidates.add((r, c))
    if not candidates:
    # Thêm ô trung tâm hoặc các ô ngẫu nhiên
        center_row, center_col = boardRows // 2, boardCols // 2
        if board[center_row][center_col] == 0:
            candidates.add((center_row, center_col))
        else:
            # found=False
            for r in range(boardRows):
                for c in range(boardCols):
                    if board[r][c] == 0:
                        candidates.add((r, c))
                        found=True
                        break
                # if found:
                #     break
    scored = [(r, c, evaluateMove(r, c, tuple(tuple(row)for row in board), player, boardRows, boardCols)) for r, c in candidates]
    topMoves = sorted(scored, key=lambda x: x[2], reverse=True)[:beamWidth]
    return [(r, c) for r, c, _ in topMoves]

# def evaluateMove(row, col, board, player, boardRows, boardCols):
#     board[row][col] = player
#     score = evaluatedMiniMax(board, player, boardRows, boardCols)
#     board[row][col] = 0
#     return score

# def evaluateMove(row, col, board, player, boardRows, boardCols):
#     board_copy = [r[:] for r in board]
#     board_copy[row][col] = player
    
#     # Nếu là nước thắng -> trả về điểm tuyệt đối
#     if checkWin(board_copy, player, boardRows, boardCols):
#         return float('inf')
    
#     return evaluatedMiniMax(board_copy, player, boardRows, boardCols)



# @lru_cache(maxsize=100000)
# def cachedEvaluateMove(row, col, boardKey, player, boardRows, boardCols):
#     board = [list(r) for r in boardKey]
#     board[row][col] = player
#     score = evaluatedMiniMax(board, player, boardRows, boardCols)
#     return score
@lru_cache(maxsize=100000)
def evaluateMove(row, col, boardTuple, player, boardRows, boardCols):
    board = [list(row) for row  in boardTuple]  # Tạo bản sao
    boardCopy = [row[:] for row in board]  # Tạo bản sao sâu của board
    boardCopy[row][col] = player
    if checkWin(boardCopy, player, boardRows, boardCols):
        return float('inf')
    score = evaluatedMiniMax(tuple(tuple(row) for row in boardCopy), player, boardRows, boardCols)
    boardCopy[row][col] = 0  # Khôi phục lại ô
    return score

def miniMax(board, boardRows, boardCols,depth,isMaximizing,alpha,beta):
    if checkWin(board,2,boardRows,boardCols):
        return float('inf')
    elif checkWin(board,1,boardRows,boardCols):
        return float('-inf')
    elif isBoardFull(board,boardRows, boardCols):
        return 0
    
    if depth>=maxDepth:
        return evaluatedMiniMax(tuple(tuple(row) for row in board),2,boardRows,boardCols)
    
    boardTuple=tuple(tuple(row) for row in board)  
    if isMaximizing:
        bestScore=float('-inf')
        moves=getCandidateMoves(board, boardRows, boardCols,player=2)
        print("Candidate Moves:", moves)

        scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, 2, boardRows, boardCols)) for r, c in moves]
        sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
        for row, col,_ in sortedMoves:
                if board[row][col] == 0:
                    board[row][col] = 2
                    # if checkWin(board, 2, boardRows, boardCols):
                    #     board[row][col] = 0
                    #     return float('inf')
                    score = miniMax(board, boardRows, boardCols, depth + 1, False,alpha,beta)
                    board[row][col] = 0
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore=float('inf')
        moves=getCandidateMoves(board, boardRows, boardCols,player=1)
        print("Candidate Moves:", moves)
        scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, 1, boardRows, boardCols)) for r, c in moves]
        sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
        for row, col,_ in sortedMoves:
                if board[row][col] == 0:
                    board[row][col] = 1
                    # if checkWin(board, 1, boardRows, boardCols):
                    #     board[row][col] = 0
                    #     return float('-inf')
                    score = miniMax(board, boardRows, boardCols, depth + 1, True,alpha,beta)
                    board[row][col] = 0
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break        
        return bestScore
    
def bestMoves(board,boardRows,boardCols):
    bestScore=float('-inf')
    move=(-1,-1)
    boardCopy = deepcopy(board) # Tạo bản sao
    moves=getCandidateMoves(boardCopy, boardRows, boardCols,player=2)
    if not moves:
        print("No valid moves found.")
        return False
    print("Candidate Moves:", moves)
    
    boardTuple=tuple(tuple(row) for row in boardCopy)
    scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, 2, boardRows, boardCols)) for r, c in moves]
    sortedMoves=sorted(scoredMoves,key=lambda x:x[2],reverse=True)
    for row, col,_ in sortedMoves:
        if board[row][col]==0:
            board[row][col]=2
            score=miniMax(board,boardRows,boardCols,0,False,float('-inf'),float('inf'))
            board[row][col]=0
            if score > bestScore:
                bestScore=score
                move=(row,col)
    
    if move!=(-1,-1):
        markSquare(board,move[0],move[1],2)
        return True
    print("No move selected.")

    return False


# def iterativeDeepeningMiniMax(board, boardRows, boardCols, maxTime):
#     import time
#     start_time = time.time()
#     best_move = (-1, -1)
#     best_score = float('-inf')
#     depth = 1
#     while time.time() - start_time < maxTime:
#         score, move = miniMaxWithDepth(board, boardRows, boardCols, depth)
#         if score > best_score:
#             best_score = score
#             best_move = move
#         depth += 1
#     return best_move