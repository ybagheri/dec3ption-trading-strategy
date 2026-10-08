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
docs/STRATEGY.md    bilingual strategy specification
.env                your private settings (never committed)
```
