# HANDOFF | یادداشت تحویل

> Updated at the end of every phase, BEFORE commit+push.
> پایان هر فاز، قبل از کامیت و پوش به‌روز می‌شود.

## Status | وضعیت
- **Audit Phase 1 DONE (2026-10-09):** git clean @ `c8aa285`, baseline 23/23 pass,
  MT5 paths verified (terminal, metaeditor64, Indicators dir, MT5 pkg 5.0.6231).
  `docs/PROJECT_AUDIT.md` created (4 high / 5 medium findings). Committed + pushed.
- **Audit Phase 2 DONE (2026-10-09):** `docs/STRATEGY_SPECIFICATION.md` created —
  30+ numbered requirements [V]/[T]/[G], signal semantics (closed-candle only), traceability table.
  Committed + pushed.
- **Audit Phase 3 DONE (2026-10-09):** refactored — tolerance `kill_as_f0`, `closed_bars` (R9.1),
  R6.4 TP1 filter in `scan_trigger`, structured logging, TF validation, `pyproject.toml`,
  `docs/ARCHITECTURE.md` + `docs/TESTING.md`. **27/27 pytest pass.** Committed + pushed.
- **Audit Phase 4 DONE (2026-10-09):** genuine MQL5 custom indicator
  `MQL5/Indicators/Dec3ptionTradingStrategy.mq5` (chart window; Buy/Sell arrow buffers + SL/TP1 ray
  buffers; closed-bar-only logic; bounds-checked; diagnostics in OnInit) + Python mirror
  `strategy/indicator.py` (single source of truth) + parity fixtures (`parity_bars.csv`,
  `parity_expected.csv`: BUY@5/13/20, SELL@23) + `test_parity.py` (fixture match, exact values,
  determinism, stability, empty-data). Deploy script `scripts/deploy_indicator.ps1` (backup-safe).
  **31/31 pytest pass. NOT yet compiled** (Phase 5). Committed + pushed.
- **Audit Phase 5 DONE (2026-10-09):** deployed `.mq5` to the live Indicators dir (backup-safe script;
  fixed one-level-too-deep `$RepoRoot` bug), compiled with the real MetaEditor:
  **0 errors, 0 warnings, 614 ms** (`MQL5\Logs\20261009.log` 10:47:10), `.ex5` generated.
  Terminal is running (user session — untouched). Chart-load verification is USER-SIDE (steps in TESTING.md).
  Committed + pushed.
- **Audit Phase 6 DONE (2026-10-09):** `scripts/historical_validation.py` ran on REAL
  Alpari-demo history (2000 closed bars/symbol, read-only terminal access, login 5319… not stored):
  XAUUSD M1 +8.0R/66.7%, NAS100 M5 +4.0R/60%, EURUSD M5 −1.0R, US30 M5 −4.0R, US500 M5 −4.0R.
  Small sample, no spread/commission, conservative same-bar SL-first, no walk-forward.
  `results/` (CSVs + summary + README with honest limits). Committed + pushed.
- **Audit Phase 7 (final) DONE (2026-10-09):** 31/31 pytest pass, secrets scan clean,
  ROADMAP/CHANGELOG/HANDOFF updated, all phases committed and pushed.
- **Refactor Phase 1 DONE (2026-10-09):** detect_range arg-order bug, self-confirming signals,
  equilibrium placeholders, lookback parity, configurable doji/max_closes/buffer modes (Python + MQL5 v1.01),
  fuzz parity fixture. **47/47 pytest pass.** MQL5 v1.01 NOT compiled yet (user-side). `results/` are STALE.
  Open rules: `docs/OPEN_QUESTIONS.md`.
- **Next:** Refactor Phase 2 (wire F0 / corresponding pair / permission into the signal path), then Phase 3 live loop (risk-sized orders from config, 0.5% sizing, journal),
  then backtest upgrades (spread/commission, IS/OOS split, daily limits).

## Final status | وضعیت نهایی
- GitHub: `git@github.com:ybagheri/dec3ption-trading-strategy` @ `main` — all pushed.
- Tests: 31/31 (config 8, client 4, strategy 15, parity 4).
- Indicator: compiled 0/0, deployed to live Indicators dir.
- No live orders ever sent (dry_run=true default).

## What works | چه چیزی کار می‌کند
- `Settings.from_env()` reads `.env` (+ explicit env wins), `validate()`, `buffer_size()`, `tp_price()`.
- `MT5Client`: lazy MT5 import, `connect()` returns False (never raises) without terminal,
  `fetch_rates()` → DataFrame, `place_market_order()` dry-run safe.
- Strategy engine pure functions on candle DataFrames (no terminal needed).
- `pytest`: 23 tests, all pass without a terminal (مستقل از ترمینال).

## Environment | محیط
- Repo: `git@github.com:ybagheri/dec3ption-trading-strategy.git` (branch `main`)
- Local: `F:\Trade Learning\Dec3ption\new\dec3ption-trading-strategy`
- Terminal: `C:\Program Files\Alpari MT5_2\terminal64.exe`
- Data folder: `...\MetaQuotes\Terminal\AF19ECCF568F855DF9D3196BBF8BF315`
- Python 3.12.9, venv `.venv`, `pip install -r requirements-dev.txt`, copy `.env.example` → `.env`.

## Open items | موارد باز
- `.env` (private) must be created from `.env.example`; set `MT5_LOGIN/PASSWORD/SERVER` or leave empty
  to use the logged-in terminal. | فایل `.env` شخصی را بسازید.
- Live-order path (`dry_run=false`) is implemented but UNTESTED against a real terminal — test on demo first.
  مسیر سفارش واقعی پیاده شده ولی تست نشده — اول روی دمو.
- Strategy engine covers only the Minor-Major touch trigger; remaining layers: refactor Phase 2.
