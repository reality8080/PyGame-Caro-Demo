from checkWin import checkWin
from isFullBoard import isBoardFull
from MarkSquare import markSquare
from concurrent.futures import ThreadPoolExecutor
import numpy as np
# # from functools import lru_cache

# # Do sau
maxDepth=3
# # Moi do sau chon ra
# beamWidth=3

def getCandidateMoves(board, boardRows, boardCols, distance=2):
    candidates = set()
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] != 0:
                for dr in range(-distance, distance + 1):
                    for dc in range(-distance, distance + 1):
                        r, c = row + dr, col + dc
                        if 0 <= r < boardRows and 0 <= c < boardCols and board[r][c] == 0:
                            candidates.add((r, c))
    return list(candidates)


def evaluateBoard(checkBoard,boardRows,boardCols):
    score = 0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col] == 2:  # AI
                score += 10
                if (row>=boardRows//2-1 and 
                    row <=boardRows//2+1 and 
                    col >=boardCols//2-1 and 
                    col <= boardCols//2+1):
                    score+=5
            elif checkBoard[row][col] == 1:  # Người chơi
                score -= 10
    if checkWin( checkBoard,2,boardRows,boardCols):
        return float('inf')
    elif checkWin( checkBoard,1,boardRows,boardCols):
        return float('-inf')
    return score

def moveHeuristic(row, col, boardRows, boardCols):
    centerRow, centerCol = boardRows // 2, boardCols // 2
    return -((row - centerRow) ** 2 + (col - centerCol) ** 2)  # càng gần trung tâm càng tốt


def miniMax(board, boardRows, boardCols,depth,isMaximizing,alpha,beta):
    if checkWin(board,2,boardRows,boardCols):
        return float('inf')
    elif checkWin(board,1,boardRows,boardCols):
        return float('-inf')
    elif isBoardFull(board,boardRows, boardCols):
        return 0
    
    if depth>=maxDepth:
        return evaluateBoard(board,boardRows,boardCols)
    
    if isMaximizing:
        bestScore=-float('inf')
        moves=getCandidateMoves(board, boardRows, boardCols)
        sortedMoves=sorted(moves,key=lambda x:moveHeuristic(x[0],x[1],boardRows,boardCols))
        for row, col in sortedMoves:
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = miniMax(board, boardRows, boardCols, depth + 1, False,alpha,beta)
                    board[row][col] = 0
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore=float('inf')
        moves=getCandidateMoves(board, boardRows, boardCols)
        sortedMoves=sorted(moves,key=lambda x:moveHeuristic(x[0],x[1],boardRows,boardCols))
        for row, col in sortedMoves:
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = miniMax(board, boardRows, boardCols, depth + 1, True,alpha,beta)
                    board[row][col] = 0
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break        
        return bestScore
    
def bestMoves(board,boardRows,boardCols):
    bestScore=-1000
    move=(-1,-1)
    
    moves=getCandidateMoves(board, boardRows, boardCols)
    sortedMoves=sorted(moves,key=lambda x:moveHeuristic(x[0],x[1],boardRows,boardCols))
    for row, col in sortedMoves:
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
    return False
