import pytest
from components.player.bjdealer import bjDealer

class MockCard:
    def __init__(self, rank):
        self.rank = rank
    def __str__(self):
        return str(self.rank)

@pytest.fixture    
def dealer():
    return bjDealer()

def test_initialisation(dealer):
    assert dealer.facedown == []

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
    dealer.isHit(17)
    assert dealer.hitting == True
    dealer.score = 17
    dealer.isHit(17)
    assert dealer.hitting == False
    dealer.score = 18
    dealer.isHit(17) 
    assert dealer.hitting == False

def test_reset(dealer):
    dealer.facedown = [MockCard(5)]
    dealer.reset()
    assert dealer.facedown == []