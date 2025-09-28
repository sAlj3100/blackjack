import pytest
from components.player.bjdealer import bjDealer
from components.deck import card

class MockCard:
    def __init__(self, rank):
        self.rank = rank
    def __str__(self):
        return str(self.rank)
    
def dealer():
    testdealer = bjDealer()
    return testdealer

def test_initialisation(dealer):
    assert dealer.hand == []
    assert dealer.score == 0
    assert dealer.blackjack == False
    assert dealer.faceDown == False

def test_facedown_flip(dealer):
    dealer.hand = [MockCard(10), MockCard(7)]
    dealer.setFaceDown()
    assert len(dealer.hand) == 1
    assert len(dealer.facedown) == 1
    dealer.flip()
    assert len(dealer.hand) == 2
    assert len(dealer.facedown) == 0

def test_isHit(dealer):
    dealer.score = 16
    assert dealer.isHit(17) == True
    dealer.score = 17
    assert dealer.isHit(17) == False
    dealer.score = 18
    assert dealer.isHit(17) == False

def test_reset(dealer):
    dealer.hand = [MockCard(10), MockCard(7)]
    dealer.score = 17
    dealer.blackjack = True
    dealer.facedown = [MockCard(5)]
    dealer.reset()
    assert dealer.hand == []
    assert dealer.score == 0
    assert dealer.blackjack == False
    assert dealer.facedown == []