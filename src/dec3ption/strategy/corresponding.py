"""Corresponding High/Low pairs + Minor-Major trigger.

جفت سقف/کف متناظر + تریگر مینور-ماجور.
Rules (docs/STRATEGY.md §2.4):
- Pair forms from a Fractal-0 origin: first level on a Minor-Major candle
  (~2 same-color candles closing into/above each other), opposite level forms
  WITHOUT price returning to the origin.
- Dead when: origin revisited as Fractal-0, or >2 closes beyond the level
  (doji/inside bars not counted).
- Entry: return to the level (not as F0, <=2 closes) + Minor-Major confirmation
  within 2 candles -> enter at close. Buy at Low / Sell at High.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

import logging

logger = logging.getLogger(__name__)


def is_bullish_minor_major(df: pd.DataFrame, i: int) -> bool:
    """Two green candles, second closes above first's high. دو کندل سبز صعودی."""
    if i < 1:
        return False
    o = df["open"].to_numpy()
    c = df["close"].to_numpy()
    h = df["high"].to_numpy()
    return bool(c[i] > o[i] and c[i - 1] > o[i - 1] and c[i] > h[i - 1])


def is_bearish_minor_major(df: pd.DataFrame, i: int) -> bool:
    """Two red candles, second closes below first's low. دو کندل قرمز نزولی."""
    if i < 1:
        return False
    o = df["open"].to_numpy()
    c = df["close"].to_numpy()
    lo = df["low"].to_numpy()
    return bool(c[i] < o[i] and c[i - 1] < o[i - 1] and c[i] < lo[i - 1])


def is_doji_or_inside(df: pd.DataFrame, i: int, doji_ratio: float = 0.1) -> bool:
    """Doji / inside bar: not counted toward the 2-close limit. دوجی/اینسایدبار حساب نیست."""
    o = df["open"].to_numpy()
    c = df["close"].to_numpy()
    h = df["high"].to_numpy()
    lo = df["low"].to_numpy()
    if i < 1:
        return False
    body = abs(c[i] - o[i])
    rng = h[i] - lo[i]
    doji = rng > 0 and body / rng < doji_ratio
    inside = h[i] <= h[i - 1] and lo[i] >= lo[i - 1]
    return bool(doji or inside)


@dataclass
class CorrespondingPair:
    """One High/Low pair sharing an origin. یک جفت متناظر."""
    origin: float
    low: float
    high: float
    direction: int  # +1: low formed first (buy setup) / -1: high first (sell setup)
    closes_beyond_low: int = 0
    closes_beyond_high: int = 0
    low_dead: bool = False
    high_dead: bool = False

    def register_close(self, close: float, is_doji_inside: bool = False) -> None:
        """Feed closes after formation; kills levels past the 2-close limit.

        کلوزهای بعد از تشکیل؛ بیش از ۲ کلوز پشت سطح = ابطال.
        """
        if is_doji_inside:
            return
        if close < self.low:
            self.closes_beyond_low += 1
            if self.closes_beyond_low > 2:
                self.low_dead = True
        if close > self.high:
            self.closes_beyond_high += 1
            if self.closes_beyond_high > 2:
                self.high_dead = True

    def kill_as_f0(self, price: float, tol: float = 0.0) -> None:
        """Price revisits a level as Fractal-0 -> that side dead.

        برگشت در قالب فرکتال صفر. `tol` is an absolute price tolerance
        (pass the symbol's tick size / point in live code) — exact-float
        comparison never fires on real quotes (audit fix).
        """
        if abs(price - self.low) <= tol:
            self.low_dead = True
        if abs(price - self.high) <= tol:
            self.high_dead = True


@dataclass(frozen=True)
class EntrySignal:
    index: int
    direction: int  # +1 buy, -1 sell
    entry: float
    level: float


def scan_trigger(df: pd.DataFrame, pair: CorrespondingPair,
                 start: int,
                 opposite_tp1_buy: float | None = None,
                 opposite_tp1_sell: float | None = None) -> EntrySignal | None:
    """Scan for return-to-level + Minor-Major confirmation within 2 candles.

    برگشت به سطح + تأیید مینور-ماجور حداکثر در ۲ کندل → سیگنال ورود در کلوز.
    R6.4: a confirmation candle that already reached the opposite side's TP1
    is skipped (pass the TP1 price); scanning continues past it.
    """
    closes = df["close"].to_numpy()
    lows = df["low"].to_numpy()
    highs = df["high"].to_numpy()
    for i in range(start, len(df)):
        # buy side: touch of the low
        if not pair.low_dead and lows[i] <= pair.low <= highs[i]:
            for j in range(i, min(i + 2, len(df))):
                if is_bullish_minor_major(df, j):
                    if opposite_tp1_buy is not None and highs[j] >= opposite_tp1_buy:
                        logger.debug("buy trigger at %d skipped: took opposite TP1", j)
                        break  # this touch is spent; wait for the next touch
                    logger.debug("buy trigger at index %d, level %f", j, pair.low)
                    return EntrySignal(j, +1, float(closes[j]), pair.low)
        # sell side: touch of the high
        if not pair.high_dead and lows[i] <= pair.high <= highs[i]:
            for j in range(i, min(i + 2, len(df))):
                if is_bearish_minor_major(df, j):
                    if opposite_tp1_sell is not None and lows[j] <= opposite_tp1_sell:
                        logger.debug("sell trigger at %d skipped: took opposite TP1", j)
                        break
                    logger.debug("sell trigger at index %d, level %f", j, pair.high)
                    return EntrySignal(j, -1, float(closes[j]), pair.high)
    return None
