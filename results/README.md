> ⚠️ **STALE (2026-10-09, refactor Phase 1):** these numbers were produced BEFORE the same-bar self-confirmation
> fix (`allow_same_bar`). Re-run `scripts/historical_validation.py` before quoting any result.
> این نتایج قبل از اصلاح سیگنال خودتأییدگر تولید شده‌اند و باید دوباره تولید شوند.

# Historical validation — 2026-10-09 (Phase 6)

Dataset: Alpari MT5 demo terminal, real OHLC history, last 2000 bars
(closed bars only; forming bar excluded). Buffer: XAUUSD 10 pts, indices 20 pts,
EURUSD 10 pts. Exit rule: signal-bar close entry; SL or TP1 (1R) within 60 bars;
same-bar SL+TP ambiguity resolved CONSERVATIVELY (SL first).
Spread/commission NOT applied; position sizing 0.5% not simulated (results are in R-multiples).

| Symbol | TF | Trades | Win rate | Net R | Expectancy R | Max DD R |
|---|---|---|---|---|---|---|
| XAUUSD | M1 | 24 | 66.7% | +8.0 | +0.33 | -2.0 |
| NAS100 | M5 | 20 | 60.0% | +4.0 | +0.20 | -4.0 |
| EURUSD | M5 | 21 | 47.6% | -1.0 | -0.05 | -6.0 |
| US30 | M5 | 26 | 42.3% | -4.0 | -0.15 | -6.0 |
| US500 | M5 | 27 | 40.7% | -4.0 | -0.15 | -6.0 |

Honest reading | خوانش صادقانه:
- ~20–27 trades per symbol is a SMALL sample; confidence intervals are wide.
- Mixed results: positive on gold/NAS100, negative on US30/US500/EURUSD in this window.
- NOT a profitability claim: no spread/slippage/commission, no walk-forward split,
  no parameter optimization (so no overfitting test possible yet).
- Next: add spread/commission from symbol specs, split in-sample/out-of-sample,
  per-day trade limit (max 3) and daily stop, then re-run.

Raw CSVs: `results/trades_<SYMBOL>_<TF>.csv`; summary: `results/summary.json`.
Reproduce: `python scripts/historical_validation.py` (read-only terminal access).
