import unittest

from blackjack.blackjack import BlackjackGame, Round, RoundResult
from components.deck.card.card import Card


class ScriptedCardSource:
    def __init__(self, cards):
        self.cards = list(cards)

    def draw(self):
        if not self.cards:
            raise AssertionError("test attempted to draw a card that was not scripted")
        return self.cards.pop(0)


def cards(*ranks):
    return [Card(rank, "H") for rank in ranks]


class RoundTests(unittest.TestCase):
    def test_natural_blackjack_pays_three_to_two(self):
        round_ = Round(ScriptedCardSource(cards("A", 9, "K", 7)))
        self.assertTrue(round_.is_complete)
        self.assertEqual(round_.outcome.result, RoundResult.PLAYER_BLACKJACK)
        self.assertEqual(round_.outcome.payout_multiplier, 1.5)
        self.assertEqual(round_.outcome.wager_units, 1)
        self.assertEqual(round_.outcome.net_profit_units, 1.5)

    def test_two_natural_blackjacks_push(self):
        round_ = Round(ScriptedCardSource(cards("A", "A", "K", "K")))
        self.assertEqual(round_.outcome.result, RoundResult.PUSH)
        self.assertEqual(round_.outcome.net_profit_units, 0)

    def test_hit_to_twenty_one_ends_the_player_turn_as_an_ordinary_win(self):
        round_ = Round(ScriptedCardSource(cards(5, 10, 6, 7, "K")))
        round_.hit()
        self.assertEqual(round_.player_hand.value, 21)
        self.assertTrue(round_.is_complete)
        self.assertEqual(round_.outcome.result, RoundResult.PLAYER_WIN)
        self.assertEqual(round_.outcome.payout_multiplier, 1)

    def test_dealer_stands_on_soft_seventeen(self):
        round_ = Round(ScriptedCardSource(cards(10, "A", 7, 6)))
        round_.stand()
        self.assertEqual(round_.dealer_hand.value, 17)
        self.assertEqual(len(round_.dealer_hand.cards), 2)
        self.assertEqual(round_.outcome.result, RoundResult.PUSH)

    def test_dealer_stands_on_initial_hard_seventeen_without_an_extra_draw(self):
        round_ = Round(ScriptedCardSource(cards(10, 10, 7, 7)))
        round_.stand()
        self.assertEqual(round_.dealer_hand.value, 17)
        self.assertEqual(len(round_.dealer_hand.cards), 2)
        self.assertEqual(round_.outcome.result, RoundResult.PUSH)

    def test_player_bust_loses_the_current_wager(self):
        round_ = Round(ScriptedCardSource(cards(10, 10, 9, 7, 5)))
        round_.hit()
        self.assertEqual(round_.outcome.result, RoundResult.DEALER_WIN)
        self.assertEqual(round_.outcome.net_profit_units, -1)

    def test_dealer_bust_wins_the_current_wager(self):
        round_ = Round(ScriptedCardSource(cards(10, 10, 8, 6, 10)))
        round_.stand()
        self.assertEqual(round_.outcome.result, RoundResult.PLAYER_WIN)
        self.assertEqual(round_.outcome.net_profit_units, 1)

    def test_double_down_doubles_wager_draws_once_and_ends_turn(self):
        round_ = Round(ScriptedCardSource(cards(5, 10, 6, 6, 10, 2)))
        round_.double_down()
        self.assertTrue(round_.is_complete)
        self.assertEqual(len(round_.player_hand.cards), 3)
        self.assertEqual(round_.wager_units, 2)
        self.assertEqual(round_.outcome.result, RoundResult.PLAYER_WIN)
        self.assertEqual(round_.outcome.net_profit_units, 2)

    def test_double_down_to_twenty_one_is_an_ordinary_doubled_win(self):
        round_ = Round(ScriptedCardSource(cards(5, 10, 6, 7, 10)))
        round_.double_down()
        self.assertEqual(round_.player_hand.value, 21)
        self.assertEqual(round_.outcome.result, RoundResult.PLAYER_WIN)
        self.assertEqual(round_.outcome.payout_multiplier, 1)
        self.assertEqual(round_.outcome.net_profit_units, 2)

    def test_double_down_bust_loses_the_doubled_wager(self):
        round_ = Round(ScriptedCardSource(cards(10, 10, 6, 6, 10)))
        round_.double_down()
        self.assertEqual(round_.outcome.result, RoundResult.DEALER_WIN)
        self.assertEqual(round_.outcome.wager_units, 2)
        self.assertEqual(round_.outcome.net_profit_units, -2)

    def test_double_down_is_unavailable_after_hitting(self):
        round_ = Round(ScriptedCardSource(cards(5, 10, 6, 6, 2)))
        round_.hit()
        with self.assertRaises(ValueError):
            round_.double_down()

    def test_hidden_card_is_not_moved_out_of_the_dealer_hand(self):
        round_ = Round(ScriptedCardSource(cards(10, 9, 7, 8)))
        self.assertEqual(str(round_.dealer_upcard), "9H")
        self.assertEqual(round_.dealer_hand.display(), ["9H", "8H"])

    def test_interactive_bankroll_is_applied_outside_round_resolution(self):
        game = BlackjackGame(bankroll=10)
        game.player.apply_net_profit(-1.5)
        self.assertEqual(game.player.bankroll, 8.5)
