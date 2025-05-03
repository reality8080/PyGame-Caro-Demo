import numpy as np
from Score.Helper.SequenceFinder import SequenceFinder
from checkWin import checkWin

DEFAULT_WEIGHTS = {
    1: 10,      # Chuỗi 1: nhỏ nhưng vẫn có giá trị
    2: 50,      # Chuỗi 2: có tiềm năng phát triển
    3: 500,     # Chuỗi 3: đáng chú ý
    4: 5000,    # Chuỗi 4: rất nguy hiểm
    5: 100000   # Chuỗi 5: gần thắng
}
BLOCKED_PENALTY = {
    0: 2.5,   # Mở cả 2 đầu: nhân 2.5
    1: 1.0,   # Mở 1 đầu: nhân 1
    2: 0.0    # Bị chặn 2 đầu: nhân 0
}
POTENTIAL_EXTENSION_BONUS = 50  # Mỗi nước tiềm năng nối dài
COMBO_BONUS = 300               # Nếu 1 nước tạo 2+ chuỗi mạnh


class CaroEvaluator20x20:
    def __init__(self,weights=None):
        self.weights = weights if weights else DEFAULT_WEIGHTS
        
    def evaluate(self,board, player, boardRows, boardCols):
        totalScore=0
        opponnent=3-player
        
        if checkWin(board, player,boardRows, boardCols):
            return 1000000
        if checkWin(board, opponnent,boardRows, boardCols):
            return -1000000
        
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
             
        # totalScore += finder.calculatePotentialExtensionBonus(player) * POTENTIAL_EXTENSION_BONUS
        # totalScore += finder.calculateComboBonus(player) * COMBO_BONUS
        # totalScore += finder.detectBlockedSequences(player) * BLOCKED_PENALTY[2]
        # totalScore += finder.detectBlockedSequences(3 - player) * BLOCKED_PENALTY[2]
        # totalScore += finder.detectComboTrap(player) * COMBO_BONUS
        
        # if hasattr(finder, 'calculateComboBonus'):
        #     totalScore += finder.calculateComboBonus(player) * COMBO_BONUS
        # if hasattr(finder, 'detectBlockedSequences'):
        #     totalScore += finder.detectBlockedSequences(player) * BLOCKED_PENALTY[2]
        #     totalScore += finder.detectBlockedSequences(3 - player) * BLOCKED_PENALTY[2]
        # if hasattr(finder, 'detectComboTrap'):
        #     totalScore += finder.detectComboTrap(player) * COMBO_BONUS
        totalScore += finder.calculatePotentialExtensionBonus(player) * POTENTIAL_EXTENSION_BONUS
        totalScore += finder.calculateComboBonus(player) * COMBO_BONUS
        totalScore += finder.detectBlockedSequences(player) * BLOCKED_PENALTY[2]
        totalScore += finder.detectBlockedSequences(opponnent) * BLOCKED_PENALTY[2]
        totalScore += finder.detectComboTrap(player) * COMBO_BONUS
        totalScore += finder.detectThreatSequences(player)
        totalScore += finder.detectDoubleThreat(player)
        totalScore += finder.evaluateCenterControl(player)
        totalScore += finder.detectLiveThree(player)
        # totalScore += finder.evaluateDefensivePotential(player)
        return totalScore