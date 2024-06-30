import random as rand
import cards

class Deck:
    suits = ['H','S','D','C']
    ranks = [i for i in range(2,11)] + ['J','Q','K','A']
    
    
    
    def __init__(self):
        self.deck = [cards.Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        
        
    def shuffleDeck(self):
        return rand.shuffle(self.deck)
    
    
    def resetDeck(self):
        self.deck = [cards.Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        return rand.shuffle(self.deck)