from .agent import Agent

class Player(Agent):
    def __init__(self, startChips):
        super().__init__()
        self.chips = startChips
    
    def isBrokie(self):    
        return self.chips == 0

    def gainChips(self, numChips):
        self.chips += numChips

    def loseChips(self, numChips):
        self.chips -= numChips