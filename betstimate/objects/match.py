from dataclasses import dataclass
from datetime import date


@dataclass
class Match:
    id: int
    date: date
    season: str
    league: str
    team_home_name: str
    team_away_name: str
