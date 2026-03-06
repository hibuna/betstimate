from dataclasses import dataclass
from datetime import date as datetime_date


@dataclass
class Match:
    id: int
    date: datetime_date
    season: str
    league: str
    team_home_name: str
    team_away_name: str
