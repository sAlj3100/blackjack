import player

class bjDealer(player.Player):

    facedown = []

    def flip(self):
        self.hand.append(self.facedown.pop())
        return 
    
    def setFaceDown(self):
        self.facedown.append(self.hand.pop())
        return
    
    def isHit(self):
        if self.score <self.cap:
            return True
        return False