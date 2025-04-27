from abc import ABC, abstractmethod
class CaroEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board, player):
        pass