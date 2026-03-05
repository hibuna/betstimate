from decimal import Decimal
from typing import Any, Literal, Optional

from betstimate.model.match import Match
from betstimate.model.statistic import TeamSeasonStatistic


class Strategy:
    balance_initial: Decimal
    bet_size: Decimal
    bet_method: Literal["percentage", "absolute"]
    quote_expected_minimum: Decimal

    bet_size_minimum = Decimal("0.01")

    @classmethod
    def should_place_bet(
        cls,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> bool: ...

    @classmethod
    def win_condition(
        cls,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> bool: ...

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
    def calculate_bet_size(cls, balance: Decimal) -> Decimal:
        if cls.bet_method == "absolute":
            bet_size = cls.bet_size
        elif cls.bet_method == "percentage":
            bet_size = balance * (cls.bet_size / Decimal("100"))
        else:
            raise ValueError(f"Unknown bet method {cls.bet_method}")

        if bet_size > cls.bet_size_minimum:
            return bet_size
        else:
            return cls.bet_size_minimum
