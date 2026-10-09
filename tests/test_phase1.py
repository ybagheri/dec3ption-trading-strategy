"""Phase-1 correctness regressions (written BEFORE the fixes).

رگرسیون‌های فاز ۱ — ابتدا تست شکست‌خورده، سپس اصلاح.
Covers: detect_range arg order, self-confirming signals, equilibrium
placeholders, Python-side constants/buffer parity with the MQL5 indicator.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dec3ption.strategy import equilibrium as E
from dec3ption.strategy import structure as S
from dec3ption.strategy.corresponding import is_bullish_minor_major, is_bearish_minor_major
from dec3ption.strategy.indicator import indicator_signals

FIX = Path(__file__).resolve().parent / "fixtures"


def random_walk(seed: int, n: int = 600) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    c = np.round(np.cumsum(rng.normal(0, 1, n)) + 100, 2)
    o = np.r_[c[0], c[:-1]]
    h = np.round(np.maximum(o, c) + np.abs(rng.normal(0, 0.3, n)), 2)
    lo = np.round(np.minimum(o, c) - np.abs(rng.normal(0, 0.3, n)), 2)
    df = pd.DataFrame({"open": o, "high": h, "low": lo, "close": c})
    df["time"] = pd.date_range("2023-01-01", periods=n, freq="min")
    df["tick_volume"] = 1
    return df


# -- 1. detect_range argument order -----------------------------------------
def test_detect_range_maps_fields_to_correct_swings():
    df = random_walk(1, 400)
    majors = [s for s in S.mark_majors(S.find_swings(df, 2)) if s.is_major]
    highs = [s for s in majors if s.kind == "high"]
    lows = [s for s in majors if s.kind == "low"]
    r = S.detect_range(df, 2)
    assert r is not None
    assert r.internal_high == pytest.approx(highs[-1].price)
    assert r.external_high == pytest.approx(highs[-2].price)
    assert r.internal_low == pytest.approx(lows[-1].price)
    assert r.external_low == pytest.approx(lows[-2].price)


def test_detect_range_values_are_plausible_prices():
    """Old bug: external_high held a LOW swing price (~35 below any high)."""
    df = random_walk(1, 400)
    r = S.detect_range(df, 2)
    assert r.internal_high > r.internal_low
    assert r.external_high > r.external_low


# -- 2. self-confirming signals ---------------------------------------------
def _bar_lookup(df):
    return df["low"].to_numpy(), df["high"].to_numpy()


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_level_is_formed_strictly_before_touch_bar(seed):
    df = random_walk(seed, 1500)
    sigs = indicator_signals(df, buffer=0.1)
    assert sigs, "fixture must produce signals to be meaningful"
    for s in sigs:
        assert s.level_index < s.touch_index <= s.index, s


def test_allow_same_bar_flag_restores_legacy_behaviour():
    df = random_walk(0, 1500)
    strict = indicator_signals(df, buffer=0.1)
    legacy = indicator_signals(df, buffer=0.1, allow_same_bar=True)
    assert len(legacy) > len(strict)
    assert any(s.level_index == s.touch_index for s in legacy)


def test_engulfing_candle_cannot_define_touch_and_confirm_itself():
    # bar0 down, bar1 up, bar2 = engulfing bull MM whose low dips below bar1 low.
    rows = [
        (101, 102, 100, 100.5), (100.5, 101, 99.5, 100.8),
        (100.2, 102.5, 99.0, 102.4),  # MM: green, green, close > high[1]
        (102.4, 102.6, 102.0, 102.1), (102.1, 102.3, 101.9, 102.0),
        (102.0, 102.2, 101.8, 101.9),
    ]
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    df["time"] = pd.date_range("2023-01-01", periods=len(df), freq="min")
    assert is_bullish_minor_major(df, 2)
    assert [s for s in indicator_signals(df, buffer=0.1) if s.direction > 0] == []
    legacy = indicator_signals(df, buffer=0.1, allow_same_bar=True)
    assert any(s.index == 2 and s.direction > 0 for s in legacy)


# -- 3. equilibrium placeholders --------------------------------------------
def test_from_leg_without_flat_start_has_no_fake_internal_lines():
    eq = E.Equilibriums.from_leg(18787.0, 19036.2)
    assert eq.fractal_external == pytest.approx(18911.6)
    assert eq.fractal_internal is None
    assert eq.leg_internal is None and eq.leg_external is None
    assert eq.overlaps() == []


def test_from_leg_with_flat_start_distinguishes_internal_external():
    eq = E.Equilibriums.from_leg(100.0, 120.0, flat_start=110.0)
    assert eq.fractal_external == pytest.approx(110.0)
    assert eq.fractal_internal == pytest.approx(115.0)
    assert eq.overlaps() == []


def test_overlaps_detects_real_coincidence_only():
    eq = E.Equilibriums(fractal_internal=10.0, fractal_external=10.0,
                        leg_internal=5.0, leg_external=1.0)
    names = {(a, b) for a, b, _ in eq.overlaps()}
    assert names == {("fractal_internal", "fractal_external")}


# -- 4. constants / buffer unification --------------------------------------
def _doji_df():
    # confirmation-like candles but tiny bodies: ratio 0.15 -> doji only if ratio>0.15
    rows = [(100, 101, 99, 100.2)] * 3
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    return df


def test_doji_ratio_is_configurable():
    from dec3ption.strategy.corresponding import is_doji_or_inside
    df = pd.DataFrame([(100, 102, 98, 101), (100, 102.5, 98, 100.5)],
                      columns=["open", "high", "low", "close"])
    # not an inside bar; body 0.5 / range 4.5 = 0.111
    assert is_doji_or_inside(df, 1, doji_ratio=0.1) is False
    assert is_doji_or_inside(df, 1, doji_ratio=0.2) is True


def test_max_closes_is_configurable():
    df = random_walk(2, 1500)
    a = indicator_signals(df, buffer=0.1, max_closes=2)
    b = indicator_signals(df, buffer=0.1, max_closes=0)
    assert [s.index for s in a] != [s.index for s in b]


def test_adaptive_buffer_matches_spec_formula():
    df = random_walk(0, 1500)
    fixed = indicator_signals(df, buffer=0.0)
    ad = indicator_signals(df, buffer_mode="adaptive", spread=0.05,
                           buffer_spread_mult=2.0, buffer_range_fraction=0.1)
    assert len(ad) == len(fixed)
    for s in ad:
        rng_h = abs(s.entry - s.level)
        want = max(2.0 * 0.05, 0.1 * rng_h)
        got = abs(s.stop_loss - s.level)
        assert got == pytest.approx(want)


def test_lookback_limits_level_search_like_mql5():
    """Python mirror used to ignore `first` when searching for the level."""
    df = random_walk(3, 800)
    short = indicator_signals(df, buffer=0.1, lookback=50)
    n = len(df) - 1
    start = max(2, n - 50)
    for s in short:
        assert s.level_index >= start
        assert s.index >= start


# -- parity fuzz fixture -----------------------------------------------------
def test_fuzz_parity_fixture_matches():
    bars = pd.read_csv(FIX / "parity_fuzz_bars.csv")
    want = pd.read_csv(FIX / "parity_fuzz_expected.csv")
    sigs = indicator_signals(bars, buffer=0.1, lookback=500)
    cols = ["index", "direction", "entry", "level", "stop_loss", "tp1",
            "level_index", "touch_index"]
    got = pd.DataFrame([s.__dict__ for s in sigs])[cols].reset_index(drop=True)
    pd.testing.assert_frame_equal(got.round(6), want[cols].round(6), check_dtype=False)
    assert len(want) >= 10
