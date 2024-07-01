### Blackjack
This project is a way for me to practice OOP in Python and explore the implementation of AI algorithms.

## blackjack.py
Simulates a game of Blackjack between one (human) player and a soft 17 dealer.
- The dealer will hit until their hand has a soft value of 17 (ex; (A, 6), (10, 7))
- The player may choose to stand or hit by providing string input "Stand" or "Hit".
- Chips are awarded at the end of a round.
- bjRound simulates a single round.
- playMany simulates many rounds.

## classlessBlackjack.py
A classless implementation of Blackjack where the player is a function that takes in a strategy matrix as input. 
A monte carlo simulation is implemented to determine the EV and Variance of the strategy provided in terms of number of Wins, Losses and Draws.

## Task list
- [x] A working blackjack simulator.
- [x] A way to test a player strategy.
- [ ] Extend to Poker.
- [ ] Splitting and doubling down.
- [ ] Explore AI algorithms (genetic learning, reinforcement learning).