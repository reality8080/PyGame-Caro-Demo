import numpy as np
from Score.Helper.SequenceFinder import SequenceFinder
from Function.checkWin import checkWin

DEFAULT_WEIGHTS = {
    1: 10,      # Chuỗi 1: nhỏ nhưng vẫn có giá trị
    2: 5000,      # Chuỗi 2: có tiềm năng phát triển
    3: float('inf'),     # Chuỗi 3: đáng chú ý
    # 4: 1000000,    # Chuỗi 4: rất nguy hiểm
    # 5: float('inf')   # Chuỗi 5: gần thắng
}
BLOCKED_PENALTY = {
    0: 3.0,   # Mở cả 2 đầu: nhân 2.5
    1: 2.5,   # Mở 1 đầu: nhân 1
    2: 0.0    # Bị chặn 2 đầu: nhân 0
}
POTENTIAL_EXTENSION_BONUS = 10
COMBO_BONUS = 50
BLOCKED_SEQUENCE_PENALTY = 20
COMBO_TRAP_BONUS = 100
class CaroEvaluator20x20:
    def __init__(self,weights=None):
        self.weights = weights if weights else DEFAULT_WEIGHTS
        
    def evaluate(self,board, player, boardRows, boardCols):
        totalScore=0
        opponnent=3-player
        
        if checkWin(board, player,boardRows, boardCols):
            return 100000
        if checkWin(board, opponnent,boardRows, boardCols):
            return -100000
        
        finder = SequenceFinder(board, boardRows, boardCols)
        for length in range(1, 6):
            sequences = finder.find_sequences(length, player)
            for sequence in sequences:
                baseScore = self.weights.get(length, 0)
                adjustedScore = baseScore * BLOCKED_PENALTY.get(sequence.blockedEnds,0)
                totalScore+= adjustedScore
        
        for length in range(1, 6):
            sequences = finder.find_sequences(length, opponnent)
            for sequence in sequences:
                baseScore = self.weights.get(length, 0)
                adjustedScore = baseScore * BLOCKED_PENALTY.get(sequence.blockedEnds,0)
                totalScore-= adjustedScore
                
        # Potential extension bonus
        totalScore += finder.calculatePotentialExtensionBonus(player) * POTENTIAL_EXTENSION_BONUS
        totalScore -= finder.calculatePotentialExtensionBonus(opponnent) * POTENTIAL_EXTENSION_BONUS

        # Combo bonus
        totalScore += finder.calculateComboBonus(player) * COMBO_BONUS
        totalScore -= finder.calculateComboBonus(opponnent) * COMBO_BONUS

        # Center control
        totalScore += finder.evaluateCenterControl(player)

        # Blocked sequences
        totalScore -= finder.detectBlockedSequences(player) * BLOCKED_SEQUENCE_PENALTY
        totalScore += finder.detectBlockedSequences(opponnent) * BLOCKED_SEQUENCE_PENALTY

        # Combo traps
        totalScore += finder.detectComboTrap(player) * COMBO_TRAP_BONUS
        totalScore -= finder.detectComboTrap(opponnent) * COMBO_TRAP_BONUS

        # Threat sequences (open twos)
        totalScore += finder.detectThreatSequences(player)

        # Live threes (open threes)
        totalScore += finder.detectLiveThree(player)

        # Double threats
        totalScore += finder.detectDoubleThreat(player)
        adjustedScore = baseScore * BLOCKED_PENALTY.get(sequence.blockedEnds, 0)
        totalScore -= adjustedScore * 1.5 
        return totalScore
    