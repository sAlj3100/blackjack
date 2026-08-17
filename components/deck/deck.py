import random
from typing import Protocol

from .card import card


class CardSource(Protocol):
    def draw(self) -> card.Card:
        """Draw one card from the source."""


class InfiniteShoe:
    """An independent random draw source with single-deck card probabilities."""

    ranks = tuple(str(rank) for rank in range(2, 11)) + ("J", "Q", "K", "A")
    suits = ("H", "S", "D", "C")

    def __init__(self, rng: random.Random | None = None):
        self._rng = rng if rng is not None else random.Random()

    def draw(self) -> card.Card:
        return card.Card(self._rng.choice(self.ranks), self._rng.choice(self.suits))
