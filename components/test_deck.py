import pytest 
import deck

TEST_DECK = deck.Deck(([i for i in range(2,11)] + ['J','Q','K','A']), ['H','S','D','C'])
NUM_CARDS = len(TEST_DECK)

def test_deal():
    assert TEST_DECK.deal() != None

def test_reset():
    assert TEST_DECK.reset() == NUM_CARDS