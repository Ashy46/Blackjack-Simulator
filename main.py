
from game.blackjack import BlackJackGame
from game.player import Player
from game.dealer import Dealer
from game.Deck import Deck
from solvers.base_solver import BaseSolver
from solvers.emanSolver import EmanSolver
from solvers.bayesianSolver import BayesianSolver

def main():
    players = [Player("Player 1", EmanSolver()), Player("Player 2", BayesianSolver())]
    dealer = Dealer()
    deck = Deck(8)
    game = BlackJackGame(players, dealer, deck)
    for i in range(100):
        game.play_round()
    
    for player in players:
        profit = str(player.bankroll)
        print(player.name + ": " + profit)
    
main()  # Output: ['Win'], ['Loss'], 1, -1 or something similar
