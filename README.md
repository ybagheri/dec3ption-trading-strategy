# Dec3ption Trading Strategy Engine | موتور معاملاتی استراتژی دک‌سپشن

Python engine implementing the **Group II** trading strategy (RTM-rooted, range + equilibrium + corresponding
high/low), executable against **MetaTrader 5**.
موتور پایتونی پیاده‌سازی استراتژی معاملاتی **گروه دوم**، قابل اجرا روی **متاتریدر ۵**.

- Strategy spec (bilingual, precise): [`docs/STRATEGY.md`](docs/STRATEGY.md) | مشخصات دقیق استراتژی (دوزبانه)
- Plan: [`ROADMAP.md`](ROADMAP.md) | نقشه‌ی راه
- Continuity notes: [`HANDOFF.md`](HANDOFF.md) | یادداشت تحویل فاز

## Quickstart | شروع سریع

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env   # then edit your values | سپس مقادیر خود را ویرایش کنید
pytest
```

```python
from dec3ption.config import Settings
from dec3ption.mt5_client import MT5Client

settings = Settings.from_env()  # reads .env | خواندن فایل
settings.validate()
with MT5Client(settings) as client:
    df = client.fetch_rates("BTCUSD", "M1", 500)
```

> ⚠️ `DRY_RUN=true` by default — no live orders are ever sent unless you explicitly disable it.
> به‌صورت پیش‌فرض در حالت شبیه‌سازی است و سفارش واقعی ارسال نمی‌شود.

## Layout | ساختار

```
src/dec3ption/      engine (config, mt5_client, strategy/...)
tests/              pytest suite (runs without a terminal)
MQL5/Indicators/    native MT5 custom indicator
scripts/            deploy + historical validation
results/            Phase-6 validation output (read me first: small sample)
docs/STRATEGY.md    bilingual strategy narrative
docs/STRATEGY_SPECIFICATION.md  testable rules contract
docs/PROJECT_AUDIT.md / ARCHITECTURE.md / TESTING.md
.env                your private settings (never committed)
```

## Indicator (MT5) | اندیکاتور متاتریدر

1. Deploy (backup-safe): `powershell -File scripts\deploy_indicator.ps1`
2. Compile: MetaEditor → open the deployed `.mq5` → F7 (0 errors/0 warnings verified 2026-10-09).
3. Load: Navigator → Indicators → Dec3ptionTradingStrategy → drag onto an M1/M5 chart.
4. Inputs: `InpBufferPoints` (SL buffer in points), `InpMaxCloses`, `InpLookback`.
5. Arrows = confirmed signals on closed candles (non-repainting); dashed rays = SL/TP1.

## Historical validation
`python scripts\historical_validation.py` → `results/` (R-multiple metrics;
see `results/README.md` for limitations — no spread, small sample, no walk-forward).

