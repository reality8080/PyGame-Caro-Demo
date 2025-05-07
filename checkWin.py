def checkWin(checkBoard, player, boardRows, boardCols):
    winCondition = min(3, min(boardRows, boardCols))  # Đặt cố định 3 cho bàn cờ 3x3
    # Debug: In trạng thái bàn cờ
    # print(f"Checking win for player {player}:")

    
    # Kiểm tra hàng ngang
    for row in range(boardRows):
        for col in range(boardCols - winCondition + 1):
            if all(checkBoard[row][col + i] == player for i in range(winCondition)):
                # print(f"Win detected for player {player} in row {row}")
                return True

    # Kiểm tra hàng dọc
    for col in range(boardCols):
        for row in range(boardRows - winCondition + 1):
            if all(checkBoard[row + i][col] == player for i in range(winCondition)):
                # print(f"Win detected for player {player} in column {col}")
                return True

    # Kiểm tra đường chéo (\)
    for r in range(boardRows - winCondition + 1):
        for c in range(boardCols - winCondition + 1):
            if all(checkBoard[r + i][c + i] == player for i in range(winCondition)):
                # print(f"Win detected for player {player} in diagonal \\")
                return True

    # Kiểm tra đường chéo (/)
    for r in range(winCondition - 1, boardRows):
        for c in range(boardCols - winCondition + 1):
            if all(checkBoard[r - i][c + i] == player for i in range(winCondition)):
                # print(f"Win detected for player {player} in diagonal /")
                return True
    
    return False