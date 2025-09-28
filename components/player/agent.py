class Agent:
    def __init__(self):
        self.hand = []
        self.score = 0
        self.bust = False
        self.blackjack = False
        self.win = False
    
    def printHand(self):
        return [str(card) for card in self.hand]
    
    def getCard(self, card):
        self.hand.append(card)
    
    def reset(self):
        self.hand = []
        self.score = 0
        self.bust = False
        self.blackjack = False
