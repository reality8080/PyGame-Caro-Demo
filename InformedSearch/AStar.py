import heapq
import numpy as np
from checkWin import checkWin
from MarkSquare import markSquare

def evaluatedAStar(checkBoard,player, boardRows,boardCols):
    score=0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col]==player:
                score+=10
            elif checkBoard[row][col]==(3-player):
                score-=10
    if checkWin(player,checkBoard):
        return 1000
    elif checkWin(3-player,checkBoard):
        return -1000
    return score

def AStar(board,boardRows,boardCols,player=2):
    pq=[]
    
    opponent=3-player
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                board[row][col]=opponent
                if checkWin(opponent,board):
                    board[row][col]=0
                    markSquare(board,row,col,player)
                    return True
                board[row][col]=0
    
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                board[row][col]=player
                h=evaluatedAStar(board,player,boardRows,boardCols)
                g = np.count_nonzero(board == 0)
                f=h+g
                heapq.heappush(pq,(-f,row,col))
                board[row][col]=0
    if pq:
        _,bestRow,bestCol=heapq.heappop(pq)
        markSquare(board,bestRow,bestCol,player)
        return True
    return False