from components.blackjack import blackjack

START_CHIPS = 1000
PAYOUT = 10
DECK_LIMIT = 26
BJ_MULTIPLIER = 2
DEALER_LIM = 17

if __name__ == "__main__":
    
    print("Blackjack good game yes.")
    haveInt = False
    while haveInt == False:
        try:
            numRounds = int(input("How many rounds?"))
            haveInt = True
        except ValueError:
            print("Input positive integer.")
    
    game = blackjack.Blackjack(START_CHIPS, PAYOUT, BJ_MULTIPLIER, 26, DEALER_LIM)
    game.playMany(numRounds)
