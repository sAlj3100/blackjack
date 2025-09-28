### Blackjack
This project is a way for me to practice OOP in Python and explore the implementation of AI algorithms.
The idea is to have something simple I can always come back to and do something new with.

## main.py
A command line blackjack game. Run in terminal with 'python3 main.py'.
- The dealer will hit until their hand has a soft value of 17 (ex; (A, 6), (10, 7))
- The player may choose to stand or hit by providing string input "Stand" or "Hit".
- Chips are awarded at the end of a round.
- bjRound simulates a single round.
- playMany simulates many rounds. (Removed because redundant for command line game)

## cruft.py
Cruft file with some of the original script. I'm keeping this in case I want to recycle the simulation statistics functionality. Run in terminal with 'python3 cruft.py'.

## Task list
- [x] A working blackjack simulator.
- [x] A way to test a player strategy. 
- [ ] Splitting and doubling down.
- [ ] Explore AI algorithms (genetic learning, reinforcement learning).