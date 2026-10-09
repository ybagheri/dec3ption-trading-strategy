# PROJECT AUDIT | ممیزی فنی پروژه

Date: 2026-10-08 · Baseline: 23/23 pytest pass · Working tree clean · `main` @ `c8aa285`

## 1. Verdict | نتیجه

Working, tested Python skeleton with a faithful-but-partial strategy engine. No MQL5 code, no backtest,
no live loop, no logging. The gaps are exactly what the new phase plan (MQL5 indicator + validation) addresses.

## 2. Findings by severity | یافته‌ها

### 🔴 High
1. **No MQL5 implementation.** Spec requires a native custom indicator; repo is Python-only.
   → Fix: Phase 4 (`MQL5/Indicators/Dec3ptionTradingStrategy.mq5`).
2. **Exact-float comparison in `CorrespondingPair.kill_as_f0`** (`abs(price-level) < 1e-12` on raw floats
   will ~never fire on real quotes). → Fix: tolerance in price steps (Phase 3).
3. **No closed-bar discipline.** `fetch_rates` returns bar 0 (still forming); future live loop must trade
   closed bars only or signals repaint. → Fix: documented rule + helper in Phase 3.
4. **No backtesting.** Zero historical validation; no profitability claim may be made. → Phase 6.

### 🟡 Medium
5. **No logging** — `print`-less but also log-less; MT5Client swallows exceptions to `False`. Acceptable for
   connect(), but operational code needs structured logging → Phase 3.
6. **`mark_majors` is a simplified BOS proxy**, not the instructor's full Major/Minor judgment (chart discretion).
   Documented as approximation; parity tests must pin its behavior → Phase 2 spec + Phase 4 fixtures.
7. **`scan_trigger` wick-touch + 2-candle confirmation window** matches spec §2.4, but the "entry candle must not
   take opposite TP1" filter is NOT implemented in code (only in checklist). → Phase 3.
8. **TIMEFRAME_MAP covers only M1/M5** though config allows arbitrary strings; unsupported TF raises at fetch
   time (acceptable, but validate early in `Settings.validate`). → Phase 3.
9. **No packaging** (`pyproject.toml`); tests rely on `sys.path` insertion. Works, but fragile → Phase 3.

### 🟢 Low
10. `.env` correctly git-ignored; no secrets in repo. ✅
11. Persian/English bilingual docs present; README is EN-primary. ✅
12. `place_market_order` dry-run path never touches terminal. ✅ (Live path untested — needs demo test.)

## 3. Baseline test results | نتیجه‌ی تست پایه
- `pytest tests/ -q`: **23 passed** (11 config/client + 12 strategy), no terminal required.
- `MetaTrader5` pkg 5.0.6231 imports; terminal, metaeditor64, Indicators dir all exist.
- pytest cache cleanup shows a benign `PermissionError` on Temp (Windows); results unaffected.

## 4. What was NOT claimed | ادعاهای اثبات‌نشده
- No live order has ever been sent; no backtest exists; no win-rate/expectancy numbers exist anywhere.
