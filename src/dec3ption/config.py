"""Environment-based configuration.

All user-tunable values live in the project's `.env` file (see `.env.example`).
تمام مقادیر قابل‌تنظیم کاربر در فایل `.env` پروژه قرار دارد.

Usage:
    from dec3ption.config import Settings
    settings = Settings.from_env()  # reads .env in project root, then os.environ
    settings.validate()
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is a hard requirement
    def load_dotenv(*args, **kwargs):  # type: ignore
        return False


def _parse_csv(value: str) -> tuple[str, ...]:
    return tuple(p.strip() for p in value.split(",") if p.strip())


def _parse_float_csv(value: str) -> tuple[float, ...]:
    return tuple(float(p.strip()) for p in value.split(",") if p.strip())


SUPPORTED_TIMEFRAMES = ("M1", "M5", "M15", "H1", "H4", "D1")


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings loaded from `.env` / environment."""

    mt5_path: Path
    mt5_data_folder: Path | None = None
    mt5_login: int | None = None
    mt5_password: str | None = None
    mt5_server: str | None = None
    mt5_timeout_ms: int = 60000
    symbols: tuple[str, ...] = ("BTCUSD",)
    timeframes: tuple[str, ...] = ("M1",)
    risk_pct: float = 0.5
    max_daily_loss_pct: float = 1.0
    max_trades_per_day: int = 3
    buffer_spread_mult: float = 2.0
    buffer_range_fraction: float = 0.1
    tp_ladder: tuple[float, ...] = (1.0, 3.0, 6.0, 9.0, 10.0, 18.0)
    tp1_move_to_breakeven: bool = True
    tp3_partial_close_pct: float = 30.0
    magic_number: int = 32026
    dry_run: bool = True

    # -- derived helpers -------------------------------------------------
    def buffer_size(self, spread: float, range_height: float) -> float:
        """Buffer = max(spread_mult * spread, range_fraction * range_height).

        بافر = بیشترِ (ضریب × اسپرد، کسر × ارتفاع رنج). واحد: قیمت (price units).
        """
        return max(self.buffer_spread_mult * spread,
                   self.buffer_range_fraction * range_height)

    def tp_price(self, entry: float, risk_distance: float, multiple: float,
                 direction: int) -> float:
        """Target price for a ladder multiple. direction: +1 long, -1 short.

        قیمت تارگت برای مضرب نردبان. جهت: ‎+1‎ لانگ، ‎−1‎ شورت.
        """
        return entry + direction * risk_distance * multiple

    # -- loading / validation --------------------------------------------
    @classmethod
    def from_env(cls, env_file: Path | str | None = None) -> "Settings":
        """Load settings; explicit env vars always win over the `.env` file."""
        if env_file is None:
            env_file = Path(__file__).resolve().parents[2] / ".env"
        else:
            env_file = Path(env_file)
        if env_file.exists():
            load_dotenv(dotenv_path=env_file)

        get = os.environ.get
        login = (get("MT5_LOGIN") or "").strip()
        return cls(
            mt5_path=Path(get("MT5_PATH", "")),
            mt5_data_folder=Path(get("MT5_DATA_FOLDER")) if get("MT5_DATA_FOLDER") else None,
            mt5_login=int(login) if login else None,
            mt5_password=get("MT5_PASSWORD") or None,
            mt5_server=get("MT5_SERVER") or None,
            mt5_timeout_ms=int(get("MT5_TIMEOUT_MS", "60000")),
            symbols=_parse_csv(get("SYMBOLS", "BTCUSD")),
            timeframes=_parse_csv(get("TIMEFRAMES", "M1")),
            risk_pct=float(get("RISK_PCT", "0.5")),
            max_daily_loss_pct=float(get("MAX_DAILY_LOSS_PCT", "1.0")),
            max_trades_per_day=int(get("MAX_TRADES_PER_DAY", "3")),
            buffer_spread_mult=float(get("BUFFER_SPREAD_MULT", "2.0")),
            buffer_range_fraction=float(get("BUFFER_RANGE_FRACTION", "0.1")),
            tp_ladder=_parse_float_csv(get("TP_LADDER", "1,3,6,9,10,18")),
            tp1_move_to_breakeven=(get("TP1_MOVE_TO_BREAKEVEN", "true").lower() == "true"),
            tp3_partial_close_pct=float(get("TP3_PARTIAL_CLOSE_PCT", "30.0")),
            magic_number=int(get("MAGIC_NUMBER", "32026")),
            dry_run=(get("DRY_RUN", "true").lower() == "true"),
        )

    def validate(self) -> None:
        """Raise ValueError on any invalid setting. تمام تنظیمات را اعتبارسنجی می‌کند."""
        errors: list[str] = []
        if str(self.mt5_path).strip() in ("", "."):
            errors.append("MT5_PATH is empty")
        if not self.symbols:
            errors.append("SYMBOLS is empty")
        if not self.timeframes:
            errors.append("TIMEFRAMES is empty")
        for tf in self.timeframes:
            if tf not in SUPPORTED_TIMEFRAMES:
                errors.append(f"Unsupported TIMEFRAME: {tf} (supported: {SUPPORTED_TIMEFRAMES})")
        if not (0 < self.risk_pct <= 100):
            errors.append(f"RISK_PCT out of range: {self.risk_pct}")
        if not (0 < self.max_daily_loss_pct <= 100):
            errors.append(f"MAX_DAILY_LOSS_PCT out of range: {self.max_daily_loss_pct}")
        if self.max_trades_per_day < 1:
            errors.append(f"MAX_TRADES_PER_DAY must be >= 1: {self.max_trades_per_day}")
        if not self.tp_ladder or any(m <= 0 for m in self.tp_ladder):
            errors.append(f"TP_LADDER must be positive multiples: {self.tp_ladder}")
        if not (0 < self.tp3_partial_close_pct <= 100):
            errors.append(f"TP3_PARTIAL_CLOSE_PCT out of range: {self.tp3_partial_close_pct}")
        if errors:
            raise ValueError("Invalid settings: " + "; ".join(errors))
