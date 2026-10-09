"""Tests for the strategy rules engine (synthetic candles, no terminal)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dec3ption.config import Settings
from dec3ption.strategy import counting as C
from dec3ption.strategy import structure as S
from dec3ption.strategy import equilibrium as E
from dec3ption.strategy import corresponding as CP
from dec3ption.strategy import targets as T
from dec3ption.strategy import checklist as CL


def make_df(rows):
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    df["time"] = pd.date_range("2023-01-01", periods=len(df), freq="min")
    df["tick_volume"] = 1
    return df


# -- counting ---------------------------------------------------------------
def test_digital_root_labels():
    assert C.digital_root(18) == 9
    assert C.digital_root(25) == 7
    assert C.digital_root(2) == 2
    assert C.is_balanced_count(2) is True
    assert C.is_balanced_count(18) is False
    assert C.is_balanced_count(25) is False
    assert C.count_leg(8)["balanced"] is True
    assert C.count_leg(5)["balanced"] is False


# -- structure ---------------------------------------------------------------
def _trend_df():
    rows = []
    price = 100.0
    # up leg, pullback, higher high, deeper pullback, lower low structure
    for o, h, l, c in [
        (100, 101, 99, 100.5), (100.5, 103, 100, 102.5), (102.5, 104, 102, 103.5),
        (103.5, 103.8, 101, 101.5), (101.5, 105, 101.2, 104.5), (104.5, 106, 104, 105.5),
        (105.5, 105.8, 103, 103.5), (103.5, 104, 100, 100.5), (100.5, 101, 99.5, 100),
    ]:
        rows.append((o, h, l, c))
    return make_df(rows)


def test_find_swings_and_majors():
    df = _trend_df()
    swings = S.find_swings(df, order=1)
    assert len(swings) >= 2
    marked = S.mark_majors(swings)
    assert any(s.is_major for s in marked)


def test_detect_range_or_none():
    assert S.detect_range(make_df([(1, 2, 0.5, 1.5)] * 6)) is None
    rng = S.detect_range(_trend_df(), order=1)
    if rng is not None:
        assert rng.internal_high >= rng.internal_low


def test_merged_side():
    m = S.RangeLines(10, 5, 10, 1)
    assert m.merged_side() == "high"
    m2 = S.RangeLines(10, 5, 12, 5)
    assert m2.merged_side() == "low"
    m3 = S.RangeLines(10, 5, 12, 1)
    assert m3.merged_side() is None


# -- equilibrium ---------------------------------------------------------------
def test_fib50_and_overlap():
    assert E.fib_50(18787.0, 19036.2) == pytest.approx(18911.6)
    eq = E.Equilibriums.from_leg(18787.0, 19036.2)
    assert eq.fractal_external == pytest.approx(18911.6)
    ov = E.Equilibriums(10.0, 10.0, 5.0, 1.0).overlaps()
    assert any(a == "fractal_internal" and b == "fractal_external" for a, b, _ in ov)


# -- corresponding ---------------------------------------------------------------
def test_minor_major_shapes():
    bull = make_df([(1, 2, 0.5, 1.8), (1.8, 3.0, 1.7, 2.9)])
    assert CP.is_bullish_minor_major(bull, 1) is True
    assert CP.is_bearish_minor_major(bull, 1) is False
    bear = make_df([(3, 3.5, 2.0, 2.2), (2.2, 2.3, 1.0, 1.1)])
    assert CP.is_bearish_minor_major(bear, 1) is True


def test_pair_invalidation_two_closes():
    pair = CP.CorrespondingPair(origin=100.0, low=90.0, high=110.0, direction=1)
    pair.register_close(89.0)
    pair.register_close(89.5)
    assert pair.low_dead is False
    pair.register_close(89.2)
    assert pair.low_dead is True


def test_pair_dojii_not_counted():
    pair = CP.CorrespondingPair(origin=100.0, low=90.0, high=110.0, direction=1)
    pair.register_close(89.0, is_doji_inside=True)
    pair.register_close(89.0, is_doji_inside=True)
    pair.register_close(89.0, is_doji_inside=True)
    assert pair.low_dead is False


def test_scan_trigger_buy():
    pair = CP.CorrespondingPair(origin=100.0, low=90.0, high=110.0, direction=1)
    df = make_df([
        (95, 96, 94, 95), (95, 95.5, 89.5, 90.5),   # touches low
        (90.5, 92, 90.0, 91.5), (91.5, 94, 91.0, 93.5),  # 2 greens, 2nd over prior high
    ])
    sig = CP.scan_trigger(df, pair, 0)
    assert sig is not None and sig.direction == +1


# -- Phase 3 regression tests (audit fixes) --------------------------------------
def test_kill_as_f0_needs_tolerance():
    pair = CP.CorrespondingPair(origin=100.0, low=90.0, high=110.0, direction=1)
    pair.kill_as_f0(90.0000001)  # float noise: exact comparison must NOT fire
    assert pair.low_dead is False
    pair.kill_as_f0(90.0000001, tol=0.001)  # tick-size tolerance fires
    assert pair.low_dead is True


def test_closed_bars_drops_forming_bar():
    df = make_df([(1, 2, 0.5, 1.5)] * 5)
    closed = S.closed_bars(df)
    assert len(closed) == 4
    assert S.closed_bars(df.iloc[0:0]).empty


def test_scan_trigger_skips_candle_taking_opposite_tp1():
    pair = CP.CorrespondingPair(origin=100.0, low=90.0, high=110.0, direction=1)
    df = make_df([
        (95, 95.6, 94, 95.5), (91, 93, 89.5, 92.5),
        (92.5, 116, 92, 110), (110, 111, 105, 106),  # MM at 2, high takes TP1=115
    ])
    assert CP.scan_trigger(df, pair, 0) is not None  # no filter -> signal
    assert CP.scan_trigger(df, pair, 0, opposite_tp1_buy=115.0) is None  # R6.4 skip


# -- targets -------------------------------------------------------------------
def _settings():
    return Settings(mt5_path=Path("x"), tp_ladder=(1.0, 3.0, 6.0))


def test_build_plan_buy():
    s = _settings()
    plan = T.build_plan("BTCUSD", +1, entry=100.0, level=90.0, spread=0.5, settings=s)
    assert plan.stop_loss < 90.0  # buffer below level
    assert plan.risk_distance == pytest.approx(plan.entry - plan.stop_loss)
    assert plan.target(1.0) == pytest.approx(plan.entry + plan.risk_distance)
    assert plan.target(3.0) == pytest.approx(plan.entry + 3 * plan.risk_distance)


def test_build_plan_sell_mirrors():
    s = _settings()
    plan = T.build_plan("BTCUSD", -1, entry=100.0, level=110.0, spread=0.5, settings=s)
    assert plan.stop_loss > 110.0
    assert plan.target(1.0) == pytest.approx(plan.entry - plan.risk_distance)


# -- checklist -------------------------------------------------------------------
def test_checklist_all_or_nothing():
    good = CL.ChecklistInput(range_drawn=True, equilibriums_marked=True, permission_granted=True,
                             pair_valid=True, confirmation_closed=True, steps_ok=True,
                             sl_beyond_sweep=True, tp_plan_set=True)
    res = CL.evaluate(good)
    assert len(res) == 10 and CL.may_trade(res) is True
    bad = CL.evaluate(CL.ChecklistInput())
    assert CL.may_trade(bad) is False
    merged_blocks = CL.evaluate(CL.ChecklistInput(range_drawn=True, merged_line="high"))
    assert merged_blocks["no_merged_reversal"] is False
