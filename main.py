from game.blackjack import BlackJackGame
from game.player import Player
from game.dealer import Dealer
from game.deck import Deck
from solvers.base_solver import BaseSolver
from solvers.emanSolver import EmanSolver
from solvers.bayesianSolver import BayesianSolver
from solvers.q_learning_solver import QLearningSolver
import numpy as np
import pickle  # For saving Q-table

def main():
    dealer = Dealer()
    deck = Deck(shoes=6)
    
    # Create players with different solvers
    players = [
        Player("QLearner", QLearningSolver(alpha=0.1, gamma=0.95, epsilon=0.1)),
        Player("Basic", EmanSolver()),
    ]

    # train_q_learning.py
    EPISODES = 2_000_000  # Blackjack needs extensive training[7][14]
    DECAY_EVERY = 100_000

    for episode in range(EPISODES):
        game = BlackJackGame([players[0]], dealer, deck)
        game.play_round()
    
    # Smooth epsilon decay
        if episode % DECAY_EVERY == 0:
            players[0].solver.epsilon = max(0.01, players[0].solver.epsilon * 0.95)
    
        # Track key metrics
        if episode % 100_000 == 0:
            print(f"States: {len(players[0].solver.q_table)} | Avg Q: {np.mean(list(players[0].solver.q_table.values())):.2f}")

    players[0].solver.print_key_decision()

    # Training phase
    print("Training Q-learning agent...")
    for i in range(1_00_000): 
        game = BlackJackGame([players[0]], dealer, deck)
        game.play_round()
        
        # Decay exploration rate
        if i % 50_000 == 0:
            players[0].solver.epsilon = max(0.01, players[0].solver.epsilon * 0.9)

        
    
    # Save learned Q-table
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(players[0].solver.q_table, f)
    
    # Evaluation phase
    print("\nTesting strategies...")
    test_players = [
        Player("Trained Q", QLearningSolver(epsilon=0)),
        Player("Basic", EmanSolver()),
    ]
    
    # Load trained Q-table
    with open('q_table.pkl', 'rb') as f:
        test_players[0].solver.q_table = pickle.load(f)
    
    # Run evaluation games
    test_deck = Deck(shoes=6)
    for i in range(100_000):
        game = BlackJackGame(test_players, dealer, test_deck)
        game.play_round()
            
    # Results
    print("\nFinal Results:")
    for player in test_players:
        profit = player.bankroll - 10000
        print(f"{player.name}: {profit:+} ({profit/100_000:.2%} ROI)")

if __name__ == "__main__":
    main()