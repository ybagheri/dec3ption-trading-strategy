"""Tests for MT5Client that never require a live terminal.

تست‌های اتصال متاتریدر بدون نیاز به ترمینال واقعی.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dec3ption.config import Settings
from dec3ption.mt5_client import MT5Client, TIMEFRAME_MAP


def _settings(**over):
    base = dict(mt5_path=Path(r"C:\Program Files\Alpari MT5_2\terminal64.exe"))
    base.update(over)
    return Settings(**base)


def test_timeframe_map_covers_env_timeframes():
    for tf in ("M1", "M5"):
        assert tf in TIMEFRAME_MAP


def test_connect_returns_false_without_package_or_terminal(monkeypatch):
    """With a bogus MT5 package import, connect() must return False, not raise."""
    client = MT5Client(_settings())
    monkeypatch.setattr(client, "_import_mt5", lambda: (_ for _ in ()).throw(ImportError("no mt5")))
    assert client.connect() is False
    assert client.is_connected is False


def test_dry_run_order_never_touches_terminal():
    client = MT5Client(_settings(dry_run=True))
    result = client.place_market_order("BTCUSD", +1, 0.01, 99.0, 103.0)
    assert result.dry_run is True
    assert result.ticket == 0


def test_methods_require_connection():
    client = MT5Client(_settings())
    with pytest.raises(RuntimeError, match="not connected"):
        client.ensure_symbol("BTCUSD")
    with pytest.raises(RuntimeError, match="not connected"):
        client.fetch_rates("BTCUSD", "M1", 10)
