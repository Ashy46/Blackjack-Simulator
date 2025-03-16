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
        self.bankroll_change = 0

    def makeDecision(self, dealer_card, deck, hand):
        # Basic strategy (simplified)
        return self.solver.decide(hand, dealer_card, deck)

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
    
    def end_round(self):
        """
        Signal end of round to solve
        """
        if hasattr(self.solver, 'update'):
            self.solver.update(self.bankroll_change, [], self.hand[0] if self.hand else '2')