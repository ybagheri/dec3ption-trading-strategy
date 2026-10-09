"""MetaTrader 5 bridge (OOP, dry-run safe).

پل ارتباطی با متاتریدر ۵. به‌صورت پیش‌فرض DRY-RUN است و سفارش واقعی ارسال نمی‌کند.
The `MetaTrader5` package is imported lazily so the rest of the engine
(and the test-suite) works on machines without MT5 installed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import logging
import pandas as pd

from .config import Settings

logger = logging.getLogger(__name__)

TIMEFRAME_MAP = {
    "M1": "TIMEFRAME_M1",
    "M5": "TIMEFRAME_M5",
    "M15": "TIMEFRAME_M15",
    "H1": "TIMEFRAME_H1",
    "H4": "TIMEFRAME_H4",
    "D1": "TIMEFRAME_D1",
}


@dataclass
class OrderResult:
    """Result of an order request (real or simulated). نتیجه‌ی سفارش (واقعی یا شبیه‌سازی‌شده)."""

    ticket: int
    symbol: str
    direction: int  # +1 buy, -1 sell | ‎+1‎ خرید، ‎−1‎ فروش
    volume: float
    entry: float
    stop_loss: float
    take_profit: float
    dry_run: bool
    comment: str = ""


class MT5Client:
    """Thin OOP wrapper around the MetaTrader5 terminal API.

    Usage:
        with MT5Client(settings) as client:
            df = client.fetch_rates("BTCUSD", "M1", 500)
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._mt5: Any | None = None
        self._connected = False

    # -- lifecycle --------------------------------------------------------
    def _import_mt5(self) -> Any:
        import MetaTrader5 as mt5  # lazy: package exists only on Windows+MT5
        return mt5

    def connect(self) -> bool:
        """Initialize + login. Returns False (never raises) when MT5 is missing."""
        try:
            mt5 = self._import_mt5()
        except ImportError:
            logger.warning("MetaTrader5 package not installed; running disconnected")
            return False
        path = str(self.settings.mt5_path)
        kwargs: dict[str, Any] = {"path": path, "timeout": self.settings.mt5_timeout_ms}
        if self.settings.mt5_data_folder is not None:
            kwargs["portable"] = False
        try:
            if not mt5.initialize(**kwargs):
                logger.warning("mt5.initialize failed for path=%s", path)
                return False
            if self.settings.mt5_login:
                if not mt5.login(
                    self.settings.mt5_login,
                    password=self.settings.mt5_password or "",
                    server=self.settings.mt5_server or "",
                ):
                    logger.warning("mt5.login failed for login=%s", self.settings.mt5_login)
                    mt5.shutdown()
                    return False
        except Exception:
            logger.exception("MT5 connect raised unexpectedly")
            return False
        self._mt5 = mt5
        self._connected = True
        return True

    def __enter__(self) -> "MT5Client":
        self.connect()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.shutdown()

    def shutdown(self) -> None:
        if self._mt5 is not None and self._connected:
            try:
                self._mt5.shutdown()
            finally:
                self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _require(self) -> Any:
        if not self._connected or self._mt5 is None:
            raise RuntimeError("MT5Client is not connected. Call connect() first.")
        return self._mt5

    # -- market data -------------------------------------------------------
    def ensure_symbol(self, symbol: str) -> bool:
        mt5 = self._require()
        info = mt5.symbol_info(symbol)
        if info is None:
            return False
        if not info.visible:
            return bool(mt5.symbol_select(symbol, True))
        return True

    def fetch_rates(self, symbol: str, timeframe: str, count: int = 500) -> pd.DataFrame:
        """Last `count` candles as a DataFrame (time, open, high, low, close, tick_volume)."""
        mt5 = self._require()
        if timeframe not in TIMEFRAME_MAP:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        tf = getattr(mt5, TIMEFRAME_MAP[timeframe])
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
        if rates is None or len(rates) == 0:
            raise RuntimeError(f"No rates for {symbol} {timeframe}")
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df[["time", "open", "high", "low", "close", "tick_volume"]]

    # -- trading ------------------------------------------------------------
    def place_market_order(self, symbol: str, direction: int, volume: float,
                           stop_loss: float, take_profit: float,
                           comment: str = "dec3ption") -> OrderResult:
        """Market order. In DRY_RUN mode returns a simulated result, no terminal call.

        سفارش مارکت. در حالت DRY_RUN فقط شبیه‌سازی می‌کند و به ترمینال دست نمی‌زند.
        """
        if self.settings.dry_run or not self._connected:
            price = self._last_price(symbol) if self._connected else float("nan")
            return OrderResult(ticket=0, symbol=symbol, direction=direction,
                               volume=volume, entry=price, stop_loss=stop_loss,
                               take_profit=take_profit, dry_run=True, comment=comment)
        mt5 = self._require()
        order_type = mt5.ORDER_TYPE_BUY if direction > 0 else mt5.ORDER_TYPE_SELL
        tick = mt5.symbol_info_tick(symbol)
        price = tick.ask if direction > 0 else tick.bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit,
            "magic": self.settings.magic_number,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            code = getattr(result, "retcode", "no-result")
            raise RuntimeError(f"order_send failed: {code}")
        return OrderResult(ticket=result.order, symbol=symbol, direction=direction,
                           volume=volume, entry=result.price, stop_loss=stop_loss,
                           take_profit=take_profit, dry_run=False, comment=comment)

    def _last_price(self, symbol: str) -> float:
        mt5 = self._require()
        tick = mt5.symbol_info_tick(symbol)
        return float(tick.ask + tick.bid) / 2.0
