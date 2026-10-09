# CHANGELOG

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
