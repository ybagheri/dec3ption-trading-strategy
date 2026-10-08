"""Pre-trade checklist evaluator (docs/STRATEGY.md §4).

ارزیاب چک‌لیست قبل از ورود — ۱۰ بند سند استراتژی.
Pure function: pass the analysis outputs in, get pass/fail per item out.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChecklistInput:
    range_drawn: bool = False
    equilibriums_marked: bool = False
    merged_line: str | None = None  # "high"/"low"/None — merged => NO reversal entry there
    permission_granted: bool = False  # minor majored
    pair_valid: bool = False
    confirmation_closed: bool = False
    entry_took_opposite_tp1: bool = False
    steps_ok: bool = False  # <= 2 steps to this side
    sl_beyond_sweep: bool = False
    tp_plan_set: bool = False


CHECKLIST_LABELS = (
    ("range_drawn", "4 range lines drawn? | ۴ خط رنج رسم شده؟"),
    ("equilibriums_marked", "Untouched vs touched marked? | تعادل‌ها مشخص شده؟"),
    ("no_merged_reversal", "No reversal entry into a merged line? | ورود برگشتی به خط یکی‌شده نیست؟"),
    ("permission_granted", "Minor majored (permission)? | اجازه صادر شده؟"),
    ("pair_valid", "Valid corresponding pair? | جفت متناظر معتبر است؟"),
    ("confirmation_closed", "Confirmation candle closed? | کندل تأیید کلوز داد؟"),
    ("entry_clean", "Entry candle didn't take opposite TP1? | کندل ورود TP1 مخالف را ندیده؟"),
    ("steps_ok", "Steps ≤ 2? | گام‌ها حداکثر ۲ است؟"),
    ("sl_beyond_sweep", "SL beyond sweep + buffer? | استاپ پشت سوئیپ + بافر است؟"),
    ("tp_plan_set", "TP ladder + management set? | برنامه‌ی مدیریت مشخص است؟"),
)


def evaluate(data: ChecklistInput) -> dict[str, bool]:
    """Evaluate all 10 items. True = may trade only if ALL pass."""
    return {
        "range_drawn": data.range_drawn,
        "equilibriums_marked": data.equilibriums_marked,
        "no_merged_reversal": data.merged_line is None,
        "permission_granted": data.permission_granted,
        "pair_valid": data.pair_valid,
        "confirmation_closed": data.confirmation_closed,
        "entry_clean": not data.entry_took_opposite_tp1,
        "steps_ok": data.steps_ok,
        "sl_beyond_sweep": data.sl_beyond_sweep,
        "tp_plan_set": data.tp_plan_set,
    }


def may_trade(result: dict[str, bool]) -> bool:
    """Trade only when every item passes. فقط وقتی همه سبز باشند."""
    return all(result.values())
