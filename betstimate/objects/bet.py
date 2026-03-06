from dataclasses import field, dataclass
from decimal import Decimal

from betstimate.types.enums import WagerType


@dataclass
class Bet:
    match_id: int
    wager_size: Decimal = field(default=Decimal("1"), kw_only=True)
    wager_type: WagerType = field(default=WagerType.ABSOLUTE, kw_only=True)


@dataclass
class BetTeamWin(Bet):
    team_name: str


@dataclass
class BetDraw(Bet):
    pass
