import numpy as np
import random
from game.blackjack import BlackJackGame
from game.player import Player
from game.dealer import Dealer
from game.deck import Deck
from base_solver import BaseSolver

class QLearningSolver(BaseSolver):
    def __init__(self, alpha=0.01, gamma=0.9, epsilon=0.1):
        super(QLearningSolver, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.state = None
        self.action = None
    
    def get_state(self, player_hand, dealer_up_card) -> tuple:
        """
        Get the current state of the game in a tuple format
        """
        pass



