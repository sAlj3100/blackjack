from .agent import Agent

class bjDealer(Agent):
    def __init__(self):
        super().__init__()
        self.facedown = []

    def flip(self):
        if self.facedown:
            self.getCard(self.facedown.pop())

    def setFaceDown(self):
        if self.hand:
            self.facedown.append(self.hand.pop())

    def isHit(self,limit):
        return self.score < limit
    
    def reset(self):
        super().reset()
        self.facedown = []