import player

class bjDealer(player.Player):
    facedown = []

    def flip(self):
        self.hand.append(self.facedown.pop())
    
    def setFaceDown(self):
        self.facedown.append(self.hand.pop())
    
    def isHit(self,limit):
        if self.score < limit:
            return True
        return False