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

    def __init__(self, strategy: CtaTemplate) -> None:
        self.__strategy = strategy

    @property
    def strategy(self) -> CtaTemplate:
        return self.__strategy

    @property
    def buy_toggle(self) -> bool:
        return self.__strategy.buy_toggle
    
    @buy_toggle.setter
    def buy_toggle(self, val: bool=True) -> None:
        self.__strategy.buy_toggle = val
    
    @property
    def sell_toggle(self) -> bool:
        return self.__strategy.sell_toggle
    
    @sell_toggle.setter
    def sell_toggle(self, val: bool=True) -> None:
        self.__strategy.sell_toggle = val

    @property
    def short_toggle(self) -> bool:
        return self.__strategy.short_toggle
    
    @short_toggle.setter
    def short_toggle(self, val: bool=True) -> None:
        self.__strategy.short_toggle = val

    @property
    def cover_toggle(self) -> bool:
        return self.__strategy.cover_toggle
    
    @cover_toggle.setter
    def cover_toggle(self, val: bool=True) -> None:
        self.__strategy.cover_toggle = val

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