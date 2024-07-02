class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return (f"{self.rank},{self.suit}")
    
    def getRank(self):
        return self.rank
    
    def getSuit(self):
        return self.suit