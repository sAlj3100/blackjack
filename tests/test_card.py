import unittest

from components.deck.card.card import Card


class CardTests(unittest.TestCase):
    def test_card_is_an_immutable_value(self):
        card = Card(2, "H")
        self.assertEqual(card.rank, "2")
        self.assertEqual(card.suit, "H")
        self.assertEqual(str(card), "2H")
        with self.assertRaises(AttributeError):
            card.rank = "A"
