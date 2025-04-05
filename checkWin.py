# boardRows = 4
# boardCols = 4

def checkWin(checkBoard,player,boardRows,boardCols):
    # winCondition = boardCols if boardCols >= boardCols else boardCols-1 # Sửa số quân cần thắng
    winCondition = min(5, min(boardRows, boardCols))
    # Kiểm tra hàng ngang
    for row in range(boardRows):
        for col in range(boardCols - winCondition + 1):
            if all(checkBoard[row][col + i] == player for i in range(winCondition)):
                return True

    # Kiểm tra hàng dọc
    for col in range(boardCols):
        for row in range(boardRows - winCondition + 1):
            if all(checkBoard[row + i][col] == player for i in range(winCondition)):
                return True

    # Kiểm tra đường chéo (\)
    for r in range(boardRows - winCondition + 1):
        for c in range(boardCols - winCondition + 1):
            if all(checkBoard[r + i][c + i] == player for i in range(winCondition)):
                return True

    # Kiểm tra đường chéo (/)
    for r in range(winCondition - 1, boardRows):
        for c in range(boardCols - winCondition + 1):
            if all(checkBoard[r - i][c + i] == player for i in range(winCondition)):
                return True
