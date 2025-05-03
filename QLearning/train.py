# import numpy as np
# import random

# import Design
# import Design.ChooseAction
# import Design.getAvailableMove
# import Design.getState
# import Move
# import CheckWin
# import Full


# qTable = {}
# alpha = 0.1  # Learning rate
# gamma = 0.9  # Discount factor
# epsilon = 1.0  # Exploration rate
# epsilon_min = 0.01
# epsilon_decay = 0.995

# def train(epsilon,boardRows,boardCols, episodes=10000):
#     for _ in range(episodes):
#         board=np.zeros((boardRows,boardCols))
#         state = Design.getState.getState(board)
#         while True:
#             if state not in qTable:
#                 qTable[state]=np.zeros(boardRows*boardCols)
#             action = Design.ChooseAction.chooseAction(board,boardRows,boardCols,state,epsilon,qTable)
#             Move.makeMove(board,action,1)
#             newState=Design.getState.getState(board)
            
#             if CheckWin.checkWin(board,1,boardRows,boardCols):
#                 reward=1
#                 qTable[state][action[0]*boardRows+action[1]]+=alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
#                 break
#             elif Full.isFull(board):
#                 reward = 0
#                 qTable[state][action[0]*boardRows+action[1]]+=alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
#                 break
            
#             opponentMove=random.choice(Design.getAvailableMove.getAvailableMoves(board,boardRows,boardCols))
#             Move.makeMove(board,opponentMove,2)
#             newState = Design.getState.getState(board)
            
#             if CheckWin.checkWin(board,2,boardRows,boardCols):
#                 reward = -1
#                 qTable[state][action[0]*boardRows+action[1]] += alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
#                 break
            
#             if newState not in qTable:
#                 qTable[newState]=np.zeros(boardCols*boardRows)
#             maxFutureQ=np.max(qTable[newState])
#             # qTable[state][action[0]*3+action[1]]+=alpha*(0+gamma*maxFutureQ-qTable[state][action[0]*3+action[1]])
#             qTable[state][action[0] * boardRows + action[1]] += alpha * (0 + gamma * maxFutureQ - qTable[state][action[0] * boardRows + action[1]])
#             state=newState
#         epsilon=max(epsilon_min,epsilon*epsilon_decay)

# train(epsilon, 5,5)

import numpy as np
import random

import MarkSquare
import getState
from isFullBoard import isBoardFull
from checkWin import checkWin
from QLearning.getAvailableMove import getAvailableMoves
import ChooseAction
# chooseAction

qTable = {}
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Exploration rate
epsilon_min = 0.01
epsilon_decay = 0.995

def train(epsilon,boardRows,boardCols, episodes=5000):
    totalCells=boardRows*boardCols
    for _ in range(episodes):
        board=np.zeros((boardRows,boardCols),dtype=np.int8)
        state = getState.getState(board)
        availableMoves=getAvailableMoves(board,boardRows,boardCols)
        while True:
            if state not in qTable:
                qTable[state]=np.zeros(totalCells, dtype=np.float32)
            action = ChooseAction.chooseAction(board,boardRows,boardCols,state,epsilon,qTable)
            MarkSquare.markSquare(board,action[0],action[1],1)
            newState=getState.getState(board)
            
            if checkWin(board,1,boardRows,boardCols):
                reward=1
                qTable[state][action[0]*boardRows+action[1]]+=alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
                break
            elif isBoardFull(board):
                reward = 0
                qTable[state][action[0]*boardRows+action[1]]+=alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
                break
            availableMoves.remove(action)
            opponentMove=random.choice(availableMoves)
            MarkSquare.markSquare(board,opponentMove[0],opponentMove[1],2)
            newState = getState.getState(board)
            
            if checkWin(board,2,boardRows,boardCols):
                reward = -1
                qTable[state][action[0]*boardRows+action[1]] += alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
                break
            availableMoves.remove(opponentMove)
            if newState not in qTable:
                qTable[newState]=np.zeros(boardCols*boardRows)
            maxFutureQ=np.max(qTable[newState])
            # qTable[state][action[0]*3+action[1]]+=alpha*(0+gamma*maxFutureQ-qTable[state][action[0]*3+action[1]])
            qTable[state][action[0] * boardRows + action[1]] += alpha * (0 + gamma * maxFutureQ - qTable[state][action[0] * boardRows + action[1]])
            state=newState
        epsilon=max(epsilon_min,epsilon*epsilon_decay)

train(epsilon, 5,5)

