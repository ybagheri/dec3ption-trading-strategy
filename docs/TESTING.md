# TESTING | تست

Five distinct categories — passing one proves nothing about the others:
۱) Python unit tests ۲) MQL5 source validation ۳) MetaEditor compilation ۴) MT5 execution ۵) Backtest.

## 1) Python unit tests
```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```
27 tests, no terminal required. Regression tests pin every audit fix (tolerance kill, closed bars,
R6.4 skip, TF validation). Note: on this machine set `$env:TMP` to a writable dir — the global Temp
symlink cleanup raises a benign `PermissionError` at session finish (results unaffected).

## 2) MQL5 source validation — manual checklist (done in review)
- chart-window indicator, 4 buffers w/ EMPTY_VALUE defaults, OnInit/OnCalculate present, inputs documented,
  closed-bar-only (`lastClosed = rates_total-2`), bounds checks (`rates_total<10`, `MathMin` ray end),
  no trading calls (pure indicator).

## 3) MetaEditor compilation — ✅ DONE 2026-10-09
`metaeditor64.exe /compile:<Indicators>\Dec3ptionTradingStrategy.mq5` →
`MQL5\Logs\20261009.log`: **0 errors, 0 warnings**, `.ex5` generated.

## 4) MT5 execution — USER-SIDE (terminal session untouched by automation)
1. In MT5: Navigator → Indicators → right-click → Refresh (Dec3ptionTradingStrategy appears).
2. Drag onto an M1/M5 chart (e.g. BTCUSD) → set `InpBufferPoints` (e.g. 10 ≈ 1 BTC point) → OK.
3. Expect: green/red arrows on confirmation closes + dashed orange SL / blue TP1 rays (30 bars).
4. Compare arrows against `tests/fixtures/parity_expected.csv` logic on the same bars; report mismatches.
## 5) Backtest — Phase 6.
