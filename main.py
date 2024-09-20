
from game.blackjack import BlackJackGame
from game.player import Player
from game.dealer import Dealer
from game.Deck import Deck
from solvers.base_solver import BaseSolver
from solvers.emanSolver import EmanSolver
from solvers.bayesianSolver import BayesianSolver

def main():
    players = [Player("Player 2", BayesianSolver())]
    dealer = Dealer()
    deck = Deck(6)
    game = BlackJackGame(players, dealer, deck)
    for i in range(1):
        game.play_round()
        players[0].solver.clear_cache()
    
    for player in players:
        profit = str(player.bankroll)
        print(player.name + ": " + profit)
    return (players[0].bankroll - 10000)
result = main()  # Output: ['Win'], ['Loss'], 1, -1 or something similar
print(result)