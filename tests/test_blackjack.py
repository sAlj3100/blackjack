import pytest
from blackjack.blackjack import Blackjack

class MockCard:
    def __init__(self, rank):
        self.rank = rank
    def __str__(self):
        return str(self.rank)

@pytest.fixture
def game():
    testgame = Blackjack(1000,100,2,26,17)
    return testgame

def test_handScore(game):
    game.player.hand = [MockCard('A'), MockCard(7)]
    assert game.handScore(game.player) == 18
    game.player.hand.append(MockCard(10))
    assert game.handScore(game.player) == 18

def test_aceCount(game):
    game.player.hand = [MockCard('A'), MockCard(7), MockCard('A')]
    assert game.aceCount(game.player) == 2
    game.player.hand = [MockCard(10), MockCard(7)]
    assert game.aceCount(game.player) == 0

def test_isBlackjack(game):
    game.player.hand = [MockCard('A'), MockCard('K')]
    game.isBlackjack(game.player)
    assert game.player.blackjack == True
    game.player.hand = [MockCard(10), MockCard(7)]
    game.isBlackjack(game.player)
    assert game.player.blackjack == False

def test_isBust(game):
    game.player.hand = [MockCard(10), MockCard(7), MockCard(5)]
    assert game.isBust(game.player) == True
    game.player.hand = [MockCard(10), MockCard(7)]
    assert game.isBust(game.player) == False

def test_deal(game):
    initial_deck_size = len(game.deck)
    game.deal(game.player)
    assert len(game.deck) == initial_deck_size - 1
    assert len(game.player.hand) == 1

def test_dealerPlay(game):
    #Test dealer won't hit on 17
    game.dealer.hand = [MockCard(10), MockCard(7)]
    game.dealer.setFaceDown()
    game.dealerPlay()
    assert game.dealer.faceDown == False
    assert len(game.dealer.hand) == 2
    assert game.dealer.score == 17
    game.dealer.hand = [MockCard(10), MockCard(6)]
    game.dealer.setFaceDown()
    game.dealerPlay()
    assert game.dealer.score >= 17
    assert len(game.dealer.hand) > 2

def test_resetRound(game):
    game.player.hand = [MockCard(10), MockCard(7)]
    game.player.score = 17
    game.player.blackjack = True
    game.dealer.hand = [MockCard(10), MockCard(6)]
    game.dealer.score = 16
    game.dealer.blackjack = False
    game.deck.cards = []
    game.resetRound()
    assert game.player.hand == []
    assert game.player.score == 0
    assert game.player.blackjack == False
    assert game.dealer.hand == []
    assert game.dealer.score == 0
    assert game.dealer.blackjack == False
    assert len(game.deck) >= game.deckMin

def test_gameSetup(game):
    game.gameSetup()
    assert len(game.player.hand) == 2
    assert len(game.dealer.hand) == 1
    assert len(game.dealer.facedown) == 1
    assert game.player.score > 0
    assert game.dealer.score > 0
    assert len(game.deck) == 52 - 4

def test_cardValue(game):
    assert game.cardValue(MockCard('J')) == 10
    assert game.cardValue(MockCard('A')) == 11
    assert game.cardValue(MockCard(5)) == 5

def test_resetRound_deck_reshuffle(game):
    #Force len(deck) < deckMin
    game.deck.cards = [MockCard(5) for _ in range(game.deckMin)]   
    game.resetRound()
    assert len(game.deck) >= game.deckMin
    #Only reset deck if strictly below deckMin
    game.deck.cards = [MockCard(5) for _ in range(game.deckMin//2)]
    preResetLength = len(game.deck)
    game.resetRound()
    assert len(game.deck) == preResetLength  

def test_compareHands(game):
    #normal win/lose/draw scenarios
    game.player.score = 17
    game.dealer.score = 16
    game.compareHands()
    assert game.player.win == True
    assert game.dealer.win == False
    game.player.score = 17
    game.dealer.score = 18
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == True
    game.dealer.score = 17
    game.player.score = 17
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == False
    #player bust
    game.player.score = 22
    game.dealer.score = 17
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == True
    #dealer bust scenarios
    game.player.score = 17
    game.dealer.score = 22
    game.compareHands()
    assert game.player.win == True
    assert game.dealer.win == False
    game.player.score = 22
    game.dealer.score = 22 
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == False
    #blackjack scenarios
    game.player.blackjack = True
    game.dealer.blackjack = False
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == False
    game.player.blackjack = True
    game.dealer.blackjack = True
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == False
    game.player.blackjack = False
    game.dealer.blackjack = True
    game.compareHands()
    assert game.player.win == False
    assert game.dealer.win == True
 
def test_settleChips(game):
    #normal win/lose/draw scenarios
    game.player.chips = 1000
    game.player.win = True
    game.player.blackjack = False
    game.settleChips()
    assert game.player.chips == 1100
    game.player.win = False
    game.dealer.win = True
    game.settleChips()
    assert game.player.chips == 1000
    game.player.win = False
    game.dealer.win = False
    game.settleChips()
    assert game.player.chips == 1000
    #win with blackjack
    game.player.win = True
    game.player.blackjack = True
    game.settleChips()
    assert game.player.chips == 1200

def test_playerPlay_hit_stand_quit(game, monkeypatch):
    #hit until bust
    inputs = iter(['h' for _ in range(15)])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    game.playerPlay()
    assert game.player.bust == True
    #stand immediately
    game.resetRound()
    inputs = iter(['s'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    game.playerPlay()
    assert game.player.bust == False
    #invalid input followed by stand
    game.resetRound()
    inputs = iter(['x','s'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    game.playerPlay()
    assert game.player.bust == False
    #quit game
    game.resetRound()
    inputs = iter(['q'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    try:
        game.playerPlay()
    except SystemExit:
        assert True

def test_bjRound(game, monkeypatch):
    inputs = iter(['s','n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    game.bjRound()
    assert game.player.win in [True, False]  # Player either wins or loses
    assert game.player.chips in [900, 1100, 1200]