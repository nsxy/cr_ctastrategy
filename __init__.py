# coding:utf-8

__version__ = "2.8.0"

from .base import BaseLogic, BaseFilter
from .backtesting import CrBacktestingEngine, OptimizationSetting
from .template import CrCtaTemplate

from vnpy_ctastrategy import (
    TickData,
    BarData,
    OrderData,
    TradeData,
    BarGenerator,
    ArrayManager,
)
from vnpy_ctastrategy.base import StopOrder