import heapq
import numpy as np
from checkWin import checkWin
from MarkSquare import markSquare

def evaluatedUCS(checkBoard, player, boardRows, boardCols):
    score=0
    if checkWin(player, checkBoard):
        return 1000
    if(checkWin(3-player, checkBoard)):
        return -1000