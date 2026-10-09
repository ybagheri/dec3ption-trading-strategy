# ARCHITECTURE | معماری

```
src/dec3ption/
  config.py          Settings (frozen dataclass, .env + environ, validate)
  mt5_client.py      MT5Client (lazy MT5 import, connect/fetch/order, dry-run safe)
  strategy/
    structure.py     swings, majors, RangeLines, merged_side, closed_bars (R9.1)
    equilibrium.py   Fib-50 x4, overlaps
    counting.py      digital_root, even/odd filter
    corresponding.py Minor-Major shapes, CorrespondingPair, scan_trigger (R6.4 filter)
    targets.py       TradePlan (SL+buffer, TP ladder, BE/partial rules)
    checklist.py     10-item evaluator (pure)
```

Rules: pure functions on candle DataFrames (`time,open,high,low,close,tick_volume`); I/O only in
`MT5Client`. Signals evaluate on **closed bars** (`closed_bars` drops the forming bar) — see R9.1.
Logging via stdlib `logging` (no prints); `MT5Client.connect` degrades to `False`, never raises.
