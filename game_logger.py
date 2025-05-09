import numpy as np


class GameStep:
    def __init__(self, board_state, move, player, step_number):
        self.board_state = np.copy(board_state)
        self.move = move
        self.player = player
        self.step_number = step_number
        self.state_count = 0

    def calculate_state_count(self, previous_steps):
        unique_states = set()
        for step in previous_steps:
            flat = tuple(step.board_state.flatten())
            unique_states.add(flat)
        current_state = tuple(self.board_state.flatten())
        unique_states.add(current_state)
        self.state_count = len(unique_states)

    def save_log(self, file):
        file.write(
            f"Bước {self.step_number}: Player {self.player} đánh tại {self.move}\n")
        file.write(f"Tổng số trạng thái: {self.state_count}\n\n")


class GameLogger:
    def __init__(self):
        self.steps = []

    def add_step(self, board, move, player):
        step = GameStep(board, move, player, len(self.steps) + 1)
        step.calculate_state_count(self.steps)
        self.steps.append(step)

    def save_log(self, file="Luutrangthai.txt"):
        with open(file, 'w', encoding="utf-8") as file:
            for step in self.steps:
                step.save_log(file)
