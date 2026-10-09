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
    """The 4 equilibrium levels; None = unknown (never faked). چهار خط تعادل.

    Phase-1 fix: `from_leg` used to copy the same 50% into all four lines, so
    `overlaps()` always reported a (fake) coincidence.
    """
    fractal_internal: float | None = None
    fractal_external: float | None = None
    leg_internal: float | None = None
    leg_external: float | None = None

    @classmethod
    def from_leg(cls, leg_start: float, consumption: float,
                 flat_start: float | None = None) -> "Equilibriums":
        """External fractal: 50% of (leg start -> consumption).
        Internal fractal: 50% of (flat/F0 start -> consumption), only when known.

        خارجی: ۵۰٪ شروع لگ تا مصرف. داخلی: فقط وقتی flat_start معلوم باشد.
        SPEC-GAP: leg (time) equilibrium needs the unrevealed II.4 procedure ->
        left None (docs/OPEN_QUESTIONS.md Q-LEG-EQ).
        """
        internal = fib_50(flat_start, consumption) if flat_start is not None else None
        return cls(fractal_internal=internal,
                   fractal_external=fib_50(leg_start, consumption))

    def overlaps(self, tol_fraction: float = 0.002) -> list[tuple[str, str, float]]:
        """Pairs of KNOWN lines coinciding within tolerance -> key zones.

        هم‌پوشانی خطوط شناخته‌شده = ناحیه‌ی کلیدی (بقیه دور ریخته می‌شود).
        """
        lines = {k: v for k, v in (
            ("fractal_internal", self.fractal_internal),
            ("fractal_external", self.fractal_external),
            ("leg_internal", self.leg_internal),
            ("leg_external", self.leg_external)) if v is not None}
        if len(lines) < 2:
            return []
        span = max(lines.values()) - min(lines.values())
        span = span if span > 0 else 1e-12
        out: list[tuple[str, str, float]] = []
        names = list(lines)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if abs(lines[names[i]] - lines[names[j]]) / span <= tol_fraction:
                    out.append((names[i], names[j],
                                (lines[names[i]] + lines[names[j]]) / 2.0))
        return out
