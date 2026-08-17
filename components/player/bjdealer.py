from .hand import Hand


class Dealer:
    def __init__(self):
        self.hand = Hand()

    @property
    def should_hit(self) -> bool:
        """S17: stand on every 17, whether soft or hard."""
        return self.hand.value < 17
