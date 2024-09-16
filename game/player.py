class Player:
    def __init__(self, name, solver):
        self.name = name
        self.solver = solver
        self.hand = []
        self.hands = []
        self.bankroll = 10000
        self.result = []
        self.bet = 1
        self.bets = []

    def makeDecision(self, dealer_card, deck, hand):
        # Basic strategy (simplified)
        return self.solver.decide(self.hand, dealer_card, deck)

    @staticmethod
    def calculate_total(hand):
        total = 0
        ace_count = 0
        for card in hand:
            if card in ["J", "Q", "K"]:
                total += 10
            elif card == "A":
                ace_count += 1
            else:
                total += int(card)
        
        for _ in range(ace_count):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1
        return total