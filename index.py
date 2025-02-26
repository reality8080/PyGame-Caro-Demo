import sys
import numpy as np
import pygame

pygame.init()


# if __name__ == "__main__":
# Mau sac
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Gray= (128, 128, 128)
Blue = (0, 0, 255)
Green = (0, 255, 0)
# Kich thuoc
WIDTH = 500
HEIGHT = 500
# Duong ke
LINEWIDTH = 5
FPS = 60
boardRows = 3
boardCols = 3
# Kich thuoc o
squareSize= WIDTH//boardCols
circleRadius = squareSize//3
circleWidth = 15
crossWidth = 25
# Tao man hinh va chu
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Co Caro")
# To mau nen
screen.fill(Black)
# Tao bang kich thuoc 3*3
board=np.zeros((boardRows, boardCols))

def drawLines(color=White):
    for i in range(1, boardRows):
        pygame.draw.line(screen, color, start_pos=(0, i*squareSize), end_pos=(WIDTH, i*squareSize), width=LINEWIDTH)
        pygame.draw.line(screen, color, start_pos=(i*squareSize, 0), end_pos=(i*squareSize, HEIGHT), width=LINEWIDTH)

def drawFigures(color=White):
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, center=(int(col*squareSize + squareSize//2), int(row*squareSize + squareSize//2)), radius= circleRadius, width= circleWidth)
            elif board[row][col] == 2:
                pygame.draw.line(screen,color,start_pos=(col*squareSize + squareSize // 4, row*squareSize + squareSize // 4), 
                end_pos=(col * squareSize + 3 * squareSize // 4, row*squareSize + 3* squareSize //4), width= crossWidth)
                pygame.draw.line(screen,color,start_pos=(col*squareSize + squareSize // 4, row*squareSize + 3 * squareSize // 4), 
                end_pos=(col * squareSize + 3 * squareSize // 4, row*squareSize + squareSize //4), width= crossWidth)

def markSquare(row, col, player):
    board[row][col] = player

def availableSquare(row,col):
    return board[row][col] == 0

def isBoardFull(checkBroad=board):
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBroad[row][col] == 0:
                return False
    return True

def checkWin(player, checkBroad=board):
    for col in range(boardCols):
        if checkBroad[0][col] ==player and checkBroad[1][col]==player and checkBroad[2][col]==player:
            return True
    for row in range(boardRows):
        if checkBroad[row][0] ==player and checkBroad[row][1]==player and checkBroad[row][2]==player:
            return True
    if checkBroad[0][0] ==player and checkBroad[1][1]==player and checkBroad[2][2]==player:
        return True
    if checkBroad[0][2] ==player and checkBroad[1][1]==player and checkBroad[2][0]==player:
        return True
    return False

#Thuat toan tim kiem toi uu MiniMax
def minimax(minimaxBoard, depth, isMaximizing):
    if checkWin(player=2, checkBroad=minimaxBoard):
        return float('inf')
    elif checkWin(player=1, checkBroad=minimaxBoard):
        return float('-inf')
    elif isBoardFull(checkBroad=minimaxBoard):
        return 0
    if isMaximizing:
        bestScore = -1000
        for row in range(boardRows):
            for col in range(boardCols):
                if minimaxBoard[row][col] == 0:
                    minimaxBoard[row][col] = 2
                    score = minimax(minimaxBoard, depth+1, isMaximizing= False)
                    minimaxBoard[row][col] = 0
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = 1000
        for row in range(boardRows):
            for col in range(boardCols):
                if minimaxBoard[row][col] == 0:
                    minimaxBoard[row][col] = 1
                    score = minimax(minimaxBoard, depth+1, isMaximizing=True)
                    minimaxBoard[row][col] = 0
                    bestScore = min(score, bestScore)
        return bestScore

def bestMove():
    bestScore=-1000
    move=(-1,-1)
    for row in range (boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                board[row][col]=2
                score= minimax(board, depth=0,isMaximizing=False)
                board[row][col]=0
                if score>bestScore:
                    bestScore=score
                    move=(row,col)
    if move != (-1,-1):
        markSquare(move[0], move[1],player=2)
        return True
    return False

def restartGame():
    screen.fill(Black)
    drawLines()
    for row in range(boardRows):
        for col in range(boardCols):
            board[row][col]=0

drawLines()

player=1
gameOver=False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type==pygame.MOUSEBUTTONDOWN and not gameOver:
            mouseX=event.pos[0]// squareSize
            mouseY=event.pos[1]//squareSize

            if availableSquare(mouseY,mouseX):
                markSquare(mouseY,mouseX, player)
                if checkWin(player):
                    gameOver=True
                player=player%2+1

                if not gameOver:
                    if bestMove():
                        if checkWin(player=2):
                            gameOver=True
                        player=player%2+1
                if not gameOver:
                    if isBoardFull():
                        gameOver=True
        if event.type==pygame.KEYDOWN:   
            if event.key==pygame.K_r:
                restartGame()
                gameOver=False           
                player=1  
    if not gameOver:
        drawFigures()
    else:
        if checkWin(1):
            drawFigures(Green)
            drawLines(Green)
        elif checkWin(2):
            drawFigures(Red)
            drawLines(Red)    
        else:
            drawFigures(Blue)
            drawLines(Blue)   
    pygame.display.update()
    pygame.time.Clock().tick(FPS)