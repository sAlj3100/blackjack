# Blackjack

Stage 0 is a small, testable blackjack rules engine with a command-line interface.

Run the interactive game with `python3 main.py`.
Run the standard-library test suite with `python3 -m unittest discover -s tests`.

## Stage 0 rules

- Cards are independently drawn from an infinite shoe with normal single-deck probabilities.
- The dealer stands on every 17, including soft 17 (S17).
- Every round starts with a one-unit wager.
- A natural blackjack is exactly two cards totalling 21 and pays 3:2.
- Blackjack versus blackjack, or any equal total, is a push.
- A three-or-more-card 21 is an ordinary win, not blackjack.
- An ordinary 21 ends the player turn and proceeds to dealer resolution.
- The player may hit or stand.
- Double down is available only on the initial two cards: it doubles the wager, draws one card, and ends the player turn.
- Splitting and other rules are intentionally out of scope.

`RoundOutcome` records result, payout multiplier, and wager separately.
`net_profit_units` is `payout_multiplier * wager_units`.
Ordinary wins/losses are `+1`/`-1`; pushes are `0`; blackjack wins are `+1.5`.
Double-down wins/losses are `+2`/`-2`.

## Model

`Card`, `Hand`, and `Round` contain the rules state.
Cards in a hand are authoritative; value, bust, blackjack, and dealer decisions are derived.
A dealer's hidden card never leaves its hand; the CLI hides it until resolution.

`CardSource` is injectable; production uses `InfiniteShoe` and tests use scripted sources.
`BlackjackGame` adds an interactive bankroll, but `Round` has no bankroll constraints.

`cruft.py` is retained as historical simulation code and is not part of the Stage 0 engine.
