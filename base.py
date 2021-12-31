# coding:utf-8

from typing import Any
from abc import ABC, abstractmethod

from vnpy.trader.utility import virtual

from vnpy_ctastrategy import (
    CtaTemplate,
    BarData,
    TickData,
    TradeData,
    OrderData,
    ArrayManager,
)


class BaseLogic(ABC):

    @abstractmethod
    def __call__(self, am: ArrayManager, *args: Any, **kwds: Any) -> bool:
        pass

class BaseFilter(ABC):

    def __init__(self) -> None:
        self.trading_toggle = True
        self.buy_toggle = True
        self.sell_toggle = True
        self.short_toggle = True
        self.cover_toggle = True

    @virtual
    def on_start(self):
        """
        set strategy toggle when strategy is started.
        """
        pass

    @virtual
    def on_bar(self, bar: BarData) -> None:
        '''
        set strategy toggle when new bar data update.
        '''
        pass

    @virtual
    def on_tick(self, tick: TickData) -> None:
        '''
        set strategy toggle when new tick data update.
        '''
        pass
    
    @virtual
    def on_order(self, order: OrderData) -> None:
        """
        set strategy toggle when new order data update.
        """
        pass

    @virtual
    def on_trade(self, trade: TradeData) -> None:
        """
        set strategy toggle when new trade data update.
        """
        pass

class Filter(BaseFilter):

    def __init__(self, strategy: CtaTemplate) -> None:
        super().__init__()
        self.__strategy = strategy

    @property
    def strategy(self) -> CtaTemplate:
        return self.__strategy
    
    def close_trading_toggle(self) -> None:
        self.__strategy.trading = False
    
    def open_trading_toggle(self) -> None:
        self.__strategy.trading = True
    
    def get_trading_toggle(self) -> bool:
        return self.__strategy.trading