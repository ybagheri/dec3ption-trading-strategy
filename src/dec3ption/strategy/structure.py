"""Market structure: fractal swings, Major/Minor, internal/external ranges.

ساختار بازار: سوینگ‌های فرکتالی، ماجور/مینور، رنج داخلی/خارجی.
Rule: range comes from 2 opposite Majors; a swing is Major when it breaks
the prior opposite structure (close beyond). Merged line (internal == external)
means that side WILL sweep.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


def closed_bars(df: pd.DataFrame) -> pd.DataFrame:
    """Drop the last (still-forming) bar. Signals evaluate on CLOSED candles only.

    حذف کندل آخر (در حال تشکیل). سیگنال‌ها فقط روی کندل‌های بسته — وگرنه repaint.
    Spec R9.1. Returns a copy; empty/small frames pass through safely.
    """
    if len(df) <= 1:
        return df.iloc[0:0].copy()
    return df.iloc[:-1].copy()


@dataclass(frozen=True)
class Swing:
    index: int
    price: float
    kind: str  # "high" | "low"
    is_major: bool = False


def find_swings(df: pd.DataFrame, order: int = 2) -> list[Swing]:
    """Fractal pivots: extreme of `order` bars on each side. سوینگ فرکتالی."""
    highs = df["high"].to_numpy()
    lows = df["low"].to_numpy()
    out: list[Swing] = []
    for i in range(order, len(df) - order):
        if highs[i] == highs[i - order:i + order + 1].max():
            out.append(Swing(i, float(highs[i]), "high"))
        if lows[i] == lows[i - order:i + order + 1].min():
            out.append(Swing(i, float(lows[i]), "low"))
    return out


def mark_majors(swings: list[Swing]) -> list[Swing]:
    """A swing is Major when it breaks the previous opposite extreme.

    ماجور شدن: شکست اکستریم مخالف قبلی (منطق شکست ساختار).
    """
    marked: list[Swing] = []
    last_high: float | None = None
    last_low: float | None = None
    for s in swings:
        major = False
        if s.kind == "high" and (last_high is None or s.price > last_high):
            major = True
            last_high = s.price
        elif s.kind == "low" and (last_low is None or s.price < last_low):
            major = True
            last_low = s.price
        marked.append(Swing(s.index, s.price, s.kind, major))
    return marked


@dataclass(frozen=True)
class RangeLines:
    """The 4 range lines. چهار خط رنج."""
    internal_high: float
    internal_low: float
    external_high: float
    external_low: float

    def merged_side(self, tol_fraction: float = 0.001) -> str | None:
        """'high'/'low' when internal == external (will sweep), else None.

        خط یکی‌شده = آن سمت حتماً سوئیپ می‌شود.
        """
        span = max(self.external_high - self.external_low, 1e-12)
        if abs(self.internal_high - self.external_high) / span <= tol_fraction:
            return "high"
        if abs(self.internal_low - self.external_low) / span <= tol_fraction:
            return "low"
        return None


def detect_range(df: pd.DataFrame, order: int = 2) -> RangeLines | None:
    """Internal range = 2 most recent opposite Majors; external = step one back.

    رنج داخلی از ۲ ماجور مخالف اخیر، خارجی یک قدم عقب‌تر.
    Returns None when fewer than 2 opposite Majors exist yet.
    """
    majors = [s for s in mark_majors(find_swings(df, order)) if s.is_major]
    highs = [s for s in majors if s.kind == "high"]
    lows = [s for s in majors if s.kind == "low"]
    if len(highs) < 2 or len(lows) < 2:
        return None
    # most recent opposite pair = internal; one step back = external.
    # SPEC-GAP: "internal inside external" nesting is NOT guaranteed by this
    # simplified rule (see docs/OPEN_QUESTIONS.md Q-RANGE-NESTING).
    # Keyword args: positional order once swapped the fields (Phase-1 fix).
    return RangeLines(
        internal_high=highs[-1].price,
        internal_low=lows[-1].price,
        external_high=highs[-2].price,
        external_low=lows[-2].price,
    )
