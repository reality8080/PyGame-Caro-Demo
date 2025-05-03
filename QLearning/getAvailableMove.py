import numpy as np

def getAvailableMoves(board: np.ndarray, boardRows, boardCols):
    return [(i,j) for i in range(boardRows) for j in range(boardCols) if board[i,j]==0]