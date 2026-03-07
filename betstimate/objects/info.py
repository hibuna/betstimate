from dataclasses import dataclass

from betstimate.backtest.backtest_result import BacktestSeasonResult
from betstimate.models.match_result import MatchResult, TeamMatchResult
from betstimate.models.statistic import TeamSeasonStatistic
from betstimate.objects.match import Match


@dataclass
class BetInfo:
    backtest_season_result: BacktestSeasonResult
    match: Match
    all_match_result_to_date: list[MatchResult]
    all_team_match_result_to_date_team_home: list[TeamMatchResult]
    all_team_match_result_to_date_team_away: list[TeamMatchResult]
    all_team_season_stat_previous: list[TeamSeasonStatistic]
    all_team_season_stat_current_to_date: list[TeamSeasonStatistic]
    all_team_name_newly_qualified: list[str]
