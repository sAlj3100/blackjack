from blackjack import blackjack

START_CHIPS = 1000
PAYOUT = 100
DECK_LIMIT = 26
BJ_MULTIPLIER = 2
DEALER_LIM = 17

if __name__ == "__main__":
    try:
        print("Blackjack good game yes?")
        while True:
            playGame = input("Play game? (y/n): ").strip().lower()
            if playGame == 'n':
                print("Ok pencil neck.")
                break
            elif playGame == 'y':
                break
            else:
                print("Invalid input, y or n")     
        game = blackjack.Blackjack(START_CHIPS, PAYOUT, BJ_MULTIPLIER, 26, DEALER_LIM)
        while not game.player.isBrokie():
            game.bjRound()
            if game.player.isBrokie():
                print("You're doneso brokie.")
                break
            again = input("Play another round? (y/n): ").strip().lower()
            if again != 'y':
                print("See you next time.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted, goodbye...")
        exit(0)