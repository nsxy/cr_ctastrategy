# coding:utf-8

from typing import Any

from vnpy.trader.utility import virtual
from vnpy.trader.constant import Direction, Offset, Interval

from vnpy_ctastrategy import (
    CtaTemplate,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
)
from vnpy_ctastrategy.base import StopOrder

from .base import BaseFilter


class CrCtaTemplate(CtaTemplate):

    author = ""
    parameters = []
    variables = []

    def __init__(
        self,
        cta_engine: Any,
        strategy_name: str,
        vt_symbol: str,
        setting: dict,
        window: int = 1,
        interval: Interval.MINUTE = Interval.MINUTE,
    ):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        ### filter toggle
        self.buy_toggle = True
        self.sell_toggle = True
        self.short_toggle = True
        self.cover_toggle = True
        self.variables.extend(['buy_toggle', 'sell_toggle', 'short_toggle', 'cover_toggle'])
        self.filter = None
        self.__bg = BarGenerator(self.on_bar, window, self.on_call_bar, interval)

    def add_filter(self, filter_class: type) -> None:
        self.filter = filter_class(self)

    def on_init(self) -> None:
        """
        check filter when strategy is started.
        """
        if self.filter and not isinstance(self.filter, BaseFilter):
            raise ValueError('wrong filter class')
        self.on_cr_init()

    def on_start(self):
        """
        filter when strategy is started.
        """
        if self.filter:
            self.filter.on_start()
        self.on_cr_start()

    def on_bar(self, bar: BarData) -> None:
        """
        generate real bar.
        """
        self.__bg.update_bar(bar)

    def on_call_bar(self, bar: BarData) -> None:
        if self.filter:
            self.filter.on_bar(bar)
        self.on_cr_bar(bar)

    def on_tick(self, tick: TickData) -> None:
        """
        filter on tick data update.
        """
        self.__bg.update_tick(tick)
        if self.filter:
            self.filter.on_tick(tick)
        self.on_cr_tick(tick)

    def on_trade(self, trade: TradeData) -> None:
        """
        filter on trade data update.
        """
        if self.filter:
            self.filter.on_trade(trade)
        self.on_cr_trade(trade)

    def on_order(self, order: OrderData) -> None:
        """
        filter on order data update.
        """
        if self.filter:
            self.filter.on_order(order)
        self.on_cr_order(order)

    def on_stop_order(self, stop_order: StopOrder) -> None:
        """
        filter on stop order update.
        """
        if self.filter:
            self.filter.on_stop_order(stop_order)
        self.on_cr_stop_order(stop_order)

    @virtual
    def on_cr_init(self) -> None:
        """
        Callback when strategy is inited.
        """
        pass

    @virtual
    def on_cr_start(self):
        """
        Callback when strategy is started.
        """
        pass

    @virtual
    def on_cr_bar(self, bar: BarData) -> None:
        '''
        Callback of new bar data update.
        '''
        pass

    @virtual
    def on_cr_tick(self, tick: TickData) -> None:
        '''
        Callback of new bar data update.
        '''
        pass

    @virtual
    def on_cr_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        pass

    @virtual
    def on_cr_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    @virtual
    def on_cr_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass

    def buy(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False
    ):
        """
        Send buy order to open a long position.
        """
        if self.buy_toggle:
            return self.send_order(
                Direction.LONG,
                Offset.OPEN,
                price,
                volume,
                stop,
                lock,
                net
            )

    def sell(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False
    ):
        """
        Send sell order to close a long position.
        """
        if self.sell_toggle:
            return self.send_order(
                Direction.SHORT,
                Offset.CLOSE,
                price,
                volume,
                stop,
                lock,
                net
            )

    def short(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False
    ):
        """
        Send short order to open as short position.
        """
        if self.short_toggle:
            return self.send_order(
                Direction.SHORT,
                Offset.OPEN,
                price,
                volume,
                stop,
                lock,
                net
            )

    def cover(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False
    ):
        """
        Send cover order to close a short position.
        """
        if self.cover_toggle:
            return self.send_order(
                Direction.LONG,
                Offset.CLOSE,
                price,
                volume,
                stop,
                lock,
                net
            )