import pygame

def drawLines(screen,squareSize,boardRows,color,WIDTH,HEIGHT,LINEWIDTH):
    for i in range(1, boardRows):
        pygame.draw.line(screen, color, start_pos=(0, i*squareSize), end_pos=(WIDTH, i*squareSize), width=LINEWIDTH)
        pygame.draw.line(screen, color, start_pos=(i*squareSize, 0), end_pos=(i*squareSize, HEIGHT), width=LINEWIDTH)
# Vẽ O và X khi người chơi và AI đánh cờ
def drawFigures(screen,board,boardRows,squareSize,boardCols,color,crossWidth,circleRadius,circleWidth):
    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, center=(int(col*squareSize + squareSize//2), int(row*squareSize + squareSize//2)), radius= circleRadius, width= circleWidth)
            elif board[row][col] == 2:
                pygame.draw.line(screen,color,start_pos=(col*squareSize + squareSize // 4, row*squareSize + squareSize // 4), 
                end_pos=(col * squareSize + 3 * squareSize // 4, row*squareSize + 3* squareSize //4), width= crossWidth)
                pygame.draw.line(screen,color,start_pos=(col*squareSize + squareSize // 4, row*squareSize + 3 * squareSize // 4), 
                end_pos=(col * squareSize + 3 * squareSize // 4, row*squareSize + squareSize //4), width= crossWidth)