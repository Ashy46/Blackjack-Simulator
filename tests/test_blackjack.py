import pytest
from game.blackjack import BlackJackGame
from game.player import Player
from game.dealer import Dealer
from game.Deck import Deck

class MockSolver:
    def decide(self, hand, dealer_card, deck):
        return "Stand"

@pytest.fixture
def game():
    players = [Player("PLayer 1", MockSolver()), Player("Player 2", MockSolver())]
    dealer = Dealer()
    dealer.hand = ["10", "10"]
    deck = Deck(1)
    return BlackJackGame(players, dealer, deck)

def test_bjGame_init(game):
    assert isinstance(game.dealer, Dealer)
    assert len(game.players) == 2
    assert isinstance(game.deck, Deck)

def test_play_round(game):
    game.play_round()
    for player in game.players:
        assert len(player.hands) >= 1
        assert len(player.bets) >= 1
        assert player.result != []
    assert len(game.dealer.hand) >= 2

def test_player_turn(game):
    game.players[0].hand = ["7", "7"]
    game.player_turn(game.players[0])
    assert len(game.players[0].hands) == 1
    assert len(game.players[0].bets) == 1
    
def test_settle_bets(game):
    game.dealer.hand = ["10", "Q"]
    game.players[0].hands = [["A", "K"]]
    game.players[0].bets = [1]
    game.players[1].hands = [["9", "9"]]
    game.players[1].bets = [1]
    game.settle_Results()
    assert game.players[0].result == ["Win"]
    assert game.players[1].result == ["Loss"]