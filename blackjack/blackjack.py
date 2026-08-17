from dataclasses import dataclass
from enum import Enum, auto

from components.deck.deck import CardSource, InfiniteShoe
from components.player.bjdealer import Dealer
from components.player.hand import Hand
from components.player.player import Player


class RoundPhase(Enum):
    PLAYER_TURN = auto()
    COMPLETE = auto()


class RoundResult(Enum):
    PLAYER_BLACKJACK = auto()
    PLAYER_WIN = auto()
    DEALER_WIN = auto()
    PUSH = auto()


@dataclass(frozen=True)
class RoundOutcome:
    result: RoundResult
    payout_multiplier: float
    wager_units: float
    player_total: int
    dealer_total: int

    @property
    def net_profit_units(self) -> float:
        return self.payout_multiplier * self.wager_units


class Round:
    """A Stage 0 round, independent of bankroll constraints."""

    def __init__(self, card_source: CardSource):
        self._card_source = card_source
        self.player_hand = Hand()
        self.dealer = Dealer()
        self.wager_units = 1
        self.phase = RoundPhase.PLAYER_TURN
        self.outcome: RoundOutcome | None = None

        for _ in range(2):
            self.player_hand.add(self._card_source.draw())
            self.dealer.hand.add(self._card_source.draw())
        self._resolve_initial_blackjacks()

    @property
    def dealer_hand(self) -> Hand:
        return self.dealer.hand

    @property
    def is_complete(self) -> bool:
        return self.phase is RoundPhase.COMPLETE

    @property
    def dealer_upcard(self):
        return self.dealer_hand.cards[0]

    def hit(self) -> None:
        self._require_player_turn()
        self.player_hand.add(self._card_source.draw())
        if self.player_hand.is_bust:
            self._complete(RoundResult.DEALER_WIN, -1)
        elif self.player_hand.value == 21:
            self._play_dealer_and_resolve()

    def stand(self) -> None:
        self._require_player_turn()
        self._play_dealer_and_resolve()

    def double_down(self) -> None:
        self._require_player_turn()
        if len(self.player_hand.cards) != 2:
            raise ValueError("double down is available only on the initial two-card hand")
        self.wager_units *= 2
        self.player_hand.add(self._card_source.draw())
        if self.player_hand.is_bust:
            self._complete(RoundResult.DEALER_WIN, -1)
            return
        self._play_dealer_and_resolve()

    def _resolve_initial_blackjacks(self) -> None:
        if self.player_hand.is_blackjack and self.dealer_hand.is_blackjack:
            self._complete(RoundResult.PUSH, 0)
        elif self.player_hand.is_blackjack:
            self._complete(RoundResult.PLAYER_BLACKJACK, 1.5)
        elif self.dealer_hand.is_blackjack:
            self._complete(RoundResult.DEALER_WIN, -1)

    def _play_dealer_and_resolve(self) -> None:
        while self.dealer.should_hit:
            self.dealer_hand.add(self._card_source.draw())
        if self.dealer_hand.is_bust:
            self._complete(RoundResult.PLAYER_WIN, 1)
        elif self.player_hand.value > self.dealer_hand.value:
            self._complete(RoundResult.PLAYER_WIN, 1)
        elif self.player_hand.value < self.dealer_hand.value:
            self._complete(RoundResult.DEALER_WIN, -1)
        else:
            self._complete(RoundResult.PUSH, 0)

    def _complete(self, result: RoundResult, payout_multiplier: float) -> None:
        self.phase = RoundPhase.COMPLETE
        self.outcome = RoundOutcome(
            result=result,
            payout_multiplier=payout_multiplier,
            wager_units=self.wager_units,
            player_total=self.player_hand.value,
            dealer_total=self.dealer_hand.value,
        )

    def _require_player_turn(self) -> None:
        if self.phase is not RoundPhase.PLAYER_TURN:
            raise RuntimeError("round is already complete")


class BlackjackGame:
    """Interactive shell; the core Round never enforces bankroll constraints."""

    def __init__(self, bankroll: float = 0, card_source: CardSource | None = None):
        self.player = Player(bankroll)
        self.card_source = card_source if card_source is not None else InfiniteShoe()

    def start_round(self) -> Round:
        return Round(self.card_source)
