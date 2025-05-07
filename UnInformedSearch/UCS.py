from checkWin import checkWin
from MarkSquare import markSquare
import numpy as np

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



def heuristic(board, row, col, player, boardRows, boardCols):
    board[row][col] = player
    if checkWin(board, player, boardRows, boardCols):
        score = 1000
    else:
        score = evaluateBoard(board, boardRows, boardCols)
    board[row][col] = 0
    return score


def ucs(board, player, boardRows, boardCols):
    bestMove = None
    bestScore = -float('inf')

    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 0:
                board[row][col] = player
                score = evaluateBoard(board, boardRows, boardCols)
                board[row][col] = 0

                if score > bestScore:
                    bestScore = score
                    bestMove = (row, col)

    return bestMove



# import numpy as np
# from queue import PriorityQueue
# from checkWin import checkWin
# from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20

# class UCS:
#     def __init__(self, board, boardRows, boardCols):
#         self.board = board
#         self.boardRows = boardRows
#         self.boardCols = boardCols
#         self.evaluator = CaroEvaluator20x20()
#         self.cache = {}  # Cache điểm số trạng thái

#     def evaluate(self, player):
#         """Đánh giá bàn cờ với cache"""
#         board_tuple = tuple(map(tuple, self.board))
#         cache_key = (board_tuple, player)
#         if cache_key in self.cache:
#             return self.cache[cache_key]
        
#         score = self.evaluator.evaluate(self.board, player, self.boardRows, self.boardCols)
#         self.cache[cache_key] = score
#         return score

#     def get_candidate_moves(self, radius=2):
#         """Lấy danh sách các ô trống gần các ô đã đánh dấu"""
#         moves = set()
#         for row in range(self.boardRows):
#             for col in range(self.boardCols):
#                 if self.board[row][col] != 0:
#                     for dr in range(-radius, radius + 1):
#                         for dc in range(-radius, radius + 1):
#                             r, c = row + dr, col + dc
#                             if 0 <= r < self.boardRows and 0 <= c < self.boardCols and self.board[r][c] == 0:
#                                 moves.add((r, c))
#         return list(moves) if moves else [(r, c) for r in range(self.boardRows) for c in range(self.boardCols) if self.board[r][c] == 0]

# def evaluateBoard(checkBoard, player, boardRows, boardCols):
#     ucsEvaluator = UCS(checkBoard, boardRows, boardCols)
#     return ucsEvaluator.evaluate(player)

# def ucs(board, player, boardRows, boardCols, max_depth=2):
#     """UCS tối ưu hóa với heuristic và giới hạn nước đi"""
#     pq = PriorityQueue()
#     visited = set()
#     best_move = None
#     best_score = float('-inf')  # Tìm điểm số cao nhất cho AI

#     # Khởi tạo UCS với trạng thái ban đầu
#     ucs_instance = UCS(board.copy(), boardRows, boardCols)
#     initial_score = ucs_instance.evaluate(player)
#     initial_state = (-initial_score, 0, board.tobytes(), None, 0)  # (heuristic_cost, step_cost, board, move, depth)
#     pq.put(initial_state)

#     while not pq.empty():
#         heuristic_cost, step_cost, board_bytes, move, depth = pq.get()
#         current_board = np.frombuffer(board_bytes, dtype=board.dtype).reshape(boardRows, boardCols)

#         # Bỏ qua trạng thái đã thăm
#         board_tuple = tuple(map(tuple, current_board))
#         if board_tuple in visited:
#             continue
#         visited.add(board_tuple)

#         # Kiểm tra điều kiện dừng
#         if depth >= max_depth or checkWin(current_board, player, boardRows, boardCols) or checkWin(current_board, 3 - player, boardRows, boardCols):
#             ucs_instance.board = current_board
#             score = ucs_instance.evaluate(player)
#             if score > best_score:  # Tìm điểm số cao nhất
#                 best_score = score
#                 best_move = move
#             continue

#         # Lấy danh sách nước đi tiềm năng
#         ucs_instance.board = current_board
#         candidate_moves = ucs_instance.get_candidate_moves(radius=2)

#         # Tạo trạng thái con
#         for row, col in candidate_moves:
#             new_board = current_board.copy()
#             new_board[row][col] = player
#             ucs_instance.board = new_board
#             new_score = ucs_instance.evaluate(player)
#             new_step_cost = step_cost + 1
#             # Chi phí heuristic là điểm số âm (để ưu tiên nước đi tốt)
#             new_heuristic_cost = -new_score
#             new_state = (new_heuristic_cost, new_step_cost, new_board.tobytes(), move if move else (row, col), depth + 1)
#             pq.put(new_state)

#     return best_move