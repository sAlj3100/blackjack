import pytest
from components.deck import deck,card 

@pytest.fixture
def d():
    d = deck.Deck(([i for i in range(2,11)] + ['J','Q','K','A']), ['H','S','D','C'])
    return d

@pytest.fixture
def n(d):    
    num = len(d)
    return num

def test_initialisation(d):
    assert len(d) == 52
    assert all(isinstance(card.rank, str) for card in d.cards)
    assert all(isinstance(card.suit, str) for card in d.cards)    
    assert isinstance(d.cards[0], deck.card.Card)

def test_print(d, n):
    printed = d.display()
    assert len(printed) == n
    assert all(isinstance(card, str) for card in printed)

def test_deal_reset(d,n):
    d.deal()
    assert len(d) == n - 1
    #Deal entire deck and then one more
    while d.cards:
        d.deal()
    assert len(d) == 0
    assert d.deal() == None    
    #Reset empty deck
    d.reset()
    assert len(d) == n
    #Deal half the deck, then reset
    for i in range(len(d)//2):
        d.deal()
    d.reset()
    assert len(d) == n

def test_shuffle(d):
    preShuffle = d.display()
    d.shuffle()
    postShuffle = d.display()
    assert preShuffle != postShuffle
    assert sorted(preShuffle) == sorted(postShuffle)
    #Shuffle empty deck
    while d.cards:
        d.deal()
    d.shuffle()