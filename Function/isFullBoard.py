def isBoardFull(checkBroad,boardRows,boardCols):
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBroad[row][col] == 0:
                return False
    return True