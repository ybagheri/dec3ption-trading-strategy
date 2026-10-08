"""Trade plan: SL + buffer, TP ladder, management rules.

پلن معامله: استاپ + بافر، نردبان تارگت، قوانین مدیریت.
1R = range height (≈ entry→SL). TP1 -> breakeven, TP3 -> close 30%.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..config import Settings


@dataclass(frozen=True)
class TradePlan:
    """Full order ladder for one signal. پلن کامل یک سیگنال."""
    symbol: str
    direction: int  # +1 buy / -1 sell
    entry: float
    stop_loss: float
    risk_distance: float
    targets: dict[float, float]  # multiple -> price
    move_to_breakeven_at: float = 1.0
    partial_close_at: float = 3.0
    partial_close_pct: float = 30.0

    def target(self, multiple: float) -> float:
        return self.targets[multiple]


def build_plan(symbol: str, direction: int, entry: float, level: float,
               spread: float, settings: Settings) -> TradePlan:
    """SL = level ± buffer (buffer from settings); targets = ladder × 1R.

    استاپ = سطح ± بافر؛ تارگت‌ها = نردبان × ریسک.
    """
    side = 1 if direction > 0 else -1  # buy: SL below level
    range_height = abs(entry - level)
    buffer = settings.buffer_size(spread, range_height)
    stop_loss = level - side * buffer
    risk = abs(entry - stop_loss)
    targets = {m: entry + side * risk * m for m in settings.tp_ladder}
    return TradePlan(symbol=symbol, direction=direction, entry=entry,
                     stop_loss=stop_loss, risk_distance=risk, targets=targets,
                     partial_close_pct=settings.tp3_partial_close_pct)
