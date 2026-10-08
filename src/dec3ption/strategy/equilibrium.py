"""Equilibrium lines: Fib 50% of (leg start -> consumption), drawn as rays.

خطوط تعادل: فیبوی ۵۰٪ از شروع لگ تا نقطه‌ی مصرف، به‌صورت خط افقی اکستندشده.
4 lines: fractal internal/external, leg internal/external. Overlap of internal +
external = keep the zone (verified with screenshots).
"""
from __future__ import annotations

from dataclasses import dataclass


def fib_50(start: float, end: float) -> float:
    """50% between two prices. پنجاه درصد بین دو قیمت."""
    return (start + end) / 2.0


@dataclass(frozen=True)
class Equilibriums:
    """The 4 equilibrium levels. چهار خط تعادل."""
    fractal_internal: float
    fractal_external: float
    leg_internal: float
    leg_external: float

    @classmethod
    def from_leg(cls, leg_start: float, consumption: float,
                 flat_start: float | None = None) -> "Equilibriums":
        """External: 50% of (leg start -> consumption). Internal: 50% of the
        flat/F0 interior (falls back to the same 50% when unknown).

        خارجی: ۵۰٪ شروع لگ تا مصرف. داخلی: ۵۰٪ فضای داخلی.
        """
        ext = fib_50(leg_start, consumption)
        internal = fib_50(flat_start if flat_start is not None else leg_start, consumption)
        return cls(fractal_internal=internal, fractal_external=ext,
                   leg_internal=internal, leg_external=ext)

    def overlaps(self, tol_fraction: float = 0.002) -> list[tuple[str, str, float]]:
        """Pairs of lines coinciding within tolerance -> key zones.

        هم‌پوشانی خطوط = ناحیه‌ی کلیدی (بقیه دور ریخته می‌شود).
        """
        lines = {"fractal_internal": self.fractal_internal,
                 "fractal_external": self.fractal_external,
                 "leg_internal": self.leg_internal,
                 "leg_external": self.leg_external}
        span = max(lines.values()) - min(lines.values())
        span = span if span > 0 else 1e-12
        out: list[tuple[str, str, float]] = []
        names = list(lines)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if abs(lines[names[i]] - lines[names[j]]) / span <= tol_fraction:
                    mid = (lines[names[i]] + lines[names[j]]) / 2.0
                    out.append((names[i], names[j], mid))
        return out
