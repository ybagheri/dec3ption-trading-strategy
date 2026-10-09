# OPEN QUESTIONS | سؤالات باز

Rules that are NOT defined precisely in the transcripts/spec. Code marks them `SPEC-GAP`.
قوانینی که در متن‌ها دقیق تعریف نشده‌اند؛ در کد با `SPEC-GAP` علامت خورده‌اند.

- **Q-RANGE-NESTING** — `detect_range`: internal = last two majors, external = previous two. This does not
  guarantee "internal inside external". Needs a worked chart example of how the external range is chosen.
- **Q-LEG-EQ** — leg (time) equilibrium internal/external: drawing procedure never revealed (II.4). Left `None`.
- **Q-MM-DEF** — Minor-Major definition. Implemented: two same-colour candles, 2nd closes beyond 1st extreme.
  Transcript II.2 also gives: pivot confirmed by two opposite candles each closing beyond the previous, OR one
  opposite candle whose extreme takes the previous candle's extreme (equal counts). To be made pluggable (Phase 2).
- **Q-F0** — exact Fractal-0 definition and "consumption" criteria.
- **Q-FIRST-TOUCH** — does a level survive after its first touch/trade, or is it spent? Current code can signal
  again on later touches.
- **Q-SPREAD-BAR** — adaptive buffer parity: Python uses a constant spread; MQL5 can use per-bar spread.
