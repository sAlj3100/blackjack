import random as rand
from ..card import card

class Deck:
    def __init__(self, ranks, suits):
        self.cards= [card.Card(rank, suit) for rank in ranks for suit in suits]
        self.ranks = ranks
        self.suits = suits
        
    def print(self):
        return [str(card) for card in self.cards]
    
    def shuffle(self):
        rand.shuffle(self.cards)
    
    def deal(self):
        return self.cards.pop()
    
    def reset(self):
        self.cards = [card.Card(rank, suit) for rank in self.ranks for suit in self.suits]
        self.shuffle()