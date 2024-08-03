import pytest
from game.player import Player
from game.Deck import Deck
from solvers.base_solver import BaseSolver 

class MockSolver(BaseSolver):
    def decide(self, hand, dealer_card, deck):
        return "Hit"

@pytest.fixture
def player():
    return Player("Test Player", MockSolver())

def test_player_init(player):
    assert player.name == "Test Player"
    assert player.bankroll == 1000
    assert player.bet == 1

def test_Make_decision(player):
    deck = Deck(1)
    assert player.makeDecision(["A"], deck, ["A", "A"]) == "Hit"

def test_calculate_total(player):
    player.hand = ["10", "6"]
    assert player.calculate_total(player.hand) == 16

    player.hand = ["A", "A", "10", "7"]
    assert player.calculate_total(player.hand) == 19

