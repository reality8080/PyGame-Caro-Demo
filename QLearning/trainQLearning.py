import numpy as np
import random
import MarkSquare
from checkWin import checkWin
from isFullBoard import isBoardFull
from QLearning.ChooseAction import chooseAction
from InformedSearch.miniMax import bestMove,evaluatedMiniMax

qTable={}
alpha=0.1
gamma=0.9
epsilon=1.0
epsilonMin=0.01
epsilonDecay=0.995

def trainQLearning(boardRows, boardCols, episodes, searchAlgorithm=None):
    """Huấn luyện Q-learning cho trò chơi trên bàn cờ.

    Args:
        boardRows (int): Số hàng của bàn cờ.
        boardCols (int): Số cột của bàn cờ.
        episodes (int): Số episode huấn luyện.
        searchAlgorithm: Thuật toán tìm kiếm (nếu có, ví dụ: Minimax).

    Returns:
        dict: Q-table đã được huấn luyện.
        list: Lịch sử các chỉ số qua các episode.
    """
    global epsilon, qTable
    history = []
    explorationCount = 0
    winCount = 0
    lossCount = 0
    drawCount = 0

    for episode in range(episodes):
        board = np.zeros((boardRows, boardCols), dtype=np.int8)
        state = tuple(board.flatten())
        if state not in qTable:
            qTable[state] = np.zeros(boardRows * boardCols)
        
        totalReward = 0
        steps = 0
        maxSteps = boardRows * boardCols
        result = "In Progress"

        while steps < maxSteps:
            steps += 1
            action = chooseAction(board, boardRows, boardCols, state, epsilon, qTable, searchAlgorithm)
            if action is None:
                result = "No Valid Moves"
                break
            
            if random.random() < epsilon:
                explorationCount += 1
            
            # Thực hiện nước đi cho AI (player 2)

            
            reward = 0
            opponentMove = bestMove(board, boardRows, boardCols, player=1)
            if opponentMove:
                MarkSquare.markSquare(board, opponentMove[0], opponentMove[1], 1)
                newState = tuple(board.flatten())
                if checkWin(board, 1, boardRows, boardCols):  # Đối thủ thắng
                    reward = -1
                    result = "Loss"
                    lossCount += 1
                    totalReward += reward
                else:
                    action_idx = action[0] * boardCols + action[1]
                    MarkSquare.markSquare(board, action[0], action[1], 2)
                    newState = tuple(board.flatten())                   
            # Tính phần thưởng
                    if checkWin(board, 2, boardRows, boardCols):  # AI thắng
                        reward = 1
                        result = "Win"
                        winCount += 1
                        totalReward += reward
                    elif isBoardFull(board, boardRows, boardCols):  # Hòa
                        reward = 0
                        result = "Draw"
                        drawCount += 1
                        totalReward += reward
                        # Đối thủ đi (player 1)
                    else:
                        # Không có nước đi cho đối thủ, AI thắng
                        reward = 1
                        result = "Win"
                        winCount += 1
                        totalReward += reward
            
            # Phần thưởng bổ sung từ evaluatedMiniMax
            if steps % 5 == 0 and result == "In Progress":
                boardTuple = tuple(tuple(row) for row in board)
                score = evaluatedMiniMax(boardTuple, 2, boardRows, boardCols)
                reward += score  # Đã chuẩn hóa trong evaluatedMiniMax
                totalReward += score
            
            # Cập nhật Q-table
            if newState not in qTable:
                qTable[newState] = np.zeros(boardRows * boardCols)
            maxFutureQ = np.max(qTable[newState])
            qTable[state][action_idx] += alpha * (reward + gamma * maxFutureQ - qTable[state][action_idx])
            
            state = newState
            if result != "In Progress":
                break
        
        # Cập nhật epsilon
        epsilon = max(epsilonMin, epsilon * epsilonDecay)
        
        # Tính các chỉ số
        avg_q = np.mean([qTable[s][a] for s in qTable for a in range(len(qTable[s])) if qTable[s][a] != 0]) if qTable else 0
        valid_moves = len([(r, c) for r in range(boardRows) for c in range(boardCols) if board[r][c] == 0])
        q_table_size = len(qTable)
        exploration_rate = explorationCount / (steps + 1) if steps > 0 else 0
        
        # In thông tin
        if episode % 100 == 0:
            win_rate = winCount / (episode + 1) if episode > 0 else 0
            print(f"Episode {episode}, Epsilon: {epsilon:.4f}, Total Reward: {totalReward:.2f}, "
                  f"Steps: {steps}, Result: {result}, Win Rate: {win_rate:.2f}, "
                  f"Avg Q-value: {avg_q:.4f}, Valid Moves: {valid_moves}, Q-table Size: {q_table_size}, "
                  f"Exploration Rate: {exploration_rate:.2f}")
        
        # Lưu lịch sử
        history.append({
            'episode': episode,
            'epsilon': epsilon,
            'total_reward': totalReward,
            'steps': steps,
            'result': result,
            'win_count': winCount,
            'loss_count': lossCount,
            'draw_count': drawCount,
            'avg_q': avg_q,
            'valid_moves': valid_moves,
            'q_table_size': q_table_size,
            'exploration_rate': exploration_rate
        })
        
        # Cắt tỉa Q-table (tùy chọn)
        if q_table_size > 100000:  # Giới hạn kích thước
            qTable = {k: v for k, v in sorted(qTable.items(), key=lambda x: np.max(np.abs(x[1])), reverse=True)[:50000]}

    # Lưu lịch sử vào CSV
    # with open('q_learning_history.csv', 'w', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=history[0].keys())
    #     writer.writeheader()
    #     writer.writerows(history)
    
    return qTable, history