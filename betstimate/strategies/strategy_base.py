from decimal import Decimal
from typing import Any, Optional

from betstimate.models.statistic import TeamSeasonStatistic
from betstimate.objects.bet import Bet
from betstimate.objects.info import BetInfo
from betstimate.objects.match import Match
from betstimate.types.enums import WagerType


class Strategy:
    balance_initial: Decimal
    wager_size: Decimal
    wager_type: WagerType
    quote_expected_minimum: Decimal

    wager_minimum = Decimal("0.01")

    @classmethod
    def create_bet_if_needed(
        cls,
        match: Match,
        bet_info: BetInfo,
        all_variable: dict[str, Any],
    ) -> Optional[Bet]: ...

    @classmethod
    def get_team_season_stat(
        cls,
        team_name: str,
        all_team_season_stat: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
    ) -> Optional[TeamSeasonStatistic]:
        if team_name in all_team_name_newly_qualified:
            return None

        for team_season_stat in all_team_season_stat:
            if team_season_stat.team == team_name:
                return team_season_stat

        raise ValueError("No team season statistic found")

    @classmethod
    def calculate_wager(cls, balance: Decimal) -> Decimal:
        if cls.wager_type == WagerType.ABSOLUTE:
            wager = cls.wager_size
        elif cls.wager_type == WagerType.PERCENTAGE:
            wager = balance * (cls.wager_size / Decimal("100"))
        else:
            raise ValueError(f"Unknown wager type {cls.wager_type}")

        if wager > cls.wager_minimum:
            return wager
        else:
            return cls.wager_minimum
