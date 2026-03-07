from dataclasses import dataclass
from datetime import date as datetime_date

from betstimate.lib.date_lib import DateLib


@dataclass
class MatchResult:
    id: int
    date: datetime_date
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
            date=datetime_date.strptime(row[1], DateLib.DATE_FORMAT_DEFAULT),
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


@dataclass
class TeamMatchResult:
    id: int
    match_id: int
    date: datetime_date
    season: str
    league: str
    team_name: str
    team_name_opponent: str
    team_goals: int
    team_goals_opponent: int
    is_home_game: bool

    @classmethod
    def load_from_row(cls, row: tuple):
        return cls(
            id=row[0],
            match_id=row[1],
            date=datetime_date.strptime(row[2], DateLib.DATE_FORMAT_DEFAULT),
            season=row[3],
            league=row[4],
            team_name=row[5],
            team_name_opponent=row[6],
            team_goals=row[7],
            team_goals_opponent=row[8],
            is_home_game=bool(row[9]),
        )

    @classmethod
    def load_all_from_all_row(cls, all_row: list[tuple]):
        return [cls.load_from_row(row) for row in all_row]
