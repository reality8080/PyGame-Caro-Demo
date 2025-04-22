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
from availableSquare import availableSquare
from MarkSquare import  markSquare

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

# Vẽ các dòng phân cách

# Đánh dấu ô đó là Người chơi hay AI đánh

# Kiểm tra các ô trống

# Kiểm tra bảng đầy

# Kiểm tra bên nào đã thắng

# Kiểm tra các ô trống

# Kiểm tra bảng đầy

# Kiểm tra bên nào đã thắng

# Them he so danh gia

# khởi tạo game



def restartGame(screen,board):
    screen.fill(Black)
    drawLines(screen,squareSize,boardRows,White,WIDTH,HEIGHT,LINEWIDTH)
    for row in range(boardRows):
        for col in range(boardCols):
            board[row][col]=0


def start(algorithm):
    player=1
    gameOver=False

    # Tao man hinh va chu
    screen=pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Co Caro")
    # To mau nen
    screen.fill(Black)
    # Tao bang kich thuoc 3*3
    board=np.zeros((boardRows, boardCols))
    drawLines(screen,squareSize,boardRows,White,WIDTH,HEIGHT,LINEWIDTH)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type==pygame.MOUSEBUTTONDOWN and not gameOver:
                mouseX=event.pos[0]// squareSize
                mouseY=event.pos[1]//squareSize
                # Người chơi
                if availableSquare(board,mouseY,mouseX):
                    markSquare(board,mouseY,mouseX, player)
                    if checkWin(checkBoard=board,player=player):
                        gameOver=True
                    player=player%2+1
                # AI đánh
                    if not gameOver:
                        if(algorithm == "Astar"):
                            if bestMoveBFS(board,boardRows,boardCols):
                                if checkWin(board,player=2):
                                 gameOver=True
                                player=player%2+1
                        if(algorithm == "BestFirstSearch"):
                            if bestMoveBFS(board,boardRows,boardCols):
                                if checkWin(board,player=2):
                                 gameOver=True
                                player=player%2+1
                        if(algorithm == "MiniMax"):
                            if bestMoveBFS(board,boardRows,boardCols):
                                if checkWin(board,player=2):
                                 gameOver=True
                                player=player%2+1
                        if(algorithm == "DHClimbing"):
                            if bestMoveMiniMax(board,boardRows,boardCols):
                                if checkWin(board,player=2):
                                 gameOver=True
                                player=player%2+1
                    if not gameOver:
                        if isBoardFull(board,boardRows, boardCols):
                            gameOver=True
            if event.type==pygame.KEYDOWN:   
                if event.key==pygame.K_r:
                    restartGame(screen,board)
                    gameOver=False           
                    player=1  
                if event.key==pygame.K_s:
                    from settings import settings
                    algo = settings()
          
                    start(algo)
                if event.key==pygame.K_q:
                    pygame.quit()
                    sys.exit()    
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

# start()