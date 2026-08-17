from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        object.__setattr__(self, "rank", str(self.rank))
        object.__setattr__(self, "suit", str(self.suit))

    def __str__(self):
        return f"{self.rank}{self.suit}"
