from Function.checkWin import checkWin
import random


def evaluate_line(line, player):
    opponent = 3 - player
    if opponent in line:
        return 0
    return line.count(player)


def heuristic(board, player, boardRows, boardCols):
    opponent = 3 - player
    winCondition = min(5, min(boardRows, boardCols))

    if checkWin(board, player, boardRows, boardCols):
        return 10000
    elif checkWin(board, opponent, boardRows, boardCols):
        return -10000

    score = 0

    # Duyệt tất cả dòng, cột, chéo có thể tạo thành chuỗi thắng
    for r in range(boardRows):
        for c in range(boardCols):
            lines = []

            # Hàng ngang
            if c + winCondition <= boardCols:
                lines.append([board[r][c + i] for i in range(winCondition)])

            # Hàng dọc
            if r + winCondition <= boardRows:
                lines.append([board[r + i][c] for i in range(winCondition)])

            # Chéo chính \
            if r + winCondition <= boardRows and c + winCondition <= boardCols:
                lines.append([board[r + i][c + i]
                             for i in range(winCondition)])

            # Chéo phụ /
            if r - winCondition + 1 >= 0 and c + winCondition <= boardCols:
                lines.append([board[r - i][c + i]
                             for i in range(winCondition)])

            for line in lines:
                score += evaluate_line(line, player) * 10
                score -= evaluate_line(line, opponent) * 8  # Chặn đối thủ

    return score


def DeepHillClimbing(board, boardRows, boardCols, player=2):
    current_score = heuristic(board, player, boardRows, boardCols)
    best_score = current_score
    best_moves = []

    for r in range(boardRows):
        for c in range(boardCols):
            if board[r][c] == 0:
                board[r][c] = player
                score = heuristic(board, player, boardRows, boardCols)
                if score > best_score:
                    best_score = score
                    best_moves = [(r, c)]
                elif score == best_score:
                    best_moves.append((r, c))
                board[r][c] = 0

    if best_moves:
        return random.choice(best_moves)
    else:
        empty = [(r, c) for r in range(boardRows)
                 for c in range(boardCols) if board[r][c] == 0]
        if empty:
            return random.choice(empty)
        return None
