# coding:utf-8

from datetime import datetime

from vnpy.trader.constant import Interval

from vnpy_ctastrategy.base import BacktestingMode
from vnpy_ctastrategy.backtesting import BacktestingEngine


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
