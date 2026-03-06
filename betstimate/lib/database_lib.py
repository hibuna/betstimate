from sqlite3 import connect as sqlite3_connect, Cursor
from sqlite3 import Connection

from betstimate.lib.file_lib import FileLib
from betstimate.models.match_result import MatchResult
from betstimate.models.statistic import TeamSeasonStatistic
from betstimate.types.enums import Season
from betstimate.types.types import Void


class DatabaseLib:
    PATH_DATABASE = "database.sqlite"

    PATH_QUERY_ALL_TEAM_SEASON_STAT_BY_SEASON = "sql/all_team_season_stat_by_season.sql"
    PATH_QUERY_MATCH_RESULT_BY_SEASON = "sql/all_match_result_by_season.sql"

    _connection: Connection

    @staticmethod
    def initialize_connection() -> Void:
        path_database = FileLib.get_path(DatabaseLib.PATH_DATABASE)

        if not getattr(DatabaseLib, "connection", None):
            DatabaseLib._connection = sqlite3_connect(path_database)

    @staticmethod
    def execute_query(query: str) -> Cursor:
        return DatabaseLib._connection.execute(query)

    @staticmethod
    def query_all_team_season_stat(
        all_season: list[Season] = None,
    ) -> list[TeamSeasonStatistic]:
        all_season = all_season or Season.get_all()
        all_season_string = DatabaseLib._format_query_arg_string_array(
            [season.value for season in all_season]
        )
        query = FileLib.read(DatabaseLib.PATH_QUERY_ALL_TEAM_SEASON_STAT_BY_SEASON)
        query = query.format(all_season_string, all_season_string)

        all_row = DatabaseLib.execute_query(query).fetchall()

        return TeamSeasonStatistic.load_all_from_all_row(all_row)

    @staticmethod
    def query_all_match_result_by_season(all_season: list[Season] = None) -> list[MatchResult]:
        all_season = all_season or Season.get_all()
        all_season_string = DatabaseLib._format_query_arg_string_array(
            [season.value for season in all_season]
        )
        query = FileLib.read(DatabaseLib.PATH_QUERY_MATCH_RESULT_BY_SEASON)
        query = query.format(all_season_string)

        all_row = DatabaseLib.execute_query(query).fetchall()

        return MatchResult.load_all_from_all_row(all_row)

    @staticmethod
    def _format_query_arg_string_array(all_value: list[str]) -> str:
        return '"{}"'.format('","'.join(all_value))
