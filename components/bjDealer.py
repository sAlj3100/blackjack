import player


class Dealer(player.Player()):
    
    def __init__(self, startChips, dealerLim):
        self.facedown = []
        self.hand = []
        self.cap = dealerLim
        self.chips = startChips
        self.state = 0 
        
        
    def flip(self):
        self.hand.append(self.facedown.pop())
        return 


    def isHit(self):
        if self.score <self.cap:
            return True
        return False