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
- **Audit Phase 6 NEXT:** backtest harness on Python mirror + honest metrics/limits.

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
- Strategy engine (Phase 2) not started; spec is `docs/STRATEGY.md`.
