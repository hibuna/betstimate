from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TeamSeasonStatistic:
    team: str
    total_points: int
    total_wins: int
    total_draws: int
    total_losses: int
    total_wins_home: int
    total_draws_home: int
    total_losses_home: int
    total_wins_away: int
    total_draws_away: int
    total_losses_away: int
    goals_for: int
    goals_against: int
    goals_for_avg: Decimal
    goals_against_avg: Decimal
    average_wins: Decimal
    average_draws: Decimal
    average_losses: Decimal

    @classmethod
    def load_from_row(cls, row: tuple):
        return cls(
            team=row[0],
            total_points=row[1],
            total_wins=row[2],
            total_draws=row[3],
            total_losses=row[4],
            total_wins_home=row[5],
            total_draws_home=row[6],
            total_losses_home=row[7],
            total_wins_away=row[8],
            total_draws_away=row[9],
            total_losses_away=row[10],
            goals_for=row[11],
            goals_against=row[12],
            goals_for_avg=Decimal(str(row[13])),
            goals_against_avg=Decimal(str(row[14])),
            average_wins=Decimal(str(row[15])),
            average_draws=Decimal(str(row[16])),
            average_losses=Decimal(str(row[17])),
        )

    @classmethod
    def load_all_from_all_row(cls, all_row: list[tuple]):
        return [cls.load_from_row(row) for row in all_row]
