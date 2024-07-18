class BlackJackGame:
    def __init__(self, players, dealer, deck) -> None:
        self.players = players
        self.dealer = dealer
        self.deck = deck
        pass

    def play_round(self):
        #Deal the initial cards out(for simplicity, everyone makes a bet of 1)
        for player in self.players:
            player.hand[0] = self.deck.deal()

        #Deal the down card for dealer
        self.dealer.hand[1] = self.deck.deal()

        #Last Card for each player
        for player in self.players:
            player.hand[1] = self.deck.deal()

        #Deal the up card for dealer
        self.dealer.hand[0] = self.deck.deal()

        #Player's Turn
        for player in self.player:
            while True:
                decision = player.makeDecision(self.dealer.getUpCard(), self.deck)
                if decision == 'Split':
                    #Implement after I commit to main
                    break
                elif decision == 'Hit':
                    player.hand.append(self.deck.deal())
                    if sum(player.hand) > 21:
                        break
                elif decision == "Stand":
                    break
        
        #Dealer's Turn
        while self.dealer.decision() == "Hit":
            self.dealer.hand.append(self.deck.deal())

        #Update all the scores
        self. settle_Results()

    #Helps update scores
    def settle_Results(self):
        pass