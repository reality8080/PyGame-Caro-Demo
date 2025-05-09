import numpy as np
import random
# import Design.getAvailableMove 
from InformedSearch.miniMax import getCandidateMoves,evaluateMove

# def chooseAction(board: np.ndarray, boardRows, boardCols,state, epsilon, qTable):
#     if random.random()<epsilon:
#         return random.choice(Design.getAvailableMove.getAvailableMoves(board, boardRows,boardCols))
#     else:
#         if state not in qTable:
#             qTable[state] = np.zeros(9)
#         available=Design.getAvailableMove.getAvailableMoves(board,boardRows,boardCols)
#         qValues=qTable[state]
#         bestMove=max(available,key=lambda x:qValues[x[0]*boardRows+x[1]])
#         return bestMove        
def chooseAction(board, boardRows, boardCols, state, epsilon, qTable,searchAlgorithm=None):
    if state not in qTable:
        qTable[state]=np.zeros(boardRows*boardCols)
    availableMoves=getCandidateMoves(board, boardRows, boardCols,player=2)
    # action = bestMoves(board, boardRows, boardCols)
    if not availableMoves:
        return None
    boardTuple = tuple(tuple(row) for row in board)
    if random.random()<epsilon:
        scoredMoves = [(r, c, evaluateMove(r, c, boardTuple, 2, boardRows, boardCols)) for r, c in availableMoves]
        sortedMoves = sorted(scoredMoves, key=lambda x: x[2], reverse=True)
        topMoves = sortedMoves[:max(1, len(sortedMoves) // 2)]
        return random.choice(availableMoves)
    else:
        validMoves = [(move, qTable[state][move[0] * boardCols + move[1]]) for move in availableMoves]
        maxQ = max(q[1] for q in validMoves) if validMoves else 0
        bestMoves = [move for move, q in validMoves if q == maxQ]
        return random.choice(bestMoves) if bestMoves else random.choice(availableMoves)
        
    