import random as rand
import card

class Deck:
    suits = ['H','S','D','C']
    ranks = [i for i in range(2,11)] + ['J','Q','K','A']
    

    def __init__(self):
        self.cards= [card.Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
            
    def shuffleDeck(self):
        return rand.shuffle(self.cards)
    
    def dealCard(self):
        return self.cards.pop()
    
    def resetDeck(self):
        self.cards = [card.Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        return rand.shuffle(self.cards)