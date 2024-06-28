import random as rand

class Card:

    def __init__(self, rank, suit):

        self.rank = rank
        self.suit = suit


    def __str__(self):

        return (f"{self.rank},{self.suit}")


    def cardValue(self):

        if self.rank == "J" or self.rank == "Q" or self.rank == "K":
            return 10

        elif self.rank == "A":
            return 11

        else:
            return self.rank


class Player():
    
    def __init__(self):

        self.hand = []
        self.state = 0
        self.chips = 1000
        self.score = 0


    def aceCount(self):
        aces = 0
        
        for card in self.hand:
            if card.rank == "A":
                aces += 1
                
        return aces


    def handScore(self):
        
        newScore = 0 
        aces = self.aceCount()
        
        for card in self.hand:
            newScore += card.cardValue()
        
        if newScore > 21 and aces > 0:
                while aces > 0 and newScore > 21:
                    newScore -= 10
                    aces -= 1
                    
        self.score = newScore
        
        return self.score


    def isBlackjack(self):
        
        if self.handScore() == 21 and len(self.hand) == 2:
            self.state = 1
            return True


    def isBust(self):
        
        if self.handScore() > 21:
            self.state = -1
            return True


    def isBrokie(self):
        
        if self.chips == 0:
            return True


    def reset(self):

        self.hand = []
        self.state = 0
        return


class Dealer(Player):

    facedown = []

    def flip(self):
        self.hand.append(self.facedown.pop())
        return 


    def isHit(self):
        if self.handScore() < 17:
            return True
        
        return False


class Game:
    suits = ['H','S','D','C']
    ranks = [i for i in range(2,11)] + ['J','Q','K','A']
    
    
    
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in Game.ranks for suit in Game.suits]
        self.player = Player()
        self.dealer = Dealer()
        self.result = 0
        self.state = (0,0,0,0,0,0)
        #self.actions = {"Stand":0,"Hit":1}
        #self.actions = {"Stand":0,"Hit":1,"Double Down":2,"Split":3}


    def updateState(self):
        
        self.state = (self.player.handScore(), self.player.state, self.player.chips, self.dealer.handScore(), self.dealer.state, self.dealer.chips)
        
        return self.state


    def shuffleDeck(self):
        return rand.shuffle(self.deck)


    def resetDeck(self):
        return self.deck


    def resetRound(self):
        self.player.reset()
        self.dealer.reset()
        
        if len(self.deck) < 26:
            self.resetDeck()
        
        return


    def deal(self, agent):        
        agent.hand.append(self.deck.pop())
        self.updateState()
        return


    def gameSetup(self):
        
        self.shuffleDeck()
        
        for i in range(0,2):
            self.deal(self.player)
        
        for i in range(0,2):
            self.deal(self.dealer)
        self.dealer.facedown.append(self.dealer.hand.pop())
        
        self.updateState()
        
        return self.state


    def dealerPlay(self):
        #Dealer is soft17
        self.dealer.flip()
        
        while self.dealer.isHit():
            self.deal(self.dealer)
                
            if self.dealer.isBust():
                self.dealer.play = -1
                break
        
        self.updateState()
        
        return 


    def playerPlay(self):
        
        print(self.state)
        playerAction = input("Stand or Hit? ")
        
        if playerAction == "Hit":
            self.deal(self.player)
            self.updateState()
                
            if self.player.isBust():
                self.player.play = -1
                self.updateState()
                return False
        
        else:
            return False


    def bjRound(self):
        
        self.gameSetup()
        
        #Check natty BJ.
        if self.player.isBlackjack():
            self.dealer.flip()
            
            if self.dealer.isBlackjack():
                self.resetRound()
                return 0
            
            else:
                self.player.chips += 10
                self.dealer.chips -= 10
                self.resetRound()
                self.updateState()
            
            return 1
        
        else:
            while self.playerPlay()!= False:
                self.playerPlay()
        
        if self.player.isBust() == False:
            self.dealerPlay()
        
            print(self.state)
        
        #Compare hands, award chips to winner, return W/L/D
        if self.player.score > self.dealer.score:
            self.player.chips += 10
            self.dealer.chips -= 10
            print(self.state)
            self.resetRound()
            self.updateState()
            return 1
        
        if self.player.score < self.dealer.score or self.player.state == -1:
            self.dealer.chips += 10
            self.player.chips -= 10
            print(self.state)
            self.resetRound()
            self.updateState()
            return -1
        
        if self.player.score == self.dealer.score:
            print(self.state)
            self.resetRound()
            self.updateState()
            return 0
#I think trying to do too much with this block. Can break up into smaller functions.

    def playMany(self, numRounds):
        
        if numRounds == 1:
            self.bjRound()
            return
        
        for i in range(0,numRounds):
            self.bjRound()
            
            if self.player.isBrokie():
                break
                
        return self.state


if __name__ == "__main__":
    
    print("Blackjack good game yes.")
    try:
        numRounds = int(input("How many rounds?"))
    
    except ValueError:
        print("Input positive integer.")
    
    game = Game()
    game.playMany()
