# TESTING | تست

Five distinct categories — passing one proves nothing about the others:
۱) Python unit tests ۲) MQL5 source validation ۳) MetaEditor compilation ۴) MT5 execution ۵) Backtest.

## 1) Python unit tests
```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```
27 tests, no terminal required. Regression tests pin every audit fix (tolerance kill, closed bars,
R6.4 skip, TF validation). Note: on this machine set `$env:TMP` to a writable dir — the global Temp
symlink cleanup raises a benign `PermissionError` at session finish (results unaffected).

## 2–4) MQL5 / compilation / execution — see Phase 4–5 sections when added.
## 5) Backtest — Phase 6.
