from game.player import Player

class Dealer:
    def __init__(self) -> None:
        self.hand = []

    # Makes the decision of dealer
    def decision(self):
        # Hit 17s
        if self.getTotal() < 17:
            return "Hit"
        else:
            return "Stand"
        
    # Gets Up Card
    def getUpCard(self):
        return self.hand[0]
    
    def getTotal(self):
        return Player.calculate_total(self.hand)