from copy import copy
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from betstimate.lib.date_lib import DateLib

from betstimate.models.match_result import MatchResult
from betstimate.types.enums import Season
from betstimate.types.types import Void


class BacktestResult:
    balance_initial: Decimal
    balance: Decimal
    balance_highest: Decimal
    balance_lowest: Decimal

    number_of_bet_total: int = 0
    streak_win_highest: int = 0
    streak_lose_highest: int = 0
    streak_under_break_even_highest: int = 0
    is_bankrupt: bool = False

    variables: dict[str, Any]
    all_back_test_season_results: list[BacktestSeasonResult]

    def __init__(self, balance_initial: Decimal, all_variable: dict[str, Any]):
        self.balance_initial = balance_initial
        self.balance = copy(balance_initial)
        self.balance_highest = copy(balance_initial)
        self.balance_lowest = copy(balance_initial)

        self.variables = all_variable
        self.all_back_test_season_results = []

    def add_season_result(self, season_result: BacktestSeasonResult) -> Void:
        self.all_back_test_season_results.append(season_result)

        self.balance = season_result.get_balance()
        self.balance_highest = max(
            self.balance, self.balance_highest, season_result.get_balance_highest()
        )
        self.balance_lowest = min(
            self.balance, self.balance_lowest, season_result.get_balance_lowest()
        )
        self.streak_win_highest = max(
            self.streak_win_highest, season_result.get_streak_win_highest()
        )
        self.streak_lose_highest = max(
            self.streak_lose_highest, season_result.get_streak_lose_highest()
        )
        self.streak_under_break_even_highest = max(
            self.streak_under_break_even_highest,
            season_result.get_streak_under_break_even_highest(),
        )
        self.is_bankrupt = self.is_bankrupt or season_result.get_is_bankrupt()


class BacktestSeasonResult:
    _season: Season
    _balance_initial: Decimal
    _balance: Decimal
    _balance_highest: Decimal
    _balance_lowest: Decimal

    _history: list[BacktestMatchResult]

    _number_of_bet_total: int = 0
    _streak_win_current: int = 0
    _streak_lose_current: int = 0
    _streak_under_break_even_current: int = 0
    _streak_win_highest: int = 0
    _streak_lose_highest: int = 0
    _streak_under_break_even_highest: int = 0
    _is_bankrupt: bool = False

    def __init__(self, season: Season, balance_initial: Decimal):
        self._season = season
        self._balance_initial = balance_initial
        self._balance = copy(balance_initial)
        self._balance_highest = copy(balance_initial)
        self._balance_lowest = copy(balance_initial)
        self._history = []

    def __str__(self) -> str:
        return str(
            {
                "season": self._season.value,
                "profit": round(float(self._balance - self._balance_initial), 2),
                "balance_initial": round(float(self._balance_initial), 2),
                "balance": round(float(self._balance), 2),
                "balance_highest": round(float(self._balance_highest), 2),
                "balance_lowest": round(float(self._balance_lowest), 2),
                "number_of_bet_total": self._number_of_bet_total,
                "streak_win_highest": self._streak_win_highest,
                "streak_lose_highest": self._streak_lose_highest,
                "streak_under_break_even_highest": self._streak_under_break_even_highest,
                "is_bankrupt": self._is_bankrupt,
                "history": str(len(self._history)) or "",
            }
        )

    def get_season(self) -> Season:
        return self._season

    def get_balance(self) -> Decimal:
        return self._balance

    def set_balance(self, balance: Decimal) -> Void:
        self._balance = balance
        self._ensure_balance_lowest_updated()

    def add_to_balance(self, balance: Decimal) -> Void:
        self._balance += balance
        self._ensure_balance_highest_updated()
        self._ensure_balance_lowest_updated()

    def subtract_from_balance(self, balance: Decimal) -> Void:
        self._balance -= balance
        self._ensure_balance_highest_updated()
        self._ensure_balance_lowest_updated()

    def number_of_bet_total_increment(self) -> Void:
        self._number_of_bet_total += 1

    def get_is_bankrupt(self) -> bool:
        return self._is_bankrupt

    def set_is_bankrupt(self, is_bankrupt: bool) -> bool:
        self._is_bankrupt = is_bankrupt

        return self._is_bankrupt

    def _is_balance_negative(self) -> bool:
        return self._balance <= Decimal("0")

    def is_balance_under_break_even(self) -> bool:
        return self._balance < self._balance_initial

    def is_bankrupt_sync(self) -> bool:
        if self._is_balance_negative():
            return self.set_is_bankrupt(True)
        else:
            return self.set_is_bankrupt(False)

    def balance_under_break_even_sync(self) -> Void:
        if self.is_balance_under_break_even():
            self.streak_under_break_even_increment()
        else:
            self.streak_under_break_even_reset()

    def log_match_result(
        self,
        match_result: MatchResult,
        has_placed_bet: bool,
        is_bet_fulfilled: bool,
    ) -> Void:
        if len(self._history):
            balance_previous = self._history[-1].balance
        else:
            balance_previous = self._balance

        self._history.append(
            BacktestMatchResult(
                season=match_result.season,
                date=match_result.date.strftime(DateLib.DATE_FORMAT_DEFAULT),
                balance=self._balance,
                balance_delta=self._balance - balance_previous,
                has_placed_bet=has_placed_bet,
                is_bet_fulfilled=is_bet_fulfilled,
            )
        )

    def get_balance_highest(self) -> Decimal:
        return self._balance_highest

    def _ensure_balance_highest_updated(self) -> Void:
        if self._balance > self._balance_highest:
            self._balance_highest = copy(self._balance)

    def get_balance_lowest(self) -> Decimal:
        return self._balance_lowest

    def _ensure_balance_lowest_updated(self) -> Void:
        if self._balance < self._balance_lowest:
            self._balance_lowest = copy(self._balance)

    def get_streak_win_highest(self) -> int:
        return self._streak_win_highest

    def streak_win_reset(self) -> Void:
        self._streak_win_current = 0

    def streak_win_increment(self) -> Void:
        self._streak_win_current += 1

        if self._streak_win_current > self._streak_win_highest:
            self._streak_win_highest = self._streak_win_current

    def get_streak_lose_highest(self) -> int:
        return self._streak_lose_highest

    def streak_lose_reset(self) -> Void:
        self._streak_lose_current = 0

    def streak_lose_increment(self) -> Void:
        self._streak_lose_current += 1

        if self._streak_lose_current > self._streak_lose_highest:
            self._streak_lose_highest = self._streak_lose_current

    def get_streak_under_break_even_highest(self) -> int:
        return self._streak_under_break_even_highest

    def streak_under_break_even_reset(self) -> Void:
        self._streak_under_break_even_current = 0

    def streak_under_break_even_increment(self) -> Void:
        self._streak_under_break_even_current += 1

        if (
            self._streak_under_break_even_current
            > self._streak_under_break_even_highest
        ):
            self._streak_under_break_even_highest = (
                self._streak_under_break_even_current
            )


@dataclass
class BacktestMatchResult:
    season: str
    date: str
    balance: Decimal
    balance_delta: Decimal
    has_placed_bet: bool
    is_bet_fulfilled: bool
