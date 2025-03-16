from checkWin import checkWin
from MarkSquare import markSquare
from collections import deque

def evaluateBoard(checkBoard,boardRows,boardCols):
    score = 0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col] == 2:  # AI
                score += 10
            elif checkBoard[row][col] == 1:  # Người chơi
                score -= 10
    if checkWin( checkBoard,2):
        return 1000
    elif checkWin( checkBoard,1):
        return -1000
    return score

def bestMoveBFS(board,boardRows,boardCols):
    queue=deque()
    
    validMoves=[]
    opponent=1
    for row in range(boardRows):
        for col in range(boardCols):
            if(board[row][col]==0):
                board[row][col]=opponent
                if checkWin(board,opponent):
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
        score=evaluateBoard(board,boardRows,boardCols)
        if score>maxScore:
            maxScore=score
            bestMove=move
        board[row][col]=0
        
    if bestMove:
        markSquare(board,bestMove[0],bestMove[1],2)
        return True
    return False