import sys
import numpy as np
import pygame
from collections import deque

# from InformedSearch.AStar import AStar
from checkWin import checkWin
from InformedSearch.miniMax import bestMoveMiniMax
from isFullBoard import isBoardFull
from InformedSearch.BestFirstSearch import bestMoveBFS
from Draw import drawLines,drawFigures

pygame.init()

# Mau sac
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Gray= (128, 128, 128)
Blue = (0, 0, 255)
Green = (0, 255, 0)
# Kich thuoc
WIDTH = 600
HEIGHT = 600
# Duong ke
LINEWIDTH = 5
FPS = 60
boardRows = 4
boardCols = 4
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
# Vẽ các dòng phân cách

# Đánh dấu ô đó là Người chơi hay AI đánh

# Kiểm tra các ô trống
# Kiểm tra bảng đầy

# Kiểm tra bên nào đã thắng

def markSquare(row, col, player):
    board[row][col] = player
# Kiểm tra các ô trống
def availableSquare(row,col):
    return board[row][col] == 0
# Kiểm tra bảng đầy

# Kiểm tra bên nào đã thắng

# Them he so danh gia

# khởi tạo game



def restartGame():
    screen.fill(Black)
    drawLines(screen,squareSize,boardRows,White,WIDTH,HEIGHT,LINEWIDTH)
    for row in range(boardRows):
        for col in range(boardCols):
            board[row][col]=0

drawLines(screen,squareSize,boardRows,White,WIDTH,HEIGHT,LINEWIDTH)

player=1
gameOver=False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type==pygame.MOUSEBUTTONDOWN and not gameOver:
            mouseX=event.pos[0]// squareSize
            mouseY=event.pos[1]//squareSize
            # Người chơi
            if availableSquare(mouseY,mouseX):
                markSquare(mouseY,mouseX, player)
                if checkWin(checkBoard=board,player=player):
                    gameOver=True
                player=player%2+1
            # AI đánh
                if not gameOver:
                    # if AStar(board,boardRows,boardCols):
                    # if bestMove(board,boardRows,boardCols):
                    if bestMoveBFS(board,boardRows,boardCols):
                        if checkWin(board,player=2):
                            gameOver=True
                        player=player%2+1
                if not gameOver:
                    if isBoardFull(board,boardRows, boardCols):
                        gameOver=True
        if event.type==pygame.KEYDOWN:   
            if event.key==pygame.K_r:
                restartGame()
                gameOver=False           
                player=1  
    if not gameOver:
        drawFigures(screen,board,boardRows,squareSize,boardCols,White,crossWidth,circleRadius,circleWidth)
    else:
        if checkWin(board,1):
            drawFigures(screen,board,boardRows,squareSize,boardCols,Green,crossWidth,circleRadius,circleWidth)
            drawLines(screen,squareSize,boardRows,Green,WIDTH,HEIGHT,LINEWIDTH)
        elif checkWin(board,2):
            drawFigures(screen,board,boardRows,squareSize,boardCols,Red,crossWidth,circleRadius,circleWidth)
            drawLines(screen,squareSize,boardRows,Red,WIDTH,HEIGHT,LINEWIDTH)    
        else:
            drawFigures(screen,board,boardRows,squareSize,boardCols,Blue,crossWidth,circleRadius,circleWidth)
            drawLines(screen,squareSize,boardRows,Blue,WIDTH,HEIGHT,LINEWIDTH)   
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    