class Sequence:
    def __init__(self, startPos, direction, length, blockedEnds):
        self.startPos = startPos
        self.direction = direction
        self.length = length
        self.blockedEnds = blockedEnds

class SequenceFinder:
    def __init__(self, board, boardRows, boardCols):
        self.board = board
        self.boardRows = boardRows
        self.boardCols = boardCols
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]

    def check_neighbors(self, row, col, condition, count_all=False):
        """Generic method to count or check neighbors satisfying a condition."""
        count = 0
        for dr, dc in self.directions:
            nR, nC = row + dr, col + dc
            if 0 <= nR < self.boardRows and 0 <= nC < self.boardCols and condition(self.board[nR][nC]):
                if count_all:
                    count += 1
                else:
                    return True
        return count if count_all else False

    def find_sequences(self, length, player, recentMove=None):
        sequences = []
        if recentMove:
            for row, col in recentMove:
                for dr in range(-4, 5):  # Check 4 cells in each direction
                    for dc in range(-4, 5):
                        nR, nC = row + dr, col + dc
                        if 0 <= nR < self.boardRows and 0 <= nC < self.boardCols and self.board[nR][nC] == player:
                            for dr, dc in self.directions:
                                if self.checkSequence(nR, nC, dr, dc, length, player):
                                    blockedEnds = self.checkBlockedEnds(nR, nC, dr, dc, length)
                                    sequences.append(Sequence((nR, nC), (dr, dc), length, blockedEnds))
        else:
            checked = set()
            for row in range(self.boardRows):
                for col in range(self.boardCols):
                    if self.board[row][col] != player or (row, col) in checked:
                        continue
                    checked.add((row, col))
                    for dr, dc in self.directions:
                        if self.checkSequence(row, col, dr, dc, length, player):
                            blockedEnds = self.checkBlockedEnds(row, col, dr, dc, length)
                            sequences.append(Sequence((row, col), (dr, dc), length, blockedEnds))
        return sequences

    def checkSequence(self, startRow, startCol, rowDir, colDir, length, player):
        for i in range(length):
            row = startRow + i * rowDir
            col = startCol + i * colDir
            if not (0 <= row < self.boardRows and 0 <= col < self.boardCols and self.board[row][col] == player):
                return False
        return True

    def checkBlockedEnds(self, startRow, startCol, rowDir, colDir, length):
        blockedEnds = 0
        # Check the start of the sequence
        if not (0 <= startRow - rowDir < self.boardRows and 0 <= startCol - colDir < self.boardCols and self.board[startRow - rowDir][startCol - colDir] == 0):
            blockedEnds += 1
        # Check the end of the sequence
        if not (0 <= startRow + length * rowDir < self.boardRows and 0 <= startCol + length * colDir < self.boardCols and self.board[startRow + length * rowDir][startCol + length * colDir] == 0):
            blockedEnds += 1
        return blockedEnds

    def calculatePotentialExtensionBonus(self, player):
        potentialBonus = 0
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == player:
                    potentialBonus += self.check_neighbors(row, col, lambda x: x == 0, count_all=True)
        return potentialBonus

    def calculateComboBonus(self, player):
        comboBonus = 0
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == player:
                    neighbor_count = self.check_neighbors(row, col, lambda x: x == player, count_all=True)
                    if neighbor_count >= 2:
                        comboBonus += 1
        return comboBonus

    def detectBlockedSequences(self, player):
        blockedCount = 0
        opponent = 3 - player
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == player:
                    blockedCount += self.check_neighbors(row, col, lambda x: x == opponent, count_all=True)
        return blockedCount

    def detectComboTrap(self, player):
        trapCount = 0
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == 0:
                    neighbor_count = self.check_neighbors(row, col, lambda x: x == player, count_all=True)
                    if neighbor_count >= 2:
                        trapCount += 1
        return trapCount

    def detectThreatSequences(self, player):
        threatScore = 0
        opponent = 3 - player
        sequences = self.find_sequences(2, opponent)
        for seq in sequences:
            if seq.blockedEnds <= 1:
                threatScore -= 100
        return threatScore

    def detectDoubleThreat(self, player):
        doubleThreatScore = 0
        opponent = 3 - player
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    playerThreats = sum(1 for seq in self.find_sequences(3, player) if seq.blockedEnds <= 1)
                    self.board[row][col] = 0
                    if playerThreats >= 2:
                        doubleThreatScore += 500
                    self.board[row][col] = opponent
                    opponentThreats = sum(1 for seq in self.find_sequences(3, opponent) if seq.blockedEnds <= 1)
                    self.board[row][col] = 0
                    if opponentThreats >= 2:
                        doubleThreatScore -= 500
        return doubleThreatScore

    def evaluateCenterControl(self, player):
        centerScore = 0
        opponent = 3 - player
        centerStart, centerEnd = self.boardRows // 2 - 2, self.boardRows // 2 + 2
        for row in range(centerStart, centerEnd):
            for col in range(centerStart, centerEnd):
                if self.board[row][col] == player:
                    centerScore += 20
                elif self.board[row][col] == opponent:
                    centerScore -= 20
        return centerScore

    def detectLiveThree(self, player):
        liveThreeScore = 0
        opponent = 3 - player
        sequences = self.find_sequences(3, player)
        liveThreeScore += sum(2000 for seq in sequences if seq.blockedEnds == 0)
        sequences = self.find_sequences(3, opponent)
        for seq in sequences:
            if seq.blockedEnds == 0:
                liveThreeScore -= 2000
            elif seq.blockedEnds == 1:
                liveThreeScore -= 800
        return liveThreeScore