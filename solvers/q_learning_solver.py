import numpy as np
import random
from game.blackjack import BlackJackGame
from game.player import Player
from game.dealer import Dealer
from game.deck import Deck
from solvers.base_solver import BaseSolver

class QLearningSolver(BaseSolver):
    def __init__(self, alpha=0.05, gamma=0.9, epsilon=0.3):
        super(QLearningSolver, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.state = None
        self.action = None
        self.episode_actions = []

    def _card_value(self, card_str: str) -> int:
        """
        Convert card string to numerical value

        Args:
            card_str: card string

        Returns:
            value: numerical value of card
        """
        if card_str in ['J','Q','K']:
            return 10
        if card_str == 'A':
            return 11  # Will be handled specially in state tracking
        return int(card_str)
    
    def get_state(self, player_hand, dealer_up_card):
        player_total = Player.calculate_total(player_hand)
        dealer_value = self._card_value(dealer_up_card)
    
        # Proper usable ace calculation
        usable_ace = False
        if 'A' in player_hand:
            # Calculate hard total (aces as 1)
            hard_total = sum(10 if c in ['J','Q','K'] else 11 if c == 'A' else int(c) for c in player_hand)
            usable_ace = (hard_total != player_total)
        
        return (player_total, dealer_value, usable_ace)
    
    def decide(self, player_hand, dealer_up_card, deck):
        state = self.get_state(player_hand, dealer_up_card)
        self.last_state = state
        
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0]  # [Hit, Stand]
            
        # Epsilon-greedy action selection
        if np.random.random() < self.epsilon:
            action = np.random.choice([0, 1])
        else:
            action = np.argmax(self.q_table[state])
            
        self.last_action = action
        self.episode_actions.append((state, action))
        return 'Hit' if action == 0 else 'Stand'
    
    def update(self, reward, new_player_hand, dealer_up_card):
        """Backpropagate final reward to all actions"""
        for state, action in self.episode_actions:
            old_q = self.q_table.get(state, [0,0])[action]
            self.q_table.setdefault(state, [0,0])[action] = old_q + self.alpha * (reward - old_q)
        self.episode_actions = []

    def print_key_decision(self):
        print("Key State -> Action Mapping:")
        print("(16, 7, True):", "Hit" if np.argmax(self.q_table.get((16,7,True), [0,0])) == 0 else "Stand")
        print("(18, 6, False):", "Hit" if np.argmax(self.q_table.get((18,6,False), [0,0])) == 0 else "Stand")



