from betstimate.lib.match_lib import MatchLib
from betstimate.models.match_result import MatchResult
from betstimate.objects.bet import Bet, BetTeamWin, BetDraw


class BetLib:
    @staticmethod
    def is_fulfilled(bet: Bet, match_result: MatchResult) -> bool:
        if isinstance(bet, BetDraw):
            return BetLib.is_fulfilled_draw(match_result)
        elif isinstance(bet, BetTeamWin):
            return BetLib.is_fulfilled_team_win(bet, match_result)
        else:
            raise NotImplementedError

    @staticmethod
    def is_fulfilled_draw(match_result: MatchResult) -> bool:
        return match_result.team_home_goals == match_result.team_away_goals

    @staticmethod
    def is_fulfilled_team_win(bet: BetTeamWin, match_result: MatchResult) -> bool:
        if MatchLib.is_draw(match_result):
            return False
        elif MatchLib.is_win_team_home(match_result):
            return bet.team_name == match_result.team_home_name
        elif MatchLib.is_win_team_away(match_result):
            return bet.team_name == match_result.team_away_name
        else:
            raise NotImplementedError
