import pytest
from components.player.agent import Agent

@pytest.fixture
def agent():
    return Agent()

def test_initialisation(agent):
    assert agent.hand == []
    assert agent.score == 0
    assert agent.blackjack == False
    assert agent.bust == False
    assert agent.win == False

def test_printHand(agent):
    agent.hand = []
    assert agent.printHand() == []
    agent.hand = [1, 'A', 'K']
    assert agent.printHand() == ['1', 'A', 'K'] 

def test_reset(agent):
    agent.hand = [1, 'A', 'K']
    agent.score = 21
    agent.blackjack = True
    agent.bust = True
    agent.win = True
    agent.reset()
    assert agent.hand == []
    assert agent.score == 0
    assert agent.blackjack == False
    assert agent.bust == False
    assert agent.win == False

def test_getCard(agent):
    agent.getCard('A')
    assert agent.hand == ['A']
    agent.getCard(10)
    assert agent.hand == ['A', 10]