import unittest

from components.deck.card.card import Card
from components.player.hand import Hand


class HandTests(unittest.TestCase):
    def test_value_uses_the_highest_non_busting_ace_total(self):
        hand = Hand([Card("A", "H"), Card("A", "S"), Card(9, "D")])
        self.assertEqual(hand.value, 21)
        self.assertTrue(hand.is_soft)
        self.assertFalse(hand.is_bust)

    def test_blackjack_is_limited_to_two_cards(self):
        blackjack = Hand([Card("A", "H"), Card("K", "S")])
        ordinary_twenty_one = Hand([Card(5, "H"), Card(6, "S"), Card("K", "D")])
        self.assertTrue(blackjack.is_blackjack)
        self.assertFalse(ordinary_twenty_one.is_blackjack)
