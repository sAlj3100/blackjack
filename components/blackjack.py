import player
import deck
import bjDealer

START_CHIPS = 1000
PAYOUT = 10
DECK_LIMIT = 26
BJ_MULTIPLIER = 2
DEALER_LIM = 17

class Blackjack:

    def __init__(self, startChips, deckMin, dealerLimit, payout, bjMultiplier):
        self.deck = deck.Deck()
        self.player = player.Player(startChips)
        self.dealer = bjDealer.bjDealer(startChips, dealerLimit)
        self.result = 0
        self.state = (0,0,0,0,'|',0,0,0,0)
        self.deckMin = deckMin
        self.payout = payout
        self.bjPayout = payout*bjMultiplier

    def cardValue(self, card):
        match card.rank: 
            case "J"|"Q"|"K":
                return 10
            case "A":
                return 11
            case val if val in [i for i in range(2,11)]:
                return val

    def aceCount(self, agent):
        aces = 0
        for card in agent.hand:
            if card.rank == "A":
                aces += 1
        return aces

    def handScore(self,agent):
        newScore = 0 
        aces = self.aceCount()
        for card in self.agent.hand:
            newScore += self.cardValue(card)    
        if newScore > 21 and aces > 0:
                while aces > 0 and newScore > 21:
                    newScore -= 10
                    aces -= 1
        agent.score = newScore
        return agent.score

    def isBlackjack(self, agent):
        if agent.handScore() == 21 and len(agent.hand) == 2:
            agent.state = 1
            return True

    def isBust(self,agent):
        if self.handScore(agent) > 21:
            agent.state = -1
            return True
    
    def updateState(self):
        self.state = (self.player.printHand(),self.handScore(self.player), self.player.state, self.player.chips, 
                    '|', 
                    self.handScore(self.dealer), self.dealer.printHand(), self.dealer.state, self.dealer.chips)
        return self.state

    def resetRound(self):
        self.player.reset()
        self.dealer.reset()
        if len(self.deck) < self.deckLimit:
            self.shoe.resetDeck()
        return

    def deal(self, agent):        
        agent.hand.append(self.deck.pop())
        self.updateState()
        return

    def gameSetup(self):
        self.deck.shuffleDeck()
        for i in range(0,2):
            self.deal(self.player)
        for i in range(0,2):
            self.deal(self.dealer)
        self.dealer.setFaceDown()
        self.updateState()
        return 

    def dealerPlay(self):
        #Dealer has a limit on hand value
        self.dealer.flip()
        while self.dealer.isHit():
            self.deal(self.dealer)
            if self.isBust(self.dealer):
                self.dealer.state = -1
                break
        self.updateState()
        return 

    def playerPlay(self):
        print(self.state)
        playerAction = input("Stand or Hit? ")
        if playerAction == "Hit":
            self.deal(self.player)
            self.updateState()
            if self.isBust(self.player):
                self.player.state = -1
                self.updateState()
                return False
        else:
            return False

    def endRound(self):
        if self.player.state > self.dealer.state:
            #Win with a natty BJ
            if self.isBlackjack(player) == True:
                self.player.gainChips(self.bjPayout)
                self.dealer.loseChips(self.bjPayout)
            #Win normally
            else:
                self.player.gainChips(self.payout)
                self.dealer.gainChips(self.payout)
            self.updateState()
            return 1
        #Lose
        elif self.player.state < self.dealer.state:
            self.player.loseChips(self.payout)
            self.dealer.gainChips(self.payout)
            self.updateState()
            return -1
        #Draw
        else:
            self.updateState()
            return 0

    def printWinner(self):
        match self.endRound():
            case 1:
                print("Player Wins!")
            case -1:
                print("Dealer Wins!")
            case 0:
                print("Draw!")

    def bjRound(self):
        self.gameSetup()
        #Check natty BJ.
        if self.player.isBlackjack():
            self.dealer.flip()
            self.endRound()
            self.updateState()
        else:
            while self.playerPlay()!= False:
                self.playerPlay()
        
        if self.isBust(player) == False:
            self.dealerPlay()
            print(self.state)
        else:
            self.endRound()
        self.endRound()
        self.printWinner()

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
    haveInt = False
    while haveInt == False:
        try:
            numRounds = int(input("How many rounds?"))
            haveInt = True
        except ValueError:
            print("Input positive integer.")
    game = Blackjack()
    game.playMany(numRounds)