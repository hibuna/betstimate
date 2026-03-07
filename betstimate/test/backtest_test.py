from decimal import Decimal
from typing import Any
from unittest import TestCase

from betstimate.backtest.backtest import Backtest
from betstimate.core.initialize import initialize
from betstimate.lib.database_lib import DatabaseLib
from betstimate.lib.match_lib import MatchLib
from betstimate.models.match_result import MatchResult
from betstimate.models.statistic import TeamSeasonStatistic
from betstimate.objects.bet import Bet, BetTeamWin, BetDraw
from betstimate.objects.match import Match
from betstimate.strategies.strategy_base import Strategy
from betstimate.types.enums import Season, WagerType


class BetstimateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        initialize()


class BacktestTest(BetstimateTest):
    def test_backtest(self):
        balance_initial = Decimal("100")
        backtest = Backtest(strategy=TestStrategy())
        backtest_result = backtest.simulate(all_variable={})

        assert backtest_result.balance == balance_initial

    def test_backtest_with_quote(self):
        balance_initial = Decimal("100")
        backtest = Backtest(strategy=TestStrategyQuote())
        backtest_result = backtest.simulate(all_variable={})
        balance_expected = balance_initial + self.get_number_of_match_total()

        assert backtest_result.balance == balance_expected

    def get_number_of_match_total(self):
        all_season_except_first = Season.get_all()[1:]
        all_match_result = DatabaseLib.query_all_match_result_by_season(
            all_season_except_first,
        )

        return len(all_match_result)

    @staticmethod
    def get_match_result_by_match_id(match_id: int) -> MatchResult:
        row = DatabaseLib.execute_query(
            """SELECT * FROM match WHERE id = {}""".format(match_id)
        ).fetchone()

        return MatchResult.load_from_row(row)


class TestStrategy(Strategy):
    balance_initial = Decimal("100")
    wager_size = Decimal("1")
    wager_type = WagerType.ABSOLUTE
    quote_expected_minimum = Decimal("1")

    def create_bet_if_needed(
        self,
        match: Match,
        all_match_result_to_date: list[MatchResult],
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_season_stat_current_to_date: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> Bet:
        match_result = BacktestTest.get_match_result_by_match_id(match.id)

        if MatchLib.is_draw(match_result):
            return BetDraw(match_result.id)
        elif MatchLib.is_win_team_home(match_result):
            return BetTeamWin(match_result.id, team_name=match_result.team_home_name)
        elif MatchLib.is_win_team_away(match_result):
            return BetTeamWin(match_result.id, team_name=match_result.team_away_name)
        else:
            raise NotImplementedError


class TestStrategyQuote(TestStrategy):
    quote_expected_minimum = Decimal("2")
