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
        agent.blackjack = agent.score == 21 and len(agent.hand) == 2

    def isBust(self,agent):
        agent.bust = agent.score > 21

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
        self.isBlackjack(self.dealer)
        if self.dealer.blackjack:
            print("Game is rigged!")
            return
        while self.dealer.hitting:
            print("Dealer hits.")
            self.deal(self.dealer)
            self.log_state()
            self.dealer.isHit(self.dealerLimit)
            self.isBust(self.dealer)
            if self.dealer.bust: 
                print("Dealer busts!")
                return
        print("Dealer stands.")
        return

    def playerPlay(self):
        self.isBlackjack(self.player)
        if self.player.blackjack:
            print("You hit Blackjack!")
            return
        
        while True:    
            try:
                playerAction = input("Stand (s) or Hit? (h): ").strip().lower()
            except(EOFError, KeyboardInterrupt):
                print("\nInterrupted, goodbye...")
                return
            if playerAction == "h":
                print("You hit.")
                self.deal(self.player)
                self.handScore(self.player)
                self.isBust(self.player)
                self.log_state()
                if self.player.bust:
                    print("You bust!")    
                    return 
            elif playerAction == "s":
                print("You stand.")
                return
            else:
                print("Invalid input, enter 'h' to Hit or 's' to Stand.")

    def compareHands(self):
        #player and dealer both blackjack
        if self.player.blackjack and self.dealer.blackjack:
            return  
        #player blackjack, dealer not
        if self.player.blackjack and not(self.dealer.blackjack):
            self.player.win = True
            return
        #dealer blackjack, player not
        if not(self.player.blackjack) and self.dealer.blackjack:
            self.dealer.win = True
            return
        #player bust, dealer wins
        if self.player.bust:
            self.dealer.win = True
            return
        #player <= 21, dealer bust
        if not(self.player.bust) and self.dealer.bust:
            self.player.win = True
            return

        if self.player.score > self.dealer.score:
            self.player.win = True
        elif self.player.score < self.dealer.score:
            self.dealer.win = True
        else:
            return
        
    def settleChips(self):
        if self.player.win:
            if self.player.blackjack:
                self.player.chips += self.bjPayout
            else:
                self.player.chips += self.payout
        elif self.dealer.win:
            self.player.chips -= self.payout
        else:
            return
        
    def bjRound(self):
        self.resetRound()
        self.gameSetup()
        self.log_state()
        self.playerPlay()    
        if self.player.bust:
            #Dealer wins
            self.compareHands()
            return
        self.dealerPlay()
        self.log_state()            
        self.compareHands()
        self.settleChips()
        return
