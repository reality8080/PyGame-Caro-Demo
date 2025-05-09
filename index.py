import sys
import numpy as np
import pygame
from collections import deque
import asyncio

from checkWin import checkWin
from InformedSearch.miniMax import bestMove
from InformedSearch.AStar import AStar
from UnInformedSearch.and_or import bestMoveAndOr
from UnInformedSearch.UCS import ucs
from isFullBoard import isBoardFull
from Draw import drawLines, drawFigures
from availableSquare import availableSquare
from MarkSquare import markSquare
from InformedSearch.DeepHillClimbing import DeepHillClimbing
from QLearning.trainQLearning import trainQLearning
from QLearning.ChooseAction import chooseAction
from QLearning.getState import getState

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
boardRows = 3
boardCols = 3
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
# qTable,_=trainQLearning(boardRows,boardCols,episodes=10000,searchAlgorithm="MiniMax")


def checkGameOver(board, player, boardRows, boardCols):
    if checkWin(board, player, boardRows, boardCols):
        return True, player
    if isBoardFull(board, boardRows, boardCols):
        return True, 0
    return False, None

def handlePlayerMove(board, row, col, player, move_history):
    if availableSquare(board, row, col):
        markSquare(board, row, col, player)
        move_history.append((row, col, player))
        return True
    return False

def handleAIMove(board:np.ndarray, algorithm, boardRows, boardCols, move_history):
    move = None
    if algorithm == "Astar":
        move = AStar(board, boardRows, boardCols)
    elif algorithm == "MiniMax":
        move = bestMove(board, boardRows, boardCols)
    elif algorithm == "DHClimbing":
        move = DeepHillClimbing(board, boardRows, boardCols)
    elif algorithm == "UCS":
        move = ucs(board, 2, boardRows, boardCols)
    elif algorithm == "AndOr":
        move = bestMoveAndOr(board, 2, boardRows, boardCols)
    # elif algorithm == "QLearning":
    #     state = getState(board)
    #     move = chooseAction(board, boardRows, boardCols, state, 0, qTable)  # epsilon=0 để khai thác
        
    # elif algorithm == "QLearning":
    #         # state = getState(board)
    #     state = tuple(board.flatten())  # Chuyển board thành tuple
    #     if state not in qTable:
    #         qTable[state] = np.zeros(boardRows * boardCols)
    #     move = chooseAction(board, boardRows, boardCols, state, 0, qTable)
        
    if move and availableSquare(board, move[0], move[1]):
        markSquare(board, move[0], move[1], 2)
        move_history.append((move[0], move[1], 2))
        return True
    return False

# def drawStatus(screen, player, gameOver, winner):
#     font = pygame.font.SysFont(None, 40)
#     if not gameOver:
#         text = font.render(f"Player {player}'s Turn", True, White)
#     else:
#         if winner == 1:
#             text = font.render("Player 1 Wins!", True, Green)
#         elif winner == 2:
#             text = font.render("AI Wins!", True, Red)
#         else:
#             text = font.render("Draw!", True, Blue)
#     screen.blit(text, (WIDTH // 2 - 100, 10))
    
def drawInstructions(screen):
    font = pygame.font.SysFont(None, 30)
    text = font.render("R: Restart | S: Settings | Q: Quit | P: Replay", True, White)
    screen.blit(text, (10, HEIGHT - 30))

def renderGame(screen, board, boardRows, boardCols, gameOver, winner):
    drawFigures(screen, board, boardRows, squareSize, boardCols, White, crossWidth, circleRadius, circleWidth)
    drawLines(screen, squareSize, boardRows, White if not gameOver else (Green if winner == 1 else Red if winner == 2 else Blue), WIDTH, HEIGHT, LINEWIDTH)
    # drawStatus(screen, 1 if not gameOver else None, gameOver, winner)
    drawInstructions(screen)
    pygame.display.update()
    
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
        renderGame(screen, board, boardRows, boardCols, False, None)
        pygame.time.wait(500)
    pygame.time.wait(2000)
    

def start(algorithm="MiniMax"):
    player = 1
    gameOver = False
    winner = None
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cờ Caro")
    screen.fill(Black)
    board = np.zeros((boardRows, boardCols))
    drawLines(screen, squareSize, boardRows, White, WIDTH, HEIGHT, LINEWIDTH)
    move_history = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver and player == 1:
                mouseX = event.pos[0] // squareSize
                mouseY = event.pos[1] // squareSize
                if handlePlayerMove(board, mouseY, mouseX, player, move_history):
                    gameOver, winner = checkGameOver(board, player, boardRows, boardCols)
                    if not gameOver:
                        player = 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restartGame(screen, board)
                    move_history.clear()
                    gameOver = False
                    player = 1
                elif event.key == pygame.K_s:
                    from settings import settings
                    algo = settings()
                    start(algo)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    replay(screen, move_history)

        if not gameOver and player == 2:
            if handleAIMove(board, algorithm, boardRows, boardCols, move_history):
                gameOver, winner = checkGameOver(board, 2, boardRows, boardCols)
                if not gameOver:
                    player = 1

        renderGame(screen, board, boardRows, boardCols, gameOver, winner)
        pygame.time.Clock().tick(FPS)