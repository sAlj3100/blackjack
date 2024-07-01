import player

class bjDealer(player.Player):

    facedown = []

    def flip(self):
        self.hand.append(self.facedown.pop())
        return 
    
    def setFaceDown(self):
        self.facedown.append(self.hand.pop())
        return
    
    def isHit(self,limit):
        if self.score < limit:
            return True
        return False