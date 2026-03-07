from decimal import Decimal
from typing import Any, Optional

from betstimate.objects.bet import BetTeamWin, Bet
from betstimate.objects.info import BetInfo
from betstimate.objects.match import Match
from betstimate.strategies.strategy_base import Strategy
from betstimate.types.enums import WagerType


class StrategySample(Strategy):
    balance_initial = Decimal("100")
    wager_size = Decimal("1")
    wager_type = WagerType.ABSOLUTE
    quote_expected_minimum = Decimal("2")

    def create_bet_if_needed(
        self,
        match: Match,
        bet_info: BetInfo,
        all_variable: dict[str, Any],
    ) -> Optional[Bet]:
        team_season_stat_home = self.get_team_season_stat(
            team_name=match.team_home_name,
            all_team_season_stat=bet_info.all_team_season_stat_previous,
            all_team_name_newly_qualified=bet_info.all_team_name_newly_qualified,
        )
        team_season_stat_away = self.get_team_season_stat(
            team_name=match.team_away_name,
            all_team_season_stat=bet_info.all_team_season_stat_previous,
            all_team_name_newly_qualified=bet_info.all_team_name_newly_qualified,
        )

        if (
            team_season_stat_home
            and team_season_stat_away
            and team_season_stat_home.total_points > all_variable["team_points_maximum"]
            and team_season_stat_away.total_points < all_variable["team_points_minimum"]
        ):
            return BetTeamWin(match.id, team_name=team_season_stat_home.team)
        else:
            return None
