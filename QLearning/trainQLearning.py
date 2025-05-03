import numpy as np
import random
# import Search.Minimax
# import Move
# import CheckWin
# import Full
# # import Search.SearchAlgorithms as SearchAlgorithms
# import Design.ChooseAction
import MarkSquare
from checkWin import checkWin
from isFullBoard import isBoardFull
from ChooseAction import chooseAction
from InformedSearch.miniMax import bestMoves,evaluatedMiniMax

qTable={}
alpha=0.1
gamma=0.9
epsilon=1.0
epsilonMin=0.01
epsilonDecay=0.095


def trainQLearning(boardRows, boardCols, episodes, searchAlgorithm=None):
    global epsilon
    # miniMax=Search.Minimax.MiniMaxSearch()
    for episode in range(episodes):
        board=np.zeros((boardRows, boardCols), dtype=np.int8)
        state = tuple(board.flatten())
        if state not in qTable:
            qTable[state] = np.zeros(boardRows * boardCols)
        maxSteps = boardRows * boardCols
        steps = 0
        while steps<maxSteps:
            steps+=1
            action= chooseAction(board, boardRows, boardCols, state, epsilon, qTable,searchAlgorithm)
            if action is None:
                break
            (board,action,1)
            newState=tuple(board.flatten())
            
            reward=0
            if checkWin(board,1,boardRows, boardCols):
                reward=1
                qTable[state][action[0]*boardRows+action[1]] += alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
                break
            elif isBoardFull(board):
                reward=0
                qTable[state][action[0]*boardRows+action[1]] += alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
                break
            opponentMoves=bestMoves(board, boardRows, boardCols, MaxDepth=2)
            if opponentMoves is None:
                available = [(r,c) for r in range(boardRows) for c in range(boardCols) if board[r][c]==0]
                opponentMoves= random.choice(available) if available else None
            if opponentMoves:
                MarkSquare.markSquare(board, opponentMoves,2)
                newState=tuple(board.flatten())
                if checkWin(board,2,boardRows, boardCols):
                    reward=-1
                    qTable[state][action[0]*boardRows+action[1]]+=alpha*(reward-qTable[state][action[0]*boardRows+action[1]])
                    break
            if steps%5==0:
                score =  evaluatedMiniMax(board, boardRows, boardCols)
                if score>0:
                    reward+=0.1*score/100000
            if newState not in qTable:
                qTable[newState]=np.zeros(boardRows*boardCols)
            maxFutureQ=np.max(qTable[newState])
            qTable[state][action[0]*boardRows+action[1]]+=alpha*(0+gamma*maxFutureQ-qTable[state][action[0]*boardRows+action[1]])    
            state=newState
        epsilon=max(epsilonMin, epsilon*epsilonDecay)
        # if episode%1000==0:
            
        
        
# miniMax=Search.Minimax.MiniMaxSearch()
# trainQLearning(5,5,episodes=5000,searchAlgorithm=miniMax)