import pytest
from game.dealer import Dealer

@pytest.fixture
def dealer():
    return Dealer()

def test_dealer_init(dealer):
    assert dealer.hand == []

def test_getTotal(dealer):
    dealer.hand = ["A" , "6"]
    assert dealer.getTotal() == 17
    
    dealer.hand = ["10", "6"]
    assert dealer.getTotal() == 16

def test_decision(dealer):
    dealer.hand = ["3", "4"]
    assert dealer.decision() == "Hit"

    dealer.hand = ["A", "8"]
    assert dealer.decision() == "Stand"

    dealer.hand = ["A", "5", "10"]
    print(dealer.getTotal())
    assert dealer.decision() == "Hit"

def test_getUpCard(dealer):
    dealer.hand = ["A", "9"]
    assert dealer.getUpCard() == "A"
