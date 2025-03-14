import sys
import numpy as np
import pygame

pygame.init()

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
circleRadius = squareSize//boardCols
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
def drawLines(color=White):
    for i in range(1, boardRows):
        pygame.draw.line(screen, color, start_pos=(0, i*squareSize), end_pos=(WIDTH, i*squareSize), width=LINEWIDTH)
        pygame.draw.line(screen, color, start_pos=(i*squareSize, 0), end_pos=(i*squareSize, HEIGHT), width=LINEWIDTH)
# Vẽ O và X khi người chơi và AI đánh cờ
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
# Đánh dấu ô đó là Người chơi hay AI đánh
def markSquare(row, col, player):
    board[row][col] = player
# Kiểm tra các ô trống
def availableSquare(row,col):
    return board[row][col] == 0
# Kiểm tra bảng đầy
def isBoardFull(checkBroad=board):
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBroad[row][col] == 0:
                return False
    return True
# Kiểm tra bên nào đã thắng
def checkWin(player, checkBroad=board):
    # Kiểm tra xem có đủ 3 điểm theo hàng dọc
    for col in range(boardCols):
        for row in range(0,boardRows-2):
            if checkBroad[0+row][col] ==player and checkBroad[1+row][col]==player and checkBroad[2+row][col]==player:
                return True
    # Kiểm tra xem có đủ 3 điểm theo hàng ngang
    # for row in range(boardRows):
    #     if checkBroad[row][0] ==player and checkBroad[row][1]==player and checkBroad[row][2]==player:
    #         return True
    # Kiểm tra xem một trong hai đường chéo có đủ 3 điểm 
    if checkBroad[0][0] ==player and checkBroad[1][1]==player and checkBroad[2][2]==player:
        return True
    if checkBroad[0][2] ==player and checkBroad[1][1]==player and checkBroad[2][0]==player:
        return True
    return False

#Thuat toan tim kiem toi uu MiniMax
def minimax(minimaxBoard, depth, isMaximizing):
    # Kiểm tra AI thắng
    if checkWin(player=2, checkBroad=minimaxBoard):
        return float('inf')
    # Kiểm tra người chơi thắng
    elif checkWin(player=1, checkBroad=minimaxBoard):
        return float('-inf')
    # Kiểm tra bàn cờ đầyđầy
    elif isBoardFull(checkBroad=minimaxBoard):
        return 0
    
    if isMaximizing:
        bestScore = -1000
        # Lặp qua tất cả các ô
        for row in range(boardRows):
            for col in range(boardCols):
                if minimaxBoard[row][col] == 0:
                    minimaxBoard[row][col] = 2
                    # Gọi đệ quy và lưu điểm với lớn nhất cho AI
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
# Duyệt qua từng ô và suy diễn ra ô có điểm số cao nhất
def bestMove():
    bestScore=-1000
    move=(-1,-1)
    for row in range (boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                # Thử đánh
                board[row][col]=2
                # Lấy điểm số lớn nhất
                score= minimax(board, depth=0,isMaximizing=False)
                board[row][col]=0
                # kiểm tra điểm số cao nhất
                if score>bestScore:
                    bestScore=score
                    move=(row,col)
    if move != (-1,-1):
        markSquare(move[0], move[1],player=2)
        return True
    return False
# khởi tạo game
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
            # Người chơi
            if availableSquare(mouseY,mouseX):
                markSquare(mouseY,mouseX, player)
                if checkWin(player):
                    gameOver=True
                player=player%2+1
            # AI đánh
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