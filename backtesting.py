# coding:utf-8

from time import perf_counter
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from typing import Dict, List, Callable, Tuple

from vnpy.trader.constant import Interval
from vnpy.trader.optimize import (
    OptimizationSetting,
    check_optimization_setting,
    run_ga_optimization
)

from vnpy_ctastrategy.base import BacktestingMode
from vnpy_ctastrategy.backtesting import BacktestingEngine, get_target_value

from .template import CrCtaTemplate

class CrBacktestingEngine(BacktestingEngine):

    def set_parameters(
        self,
        vt_symbol: str,
        interval: Interval,
        start: datetime,
        rate: float,
        slippage: float,
        size: float,
        pricetick: float,
        capital: int = 0,
        end: datetime = None,
        mode: BacktestingMode = BacktestingMode.BAR,
        inverse: bool = False,
        risk_free: float = 0,
        annual_days: int = 240,
        window: int = 1,
    ):
        super().set_parameters(
            vt_symbol,
            interval,
            start,
            rate,
            slippage,
            size,
            pricetick,
            capital,
            end,
            mode,
            inverse,
            risk_free,
            annual_days,
        )
        self.window = window

    def add_strategy(self, strategy_class: type, setting: dict):
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self,
            strategy_class.__name__,
            self.vt_symbol,
            setting,
            self.window,
            self.interval,
        )

    def run_bf_optimization(self, optimization_setting: OptimizationSetting, output=True):
        """"""
        if not check_optimization_setting(optimization_setting):
            return

        evaluate_func: callable = wrap_evaluate(self, optimization_setting.target_name)
        results = run_bf_optimization(
            evaluate_func,
            optimization_setting,
            get_target_value,
            output=self.output
        )

        if output:
            for result in results:
                msg: str = f"参数：{result[0]}, 目标：{result[1]}"
                self.output(msg)

        return results

    def run_ga_optimization(self, optimization_setting: OptimizationSetting, output=True):
        """"""
        if not check_optimization_setting(optimization_setting):
            return

        evaluate_func: callable = wrap_evaluate(self, optimization_setting.target_name)
        results = run_ga_optimization(
            evaluate_func,
            optimization_setting,
            get_target_value,
            output=self.output
        )

        if output:
            for result in results:
                msg: str = f"参数：{result[0]}, 目标：{result[1]}"
                self.output(msg)

        return results


def wrap_evaluate(engine: CrBacktestingEngine, target_name: str) -> callable:
    """
    Wrap evaluate function with given setting from backtesting engine.
    """
    func: callable = partial(
        evaluate,
        target_name,
        engine.strategy_class,
        engine.vt_symbol,
        engine.interval,
        engine.window,
        engine.start,
        engine.rate,
        engine.slippage,
        engine.size,
        engine.pricetick,
        engine.capital,
        engine.end,
        engine.mode,
        engine.inverse
    )
    return func

def evaluate(
    target_name: str,
    strategy_class: CrCtaTemplate,
    vt_symbol: str,
    interval: Interval,
    window: int,
    start: datetime,
    rate: float,
    slippage: float,
    size: float,
    pricetick: float,
    capital: int,
    end: datetime,
    mode: BacktestingMode,
    inverse: bool,
    setting: dict
):
    """
    Function for running in multiprocessing.pool
    """
    engine = CrBacktestingEngine()

    engine.set_parameters(
        vt_symbol=vt_symbol,
        interval=interval,
        window=window,
        start=start,
        rate=rate,
        slippage=slippage,
        size=size,
        pricetick=pricetick,
        capital=capital,
        end=end,
        mode=mode,
        inverse=inverse
    )

    engine.add_strategy(strategy_class, setting)
    engine.load_data()
    engine.run_backtesting()
    engine.calculate_result()
    statistics = engine.calculate_statistics(output=False)

    target_value = statistics[target_name]
    return (str(setting), target_value, statistics)

OUTPUT_FUNC = Callable[[str], None]
EVALUATE_FUNC = Callable[[dict], dict]
KEY_FUNC = Callable[[list], float]

def run_bf_optimization(
    evaluate_func: EVALUATE_FUNC,
    optimization_setting: OptimizationSetting,
    key_func: KEY_FUNC,
    max_workers: int = 4,
    output: OUTPUT_FUNC = print
) -> List[Tuple]:
    """Run brutal force optimization"""
    settings: List[Dict] = optimization_setting.generate_settings()

    output(f"开始执行穷举算法优化")
    output(f"参数优化空间：{len(settings)}")

    start: int = perf_counter()

    p = Pool(max_workers)
    results: List[Tuple] = p.map(evaluate_func, settings)
    results.sort(reverse=True, key=key_func)
    p.close()
    p.join()

    end: int = perf_counter()
    cost: int = int((end - start))
    output(f"穷举算法优化完成，耗时{cost}秒")

    return results