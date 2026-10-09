"""Parity + determinism tests: Python mirror output must equal the committed fixture.

تست parity — خروجی موتور باید دقیقاً با فیکسچر ثبت‌شده یکی باشد.
The MQL5 indicator implements the same algorithm (`indicator_signals` is the
single source of truth); `parity_bars.csv` / `parity_expected.csv` are the
cross-platform contract (see docs/STRATEGY_SPECIFICATION.md R9.2).
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures"))

from dec3ption.strategy.indicator import indicator_signals
from make_parity_fixture import make_frame

FIX = Path(__file__).resolve().parent / "fixtures"


def test_signals_match_committed_fixture():
    sigs = indicator_signals(make_frame(), buffer=0.5)
    cols = ["index", "direction", "entry", "level", "stop_loss", "tp1"]
    got = pd.DataFrame([s.__dict__ for s in sigs])[cols].reset_index(drop=True)
    want = pd.read_csv(FIX / "parity_expected.csv")[cols]
    pd.testing.assert_frame_equal(got.round(6), want.round(6), check_dtype=False)


def test_exact_expected_values():
    sigs = {(s.index, s.direction): s for s in indicator_signals(make_frame(), buffer=0.5)}
    assert set(sigs) == {(5, 1), (13, 1), (20, 1), (23, -1)}
    b = sigs[(13, 1)]
    assert b.entry == pytest.approx(101.2) and b.level == pytest.approx(99.8)
    assert b.stop_loss == pytest.approx(99.3) and b.tp1 == pytest.approx(103.1)
    s = sigs[(23, -1)]
    assert s.entry == pytest.approx(99.2) and s.level == pytest.approx(101.2)
    assert s.stop_loss == pytest.approx(101.7) and s.tp1 == pytest.approx(96.7)


def test_deterministic_and_stable():
    first = [s.__dict__ for s in indicator_signals(make_frame(), buffer=0.5)]
    second = [s.__dict__ for s in indicator_signals(make_frame(), buffer=0.5)]
    assert first == second
    # truncating history must not change earlier signals (stability)
    part = [s.__dict__ for s in indicator_signals(make_frame().iloc[:25], buffer=0.5)]
    assert part == [s for s in first if s["index"] < 24]


def test_no_signal_on_empty_or_flat():
    flat = make_frame().iloc[:3].copy()
    flat[["open", "high", "low", "close"]] = 100.0
    assert indicator_signals(flat, buffer=0.5) == []
