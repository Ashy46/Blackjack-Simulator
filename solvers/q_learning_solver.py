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
    
    def get_state(self, player_hand: list[int], dealer_up_card: str) -> tuple:
        """
        Convert game components to Q-learning state tuple

        Args:
            player_hand: list of player's hand
            dealer_up_card: dealer's up card
        
        Returns:
            state: tuple representing the state
        """
        player_total = Player.calculate_total(player_hand)
        dealer_value = self._card_value(dealer_up_card)
        
        # Track usable ace (ace counted as 11 without busting)
        usable_ace = False
        temp_total = sum([self._card_value(c) for c in player_hand])
        if 'A' in player_hand and temp_total <= 21:
            usable_ace = True
            
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
        return 'Hit' if action == 0 else 'Stand'
    
    def update(self, reward, new_player_hand, dealer_up_card):
        """
        Update Q-table after action
        
        Args:
            reward: reward for the action
            new_player_hand: new player hand after action
            dealer_up_card: dealer

        Returns:
            None
        """
        if self.last_state is None:
            return
            
        new_state = self.get_state(new_player_hand, dealer_up_card)
        
        current_q = self.q_table[self.last_state][self.last_action]
        next_max = np.max(self.q_table.get(new_state, [0, 0]))
        
        # Q-learning update rule
        updated_q = current_q + self.alpha * (
            reward + self.gamma * next_max - current_q
        )
        
        self.q_table[self.last_state][self.last_action] = updated_q
        self.last_state = None  # Reset for next decision




