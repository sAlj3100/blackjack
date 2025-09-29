from .agent import Agent

class bjDealer(Agent):
    def __init__(self):
        super().__init__()
        self.facedown = []
        self.hitting = True

    def flip(self):
        if self.facedown:
            self.getCard(self.facedown.pop())

    def setFaceDown(self):
        if self.hand:
            self.facedown.append(self.hand.pop())

    def isHit(self,limit):
        if self.score >= limit:
            self.hitting = False
        else:
            self.hitting = True
    
    def reset(self):
        super().reset()
        self.facedown = []
        self.hitting = True