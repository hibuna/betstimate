from pathlib import Path

from betstimate.lib.config_lib import ConfigLib
from betstimate.types.types import Void


class FileLib:
    @staticmethod
    def read(file_name: str) -> str:
        path = FileLib.get_path_project_root() / file_name

        with open(path, "r") as f:
            return f.read()

    @staticmethod
    def write(file_name: str, content: str) -> Void:
        path = FileLib.get_path_project_root() / file_name

        with open(path, "w") as f:
            f.write(content)

    @staticmethod
    def get_path_project_root() -> Path:
        return Path(ConfigLib.get_path_project_root())

    @staticmethod
    def get_path(path: str) -> Path:
        return FileLib.get_path_project_root() / path
