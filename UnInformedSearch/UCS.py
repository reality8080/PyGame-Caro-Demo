import copy
import heapq
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20
import math

class Node:
    def __init__(self, board, move, cost):
        self.board = board
        self.move = move  # (row, col)
        self.cost = cost

    def __lt__(self, other):
        # Vì UCS chọn cost thấp nhất, nên ta cần -cost để chọn điểm số cao hơn
        return self.cost > other.cost  # Đổi hướng ưu tiên (maximize score)


def is_near_existing_move(board, row, col, distance=2):
    for dr in range(-distance, distance + 1):
        for dc in range(-distance, distance + 1):
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                if board[nr][nc] != 0:
                    return True
    return False


def ucs(board, player, boardRows, boardCols, evaluator=None):
    if evaluator is None:
        evaluator = CaroEvaluator20x20()

    pq = []
    center_row, center_col = boardRows // 2, boardCols // 2
    opponent = 3 - player

    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 0 and is_near_existing_move(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = player

                cost = evaluator.evaluate(new_board, player, boardRows, boardCols)

                # Ưu tiên ô gần trung tâm hơn nếu điểm số bằng nhau
                center_dist = math.hypot(row - center_row, col - center_col)
                cost -= center_dist * 0.1  # điều chỉnh nhẹ theo khoảng cách trung tâm

                heapq.heappush(pq, Node(new_board, (row, col), cost))

    if not pq:
        return None

    best_node = heapq.heappop(pq)
    return best_node.move
