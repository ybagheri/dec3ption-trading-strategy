# STRATEGY SPECIFICATION | مشخصات فنی استراتژی

Source of truth for both implementations (Python reference + MQL5 indicator).
مرجع هر دو پیاده‌سازی. Narrative background lives in `docs/STRATEGY.md`; this file is the testable contract.

Status tags: **[V]** verified (transcript + screenshot or user-confirmed) · **[T]** from transcript, chart-dependent ·
**[G]** gap — isolated, NOT implemented as fact.

## 1. Core concept | ایده‌ی مرکزی — [V]

Price moves from a balanced place to an unbalanced place: **balanced in TIME, unbalanced in PRICE**.
Trade only zones that are time-balanced but price-unbalanced. Understanding ≠ trading permission.

## 2. Market & timeframe assumptions — [V]

- Instruments: US30, NAS100, US500, XAUUSD, BTCUSD, EURUSD (user-confirmed).
- Timeframes: M1 primary, M5 secondary. Single-TF analysis (no multi-TF confirmation mixing).
- Scalping style; entries occur inside micro-ranges ("barcode" chop), not only on clean swings.

## 3. Range: internal / external — [V/T]

- **R3.1 [V]:** At any time 4 lines exist: internal high/low + external high/low, derived from 2 opposite Majors.
- **R3.2 [T]:** If the opposite Major is not visible inside the current leg, step one extreme back to reveal it.
- **R3.3 [V]:** Merged line (internal == external within tolerance) → that side WILL be swept. No reversal
  entry into a merged line; expect the sweep.
- **R3.4 [T]:** Ranges are fractal/nested; redraw after a ceiling/floor is taken.
- **[G]:** The instructor's discretionary Major/Minor judgment is approximated in code by fractal pivots +
  break-of-structure (see `structure.py`). Wiper-vs-close edge cases unverified.

## 4. Equilibrium — [V]

- **R4.1 [V]:** 4 levels: fractal internal/external, leg internal/external.
- **R4.2 [V]:** External = Fib 50% of (leg start → consumption point), drawn as a horizontal ray extended right.
  Confirmed numerically: fib 19036.2 → 18895.0 ⇒ 0.5 = 18965.5, ray at ~18964.5.
- **R4.3 [V]:** Internal = Fib 50% of the F0 interior (falls back to the same 50% when unknown).
- **R4.4 [V]:** Overlap of internal + external 50% lines = keep the zone, discard the rest.
- **R4.5 [V]:** Untouched = magnet (must-see, «خط قطعی»); touched = balanced.
- **R4.6 [T]:** Expected path: come balanced → sit on balanced → leave toward the unbalanced target. A ceiling
  taken without prior equilibration forces a return to the leftover equilibrium.

## 5. Minor-Major — the permission — [V/T]

- **R5.1 [V]:** Floor validated by ≈ two bullish candles closing into/above each other (green + green closing
  above the prior high); mirrored for ceilings.
- **R5.2 [T]:** Break of the extreme + opposite close turns minor into major. No analysis before this permission.
- **R5.3 [T]:** Confirmation/entry must complete within **2 candles** of the touch; a 3-candle break = no entry.

## 6. Corresponding High/Low — entry model — [V/T]

- **R6.1 [T]:** From a Fractal-0 origin: first level forms on Minor-Major; opposite level forms WITHOUT price
  returning to the origin → the two levels "correspond".
- **R6.2 [V]:** Invalidation: (a) level revisited as Fractal-0 → that side dead (other side survives);
  (b) more than **2 closes** beyond the level → dead; doji/inside-bar closes are NOT counted;
  (c) a wick counts as a close (lower-TF equivalence).
- **R6.3 [V]:** Trigger: return to the level (not as F0, ≤2 closes) + Minor-Major confirmation within 2 candles →
  enter at that candle's close. Buy at Low, Sell at High.
- **R6.4 [T]:** Skip when the entry candle itself already reached the opposite side's TP1.
- **R6.5 [T]:** Escalation: a signal failing TP1 upgrades the next opposite signal ( Sell✗ → Buy stronger →
  next Sell strongest).
- **[G]:** Formal Fractal-0 identification from live flow is discretionary; code models an already-formed pair.

## 7. SL / TP / management — [V]

- **R7.1 [V]:** 1R = range height ≈ entry→SL distance (user-confirmed).
- **R7.2 [V]:** SL = level ± buffer; buffer = max(2×spread, 0.1×range) until the per-symbol point rule is set
  (BTC "1 point" does not transfer to indices/metals).
- **R7.3 [V]:** TP ladder (×R): 1, 3, 6, 9, 10, 18, 24, 40, 66, 90.
- **R7.4 [V]:** TP1 → move SL to breakeven. TP3 → close 30%, SL to entry. Hold remainder up the ladder.
- **R7.5 [T]:** Strong momentum through TP1 implies TP3; through TP3 implies TP6.

## 8. Filters — [V/T]

- **R8.1 [V]:** Candle-count filter: count leg candles (one consistent method) → digital root
  (18→9, 25→7) → even = balanced, odd = imbalanced. Verified from chart labels.
- **R8.2 [T]:** RSI divergence is an eye-aid only, never an entry. Best confluence: external divergence +
  equilibrium overlap ("super setup").
- **R8.3 [T]:** Max 2 one-sided steps; 3+ steps = regime change, reset counts.
- **R8.4 [T]:** One "preferred" trade per chart/day; skip mediocre first signals.
- **[G]:** The inter-leg "coefficient" (ضریب) formula was hinted, never revealed — not implemented.

## 9. Signal semantics & candle indexing | معنای سیگنال

- **R9.1:** All signals evaluate on **CLOSED candles only** (index shift 1). No intrabar confirmed signals.
  Rationale: entry is defined at a candle's close (R6.3); evaluating bar 0 would repaint.
- **R9.2:** Python reference and MQL5 indicator must emit identical (direction, bar time, level) triples on the
  same data — enforced by parity fixtures (Phase 4).
- **R9.3:** Buffers use EMPTY_VALUE for no-signal bars; a signal bar carries direction ±1 exactly once (no
  duplicates while the pair stays valid — first trigger wins).

## 10. Risk — [V/user]

- 0.5% per trade (user-confirmed). Max 3 trades/day, −1.0% daily stop (defaults in `.env.example`;
  transcripts contain no risk rules — these are user constraints, not instructor rules).
- No session/news filter in the source material — documented as user responsibility.

## 11. Testable requirements traceability

| Req | Python | MQL5 | Test |
|---|---|---|---|
| R3.3 merged→sweep | `RangeLines.merged_side` | input + buffer flag | `test_merged_side` + parity fixture |
| R4.2 fib-50 ray | `Equilibriums.from_leg` | 50% calc on F0 leg | `test_fib50_and_overlap` + parity |
| R5.1/R5.3 MM shape, 2-candle window | `is_*_minor_major`, `scan_trigger` | same logic | `test_minor_major_shapes`, `test_scan_trigger_buy` |
| R6.2 invalidation | `register_close`, `kill_as_f0` | same logic | `test_pair_invalidation_two_closes`, doji test |
| R7 ladder | `build_plan` | SL/TP level buffers | `test_build_plan_*` |
| R8.1 counting | `digital_root` | same | `test_digital_root_labels` |
| R9 closed-bar | closed-bar helper (Phase 3) | shift-1 | stability test (Phase 6) |
