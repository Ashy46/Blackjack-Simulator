from game.Deck import Deck
from game.player import Player
from solvers.base_solver import BaseSolver
from functools import lru_cache

class BayesianSolver(BaseSolver):
    def decide(self, player_hand, dealer_up_card, deck, return_ev=False):
        ev_hit = self.calculate_ev_hit(tuple(player_hand), dealer_up_card, deck)
        ev_stand = self.calculate_ev_stand(tuple(player_hand), dealer_up_card, deck)
        ev_double = self.calculate_ev_double(tuple(player_hand), dealer_up_card, deck)
        ev_split = self.calculate_ev_split(tuple(player_hand), dealer_up_card, deck)
        
        best_ev = max(ev_hit, ev_stand, ev_double, ev_split)
        
        if return_ev:
            return best_ev
        print(player_hand, dealer_up_card, best_ev)
        if best_ev == ev_hit:
            return 'Hit'
        elif best_ev == ev_double:
            return 'Double'
        elif best_ev == ev_split:
            return 'Split'
        else:
            return 'Stand'
    
    @lru_cache(maxsize=None)
    def calculate_ev_hit(self, player_hand, dealer_up_card, deck):
        player_total = Player.calculate_total(player_hand)
        if player_total > 21:
            return -1
        if player_total == 21:
            return 1
        ev = 0
        for card in deck.cards():
            new_hand = player_hand + (card,)
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
        
        dealer_probabilities = self.simulate_dealer(dealer_up_card, deck)
        return sum(prob if dealer_total < player_total or dealer_total > 21 else -prob
                   for dealer_total, prob in dealer_probabilities.items())

    @lru_cache(maxsize=None)
    def simulate_dealer(self, dealer_up_card, deck):
        dealer_probabilities = {}
        
        def rec_dealer_sim(current_hand, current_deck, probability):
            total = Player.calculate_total(current_hand)
            
            if total > 21 or total >= 17:
                dealer_probabilities[total] = dealer_probabilities.get(total, 0) + probability
            else:
                for card in current_deck.cards():
                    new_hand = current_hand + (card,)
                    new_deck = current_deck.copy()
                    new_deck.deck[card] -= 1
                    rec_dealer_sim(new_hand, new_deck, probability * current_deck.getProbability(card))

        rec_dealer_sim((dealer_up_card,), deck, 1)
        return dealer_probabilities

    def calculate_ev_double(self, player_hand, dealer_up_card, deck):
        if len(player_hand) != 2:
            return float('-inf')
        
        ev = 0
        for card in deck.cards():
            new_hand = player_hand + (card,)
            new_deck = deck.copy()
            new_deck.deck[card] -= 1
            card_prob = deck.getProbability(card)
            
            if Player.calculate_total(new_hand) > 21:
                ev -= 2 * card_prob
            else:
                ev += 2 * self.calculate_ev_stand(new_hand, dealer_up_card, new_deck) * card_prob
        
        return ev

    def calculate_ev_split(self, player_hand, dealer_up_card, deck):
        if player_hand[0] != player_hand[1] or len(player_hand) != 2:
            return float('-inf')
        
        ev = 0
        for card1 in deck.cards():
            for card2 in deck.cards():
                hand1 = (player_hand[0], card1)
                hand2 = (player_hand[1], card2)
                new_deck = deck.copy()
                new_deck.deck[card1] -= 1
                new_deck.deck[card2] -= 1
                prob = deck.getProbability(card1) * deck.getProbability(card2)
                ev += (self.decide(hand1, dealer_up_card, new_deck, return_ev=True) +
                       self.decide(hand2, dealer_up_card, new_deck, return_ev=True)) * prob
        
        return ev