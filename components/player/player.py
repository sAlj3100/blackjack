class Player:
    def __init__(self, bankroll: float):
        self.bankroll = bankroll

    def apply_net_profit(self, net_profit_units: float) -> None:
        self.bankroll += net_profit_units
