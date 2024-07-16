
from game.Deck import Deck
from solvers.base_solver import BaseSolver

class BayesianSolver(BaseSolver):
    def decide(self, player_hand, dealer_up_card, deck):
        pass

    def __init__(self, deck):
        self.priorProbability = self.priorProbabilities(deck)
        self.currentProbs = self.priorProbability

    #Calculates the  prior probablities for each possible dealer hand 
    def priorProbabilities(deck):
        priorProbs = {}
        total_cards = deck.size()

        #ALl the two card probabilities
        for card1 in deck:
            for card2 in deck:
                hand = tuple(sorted([card1, card2]))
                if hand not in priorProbs:
                    #if cards are the same, then its just P(C1) * P(C2|C1)
                    if card1 == card2:
                        p = deck.getProbability(card1) * (deck.deck[card1] - 1)/(total_cards - 1)
                    #if they are not equal, then its just P(C!) * P(C2|C1) * 2(Two different ways to draw the 2 cards)
                    else:
                         p = deck.getProbability(card1) * (deck.deck[card2])/(total_cards - 1)
                priorProbs[hand] = p

        return priorProbs

    def likelihood_function(observed_card, true_hand, deck):
        if observed_card in true_hand:
            # If the card is in the hand, 50% chance it's the up card
            return 0.5
        else:
            # If not in the hand, probability depends on remaining cards
            return deck.getProbability(observed_card)



