import heapq
import numpy as np
from checkWin import checkWin
from MarkSquare import markSquare
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20
class EvaluatedAStar:
    def __init__(self, board, boardRows, boardCols):
        self.board = board
        self.boardRows = boardRows
        self.boardCols = boardCols
        # self.sequenceFinder = SequenceFinder(board, boardRows, boardCols)
        self.evaluator = CaroEvaluator20x20()
    # def evaluate(self,player):
    #     opponent = 3 - player
    #     playerSequences = self.sequenceFinder.find_sequences(5, player)+\
    #         self.sequenceFinder.find_sequences(4, player)+\
    #         self.sequenceFinder.find_sequences(3, player)+\
    #         self.sequenceFinder.find_sequences(2, player)
        
    #     opponentSequences = self.sequenceFinder.find_sequences(5, opponent)+\
    #         self.sequenceFinder.find_sequences(4, player)+\
    #         self.sequenceFinder.find_sequences(3, player)+\
    #         self.sequenceFinder.find_sequences(2, player)

    #     score=0
        
    #     score+= self.calculateScore(playerSequences,True)-self.calculateScore(opponentSequences,False)
    #     return score
    
    def evaluate(self, player):
        return self.evaluator.evaluate(self.board, player, self.boardRows, self.boardCols)
    
    # def calculateScore(self, sequences, isPlayer):
        
    #     total = 0
    #     for seq in sequences:
    #         if seq.length == 5:
    #             total += 100000
    #         elif seq.length == 4:
    #             if seq.blockedEnds == 0:
    #                 total += 10000
    #             elif seq.blockedEnds == 1:
    #                 total += 5000
    #         elif seq.length == 3:
    #             if seq.blockedEnds == 0:
    #                 total += 1000
    #             elif seq.blockedEnds == 1:
    #                 total += 500
    #         elif seq.length == 2:
    #             if seq.blockedEnds == 0:
    #                 total += 200
    #             elif seq.blockedEnds == 1:
    #                 total += 100
    #     return total
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
        # markSquare(board,bestRow,bestCol,player)
        # return True
        return (bestRow,bestCol)
    return None