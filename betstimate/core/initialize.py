from json import loads as json_loads
from os import environ as environ
from pathlib import Path

from betstimate.types.types import Void


def initialize():
    load_env()
    load_lib()


def load_env() -> Void:
    with open(Path(__file__).parent.parent.parent / "config.json", "r") as f:
        config = json_loads(f.read())

    for key, value in config.items():
        environ[key] = str(value)


def load_lib() -> Void:
    from betstimate.lib.database_lib import DatabaseLib

    DatabaseLib.initialize_connection()
