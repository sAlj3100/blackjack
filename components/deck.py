import random as rand
import card

class Deck:
    def __init__(self, ranks, suits):
        self.cards= [card.Card(rank, suit) for rank in ranks for suit in suits]
    
    def printDeck(self):
        return [str(card) for card in self.cards]
    
    def shuffle(self):
        return rand.shuffle(self.cards)
    
    def dealCard(self):
        return self.cards.pop()
    
    def reset(self):
        self.cards = [card.Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        return rand.shuffle(self.cards)