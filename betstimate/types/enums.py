from enum import Enum as enum_Enum
from typing import Self


class Enum(enum_Enum):
    @classmethod
    def get_all(cls) -> list[Self]:
        return list(cls)

    @classmethod
    def get_all_name(cls) -> list[str]:
        return [str(key) for key in cls.__members__.keys()]

    @classmethod
    def get_all_value(cls) -> list[int] | list[str]:
        return [e.value for e in cls]


class EnumUnordered(enum_Enum): ...


class EnumOrdered(Enum):
    def get_previous(self) -> Self:
        all_member = tuple(type(self))
        index = all_member.index(self)

        if index == 0:
            raise ValueError("Cannot get previous member from Enum")

        return all_member[index - 1]


class Season(EnumOrdered):
    SEASON_16_17 = "2016_2017"
    SEASON_17_18 = "2017_2018"
    SEASON_18_19 = "2018_2019"
    SEASON_19_20 = "2019_2020"
    SEASON_20_21 = "2020_2021"
    SEASON_21_22 = "2021_2022"
    SEASON_22_23 = "2022_2023"
    SEASON_23_24 = "2023_2024"
    SEASON_24_25 = "2024_2025"
    SEASON_25_26 = "2025_2026"


class WagerType(EnumUnordered):
    ABSOLUTE = 1
    PERCENTAGE = 2
