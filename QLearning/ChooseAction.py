import numpy as np
import random
# import Design.getAvailableMove 
from InformedSearch.miniMax import MiniMaxSearch

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
    availableMoves=MiniMaxSearch
    if not availableMoves:
        return None
    if random.random()<epsilon:
        return random.choice(availableMoves)
    else:
        qValues=qTable[state]
        validMoves=[(move, qValues[move[0]*boardRows+move[1]]) for move in availableMoves]
        return max(validMoves, key=lambda x: x[1])[0]
    