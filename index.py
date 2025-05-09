import sys
import numpy as np
import pygame
from collections import deque
import asyncio

from checkWin import checkWin
from InformedSearch.miniMax import bestMoveMiniMax
from InformedSearch.BestFirstSearch import bestMoveBFS
from InformedSearch.AStar import AStar
from UnInformedSearch.and_or import bestMoveAndOr
from UnInformedSearch.UCS import ucs

from isFullBoard import isBoardFull
from Draw import drawLines, drawFigures
from availableSquare import availableSquare
from MarkSquare import markSquare

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
boardRows = 5
boardCols = 5
squareSize = WIDTH // boardCols
circleRadius = squareSize // 3
circleWidth = 15
crossWidth = 25

def restartGame(screen, board):
    screen.fill(Black)
    drawLines(screen, squareSize, boardRows, White, WIDTH, HEIGHT, LINEWIDTH)
    for row in range(boardRows):
        for col in range(boardCols):
            board[row][col] = 0

def replay(screen, history):
    board = np.zeros((boardRows, boardCols))
    screen.fill(Black)
    drawLines(screen, squareSize, boardRows, White, WIDTH, HEIGHT, LINEWIDTH)

    for move in history:
        row, col, player = move
        markSquare(board, row, col, player)
        drawFigures(screen, board, boardRows, squareSize, boardCols, White, crossWidth, circleRadius, circleWidth)
        pygame.display.update()
        pygame.time.wait(500)  # đợi 0.5s cho mỗi bước

    pygame.time.wait(2000)  # Đợi sau khi kết thúc phát lại


def start(algorithm="MiniMax"):
    player = 1
    gameOver = False

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cờ Caro")
    screen.fill(Black)
    board = np.zeros((boardRows, boardCols))
    drawLines(screen, squareSize, boardRows, White, WIDTH, HEIGHT, LINEWIDTH)

    move_history = []  # Lưu các bước đi

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                mouseX = event.pos[0] // squareSize
                mouseY = event.pos[1] // squareSize
                if availableSquare(board, mouseY, mouseX):
                    markSquare(board, mouseY, mouseX, player)
                    move_history.append((mouseY, mouseX, player))

                    if checkWin(board, player, boardRows, boardCols):
                        gameOver = True
                    elif isBoardFull(board, boardRows, boardCols):
                        gameOver = True
                    player = player % 2 + 1

                    if not gameOver:
                        if algorithm == "MiniMax":
                            move = bestMoveMiniMax(board, boardRows, boardCols)
                        elif algorithm == "BestFirstSearch":
                            move = bestMoveBFS(board, boardRows, boardCols)
                        elif algorithm == "Astar":
                            move = AStar(board, boardRows, boardCols)
                        elif algorithm == "UCS":
                            move = ucs(board, 2, boardRows, boardCols)
                        elif algorithm == "AndOr":
                            move = bestMoveAndOr(board, 2, boardRows, boardCols)
                        else:
                            move = None
                        if move:
                            markSquare(board, move[0], move[1], 2)
                            move_history.append((move[0], move[1], 2))
                        
                        if checkWin(board, 2, boardRows, boardCols):
                            gameOver = True
                        elif isBoardFull(board, boardRows, boardCols):
                            gameOver = True
                        else:
                            player = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restartGame(screen, board)
                    move_history.clear()
                    gameOver = False
                    player = 1
                elif event.key == pygame.K_s:
                    from settings import settings
                    algo = settings()
                    if algo and algo != "Back":
                        start(algo)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    replay(screen, move_history)
                elif event.key == pygame.K_g:
                    from replay_export import save_caro_replay_gif
                    save_caro_replay_gif(move_history, "caro_replay.gif")


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

if __name__ == "__main__":
    start()
