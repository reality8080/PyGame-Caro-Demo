import heapq
import numpy as np
from Function.checkWin import checkWin
from Function.MarkSquare import markSquare
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20
class EvaluatedAStar:
    def __init__(self, board, boardRows, boardCols):
        self.board = board
        self.boardRows = boardRows
        self.boardCols = boardCols
        # self.sequenceFinder = SequenceFinder(board, boardRows, boardCols)
        self.evaluator = CaroEvaluator20x20()
    
    def evaluate(self, player):
        return self.evaluator.evaluate(self.board, player, self.boardRows, self.boardCols)
    

def evaluatedAStar(checkBoard,player, boardRows,boardCols):
    myEvaluator = EvaluatedAStar(checkBoard, boardRows, boardCols)
    return myEvaluator.evaluate(player)

def AStar(board,boardRows,boardCols,player=2):
    pq=[]
    opponent=3-player
    
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                board[row][col]=opponent
                if checkWin(board,opponent, boardRows,boardCols):
                    board[row][col]=0
                    return (row, col)
                board[row][col]=0
    
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                board[row][col]=player
                h=evaluatedAStar(board,player,boardRows,boardCols)
                g = boardCols*boardRows- np.count_nonzero(board == 0)
                f=h+g
                heapq.heappush(pq,(-f,row,col))
                board[row][col]=0
    if pq:
        _,bestRow,bestCol=heapq.heappop(pq)
        # markSquare(board,bestRow,bestCol,player)
        # return True
        return (bestRow,bestCol)
    return None