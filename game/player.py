class Player:
    def __init__(self, name, solver):
        self.name = name
        self.solver = solver
        self.hand = []
        self.bankroll = 1000
    
    def makeDecision(self, dealer_card, deck):
        return self.solver.decide(self.hand, )
    