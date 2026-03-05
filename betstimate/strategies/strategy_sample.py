from decimal import Decimal
from typing import Any

from betstimate.model.match import Match
from betstimate.model.statistic import TeamSeasonStatistic
from betstimate.strategies.strategy_base import Strategy


class StrategySample(Strategy):
    balance_initial = Decimal("100")
    bet_size = Decimal("1")
    bet_method = "absolute"
    quote_expected_minimum = Decimal("2")

    def should_place_bet(
        self,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> bool:
        stat_team_home = self.get_team_season_stat(
            team_name=match.team_home_name,
            all_team_season_stat=all_team_season_stat_previous,
            all_team_name_newly_qualified=all_team_name_newly_qualified,
        )
        stat_team_away = self.get_team_season_stat(
            team_name=match.team_away_name,
            all_team_season_stat=all_team_season_stat_previous,
            all_team_name_newly_qualified=all_team_name_newly_qualified,
        )

        return (
            stat_team_home
            and stat_team_away
            and stat_team_home.total_points > all_variable["team_points_maximum"]
            and stat_team_away.total_points < all_variable["team_points_minimum"]
        )

    def win_condition(
        self,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> bool:
        return match.team_home_goals > match.team_away_goals
