from betstimate.backtest.backtest import Backtest
from betstimate.backtest.backtest_variable import BacktestIntegerGenerator
from betstimate.core.initialize import initialize
from betstimate.lib.file_lib import FileLib
from betstimate.strategies.strategy_sample import StrategySample

initialize()


backtest = Backtest(strategy=StrategySample())

all_variable_generator = [
    BacktestIntegerGenerator("team_points_minimum", 50, 55),
    BacktestIntegerGenerator("team_points_maximum", 60, 62),
]

all_backtest_result = backtest.execute_all(all_variable_generator)

result_string = Backtest.generate_result_string_all_backtest_result(
    all_backtest_result,
    filter_losses=False,
)

FileLib.write("output.txt", result_string)
