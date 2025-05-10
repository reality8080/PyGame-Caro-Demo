from Function.checkWin import checkWin
from Function.MarkSquare import markSquare

def evaluateBoard(board, boardRows, boardCols):
    def get_line_score(line, player):
        opp = 1 if player == 2 else 2
        if line.count(player) == 5:
            return 1000
        elif line.count(player) == 4 and line.count(0) == 1:
            return 200
        elif line.count(player) == 3 and line.count(0) == 2:
            return 50
        elif line.count(opp) == 5:
            return -1000
        elif line.count(opp) == 4 and line.count(0) == 1:
            return -300
        elif line.count(opp) == 3 and line.count(0) == 2:
            return -70
        return 0

    score = 0

    # Duyệt theo 4 hướng
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # ngang, dọc, chéo \, chéo /

    for row in range(boardRows):
        for col in range(boardCols):
            for dr, dc in directions:
                line = []
                for i in range(5):
                    r = row + i * dr
                    c = col + i * dc
                    if 0 <= r < boardRows and 0 <= c < boardCols:
                        line.append(board[r][c])
                    else:
                        break
                if len(line) == 5:
                    score += get_line_score(line, 2)  # 2 là AI
    return score

def bestMoveAndOr(board, player, boardRows, boardCols):
    def opponent(p):
        return 1 if p == 2 else 2

    bestMove = None
    bestScore = -float('inf')

    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 0:
                board[row][col] = player

                if checkWin(board, player, boardRows, boardCols):
                    score = 1000
                else:
                    # "Or" node – nếu đối phương phản ứng tệ, ta được lợi
                    worstResponseScore = float('inf')
                    for r2 in range(boardRows):
                        for c2 in range(boardCols):
                            if board[r2][c2] == 0:
                                board[r2][c2] = opponent(player)
                                if checkWin(board, opponent(player), boardRows, boardCols):
                                    responseScore = -1000
                                else:
                                    responseScore = evaluateBoard(board, boardRows, boardCols)
                                worstResponseScore = min(worstResponseScore, responseScore)
                                board[r2][c2] = 0

                    score = worstResponseScore
                board[row][col] = 0

                if score > bestScore:
                    bestScore = score
                    bestMove = (row, col)

    return bestMove
