class Player:
    def __init__(self, startChips):
        self.hand = []
        self.state = 0
        self.chips = startChips
        self.score = 0

    def printHand(self):
        print([str(card for card in self.hand)])

    def getCard(self, card):
        self.hand.append(card)
    
    def isBrokie(self):    
        if self.chips == 0:
            return True

    def gainChips(self, numChips):
        self.chips += numChips

    def loseChips(self, numChips):
        self.chips -= numChips

    def reset(self):
        self.hand = []
        self.state = 0