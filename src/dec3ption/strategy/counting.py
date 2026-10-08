"""Leg candle-counting filter: digital root -> even = balanced, odd = imbalanced.

فیلتر شمارش کندل لگ: جمع ارقام تا تک‌رقمی؛ زوج = متعادل، فرد = نامتعادل.
Verified from chart labels: «2 = even», «18 = 9 = odd», «25 = 7 = odd».
"""


def digital_root(n: int) -> int:
    """Reduce to a single digit by summing digits. جمع ارقام تا تک‌رقمی شدن."""
    n = abs(int(n))
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def is_balanced_count(n: int) -> bool:
    """True when the digital root is even. زوج بودن ریشه = لگ متعادل."""
    return digital_root(n) % 2 == 0


def count_leg(candles: int) -> dict:
    """Classify a leg length. خروجی: تعداد، ریشه، وضعیت تعادل."""
    root = digital_root(candles)
    balanced = root % 2 == 0
    return {"candles": candles, "root": root,
            "balanced": balanced,
            "label": "balanced/متعادل" if balanced else "imbalanced/نامتعادل"}
