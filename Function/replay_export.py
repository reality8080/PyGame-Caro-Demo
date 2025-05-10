import pygame
import imageio
import os
import numpy as np

def save_caro_replay_gif(board_history, output_file="caro_replay.gif"):
    if not board_history:
        print("Không có dữ liệu để tạo replay.")
        return

    #  Tự động xác định kích thước bàn cờ
    max_row = max(move[0] for move in board_history) + 1
    max_col = max(move[1] for move in board_history) + 1
    boardRows = max_row
    boardCols = max_col

    pygame.init()

    WIDTH, HEIGHT = 600, 600
    squareSize = WIDTH // boardCols
    LINE_WIDTH = 6
    CROSS_WIDTH = 10
    CIRCLE_WIDTH = 10
    CIRCLE_RADIUS = squareSize // 3
    LINE_COLOR = (0, 0, 0)
    X_COLOR = (255, 0, 0)
    O_COLOR = (0, 0, 255)
    BG_COLOR = (255, 255, 255)

    screen = pygame.Surface((WIDTH, HEIGHT))
    frames = []
    board = np.zeros((boardRows, boardCols))

    for move in board_history:
        row, col, player = move
        board[row][col] = player

        screen.fill(BG_COLOR)

        # Vẽ lưới
        for i in range(1, boardRows):
            pygame.draw.line(screen, LINE_COLOR, (0, i * squareSize), (WIDTH, i * squareSize), LINE_WIDTH)
        for i in range(1, boardCols):
            pygame.draw.line(screen, LINE_COLOR, (i * squareSize, 0), (i * squareSize, HEIGHT), LINE_WIDTH)

        # Vẽ O và X
        for r in range(boardRows):
            for c in range(boardCols):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, O_COLOR,
                        (c * squareSize + squareSize // 2, r * squareSize + squareSize // 2),
                        CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif board[r][c] == 2:
                    pygame.draw.line(screen, X_COLOR,
                        (c * squareSize + squareSize // 4, r * squareSize + squareSize // 4),
                        (c * squareSize + 3 * squareSize // 4, r * squareSize + 3 * squareSize // 4), CROSS_WIDTH)
                    pygame.draw.line(screen, X_COLOR,
                        (c * squareSize + squareSize // 4, r * squareSize + 3 * squareSize // 4),
                        (c * squareSize + 3 * squareSize // 4, r * squareSize + squareSize // 4), CROSS_WIDTH)

        # Lưu frame
        temp_path = "temp_frame.png"
        pygame.image.save(screen, temp_path)
        frames.append(imageio.imread(temp_path))

    imageio.mimsave(output_file, frames, duration=0.6)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    print(f"GIF đã được lưu tại: {output_file}")
