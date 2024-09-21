import random
from game.Deck import Deck
from game.player import Player
from solvers.base_solver import BaseSolver
from functools import lru_cache

class BayesianSolver(BaseSolver):
    def __init__(self):
        self.memoized_decisions = {}
        self.uni_Deck = Deck(1)
        self.decide = lru_cache(maxsize=100000)(self.decide)
        self.memoized_dealer = {}

    def create_game_key(self, player_hand, dealer_up_card, deck):
        deck_state = tuple(sorted(deck.deck.items()))
        return (tuple(player_hand), tuple(dealer_up_card), deck_state)

    @lru_cache(maxsize=None)
    def decide(self, player_hand, dealer_up_card, deck, return_ev=False):
        state_key = self.create_game_key(player_hand, dealer_up_card, deck)
        if state_key in self.memoized_decisions.keys():
            return self.memoized_decisions[state_key]
        
        ev_hit = self.calculate_ev_hit(tuple(player_hand), dealer_up_card, deck)
        ev_stand = self.calculate_ev_stand(tuple(player_hand), dealer_up_card, deck)
        ev_double = self.calculate_ev_double(tuple(player_hand), dealer_up_card, deck)
        ev_split = self.calculate_ev_split(tuple(player_hand), dealer_up_card, deck)
        
        best_ev = max(ev_hit, ev_stand, ev_double, ev_split)
        decision = None
        if return_ev:
            return best_ev
        if best_ev == ev_stand:
            decision = 'Stand'
        elif best_ev == ev_double:
            decision = 'Double'
        elif best_ev == ev_split:
            decision = 'Split'
        elif best_ev == ev_hit:
            decision = 'Hit'

        self.memoized_decisions[state_key] = decision
        return decision    
    
    @lru_cache(maxsize=None)
    def calculate_ev_hit(self, player_hand, dealer_up_card, deck):
        player_total = Player.calculate_total(player_hand)
        if player_total > 21:
            return -1
        if player_total == 21:
            return 1
        ev = 0
        for card in deck.cards():
            if deck.deck[card] <= 0:
                continue
            new_hand = player_hand + (card, )
            new_deck = deck.copy()
            new_deck.deck[card] -= 1
            card_prob = deck.getProbability(card)
            
            if Player.calculate_total(new_hand) > 21:
                ev -= card_prob
            else:
                ev += self.decide(new_hand, dealer_up_card, new_deck, return_ev=True) * card_prob
        
        return ev

    @lru_cache(maxsize=None)
    def calculate_ev_stand(self, player_hand, dealer_up_card, deck):
        player_total = Player.calculate_total(player_hand)
        if player_total > 21:
            return -1
        if player_total == 21:
            return 1
        
        dealer_probabilities = self.get_dealer_probabilities(dealer_up_card)
        return sum(prob if dealer_total < player_total or dealer_total > 21 else -prob
                   for dealer_total, prob in dealer_probabilities.items())

    def get_dealer_probabilities(self, dealer_up_card):
        if dealer_up_card in self.memoized_dealer.keys():
            return self.memoized_dealer[dealer_up_card]
        dealer_probabilities = self.simulate_dealer(dealer_up_card)
        self.memoized_dealer[dealer_up_card] = dealer_probabilities
        return dealer_probabilities
    
    @lru_cache(maxsize=None)
    def simulate_dealer(self, dealer_up_card):
        dealer_probabilities = {}
        
        def rec_dealer_sim(current_hand, probability):
            total = Player.calculate_total(current_hand)
            
            if total > 21 or total >= 17:
                dealer_probabilities[total] = dealer_probabilities.get(total, 0) + probability
            else:
                for card in self.uni_Deck.cards():
                    if self.uni_Deck.deck[card] <= 0:
                        continue
                    new_hand = current_hand + (card,)
                    new_deck = self.uni_Deck.copy()
                    new_deck.deck[card] -= 1
                    rec_dealer_sim(new_hand, probability * self.uni_Deck.getProbability(card))

        self.uni_Deck.reset()
        rec_dealer_sim((dealer_up_card,), 1)
        return dealer_probabilities

    @lru_cache(maxsize=None)
    def calculate_ev_double(self, player_hand, dealer_up_card, deck):
        if len(player_hand) != 2:
            return float('-inf')
        
        ev = 0
        for card in deck.cards():
            if deck.deck[card] <= 0:
                continue
            new_hand = player_hand + (card,)
            new_deck = deck.copy()
            new_deck.deck[card] -= 1
            card_prob = deck.getProbability(card)
            
            if Player.calculate_total(new_hand) > 21:
                ev -= 2 * card_prob
            else:
                ev += 2 * self.calculate_ev_stand(new_hand, dealer_up_card, new_deck) * card_prob
        
        return ev

    @lru_cache(maxsize=None)
    def calculate_ev_split(self, player_hand, dealer_up_card, deck, aces=False):
        if player_hand[0] != player_hand[1] or len(player_hand) != 2:
            return float('-inf')

        if player_hand[0] == 'A' and not aces:
            return self.calculate_ev_split_aces(player_hand, dealer_up_card, deck)

        pairs_chart = {
            '2,2': {'5': 'inf', '6': 'inf', '7': 'inf'} | {str(i): '-inf' for i in [2, 3, 4, 8, 9, 10, 11]},
            '3,3': {'4': 'inf', '5': 'inf', '6': 'inf', '7': 'inf'} | {str(i): '-inf' for i in [2, 3, 8, 9, 10, 11]},
            '4,4': {str(i): '-inf' for i in range(2, 12)},
            '5,5': {str(i): '-inf' for i in range(2, 10)} | {'10': '-inf', '11': '-inf'},
            '6,6': {str(i): 'inf' for i in range(2, 7)} | {str(i): '-inf' for i in range(7, 12)},
            '7,7': {str(i): 'inf' for i in range(2, 9)} | {str(i): '-inf' for i in range(9, 12)},
            '8,8': {str(i): 'inf' for i in range(2, 12)},
            '9,9': {str(i): '-inf' for i in range(2, 12)},
            '10,10': {str(i): '-inf' for i in range(2, 12)},
        }

        return float(pairs_chart.get(f'{player_hand[0]},{player_hand[0]}', {}).get(str(dealer_up_card), '-inf'))

    def calculate_ev_split_aces(self, player_hand, dealer_up_card, deck):
        ev = 0
        for card1 in deck.cards():
            if deck.deck[card1] <= 0:
                continue
            for card2 in deck.cards():
                if deck.deck[card2] <= 0:
                    continue
                new_hands = [(player_hand[0], card1), (player_hand[1], card2)]
                new_deck = deck.copy()
                new_deck.deck[card1] -= 1
                new_deck.deck[card2] -= 1
                prob = deck.getProbability(card1) * deck.getProbability(card2)
                
                ev += (prob) * sum(self.calculate_ev_stand(hand, dealer_up_card, new_deck) for hand in new_hands)

        return ev

    def clear_cache(self):
        self.memoized_dealer.clear()
        self.memoized_decisions.clear()
        self.decide.cache_clear()
        self.calculate_ev_hit.cache_clear()
        self.calculate_ev_stand.cache_clear()
        self.calculate_ev_double.cache_clear()
        self.calculate_ev_split.cache_clear()
        self.simulate_dealer.cache_clear()
