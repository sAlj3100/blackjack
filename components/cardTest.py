import pytest 
import card 

def test_getRank():
    assert card.Card('A','H').getRank() == 'B'
    
def test_getSuit():
    assert card.Card('A','H').getSuit() == 'H'