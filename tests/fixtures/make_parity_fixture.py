"""Parity fixture: deterministic bars + expected indicator signals.

فیکسچر parity — مبنای یکسان بودن پایتون و MQL5.
Expected (buffer=0.5): BUY@5 (102.0/100.0/99.5/104.5), BUY@13 (101.2/99.8/99.3/103.1),
BUY@20 (99.8/99.5/99.0/100.6), SELL@23 (99.2/101.2/101.7/96.7). Bar 29 is forming (excluded).
Covers: touch+MM trigger, 2-close kill, doji skip, 2-bar window expiry, no-touch MM.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from dec3ption.strategy.indicator import indicator_signals

BARS = [
    (100, 101, 99, 100.5), (100.5, 102, 100, 101.5), (101.5, 103, 101, 102.5),
    (102.5, 103, 100, 100.5), (100.5, 101, 99.8, 100.8), (100.8, 102.5, 100.5, 102.0),
    (102, 103, 101, 102.5), (102.5, 103, 101.5, 102), (102, 102.5, 101, 101.5),
    (101.5, 102, 100.5, 101.8), (101.8, 102.2, 101, 101.5), (101.5, 101.8, 100, 100.2),
    (100.2, 100.6, 99.5, 100.4), (100.4, 101.5, 100.0, 101.2),
    (101.2, 101.6, 100.5, 100.8), (100.8, 101.2, 100.0, 100.3),
    (100.3, 100.9, 99.9, 100.6), (101.0, 101.2, 100.0, 100.1),
    (100.1, 100.3, 98.5, 98.7), (98.7, 99.5, 98.5, 99.0),
    (99.0, 100.0, 98.8, 99.8), (99.8, 100.5, 99.5, 100.2),
    (100.5, 101.3, 100.0, 100.1), (100.1, 100.2, 99.0, 99.2),
    (99.2, 99.8, 98.9, 99.0), (99.0, 99.6, 98.7, 99.4),
    (99.4, 99.7, 99.0, 99.1), (99.1, 99.9, 98.8, 99.7),
    (99.7, 100.0, 99.3, 99.5), (99.5, 99.9, 99.2, 99.6),
]


def make_frame() -> pd.DataFrame:
    df = pd.DataFrame(BARS, columns=["open", "high", "low", "close"])
    df["time"] = pd.date_range("2023-01-20 16:00", periods=len(df), freq="min")
    df["tick_volume"] = 100
    return df


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    df = make_frame()
    df.to_csv(out_dir / "parity_bars.csv", index=False)
    sigs = indicator_signals(df, buffer=0.5)
    exp = pd.DataFrame([s.__dict__ for s in sigs])
    exp.to_csv(out_dir / "parity_expected.csv", index=False)
    print(exp.to_string(index=False))
