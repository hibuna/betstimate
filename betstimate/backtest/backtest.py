from decimal import Decimal
from functools import lru_cache
from itertools import product
from typing import Any

from betstimate.backtest.backtest_result import BacktestSeasonResult, BacktestResult
from betstimate.backtest.backtest_variable import BacktestVariableGenerator
from betstimate.lib.cache_lib import CacheLib
from betstimate.lib.database_lib import DatabaseLib
from betstimate.model.match import Match
from betstimate.model.statistic import TeamSeasonStatistic
from betstimate.strategies.strategy_base import Strategy
from betstimate.types.enums import Season


class Backtest:
    strategy: Strategy

    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def execute_all(
        self,
        all_variable_generator: list[BacktestVariableGenerator],
        all_season: list[Season] = None,
    ) -> list[BacktestResult]:
        all_name = [
            variable_generator.name for variable_generator in all_variable_generator
        ]
        all_generator_value = [
            list(variable_generator.generate())
            for variable_generator in all_variable_generator
        ]
        all_combination_all_variable = [
            dict(zip(all_name, combo)) for combo in product(*all_generator_value)
        ]

        all_result = []

        for all_variable in all_combination_all_variable:
            result = self.execute(all_variable, all_season)
            all_result.append(result)

        return all_result

    def execute(
        self,
        all_variable: dict[str, Any],
        all_season: list[Season] = None,
    ) -> BacktestResult:
        all_season = all_season or Season.get_all()[1:]

        backtest_result = BacktestResult(
            balance_initial=self.strategy.balance_initial,
            all_variable=all_variable,
        )

        balance_before_season = self.strategy.balance_initial

        for season in all_season:
            backtest_season_result = self.execute_season(
                balance=balance_before_season,
                season_to_test=season,
                all_variable=all_variable,
            )
            backtest_season_result.is_bankrupt_sync()

            backtest_result.add_season_result(backtest_season_result)

            if backtest_season_result.get_is_bankrupt():
                break

            balance_before_season = backtest_season_result.get_balance()

        return backtest_result

    def execute_season(
        self,
        balance: Decimal,
        season_to_test: Season,
        all_variable: dict[str, Any],
    ):
        season_previous = season_to_test.get_previous()
        all_stat_season_previous = self.get_all_stat_by_season(season_previous)
        all_stat_season_current = self.get_all_stat_by_season(season_to_test)
        teams_newly_qualified = self.get_all_team_newly_qualified(
            all_stat_season_previous=all_stat_season_previous,
            all_stat_season_current=all_stat_season_current,
        )

        backtest_result = BacktestSeasonResult(
            season=season_to_test,
            balance_initial=balance,
        )

        for match in self.query_all_match(season_to_test):
            backtest_result = self.execute_match(
                backtest_result=backtest_result,
                match=match,
                all_team_season_stat_previous=all_stat_season_previous,
                all_team_name_newly_qualified=teams_newly_qualified,
                all_variable=all_variable,
            )

            backtest_result.balance_under_break_even_sync()

            if backtest_result.is_bankrupt_sync():
                break

        return backtest_result

    def execute_match(
        self,
        backtest_result: BacktestSeasonResult,
        match: Match,
        all_team_season_stat_previous: list[TeamSeasonStatistic],
        all_team_name_newly_qualified: list[str],
        all_variable: dict[str, Any],
    ) -> BacktestSeasonResult:
        if self.strategy.should_place_bet(
            match=match,
            all_team_season_stat_previous=all_team_season_stat_previous,
            all_team_name_newly_qualified=all_team_name_newly_qualified,
            all_variable=all_variable,
        ):
            balance_before = backtest_result.get_balance()
            backtest_result = self.process_result(
                backtest_result,
                match,
                all_team_season_stat_previous,
                all_team_name_newly_qualified,
                all_variable,
            )

            did_bet = True
            has_won = backtest_result.get_balance() >= balance_before
        else:
            did_bet = False
            has_won = False

        backtest_result.log_match_result(
            match=match,
            did_bet=did_bet,
            has_won=has_won,
        )
        return backtest_result

    def process_result(
        self,
        backtest_result: BacktestSeasonResult,
        match: Match,
        all_stat_season_previous: list[TeamSeasonStatistic],
        teams_newly_qualified: list[str],
        variables: dict[str, Any],
    ) -> BacktestSeasonResult:
        backtest_result.number_of_bet_total_increment()
        bet_size_current = self.strategy.calculate_bet_size(
            backtest_result.get_balance()
        )

        if self.strategy.win_condition(
            match,
            all_stat_season_previous,
            teams_newly_qualified,
            variables,
        ):
            return self.process_win(backtest_result, bet_size_current)
        else:
            return self.process_loss(backtest_result, bet_size_current)

    def process_win(
        self, backtest_result: BacktestSeasonResult, bet_size_current: Decimal
    ) -> BacktestSeasonResult:
        profit = bet_size_current * self.strategy.quote_expected_minimum
        profit = profit - bet_size_current

        backtest_result.add_to_balance(profit)
        backtest_result.streak_win_increment()
        backtest_result.streak_lose_reset()

        return backtest_result

    def process_loss(
        self,
        backtest_result: BacktestSeasonResult,
        bet_size_current: Decimal,
    ) -> BacktestSeasonResult:
        backtest_result.subtract_from_balance(bet_size_current)
        backtest_result.streak_lose_increment()
        backtest_result.streak_win_reset()

        return backtest_result

    @lru_cache(maxsize=CacheLib.SIZE_CACHE_TEAM_SEASON)
    def get_all_stat_by_season(self, season: Season) -> list[TeamSeasonStatistic]:
        all_stat = DatabaseLib.query_all_stat_by_season([season])

        return sorted(all_stat, key=lambda stat: stat.total_points, reverse=True)

    def get_all_team_name(
        self, season_all_stat: list[TeamSeasonStatistic]
    ) -> list[str]:
        return [stat.team for stat in season_all_stat]

    def get_all_team_newly_qualified(
        self,
        all_stat_season_previous: list[TeamSeasonStatistic],
        all_stat_season_current: list[TeamSeasonStatistic],
    ) -> list[str]:
        all_team_name_season_previous = self.get_all_team_name(all_stat_season_previous)

        return [
            stat.team
            for stat in all_stat_season_current
            if stat.team not in all_team_name_season_previous
        ]

    @lru_cache(maxsize=CacheLib.SIZE_CACHE_MATCH_SEASON)
    def query_all_match(self, season_to_test: Season) -> list[Match]:
        return DatabaseLib.query_all_match_by_season([season_to_test])

    @staticmethod
    def generate_result_string_all_backtest_result(
        all_backtest_result: list[BacktestResult],
        filter_losses=True,
        add_season_info=True,
    ) -> str:
        output = []

        for backtest_result in all_backtest_result:
            if (
                filter_losses
                and backtest_result.balance <= backtest_result.balance_initial
            ):
                continue

            profit = backtest_result.balance - backtest_result.balance_initial

            if profit == Decimal("0"):
                profit_avg = Decimal("0")
            else:
                profit_avg = profit / len(all_backtest_result)

            profit = round(float(profit), 2)
            profit_avg = round(float(profit_avg), 2)

            output.append("profit: {}".format(profit))
            output.append("profit season avg: {}".format(profit_avg))
            output.append("all_variable: {}".format(backtest_result.variables))

            if add_season_info:
                for season_result in backtest_result.all_back_test_season_results:
                    output.append("\t{}".format(season_result))

            output.append("___________")

        return "\n".join(output)
