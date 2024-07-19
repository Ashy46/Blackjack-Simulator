class Player:
    def __init__(self, name, solver):
        self.name = name
        self.solver = solver
        self.hand = []
        self.hands = []
        self.bankroll = 1000
        self.result = []
        self.bet = 1
        self.bets = []

    def makeDecision(self, dealer_card, deck, hand):
        # Basic strategy (simplified)
        player_total = self.calculate_total(hand)
        
        if len(hand) == 2 and hand[0] == hand[1]:
            if hand[0] in ['8', 'A']:
                return "Split"
        
        if len(hand) == 2 and player_total in [10, 11] and self.calculate_total([dealer_card]) < 10:
            return "Double Down"
        
        if player_total < 17:
            return "Hit"
        else:
            return "Stand"

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