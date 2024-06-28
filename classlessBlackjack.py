import numpy as np
import random as rand
import matplotlib as plt


class Deck:
    suits = ['H','S','D','C']
    ranks= [i for i in range(2,11)] + ['J','Q','K','A']


    def __init__(self):
        self.cards = [(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        self.shuffle()
    
    def shuffle(self):
        return rand.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards)>1:
            return self.cards.pop()


def handVal(hand):
    
    value = 0
    
    for i in range(0,len(hand)):
        
        if hand[i][0] == 'J' or hand[i][0] == 'Q' or hand[i][0] == 'K': 
            value += 10
            
        elif hand[i][0] == 'A':
                
            if  value > 10:
                value += 1
                
            else:
                value += 11
            
        elif hand[i][0] in [i for i in range(2,11)]:
            value += hand[i][0]
            
    return value


def isBlackjack(hand):
    if handVal(hand) == 21 and len(hand) == 2: 
        return True
    
    return False


def isBust(hand):
    if handVal(hand) > 21:
        
        return True
    return False


def checkState(playerHand, dealerHand):
    
    if isBust(playerHand) == False or handVal(playerHand) < handVal(dealerHand):
        return False
    
    if handVal(playerHand)!= False and handVal(playerHand) == handVal(dealerHand):
        return None
    
    if handVal(playerHand) > handVal(dealerHand):
        return  True


def checkWin(state):
    if state == True:
        return 'Player Win'
    
    if state == None:
        return 'Draw'
    
    return 'Player Lose'


def smartPlayer(hand, dealer, strategy):
    #Player hand value -> pIndex, Dealer hand value -> dIndex
    dealerVal = 0
    
    if dealer[0][0] == 'J' or dealer[0][0] == 'Q'or dealer[0][0] == 'K':
        dealerVal = 10
    
    elif dealer[0][0] == 'A':
        dealerVal = 11
    
    else:
        dealerVal = dealer[0][0]
    
    pIndex = handVal(hand) - 4
    dIndex = dealerVal - 2
    
    if strategy[pIndex][dIndex] == 'Hit':
        return True
        
    else:
        return False


def smartBlackjack(strategy):
    #Dealer is Soft 17
    #Set up game
    deck = Deck()
    player = [deck.deal() for i in range(0,2)]
    dealer = [deck.deal()]
    facedown = [deck.deal()]

    #Player turn
    if isBlackjack(player) == True:
        
        dealer = dealer + facedown
        if isBlackjack(dealer) == True:
            return player, dealer, 'Draw'
        
        return player, dealer, 'Blackjack!'
    
    playerHit = True
    while playerHit == True:
        
        if smartPlayer(player, dealer, strategy) == True:
            player.append(deck.deal())
            if handVal(player) == False:
                return player, dealer, 'Bust!'
        
        if smartPlayer(player, dealer, strategy) == False:
            playerHit = False
            
    #Dealer turn, dealer stands on soft 17
    dealer = dealer + facedown
    
    while handVal(dealer) < 17:
        dealer.append(deck.deal())
        if handVal(dealer) == False:
            return player, dealer, 'Draw'
        
    return player, handVal(player), dealer, handVal(dealer),checkWin(checkState(player,dealer))


def simulate(strategy,trials):
    
    wins = 0
    losses = 0
    draws = 0 
    
    playerChips = 1000
    dealerChips = 1000
    
    for i in range(0,trials):
        outcome = smartBlackjack(strategy)[-1]
        
        if outcome == 'Bust!' or outcome == 'Player Lose':
            losses += 1
            dealerChips += 10
            playerChips -= 10
            
        elif outcome == 'Blackjack!' or outcome == 'Player Win':
            wins += 1
            playerChips += 10
            dealerChips -= 10
            
        elif outcome == 'Draw':
            draws += 1
        
        if playerChips == 0:
            break
        
    return "W|L|D|Total",wins, losses, draws, trials

def simStats(simulation):
    #EV = W*P(W) + L*P(L) + D*P(D), W = 1, L = -1, D = 0.
    ev = (np.float64(simulation[1]/simulation[4])) - (np.float64(simulation[3]/simulation[4])) 
    var = np.divide(np.power(1-ev,2, dtype = np.float64) + np.power(-1-ev, 2, dtype = np.float64)+ np.power(ev, 2, dtype = np.float64),3)
    sig = np.sqrt(var)
    
    return "EV|Var|StDev",ev, var, sig

#Example
if __name__ == "__main__":
    
    soft17 = [ ['Hit']*10,['Hit']*10,['Hit']*10,         
                ['Hit']*10,['Hit']*10,['Hit']*10,
                ['Hit']*10,['Hit']*10,['Hit']*10,
                ['Hit']*10,['Hit']*10,['Hit']*10,
                ['Hit']*10,['Stand']*10,['Stand']*10,
                ['Stand']*10,['Stand']*10,['Stand']*10]
    
    print(simulate(soft17, 1000))
    print(simStats(soft17, 10000))