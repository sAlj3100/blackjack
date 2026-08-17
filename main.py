from blackjack.blackjack import BlackjackGame, RoundPhase


STARTING_BANKROLL = 1000


def show_round(round_, reveal_dealer: bool = False) -> None:
    dealer_cards = round_.dealer_hand.display() if reveal_dealer else [str(round_.dealer_upcard), "??"]
    dealer_value = round_.dealer_hand.value if reveal_dealer else "?"
    print(f"Player: {round_.player_hand.display()} ({round_.player_hand.value})")
    print(f"Dealer: {dealer_cards} ({dealer_value})")


def play_round(game: BlackjackGame) -> None:
    round_ = game.start_round()
    while round_.phase is RoundPhase.PLAYER_TURN:
        show_round(round_)
        actions = "hit (h), stand (s), or double (d)" if len(round_.player_hand.cards) == 2 else "hit (h) or stand (s)"
        action = input(f"{actions}: ").strip().lower()
        if action == "h":
            round_.hit()
        elif action == "s":
            round_.stand()
        elif action == "d" and len(round_.player_hand.cards) == 2:
            round_.double_down()
        else:
            print("Invalid action.")

    show_round(round_, reveal_dealer=True)
    outcome = round_.outcome
    game.player.apply_net_profit(outcome.net_profit_units)
    print(f"{outcome.result.name.replace('_', ' ').title()}: {outcome.net_profit_units:+g} units")
    print(f"Bankroll: {game.player.bankroll:g} units")


if __name__ == "__main__":
    try:
        game = BlackjackGame(bankroll=STARTING_BANKROLL)
        print("Blackjack: S17, one-unit wager, blackjack pays 3:2.")
        while input("Play a round? (y/n): ").strip().lower() == "y":
            play_round(game)
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted, goodbye.")
