import sys
import numpy as np
import pygame
from collections import deque
import asyncio

from checkWin import checkWin
from InformedSearch.miniMax import bestMoves
from InformedSearch.BestFirstSearch import bestMoveBFS
from InformedSearch.AStar import AStar
from UnInformedSearch.UCS import ucs

from isFullBoard import isBoardFull
from Draw import drawLines, drawFigures
from availableSquare import availableSquare
from MarkSquare import markSquare
from InformedSearch.AStar import AStar
from InformedSearch.DeepHillClimbing import DeepHillClimbing
# from InformedSearch.miniMaxConSult_Le import bestMoveMiniMax as bestMoveMiniMaxLe

pygame.init()

# Màu sắc
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Gray = (128, 128, 128)
Blue = (0, 0, 255)
Green = (0, 255, 0)

# Kích thước
WIDTH = 600
HEIGHT = 600
LINEWIDTH = 5
FPS = 60
boardRows = 6
boardCols = 6
squareSize = WIDTH // boardCols
circleRadius = squareSize // 3
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
# async def callMiniMax(board,boardRows,boardCols):
#     return await bestMoveMiniMaxLe(board,boardRows,boardCols)

def restartGame(screen,board):
    screen.fill(Black)
    drawLines(screen, squareSize, boardRows, White, WIDTH, HEIGHT, LINEWIDTH)
    for row in range(boardRows):
        for col in range(boardCols):
            board[row][col] = 0

def start(algorithm="MiniMax"):
    player = 1
    gameOver = False

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cờ Caro")
    screen.fill(Black)
    board = np.zeros((boardRows, boardCols))
    drawLines(screen, squareSize, boardRows, White, WIDTH, HEIGHT, LINEWIDTH)

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
                    if checkWin(checkBoard=board,player=player,boardRows=boardRows,boardCols=boardCols):
                        gameOver=True
                    # elif isBoardFull(board, boardRows, boardCols):
                        # gameOver=True
                    else:
                        player = 2
                # AI đánh
                    if not gameOver:
                        if(algorithm == "Astar"):
                            if(AStar(board,boardRows,boardCols)):
                                if checkWin(board,2,boardRows,boardCols):
                                    gameOver=True
                            player=1
                        elif(algorithm == "BestFirstSearch"):
                            if(bestMoveBFS(board,boardRows,boardCols)):
                                if checkWin(board,2,boardRows,boardCols):
                                    gameOver=True   
                            player=1                             
                        elif(algorithm == "MiniMax"):
                            if(bestMoves(board,boardRows,boardCols)):
                                if checkWin(board,2,boardRows,boardCols):
                                    gameOver=True       
                            player=1
                         
                        elif(algorithm == "DHClimbing"):
                            if(DeepHillClimbing(board,boardRows,boardCols)):
                                if checkWin(board,2,boardRows,boardCols):
                                    gameOver=True                                
                            player=1
                        elif algorithm == "UCS":
                            move = ucs(board, 2, boardRows, boardCols)
                            if move:
                                markSquare(board, move[0], move[1], 2)
                                if checkWin(board,2,boardRows,boardCols):
                                    gameOver=True
                            player=1
                            
                        # if checkWin(checkBoard=board,player=player,boardRows=boardRows,boardCols=boardCols):
                        #     gameOver=True
                        # elif isBoardFull(board, boardRows, boardCols):
                        #     gameOver=True
                        # else:
                        #     player = 1
                    if not gameOver:
                        if isBoardFull(board,boardRows, boardCols):
                            gameOver=True
                        # player=player%2-1
                        # player = 1
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
            drawFigures(screen, board, boardRows, squareSize, boardCols, White, crossWidth, circleRadius, circleWidth)
        else:
            if checkWin(board, 1, boardRows, boardCols):
                drawFigures(screen, board, boardRows, squareSize, boardCols, Green, crossWidth, circleRadius, circleWidth)
                drawLines(screen, squareSize, boardRows, Green, WIDTH, HEIGHT, LINEWIDTH)
            elif checkWin(board, 2, boardRows, boardCols):
                drawFigures(screen, board, boardRows, squareSize, boardCols, Red, crossWidth, circleRadius, circleWidth)
                drawLines(screen, squareSize, boardRows, Red, WIDTH, HEIGHT, LINEWIDTH)
            else:
                drawFigures(screen, board, boardRows, squareSize, boardCols, Blue, crossWidth, circleRadius, circleWidth)
                drawLines(screen, squareSize, boardRows, Blue, WIDTH, HEIGHT, LINEWIDTH)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
