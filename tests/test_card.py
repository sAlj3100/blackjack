from components.deck.card import card

def test_rank():
    assert card.Card(2, 'H').rank == '2'
    assert card.Card('A','C').rank == 'A'
    
def test_suit(): 
    assert card.Card(2, 'H').suit == 'H'

def test_card_str():
    assert str(card.Card(2, 'H')) == '2H'
    