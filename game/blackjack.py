from game.player import Player
from game.dealer import Dealer
from game.Deck import Deck

class BlackJackGame:
    def __init__(self, players, dealer, deck) -> None:
        self.players = players
        self.dealer = dealer
        self.deck = deck

    def play_round(self):
        # If we run out of cards, refresh shoe
        if self.deck.size() < (0.35*self.deck.shoes*52):
            self.deck.reset()
        # Deal the initial cards out (for simplicity, everyone makes a bet of 1)
        for player in self.players:
            player.hand = [self.deck.deal()]
            player.bet = 1

        self.dealer.hand = [self.deck.deal()]

        # Deal the second card
        for player in self.players:
            player.hand.append(self.deck.deal())

        self.dealer.hand.append(self.deck.deal())
        # Player's Turn
        for player in self.players:
            print(player.hand)
            self.player_turn(player)

        # Dealer's Turn
        while self.dealer.decision() == "Hit":
            self.dealer.hand.append(self.deck.deal())

        # Update all the scores
        self.settle_Results()

    def player_turn(self, player):
        hands = [player.hand]
        bets = [player.bet]
        
        for i, hand in enumerate(hands):
            while True:
                decision = player.makeDecision(self.dealer.getUpCard(), self.deck, hand)
                if decision == 'Split' and len(hand) == 2 and hand[0] == hand[1]:
                    new_hand = [hand.pop()]
                    new_hand.append(self.deck.deal())
                    hand.append(self.deck.deal())
                    hands.append(new_hand)
                    bets.append(bets[i])
                elif decision == 'Double' and len(hand) == 2:
                    bets[i] *= 2
                    hand.append(self.deck.deal())
                    break
                elif decision == 'Hit' or decision == 'Double' and len(hand) > 2:
                    while decision == 'Hit' and Player.calculate_total(hand) <= 21 or decision == 'Double' and Player.calculate_total(hand) <= 21:
                        hand.append(self.deck.deal())
                        decision = player.makeDecision(self.dealer.getUpCard(), self.deck, hand)
                    break
                elif decision == "Stand":
                    break
        
        player.hands = hands
        player.bets = bets

    def settle_Results(self):
        dealer_total = self.dealer.getTotal()
        for player in self.players:
            player.result = []
            player.bankroll_change = 0
            for i, hand in enumerate(player.hands):
                player_total = Player.calculate_total(hand)
                if player_total > 21:
                    result = "Loss"
                elif dealer_total > 21:
                    result = "Win"
                elif dealer_total > player_total:
                    result = "Loss"
                elif dealer_total < player_total:
                    result = "Win"
                else:
                    result = "Push"
                
                
                # Update bankroll
                if result == "Win":
                    player.bankroll_change += player.bets[i]
                elif result == "Loss":
                    player.bankroll_change -= player.bets[i]
            
            player.bets = []
            player.hands = []
            player.bankroll += player.bankroll_change