import pytest
from components.player.player import Player

class MockCard:
    def __init__(self, rank):
        self.rank = rank
    def __str__(self):
        return str(self.rank)

@pytest.fixture
def player():
    return Player(1000)

def test_initialisation(player):
    assert player.chips == 1000

def test_isBrokie(player):
    assert player.isBrokie() == False
    player.chips = 0
    assert player.isBrokie() == True

def test_gainChips(player):
    player.gainChips(500)
    assert player.chips == 1500
    player.gainChips(0)
    assert player.chips == 1500

def test_loseChips(player):
    player.loseChips(300)
    assert player.chips == 700
    player.loseChips(0)
    assert player.chips == 700
    player.loseChips(800)
    assert player.chips == -100

