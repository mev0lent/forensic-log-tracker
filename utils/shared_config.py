# utils/shared_config.py
import yaml
from functools import lru_cache
from zoneinfo import ZoneInfo  # Requires Python 3.9+
from pathlib import Path

@lru_cache()
def load_config():
    base_path = Path(__file__).resolve().parent.parent  # Go from utils/ to project root
    config_path = base_path / "config" / "config.yaml"

    with config_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Add derived runtime values
    tz_name = cfg.get("project", {}).get("timezone", "UTC")
    cfg["TIMEZONE"] = ZoneInfo(tz_name)

    return cfg

