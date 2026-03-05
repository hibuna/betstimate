from decimal import Decimal
from typing import Generator


class BacktestVariableGenerator:
    name: str

    def generate(self) -> Generator[Decimal]: ...


class BacktestIntegerGenerator(BacktestVariableGenerator):
    value_start: int
    value_end: int
    increment = 1

    def __init__(
        self,
        name: str,
        value_start: int,
        value_end: int,
        increment: int = None,
    ):
        self.name = name
        self.value_start = value_start
        self.value_end = value_end
        self.increment = increment or self.increment

    def generate(self) -> Generator[int]:
        current = self.value_start

        while current <= self.value_end:
            yield current

            current += self.increment


class BacktestDecimalGenerator(BacktestVariableGenerator):
    value_start: Decimal
    value_end: Decimal
    increment = Decimal("1")

    def __init__(
        self,
        name: str,
        value_start: Decimal,
        value_end: Decimal,
        increment: Decimal = None,
    ):
        self.name = name
        self.value_start = value_start
        self.value_end = value_end
        self.increment = increment or self.increment

    def generate(self) -> Generator[Decimal]:
        current = self.value_start

        while current <= self.value_end:
            yield current

            current += self.increment
