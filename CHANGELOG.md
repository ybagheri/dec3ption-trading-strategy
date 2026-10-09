# CHANGELOG

## 2026-10-09 — Refactor Phase 1 (correctness)
- **FIX** `structure.detect_range`: `RangeLines` was built with positional args in the wrong order
  (external_high held a LOW swing price). Now keyword args + test.
- **FIX** self-confirming signals: the Minor-Major candle that defined the level could also touch it and
  confirm the entry on the same bar (~half of signals on random-walk data). Level must now be formed
  strictly BEFORE the touch bar. Legacy behaviour: `allow_same_bar=True` / `InpAllowSameBar=true`.
  `IndicatorSignal` gains `level_index`, `touch_index`.
- **FIX** `equilibrium.Equilibriums`: `from_leg` no longer fabricates identical internal/leg lines
  (`None` = unknown); `overlaps()` ignores unknown lines.
- **FIX** Python mirror ignored the `lookback` bound when searching for the level (MQL5 did not).
- **PARITY** configurable `doji_ratio`, `max_closes`; buffer modes `fixed` / `adaptive`
  (`max(2*spread, 0.1*|entry-level|)`) in Python and MQL5 (v1.01).
- New fuzz parity fixture `tests/fixtures/parity_fuzz_*.csv` (15 signals). 47 tests pass.
- **NOTE** `results/` (Phase 6) were produced with the legacy same-bar behaviour and must be regenerated.
  MQL5 v1.01 is NOT yet compiled/verified in MetaEditor.

## 2026-10-09 — Audit + completion pass
### Phase 1–2 (audit & spec)
- `docs/PROJECT_AUDIT.md` — 4 high / 5 medium findings, baseline 23/23 pass.
- `docs/STRATEGY_SPECIFICATION.md` — numbered requirements [V]/[T]/[G], signal semantics,
  traceability table.
### Phase 3 (refactor)
- Tolerance-based `kill_as_f0` (exact-float bug); `closed_bars` helper (R9.1);
  R6.4 opposite-TP1 skip in `scan_trigger`; TF validation; structured logging;
  `pyproject.toml`; `docs/ARCHITECTURE.md`, `docs/TESTING.md`. 27/27 pass.
### Phase 4 (MQL5 indicator)
- Genuine custom indicator `MQL5/Indicators/Dec3ptionTradingStrategy.mq5`
  (chart window, 4 buffers: Buy/Sell arrows + SL/TP1 rays, closed-bar logic).
- Python mirror `strategy/indicator.py` = single source of truth.
- Parity fixtures `parity_bars.csv` / `parity_expected.csv` + `test_parity.py`
  (fixture match, exact values, determinism, stability). 31/31 pass.
### Phase 5 (compile & deploy)
- Deployed to live Indicators dir (backup-safe script; fixed path bug).
- MetaEditor compile: **0 errors, 0 warnings** (`MQL5\Logs\20261009.log`), `.ex5` generated.
### Phase 6 (historical validation)
- `scripts/historical_validation.py` on real Alpari demo history (2000 closed bars/symbol).
- Results in R: XAUUSD M1 +8.0R (66.7%), NAS100 M5 +4.0R (60%), EURUSD M5 −1.0R,
  US30 M5 −4.0R, US500 M5 −4.0R. Small sample; no spread/commission; no walk-forward.
  See `results/README.md` — NOT a profitability claim.
