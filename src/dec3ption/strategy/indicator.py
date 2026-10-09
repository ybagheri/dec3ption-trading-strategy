"""Indicator rule mirror: the exact bar-by-bar logic the MQL5 indicator implements.

منطق دقیق اندیکاتور — مرجع parity بین پایتون و MQL5.
Evaluates CLOSED bars only (R9.1). Deterministic function of the frame:
same data -> same signals (stability requirement).

Procedure per side (buy shown; sell mirrored):
1. Level = most recent bullish Minor-Major extreme (two greens, 2nd close above 1st high).
2. Count closes beyond the level since formation (doji/inside skipped); >2 kills it.
3. Touch of the level + new Minor-Major confirmation within 2 bars -> signal at confirmation close.
4. SL = level - buffer; TP1 = entry + 1R (R = entry - SL).
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .corresponding import is_bullish_minor_major, is_bearish_minor_major, is_doji_or_inside


@dataclass(frozen=True)
class IndicatorSignal:
    index: int
    direction: int  # +1 buy, -1 sell
    entry: float
    level: float
    stop_loss: float
    tp1: float


def _last_mm_level(df: pd.DataFrame, end: int, direction: int, first: int = 0) -> tuple[int, float] | None:
    """Most recent Minor-Major formation in (first, end] (closed bars)."""
    is_mm = is_bullish_minor_major if direction > 0 else is_bearish_minor_major
    for j in range(end, 0, -1):
        if is_mm(df, j):
            extreme = float(df["low"].iloc[j - 1] if direction > 0 else df["high"].iloc[j - 1])
            return j, extreme
    return None


def _killed_by_closes(df: pd.DataFrame, formed: int, end: int, level: float,
                      direction: int) -> bool:
    """True when >2 (non-doji) closes went beyond the level after formation."""
    count = 0
    for k in range(formed + 1, end + 1):
        if is_doji_or_inside(df, k):
            continue
        c = float(df["close"].iloc[k])
        if (direction > 0 and c < level) or (direction < 0 and c > level):
            count += 1
            if count > 2:
                return True
    return False


def indicator_signals(df: pd.DataFrame, buffer: float = 0.0,
                      lookback: int = 500) -> list[IndicatorSignal]:
    """All indicator signals over closed bars of `df` (last bar = forming, excluded)."""
    out: list[IndicatorSignal] = []
    n = len(df) - 1  # exclude forming bar
    start = max(2, n - lookback)
    for i in range(start, n):
        for direction in (+1, -1):
            found = _last_mm_level(df, i, direction, first=start - 1)
            if found is None:
                continue
            formed, level = found
            if _killed_by_closes(df, formed, i, level, direction):
                continue
            # touch of the level on bar i?
            if not (float(df["low"].iloc[i]) <= level <= float(df["high"].iloc[i])):
                continue
            for j in range(i, min(i + 2, n)):
                mm = is_bullish_minor_major(df, j) if direction > 0 else is_bearish_minor_major(df, j)
                if mm:
                    entry = float(df["close"].iloc[j])
                    sl = level - buffer if direction > 0 else level + buffer
                    risk = abs(entry - sl)
                    tp1 = entry + risk if direction > 0 else entry - risk
                    out.append(IndicatorSignal(j, direction, entry, level, sl, tp1))
                    break
    # first trigger per touch wins; drop duplicates on the same bar+side
    seen: set[tuple[int, int]] = set()
    deduped: list[IndicatorSignal] = []
    for s in out:
        if (s.index, s.direction) not in seen:
            seen.add((s.index, s.direction))
            deduped.append(s)
    return deduped
