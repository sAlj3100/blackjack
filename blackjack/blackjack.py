from components.player import player
from components.deck import deck
from components.player import bjdealer

class Blackjack:
    def __init__(self, startChips, payout, bjMultiplier, deckMin, dealerLimit):
        self.deck = deck.Deck(([i for i in range(2,11)] + ['J','Q','K','A']), ['H','S','D','C'])
        self.player = player.Player(startChips)
        self.dealer = bjdealer.bjDealer()
        self.deckMin = deckMin
        self.payout = payout
        self.bjPayout = payout*bjMultiplier
        self.dealerLimit = dealerLimit

    def get_state(self):
        return {
            "player_hand": self.player.printHand(),
            "player_score": self.player.score,
            "player_chips": self.player.chips,
            "dealer_hand": self.dealer.printHand(),
            "dealer_score": self.dealer.score,
        }

    def log_state(self):
        state = self.get_state()
        print(f"Player: {state['player_hand']} (Score: {state['player_score']}, Chips: {state['player_chips']})")
        print(f"Dealer: {state['dealer_hand']} (Score: {state['dealer_score']})")

    def cardValue(self, card):
        match card.rank: 
            case "J"|"Q"|"K":
                return 10
            case "A":
                return 11
            case _:
                return int(card.rank)

    def aceCount(self, agent):
        aces = 0
        for card in agent.hand:
            if card.rank == "A":
                aces += 1
        return aces

    def handScore(self,agent):
        newScore = 0 
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
            return True

    def isBust(self,agent):
        if agent.score > 21:
            return True

    def resetRound(self):
        self.player.reset()
        self.dealer.reset()
        if len(self.deck) < self.deckMin:
            self.deck.reset()

    def deal(self, agent):        
        agent.getCard(self.deck.deal())
        self.handScore(agent)

    def gameSetup(self):
        self.deck.shuffle()
        for i in range(0,2):
            self.deal(self.player)
        for i in range(0,2):
            self.deal(self.dealer)
        self.dealer.setFaceDown()
        self.handScore(self.dealer)

    def dealerPlay(self):
        self.dealer.flip()
        self.log_state()
        if self.isBlackjack(self.dealer):
            self.dealer.blackjack = True
            print("Game is rigged gg!")
            return
        while self.dealer.isHit(self.dealerLimit):
            self.deal(self.dealer)
            self.log_state()
            if self.isBust(self.dealer):
                self.dealer.bust = True
                print("Dealer busted!")
                break
            return

    def playerPlay(self):
        while True:    
            try:
                playerAction = input("Stand (s) or Hit? (h): ").strip().lower()
            except(EOFError, KeyboardInterrupt):
                print("\nInterrupted, goodbye...")
                return
            if playerAction == "h":
                self.deal(self.player)
                self.log_state()
                if self.isBust(self.player):
                    self.log_state()
                    self.player.bust = True
                    print("You busted!")    
                    return 
            elif playerAction == "s":
                return
            else:
                print("Invalid input, enter 'h' to Hit or 's' to Stand.")

    def compareHands(self):
        #player <= 21, dealer bust
        if self.player.bust == False and self.dealer.bust == True:
            if self.player.blackjack:
                self.player.win = True
                print("You won with a natty BJ!")
                return
            print("You won!")
            return 
        #player bust, dealer <= 21
        elif self.player.bust == True and self.dealer.bust == False:
            self.player.win = False
            print("You lost!")
            return 
        #neither bust, player > dealer
        elif self.player.score > self.dealer.score:
            self.player.win = True
            print("You won!")
            return
        #neither bust, player < dealer
        elif self.player.score < self.dealer.score:
            self.player.win = False
            print("You lost!")
            return
        #neither bust, same value
        else:
            print("You drew!")
            return 

    def settleChips(self, amount):
        if self.player.win:
            self.player.gainChips(amount)
            return
        elif self.player.win == False and self.dealer.win == True:
            self.player.loseChips(amount)
            return
        else:
            return
        
    def bjRound(self):
        self.resetRound()
        self.gameSetup()
        self.log_state()
        if self.player.blackjack:    
            print("You got a natty BJ!")
            #Dealer still plays
            self.dealerPlay()
        else:
            self.playerPlay()    
        if self.player.bust:
            #Dealer wins
            self.compareHands()
            return
        self.dealerPlay()
        self.log_state()            
        self.compareHands()
        self.settleChips(self.bjPayout if self.player.blackjack else self.payout)
        return
