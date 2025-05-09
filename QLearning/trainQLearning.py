import numpy as np
import random
import MarkSquare
from checkWin import checkWin
from isFullBoard import isBoardFull
from QLearning.ChooseAction import chooseAction
from InformedSearch.miniMax import bestMove, evaluatedMiniMax

qTable = {}
alpha = 0.1
gamma = 0.9
epsilon = 1.0
epsilonMin = 0.01
epsilonDecay = 0.995

def trainQLearning(boardRows, boardCols, episodes, searchAlgorithm=None):
    """Huấn luyện Q-learning cho trò chơi Caro trên bàn cờ.

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

            # AI (player 2) move
            action = chooseAction(board, boardRows, boardCols, state, epsilon, qTable, searchAlgorithm)
            if action is None:
                result = "No Valid Moves"
                break
            
            if random.random() < epsilon:
                explorationCount += 1
            
            # Apply AI move
            action_idx = action[0] * boardCols + action[1]
            MarkSquare.markSquare(board, action[0], action[1], 2)
            newState = tuple(board.flatten())

            # Check AI win
            reward = 0
            if checkWin(board, 2, boardRows, boardCols):
                reward = 100  # Large reward for winning
                result = "Win"
                winCount += 1
                totalReward += reward
            elif isBoardFull(board, boardRows, boardCols):
                reward = 0
                result = "Draw"
                drawCount += 1
                totalReward += reward
            else:
                # Opponent (player 1) move
                opponentMove = bestMove(board, boardRows, boardCols, player=1)
                if opponentMove:
                    MarkSquare.markSquare(board, opponentMove[0], opponentMove[1], 1)
                    newState = tuple(board.flatten())
                    if checkWin(board, 1, boardRows, boardCols):
                        reward = -100  # Large penalty for losing
                        result = "Loss"
                        lossCount += 1
                        totalReward += reward
                    else:
                        # Intermediate reward based on board evaluation
                        boardTuple = tuple(tuple(row) for row in board)
                        score = evaluatedMiniMax(boardTuple, 2, boardRows, boardCols)
                        reward += score * 0.01  # Scale to avoid overpowering win/loss rewards
                        totalReward += reward
                else:
                    # No opponent move, but game not full (rare case)
                    reward = 10  # Small reward for opponent having no moves
                    totalReward += reward

            # Update Q-table
            if newState not in qTable:
                qTable[newState] = np.zeros(boardRows * boardCols)
            maxFutureQ = np.max(qTable[newState])
            qTable[state][action_idx] += alpha * (reward + gamma * maxFutureQ - qTable[state][action_idx])
            
            state = newState
            if result != "In Progress":
                break
        
        # Update epsilon
        epsilon = max(epsilonMin, epsilon * epsilonDecay)
        
        # Calculate metrics
        avg_q = np.mean([qTable[s][a] for s in qTable for a in range(len(qTable[s])) if qTable[s][a] != 0]) if qTable else 0
        valid_moves = np.count_nonzero(board == 0)
        q_table_size = len(qTable)
        exploration_rate = explorationCount / steps if steps > 0 else 0
        win_rate = winCount / (episode + 1) if episode > 0 else 0
        
        # Log information
        if episode % 100 == 0:
            print(f"Episode {episode}, Epsilon: {epsilon:.4f}, Total Reward: {totalReward:.2f}, "
                  f"Steps: {steps}, Result: {result}, Win Rate: {win_rate:.2f}, "
                  f"Avg Q-value: {avg_q:.4f}, Valid Moves: {valid_moves}, Q-table Size: {q_table_size}, "
                  f"Exploration Rate: {exploration_rate:.2f}")
        
        # Save history
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
        
        # Prune Q-table if too large
        if q_table_size > 100000:
            qTable = {k: v for k, v in sorted(qTable.items(), key=lambda x: np.max(np.abs(x[1])), reverse=True)[:50000]}

    return qTable, history