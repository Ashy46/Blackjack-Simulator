import pytest
from game.Deck import Deck

@pytest.fixture
def deck():
    return Deck(1)

def test_deck_init(deck):
    assert deck.shoes == 1
    assert sum(deck.deck.values()) == 52
    assert len(deck.deck) == 13

def test_deal(deck):
    n = deck.deal()
    assert n in deck.deck.keys()
    assert sum(deck.deck.values()) == 51

def test_size(deck):
    assert deck.size() == 52
    deck.deal()
    assert deck.size() == 51

def test_getProbability(deck):
    n = deck.getProbability("A")
    assert n == (4/52)

