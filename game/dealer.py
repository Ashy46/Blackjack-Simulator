class Dealer:
    def __init__(self) -> None:
        self.hand = []

    def decision(self):
        if sum(self.hand) > 17:
            return 'Stand'
        else:
            return "Hit"
    def getUpCard(self):
        return self.hand[0]
    
