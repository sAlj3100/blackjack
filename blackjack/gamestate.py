from dataclasses import dataclass, field

@dataclass
class GameState:
	playerHand: list = field(default_factory=list)
	playerScore: int = 0
	playerChips: int = 0
	dealerHand: list = field(default_factory=list)
	dealerScore: int = 0
	roundResult: str = "playing" 