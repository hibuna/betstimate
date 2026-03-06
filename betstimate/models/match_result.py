from dataclasses import dataclass
from datetime import date

from betstimate.lib.date_lib import DateLib


@dataclass
class MatchResult:
    id: int
    date: date
    season: str
    league: str
    team_home_name: str
    team_away_name: str
    team_home_goals: str
    team_away_goals: str

    @classmethod
    def load_from_row(cls, row: tuple):
        return cls(
            id=row[0],
            date=date.strptime(row[1], DateLib.DATE_FORMAT_DEFAULT),
            season=row[2],
            league=row[3],
            team_home_name=row[4],
            team_away_name=row[5],
            team_home_goals=row[6],
            team_away_goals=row[7],
        )

    @classmethod
    def load_all_from_all_row(cls, all_row: list[tuple]):
        return [cls.load_from_row(row) for row in all_row]
