from decimal import Decimal
from typing import Any
from unittest import TestCase

from betstimate.backtest.backtest import Backtest
from betstimate.core.initialize import initialize
from betstimate.lib.database_lib import DatabaseLib
from betstimate.model.match import Match
from betstimate.model.statistic import TeamSeasonStatistic
from betstimate.strategies.strategy_base import Strategy
from betstimate.types.enums import Season


class BetstimateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        initialize()


class BacktestTest(BetstimateTest):
    def test_backtest(self):
        balance_initial = Decimal("100")
        backtest = Backtest(strategy=TestStrategy())
        backtest_result = backtest.execute(all_variable={})

        assert backtest_result.balance == balance_initial

    def test_backtest_with_quote(self):
        balance_initial = Decimal("100")
        backtest = Backtest(strategy=TestStrategyQuote())
        backtest_result = backtest.execute(all_variable={})
        balance_expected = balance_initial + self.get_number_of_match_total()

        assert backtest_result.balance == balance_expected

    def get_number_of_match_total(self):
        all_season_except_first = Season.get_all()[1:]
        all_match = DatabaseLib.query_all_match_by_season(all_season_except_first)

        return len(all_match)


class TestStrategy(Strategy):
    balance_initial = Decimal("100")
    bet_size = Decimal("1")
    bet_method = "absolute"
    quote_expected_minimum = Decimal("1")

    def should_place_bet(
        self,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> bool:
        return True

    def win_condition(
        self,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> bool:
        return True


class TestStrategyQuote(TestStrategy):
    quote_expected_minimum = Decimal("2")
