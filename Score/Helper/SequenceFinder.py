class Sequence:
    def __init__(self, startPos, direction, length, blockedEnds):
        self.startPos=startPos
        self.direction=direction
        self.length=length
        self.blockedEnds=blockedEnds

class SequenceFinder:
    def __init__(self, board, boardRows, boardCols):
        self.board = board
        self.boardRows = boardRows
        self.boardCols = boardCols

    def find_sequences(self, length, player, recentMove=None):
        sequences = []
        directions=[    (-1,-1) ,(-1,0)  ,(-1,1),
                        (0,-1)           ,(0,1),
                        (1,-1)  ,(1,0)   ,(1,1),
                        ]
        if recentMove:
            for row,col in recentMove:
                for dr in range(-2,3):
                    for dc in range(-2,3):
                        nR,nC=row+dr,col+dc
                        if 0<=nR<self.boardRows and 0<=nC<self.boardCols and self.board[nR][nC]==player:
                            for dr,dc in directions:
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
                    for dr, dc in directions:
                        if self.checkSequence(row, col, dr, dc, length, player):
                            blockedEnds = self.checkBlockedEnds(row, col, dr, dc, length)
                            sequences.append(Sequence((row, col), directions, length, blockedEnds))
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
        if not (0 <= startRow + (length - 1) * rowDir + rowDir < self.boardRows and 0 <= startCol + (length - 1) * colDir + colDir < self.boardCols and self.board[startRow + (length - 1) * rowDir + rowDir][startCol + (length - 1) * colDir + colDir] == 0):
            blockedEnds += 1
        return blockedEnds

    def calculatePotentialExtensionBonus(self, player):
        potentialBonus = 0
        directions=[
        (-1, -1),(-1, 0),(-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1),   
        ]
        
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col]==player:
                    for dr,dc in directions:
                        nR,nC=row+dr, col+dc
                        if 0<=nR<self.boardRows and 0<=nC<self.boardCols and self.board[nR][nC]==0:
                            potentialBonus+=1
        return potentialBonus
    
    def calculateComboBonus(self, player):
        comboBonus = 0
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),  (1, 1),
        ]
        
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == player:
                    count = 0
                    for dr, dc in directions:
                        nR, nC = row + dr, col + dc
                        if 0 <= nR < self.boardRows and 0 <= nC < self.boardCols and self.board[nR][nC] == player:
                            count += 1
                    if count >= 2:
                        comboBonus += 1
        return comboBonus

    def detectBlockedSequences(self, player):
        blockedCount = 0
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),  (1, 1),
        ]
        
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == player:
                    for dr, dc in directions:
                        nR, nC = row + dr, col + dc
                        if 0 <= nR < self.boardRows and 0 <= nC < self.boardCols and self.board[nR][nC] == (3 - player):
                            blockedCount += 1
        return blockedCount

    def detectComboTrap(self, player):
        trapCount = 0
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),  (1, 1),
        ]
        
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == 0:
                    neighborPlayer = 0
                    for dr, dc in directions:
                        nR, nC = row + dr, col + dc
                        if 0 <= nR < self.boardRows and 0 <= nC < self.boardCols:
                            if self.board[nR][nC] == player:
                                neighborPlayer += 1
                    if neighborPlayer >= 2:
                        trapCount += 1
        return trapCount
    def detectThreatSequences(self, player):
        threatScore = 0
        opponent = 3 - player
        for length in [3, 4]:
            sequences = self.find_sequences(length, opponent)
            for seq in sequences:
                if seq.blockedEnds <= 1:  # Chuỗi có ít nhất một đầu mở
                    if length == 4 and seq.blockedEnds == 0:
                        threatScore -= 50000  # Chuỗi 4 mở cả hai đầu
                    elif length == 4 and seq.blockedEnds == 1:
                        threatScore -= 20000  # Chuỗi 4 mở một đầu
                    elif length == 3 and seq.blockedEnds == 0:
                        threatScore -= 5000   # Chuỗi 3 mở cả hai đầu
                    elif length == 3 and seq.blockedEnds == 1:
                        threatScore -= 1000   # Chuỗi 3 mở một đầu
        return threatScore
    def detectDoubleThreat(self, player):
        doubleThreatScore = 0
        opponent = 3 - player
        for row in range(self.boardRows):
            for col in range(self.boardCols):
                if self.board[row][col] == 0:
                    # Thử đặt quân của người chơi
                    self.board[row][col] = player
                    playerThreats = sum(1 for seq in self.find_sequences(3, player) if seq.blockedEnds <= 1) + \
                                    sum(2 for seq in self.find_sequences(4, player) if seq.blockedEnds <= 1)
                    self.board[row][col] = 0
                    if playerThreats >= 2:
                        doubleThreatScore += 10000

                    # Thử đặt quân của đối thủ
                    self.board[row][col] = opponent
                    opponentThreats = sum(1 for seq in self.find_sequences(3, opponent) if seq.blockedEnds <= 1) + \
                                    sum(2 for seq in self.find_sequences(4, opponent) if seq.blockedEnds <= 1)
                    self.board[row][col] = 0
                    if opponentThreats >= 2:
                        doubleThreatScore -= 10000
        return doubleThreatScore
    def evaluateCenterControl(self, player):
        centerScore = 0
        opponent = 3 - player
        centerStart, centerEnd = self.boardRows//2-2, self.boardRows//2+2  # Vùng trung tâm 10x10
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
        liveThreeScore -= sum(2000 for seq in sequences if seq.blockedEnds == 0)
        return liveThreeScore