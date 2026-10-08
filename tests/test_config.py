"""Tests for Settings (no MT5/terminal required)."""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dec3ption.config import Settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for key in list(os.environ):
        if key.startswith("MT5_") or key in {
            "SYMBOLS", "TIMEFRAMES", "RISK_PCT", "MAX_DAILY_LOSS_PCT",
            "MAX_TRADES_PER_DAY", "BUFFER_SPREAD_MULT", "BUFFER_RANGE_FRACTION",
            "TP_LADDER", "TP1_MOVE_TO_BREAKEVEN", "TP3_PARTIAL_CLOSE_PCT",
            "MAGIC_NUMBER", "DRY_RUN",
        }:
            monkeypatch.delenv(key, raising=False)


def _base_env(monkeypatch, tmp_path):
    monkeypatch.setenv("MT5_PATH", str(tmp_path / "terminal64.exe"))


def test_defaults_and_validate(monkeypatch, tmp_path):
    _base_env(monkeypatch, tmp_path)
    s = Settings.from_env(env_file=tmp_path / "nonexistent.env")
    s.validate()
    assert s.risk_pct == 0.5
    assert s.dry_run is True
    assert s.symbols == ("BTCUSD",)


def test_env_example_parses(monkeypatch):
    example = Path(__file__).resolve().parents[1] / ".env.example"
    s = Settings.from_env(env_file=example)
    s.validate()
    assert "BTCUSD" in s.symbols or "BTC" in str(s.symbols)
    assert s.tp_ladder[0] == 1.0
    assert s.buffer_size(spread=0.5, range_height=50.0) == pytest.approx(5.0)


def test_explicit_env_wins_over_file(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("RISK_PCT=2.0\n", encoding="utf-8")
    _base_env(monkeypatch, tmp_path)
    monkeypatch.setenv("RISK_PCT", "0.25")
    s = Settings.from_env(env_file=env_file)
    assert s.risk_pct == pytest.approx(0.25)


def test_buffer_rule_max_of_both(monkeypatch, tmp_path):
    _base_env(monkeypatch, tmp_path)
    monkeypatch.setenv("BUFFER_SPREAD_MULT", "2.0")
    monkeypatch.setenv("BUFFER_RANGE_FRACTION", "0.1")
    s = Settings.from_env(env_file=tmp_path / "none.env")
    assert s.buffer_size(spread=0.5, range_height=2.0) == pytest.approx(1.0)  # spread leg wins
    assert s.buffer_size(spread=0.5, range_height=50.0) == pytest.approx(5.0)  # range leg wins


def test_tp_price_direction(monkeypatch, tmp_path):
    _base_env(monkeypatch, tmp_path)
    s = Settings.from_env(env_file=tmp_path / "none.env")
    assert s.tp_price(100.0, 10.0, 3.0, +1) == pytest.approx(130.0)
    assert s.tp_price(100.0, 10.0, 3.0, -1) == pytest.approx(70.0)


def test_invalid_settings_raise(monkeypatch, tmp_path):
    _base_env(monkeypatch, tmp_path)
    monkeypatch.setenv("RISK_PCT", "0")
    with pytest.raises(ValueError, match="RISK_PCT"):
        Settings.from_env(env_file=tmp_path / "none.env").validate()


def test_missing_mt5_path_raises(monkeypatch, tmp_path):
    with pytest.raises(ValueError, match="MT5_PATH"):
        Settings.from_env(env_file=tmp_path / "none.env").validate()
