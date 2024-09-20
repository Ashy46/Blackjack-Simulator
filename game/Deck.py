import random


class Deck:
    def __init__(self, shoes) -> None:
        #Number of decks being played with
        self.shoes = shoes
        self.deck = {}
        
        # 2-9
        for i in range(8):
            num = i + 2
            self.deck[str(num)] = 4 * shoes
        
        # 10
        self.deck["10"] = 4 * shoes
        
        # Face cards (Jack, Queen, King)
        for face in ["J", "Q", "K"]:
            self.deck[face] = 4 * shoes
        
        # Ace
        self.deck["A"] = 4 * shoes
        


    def size(self) -> int:
        total = 0
        for count in self.deck.values():
            total += count
        return total
    
    def deal(self):
        total_cards = self.size()
        random_pick = random.randint(1, total_cards)
        
        cumulative_count = 0
        for card, count in self.deck.items():
            cumulative_count += count
            if random_pick <= cumulative_count:
                self.deck[card] -= 1  # Remove the card from the deck
                return card
        
        raise ValueError("No card was selected. Check your deck definition.")

    def getProbability(self, card):
        probability  = (self.deck[card])/(self.size())
        return probability
    
    def reset(self):
        self.__init__(self.shoes)

    def cards(self):
        return self.deck.keys()
    
    def copy(self):
        new_deck = Deck(self.shoes)
        new_deck.deck = self.deck.copy()
        return new_deck
    