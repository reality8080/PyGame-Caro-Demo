import copy
import heapq
from Score.CaroEvaluator.CaroEvaluator20x20 import CaroEvaluator20x20  # chỉnh lại nếu cần import khác

class Node:
    def __init__(self, board, move, cost):
        self.board = board
        self.move = move  # tọa độ (row, col)
        self.cost = cost

    def __lt__(self, other):  # dùng để so sánh trong priority queue
        return self.cost < other.cost


def ucs(board, player, boardRows, boardCols, evaluator=None):
    if evaluator is None:
        evaluator = CaroEvaluator20x20()
        
    pq = []  # priority queue
    # visited = set()

    for row in range(boardRows):
        for col in range(boardCols):
            if board[row][col] == 0:
                # Tạo bản sao bàn cờ
                new_board = copy.deepcopy(board)
                new_board[row][col] = player

                # Đánh giá chi phí với hàm evaluate
                cost = evaluator.evaluate(new_board, player, boardRows, boardCols)

                # Thêm vào hàng đợi ưu tiên
                heapq.heappush(pq, Node(new_board, (row, col), cost))

    if not pq:
        return None  # Không còn nước đi

    # Lấy nước đi có chi phí thấp nhất
    best_node = heapq.heappop(pq)
    return best_node.move
