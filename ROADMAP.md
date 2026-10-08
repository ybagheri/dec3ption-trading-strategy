# ROADMAP | نقشه‌ی راه

Rule: at the end of EVERY phase → complete + update `HANDOFF.md` → commit → push.
قانون: پایان هر فاز ← تکمیل و به‌روزرسانی `HANDOFF.md` ← کامیت ← پوش.

- [x] **Phase 1 — Scaffold / زیرساخت**
  `.env` config (`Settings`), `MT5Client` bridge (dry-run safe), pytest suite, README/ROADMAP/HANDOFF,
  `docs/STRATEGY.md` (bilingual spec).
- [ ] **Phase 2 — Strategy rules engine / موتور قوانین**
  `Range`, `Equilibrium` (fractal/leg × int/ext), `CorrespondingPair`, candle-count digital-root filter,
  TP-ladder + SL/buffer calculator, checklist evaluator. Unit tests on synthetic candles.
- [ ] **Phase 3 — Live loop / حلقه‌ی زنده**
  Watch loop over `SYMBOLS × TIMEFRAMES`, signal → risk-sized order via `MT5Client`, TP1-BE / TP3-30% management,
  daily-loss guard, journal CSV.
- [ ] **Phase 4 — Backtest / بک‌تست**
  Offline replay on MT5 history export, metrics (win-rate, expectancy, max drawdown), report.
- [ ] **Phase 5 — Harden / مقاوم‌سازی**
  Logging, alerts, MQL5 EA bridge (optional), multi-symbol risk budgeting.
