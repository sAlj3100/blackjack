from dataclasses import dataclass, field

from components.deck.card.card import Card


@dataclass
class Hand:
    """Cards are the only stored hand state; all game properties are derived."""

    cards: list[Card] = field(default_factory=list)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def _total_and_soft_aces(self) -> tuple[int, int]:
        total = sum(
            11 if card.rank == "A" else min(10, int(card.rank)) if card.rank.isdigit() else 10
            for card in self.cards
        )
        soft_aces = sum(card.rank == "A" for card in self.cards)
        while total > 21 and soft_aces:
            total -= 10
            soft_aces -= 1
        return total, soft_aces

    @property
    def value(self) -> int:
        return self._total_and_soft_aces()[0]

    @property
    def is_soft(self) -> bool:
        total, soft_aces = self._total_and_soft_aces()
        return total <= 21 and soft_aces > 0

    @property
    def is_bust(self) -> bool:
        return self.value > 21

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value == 21

    def display(self) -> list[str]:
        return [str(card) for card in self.cards]
