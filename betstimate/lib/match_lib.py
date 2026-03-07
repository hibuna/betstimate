from betstimate.models.match_result import MatchResult
from betstimate.objects.match import Match


class MatchLib:
    @staticmethod
    def strip_match_result_outcome(match_result: MatchResult) -> Match:
        return Match(
            id=match_result.id,
            date=match_result.date,
            season=match_result.season,
            league=match_result.league,
            team_home_name=match_result.team_home_name,
            team_away_name=match_result.team_away_name,
        )

    @staticmethod
    def is_win_team(match_result: MatchResult, team_name: str) -> bool:
        if match_result.team_home_name == team_name:
            return MatchLib.is_win_team_home(match_result)
        elif match_result.team_away_name == team_name:
            return MatchLib.is_win_team_away(match_result)
        else:
            return False

    @staticmethod
    def is_draw(match_result: MatchResult) -> bool:
        return match_result.team_home_goals == match_result.team_away_goals

    @staticmethod
    def is_win_team_home(match_result: MatchResult) -> bool:
        return match_result.team_home_goals > match_result.team_away_goals

    @staticmethod
    def is_win_team_away(match_result: MatchResult) -> bool:
        return match_result.team_home_goals < match_result.team_away_goals

    @staticmethod
    def filter_match_result_by_team(
        team_name: str,
        all_match_result: list[MatchResult],
    ) -> list[MatchResult]:
        all_match_result_by_team = []

        for all_match_result in all_match_result:
            if team_name in (
                all_match_result.team_home_name,
                all_match_result.team_away_name,
            ):
                all_match_result_by_team.append(all_match_result)

        return all_match_result_by_team
