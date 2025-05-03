from checkWin import checkWin
from MarkSquare import markSquare
from collections import deque
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20

class EvaluatedBFS:
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
def evaluateBoard(checkBoard,player, boardRows,boardCols):
    myEvaluator = EvaluatedBFS(checkBoard, boardRows, boardCols)
    return myEvaluator.evaluate(player)

def bestMoveBFS(board,boardRows,boardCols):
    queue=deque()
    
    validMoves=[]
    opponent=1
    for row in range(boardRows):
        for col in range(boardCols):
            if(board[row][col]==0):
                board[row][col]=opponent
                if checkWin(board,opponent,boardRows,boardCols):
                    board[row][col]=0
                    markSquare(board,row,col,2)
                    return True
                board[row][col]=0
                validMoves.append((row,col))
    
    bestMove =None
    maxScore=-float('inf')
    
    for move in validMoves:
        row,col=move
        board[row][col]=2
        score=evaluateBoard(board,2,boardRows,boardCols)
        if score>maxScore:
            maxScore=score
            bestMove=move
        board[row][col]=0
        
    if bestMove:
        markSquare(board,bestMove[0],bestMove[1],2)
        return True
    return False