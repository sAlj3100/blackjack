import player
import deck
import bjDealer

START_CHIPS = 1000
PAYOUT = 10
BJ_MULTIPLIER = 2
DECK_LIMIT = 26
BJ_PAYOUT = BJ_MULTIPLIER*PAYOUT
DEALER_LIM = 17

class Blackjack:
    def __init__(self, startChips, payout, bjMultiplier, deckMin, dealerLimit):
        self.deck = deck.Deck(([i for i in range(2,11)] + ['J','Q','K','A']), ['H','S','D','C'])
        self.player = player.Player(startChips)
        self.dealer = bjDealer.bjDealer(startChips)
        self.result = 0
        self.state = (0,0,0,0,'|',0,0,0,0)
        self.deckMin = deckMin
        self.payout = payout
        self.bjPayout = payout*bjMultiplier
        self.dealerLimit = dealerLimit

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
            if card.getRank() == "A":
                aces += 1
        return aces

    def handScore(self,agent):
        newScore = 0 
        aces = self.aceCount(agent)
        for card in agent.hand:
            newScore += self.cardValue(card)    
        aces = self.aceCount(agent)
        for card in agent.hand:
            newScore += self.cardValue(card)
        if newScore > 21 and aces > 0:
                while aces > 0 and newScore > 21:
                    newScore -= 10
                    aces -= 1
        agent.score = newScore

    def isBlackjack(self, agent):
        if agent.score == 21 and len(agent.hand) == 2:
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
        if len(self.deck) < self.deckMin:
            self.deck.reset()

    def deal(self, agent):        
        agent.hand.append(self.deck.cards.pop())
        self.updateState()

    def gameSetup(self):
        self.deck.shuffle()
        for i in range(0,2):
            self.deal(self.player)
        for i in range(0,2):
            self.deal(self.dealer)
        self.dealer.facedown.append(self.dealer.hand.pop())
        self.updateState()

    def dealerPlay(self):
        #Dealer has a limit on hand value
        self.dealer.flip()
        while self.dealer.isHit(self.dealerLimit):
            self.deal(self.dealer)
            if self.isBust(self.dealer):
                self.dealer.state = -1
                break
        self.updateState()

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

    def endRound(self):
        if self.player.state > self.dealer.state:
            match self.isBlackjack(self.player):
                #Win with a natty BJ
                case True: 
                    self.player.gainChips(self.bjPayout)
                    self.dealer.loseChips(self.bjPayout)
                #Win normally
                case False:
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
        match self.isBlackjack(self.player):
            case True:
            #If dealer BJ, draw
                self.dealer.flip()
                self.isBlackjack(self.dealer)
                self.endRound()
                self.updateState()
            case False:
                while self.playerPlay()!= False:
                    self.playerPlay()
                    
        match self.isBust(self.player):
            case False:
                self.dealerPlay()
                print(self.state)
            case True:
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
            print("Input positive integer. ")
    game = Blackjack(1000,10,2,26,17)
    game.gameSetup()
    game.player.printHand()
    print(len(game.deck.cards))
    print(game.handScore(game.player))
    #game.playMany(numRounds)