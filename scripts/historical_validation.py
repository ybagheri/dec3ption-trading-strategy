"""Historical validation harness (Phase 6).

Reads REAL closed-bar history from the (read-only) MT5 terminal, runs the
indicator mirror (`strategy/indicator.py` = same rules as the MQL5 indicator),
then simulates trades: enter at signal close, exit at SL or TP1 (ladder 1R).

Same-bar SL/TP ambiguity: with OHLC data the intrabar order is unknown;
the CONSERVATIVE convention is used (SL assumed hit first). Documented limitation.

Outputs per-symbol CSV of trades + a metrics JSON. No live orders are placed.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dec3ption.strategy.indicator import indicator_signals


@dataclass
class Trade:
    entry_time: str
    direction: int
    entry: float
    sl: float
    tp1: float
    result_r: float  # +1 TP1 hit, -1 SL hit, 0 neither within max_bars
    bars_held: int


def simulate(df: pd.DataFrame, signals, max_bars: int = 60) -> list[Trade]:
    """Entry at signal-bar close; scan forward on closed bars only."""
    closes = df["close"].to_numpy()
    lows = df["low"].to_numpy()
    highs = df["high"].to_numpy()
    times = df["time"].to_numpy()
    trades: list[Trade] = []
    for s in signals:
        j = s.index
        entry, sl, tp1 = s.entry, s.stop_loss, s.tp1
        result, held = 0.0, 0
        for k in range(j + 1, min(j + 1 + max_bars, len(df) - 1)):
            hit_sl = lows[k] <= sl if s.direction > 0 else highs[k] >= sl
            hit_tp = highs[k] >= tp1 if s.direction > 0 else lows[k] <= tp1
            if hit_sl and hit_tp:
                result = -1.0  # conservative: SL first (ambiguous intrabar order)
            elif hit_sl:
                result = -1.0
            elif hit_tp:
                result = +1.0
            else:
                continue
            held = k - j
            break
        trades.append(Trade(str(times[j]), s.direction, entry, sl, tp1,
                             result, held))
    return trades


def metrics(trades: list[Trade]) -> dict:
    n = len(trades)
    wins = sum(1 for t in trades if t.result_r > 0)
    losses = sum(1 for t in trades if t.result_r < 0)
    open_ = sum(1 for t in trades if t.result_r == 0)
    net_r = sum(t.result_r for t in trades)
    win_rate = wins / n if n else 0.0
    expectancy = net_r / n if n else 0.0
    equity, peak, mdd = 0.0, 0.0, 0.0
    for t in trades:
        equity += t.result_r
        peak = max(peak, equity)
        mdd = min(mdd, equity - peak)
    return {
        "trades": n, "wins": wins, "losses": losses, "expired_no_hit": open_,
        "net_R": round(net_r, 2), "win_rate": round(win_rate, 4),
        "expectancy_R": round(expectancy, 4), "max_dd_R": round(mdd, 2),
    }


def run(symbol: str, timeframe: str, bars: int, buffer_points: float,
        point: float) -> dict:
    import MetaTrader5 as mt5
    tf = getattr(mt5, f"TIMEFRAME_{timeframe}")
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
    if rates is None or len(rates) < 50:
        return {"error": f"no history for {symbol} {timeframe}"}
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df[["time", "open", "high", "low", "close", "tick_volume"]]
    buffer = buffer_points * point
    sigs = indicator_signals(df, buffer=buffer)
    trades = simulate(df, sigs)
    return {
        "symbol": symbol, "timeframe": timeframe,
        "bars": len(df) - 1,  # closed bars only
        "signals": len(sigs),
        "metrics": metrics(trades),
        "trades": [t.__dict__ for t in trades],
    }


if __name__ == "__main__":
    import MetaTrader5 as mt5
    mt5.initialize(path=r"C:\Program Files\Alpari MT5_2\terminal64.exe",
                     timeout=60000)
    out_dir = Path(__file__).resolve().parents[1] / "results"
    out_dir.mkdir(exist_ok=True)
    specs = [
        ("XAUUSD", "M1", 2000, 10.0),
        ("US30", "M5", 2000, 20.0),
        ("NAS100", "M5", 2000, 20.0),
        ("US500", "M5", 2000, 20.0),
        ("EURUSD", "M5", 2000, 10.0),
    ]
    summary = []
    for symbol, tf, bars, buf in specs:
        info = mt5.symbol_info(symbol)
        point = info.point if info else 0.01
        res = run(symbol, tf, bars, buf, point)
        print(symbol, tf, "->", res.get("metrics", res.get("error")))
        summary.append({k: v for k, v in res.items() if k != "trades"})
        pd.DataFrame(res.get("trades", [])).to_csv(
            out_dir / f"trades_{symbol}_{tf}.csv", index=False)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1),
                                            encoding="utf-8")
    mt5.shutdown()
    print("saved to", out_dir)
