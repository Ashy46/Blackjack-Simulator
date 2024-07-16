from abc import ABC, abstractmethod

class BaseSolver(ABC):
    @abstractmethod
    def decide(self, player_hand, dealer_up_card, deck):
        pass
    