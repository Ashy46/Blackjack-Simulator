import time
from solvers import base_solver
from game.player import Player

#The EmanSovler, or the basic intuition solver, is just the basic solver that uses human intuition to make decisions.
class EmanSolver(base_solver.BaseSolver):
    def __init__(self):
        self.hard_totals = {
            5: {str(i): 'Hit' for i in range(2, 12)},
            6: {str(i): 'Hit' for i in range(2, 12)},
            7: {str(i): 'Hit' for i in range(2, 12)},
            8: {str(i): 'Hit' for i in range(2, 12)},
            9: {str(i): 'Hit' for i in range(2, 8)} | {'7': 'Hit', '8': 'Hit', '9': 'Hit', '10': 'Hit', '11': 'Hit'},
            10: {str(i): 'Double' for i in range(2, 10)} | {'10': 'Hit', '11': 'Hit'},
            11: {str(i): 'Double' for i in range(2, 11)} | {'11': 'Hit'},
            12: {'2': 'Hit', '3': 'Hit', '4': 'Stand', '5': 'Stand', '6': 'Stand'} | {str(i): 'Hit' for i in range(7, 12)},
            13: {str(i): 'Stand' for i in range(2, 7)} | {str(i): 'Hit' for i in range(7, 12)},
            14: {str(i): 'Stand' for i in range(2, 7)} | {str(i): 'Hit' for i in range(7, 12)},
            15: {str(i): 'Stand' for i in range(2, 7)} | {str(i): 'Hit' for i in range(7, 12)},
            16: {str(i): 'Stand' for i in range(2, 7)} | {str(i): 'Hit' for i in range(7, 12)},
            17: {str(i): 'Stand' for i in range(2, 12)},
            18: {str(i): 'Stand' for i in range(2, 12)},
            19: {str(i): 'Stand' for i in range(2, 12)},
            20: {str(i): 'Stand' for i in range(2, 12)}
        }

        self.soft_totals = {
            13: {'5': 'Double', '6': 'Double'} | {str(i): 'Hit' for i in [2, 3, 4, 7, 8, 9, 10, 11]},
            14: {'5': 'Double', '6': 'Double'} | {str(i): 'Hit' for i in [2, 3, 4, 7, 8, 9, 10, 11]},
            15: {'4': 'Double', '5': 'Double', '6': 'Double'} | {str(i): 'Hit' for i in [2, 3, 7, 8, 9, 10, 11]},
            16: {'4': 'Double', '5': 'Double', '6': 'Double'} | {str(i): 'Hit' for i in [2, 3, 7, 8, 9, 10, 11]},
            17: {'3': 'Double', '4': 'Double', '5': 'Double', '6': 'Double'} | {str(i): 'Hit' for i in [2, 7, 8, 9, 10, 11]},
            18: {'2': 'Stand', '3': 'Double', '4': 'Double', '5': 'Double', '6': 'Double', '7': 'Stand', '8': 'Stand'} | {str(i): 'Hit' for i in [9, 10, 11]},
            19: {str(i): 'Stand' for i in range(2, 12)},
            20: {str(i): 'Stand' for i in range(2, 12)},
            21: {str(i): 'Stand' for i in range(2, 12)}
        }

        self.pairs = {
            'A,A': {str(i): 'Split' for i in range(2, 12)},
            '2,2': {'5': 'Split', '6': 'Split', '7': 'Split'} | {str(i): 'Hit' for i in [2, 3, 4, 8, 9, 10, 11]},
            '3,3': {'4': 'Split', '5': 'Split', '6': 'Split', '7': 'Split'} | {str(i): 'Hit' for i in [2, 3, 8, 9, 10, 11]},
            '4,4': {str(i): 'Hit' for i in range(2, 12)},
            '5,5': {str(i): 'Double' for i in range(2, 10)} | {'10': 'Hit', '11': 'Hit'},
            '6,6': {str(i): 'Split' for i in range(2, 7)} | {str(i): 'Hit' for i in range(7, 12)},
            '7,7': {str(i): 'Split' for i in range(2, 9)} | {str(i): 'Hit' for i in range(9, 12)},
            '8,8': {str(i): 'Split' for i in range(2, 12)},
            '9,9': {str(i): 'Stand' for i in range(2, 12)},
        }

    def decide(self, player_hand, dealer_up_card, deck):
        hand_total = Player.calculate_total(player_hand)
        if hand_total >= 21:
            return 'Stand'
        if dealer_up_card == 'A':
            dealer_up_card = '11'
        if dealer_up_card in ['J', 'Q', 'K']:
            dealer_up_card = '10'
        dealer_up_card = str(dealer_up_card)
        print(dealer_up_card)
        print(player_hand)
        # Check for pairs
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            action = self.pairs.get(f'{player_hand[0]},{player_hand[0]}', {}).get(dealer_up_card, 'Stand')
            return action

        # Check for soft hands
        if 'A' in player_hand and hand_total <= 21:
            action = self.soft_totals.get(hand_total, {}).get(dealer_up_card, 'Stand')
            return action

        # Hard totals
        action = self.hard_totals.get(hand_total, {}).get(dealer_up_card, 'Stand')
        return action