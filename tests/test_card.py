from components.deck.card import card

def test_rank():
    assert card.Card(2, 'H').rank == 2
    assert card.Card('A','C').rank == 'A'
    
def test_suit(): 
    assert card.Card(2, 'H').rank == 'H'
    assert card.Card('A','C').suit == 'C'