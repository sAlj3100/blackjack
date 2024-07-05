import blackjack

START_CHIPS = 1000
PAYOUT = 10
SHOE_SIZE = 1
DECK_LIMIT = 26
BJ_MULT = 2
BJ_PAYOUT = BJ_MULT*PAYOUT
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
    
    game = blackjack.Blackjack()
    game.playMany(numRounds)
