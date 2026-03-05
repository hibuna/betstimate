from functools import lru_cache
from os import environ

from betstimate.lib.cache_lib import CacheLib


class ConfigLib:
    ENV_VAR_PATH_PROJECT_ROOT = "path_project_root"

    @staticmethod
    @lru_cache(maxsize=CacheLib.SIZE_CACHE_SINGLETON)
    def get_path_project_root() -> str:
        return environ[ConfigLib.ENV_VAR_PATH_PROJECT_ROOT]
