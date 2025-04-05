from checkWin import checkWin
from isFullBoard import isBoardFull
from MarkSquare import markSquare
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from functools import lru_cache

# Do sau
maxDepth=5
# Moi do sau chon ra
beamWidth=5

def evaluatePosition(board, boardRows,boardCols,player,row,col):
    winCondition = min(5, min(boardRows, boardCols))
    allDirections=[(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    totalScore=0
    
    for dr,dc in allDirections:
        count = 1
        blocked=0
        for i in range(1, winCondition):
            r,c = row + dr*i, col + dc*i
            if 0 <= r < boardRows and 0 <= c <boardCols:
                if board[r][c]==player:
                    count+=1
                elif board[r][c] == 0:
                    break
                else:
                    blocked+=1
                    break
    
        if count >= winCondition:
            return 100000
        score = 0
        if count == 4 and blocked ==0:
            score = 10000
        elif count == 3 and blocked == 0:
            score = 1000
        else:
            score = count ** 3
            
        r1,c1=row-dr,col-dc
        r2,c2=row+dr*count,col+dc*count
        openEnds=0
        if 0<=r1<boardRows and 0<=c1<boardCols and board[r1][c1]==0:
            openEnds+=1
        if 0<=r2<boardRows and 0<=c2<boardCols and board[r2][c2]==0:
            openEnds+=1
        totalScore += score*(openEnds+1)
    centerDist=abs(row-boardRows//2)+abs(col-boardCols//2)
    totalScore+=(boardRows//2-centerDist)*10
    return totalScore
    
def evaluateOpenness(board, row, col,dr,dc,count, player, boardRows, boardCols):
    openEnds=0
    
    r1,c1 = row -dr, col - dc
    if 0 <= r1 < boardRows and 0 <= c1 < boardCols and board[r1][c1] == 0:
        openEnds+=1
    r2,c2 = row + dr*count, col + dc*count
    if 0 <= r2 < boardRows and 0 <= c2 < boardCols and board[r2][c2] == 0:
        openEnds+=1
    return openEnds * 10 *count   

                
def evaluateBoard(checkBoard,boardRows,boardCols):
    score = 0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col] == 2:  # AI
                score += evaluatePosition(checkBoard,row,col,2,boardRows,boardCols)
                if (row>=boardRows//2-1 and 
                    row <=boardRows//2+1 and 
                    col >=boardCols//2-1 and 
                    col <= boardCols//2+1):
                    score+=3
            elif checkBoard[row][col] == 1:  # Người chơi
                score -= evaluatePosition(checkBoard,row,col,1,boardRows, boardCols)
    if checkWin( checkBoard,2,boardRows,boardCols):
        return 100000
    elif checkWin( checkBoard,1,boardRows,boardCols):
        return -100000
    return score

def quickEvaluate(board, row, col, boardRows, boardCols):
 
    player=board[row][col]
    opponent= 1 if player==2 else 2
    attackScore = evaluatePosition(board, row,col, player, boardRows, boardCols)
    board[row][col]=opponent
    defenceScore=evaluatePosition(board,row,col,opponent,boardRows, boardCols)*0.8
    board[row][col]=player
    return attackScore+defenceScore

def getRelevantMoves(board, boardRows, boardCols):
    relevantMoves = set()
    directions = [
        (-1,-1),(-1,0),(-1,1),
        (0,-1),         (0,1),
        (1,-1),  (1,0), (1,1)
    ]
    
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col]!=0:
                for dr, dc in directions:
                    r,c =row +dr, col +dc
                    if 0 <= r <boardRows and 0 <= c < boardCols and board[r][c] == 0:
                        relevantMoves.add((r,c))
    
    if not relevantMoves and board[boardRows//2][boardCols//2] == 0:
        return [(boardRows//2,boardCols//2)]
    
    return list(relevantMoves)                

#Thuat toan tim kiem toi uu MiniMax

minimaxCache={}

def minimax(board, boardRows, boardCols, depth, isMaximizing, alpha, beta):
    boardTuple = tuple(map(tuple, board))
    cacheKey=(boardTuple,depth,isMaximizing,alpha,beta)
    if cacheKey in minimaxCache:
        return minimaxCache[cacheKey]
    
    if checkWin(board,2,len(board),len(board[0])):
        return float('inf')
    if checkWin(board,1,len(board),len(board[0])):
        return float('-inf')
    if isBoardFull(board,len(board),len(board[0])) or depth>=maxDepth:
        return evaluateBoard(board,boardRows,boardCols)

    
    possibleMoves = getRelevantMoves(board, len(board),len(board[0]))
    
    scoredMoves=[]
    for row, col in possibleMoves:
        board[row][col] = 2 if isMaximizing else 1
        score = quickEvaluate(board, row, col, len(board),len(board[0]))
        board[row][col] = 0
        scoredMoves.append((score,row,col))
    
    scoredMoves.sort(reverse=isMaximizing, key=lambda x:x[0])
    topMoves=scoredMoves[:beamWidth]
    
    bestScore = float('-inf') if isMaximizing else float('inf')
    
    for _, row, col in topMoves:
        board[row][col]=2 if isMaximizing else 1
        score = minimax(board, boardRows, boardCols,depth+1, not isMaximizing,alpha,beta)
        board[row][col]=0
        if isMaximizing:
            bestScore=max(bestScore,score)
            alpha=max(alpha,bestScore)
        else:
            bestScore=min(bestScore,score)
            beta=min(beta,bestScore)
        if beta <= alpha:
            break
    minimaxCache[cacheKey]=bestScore
    return bestScore
    
def evaluateMoveWrapper(args):
    board, move, boardRows, boardCols, alpha, beta = args
    row, col = move
    boardCopy=np.copy(board)
    boardCopy[row][col]=2
    boardTuple = tuple(map(tuple, boardCopy))
    score=minimax(boardCopy, boardRows, boardCols, 0, False, alpha, beta)
    return (score, row, col)

# Duyệt qua từng ô và suy diễn ra ô có điểm số cao nhất
def bestMoveMiniMax(board, boardRows, boardCols):
    bestScore=float('-inf')
    bestMove=(-1,-1)
    alpha = float('-inf')
    beta = float('inf')
    
    possibleMoves=getRelevantMoves(board, boardRows, boardCols)
    if not possibleMoves:
        return False
    

    tasks=[(board, move, boardRows, boardCols, alpha,beta) for move in possibleMoves]

    with ThreadPoolExecutor() as executor:
        results=list(executor.map(evaluateMoveWrapper, tasks))
    

    for score,row,col in results:
        if(score>bestScore):
            bestScore=score
            bestMove=(row,col)
            alpha = max(alpha,bestScore)
    
    if bestMove!=(-1,-1):
        markSquare(board,bestMove[0], bestMove[1],2)
        return True
    return False
