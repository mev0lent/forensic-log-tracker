# utils/shared_config.py
import yaml
from functools import lru_cache
from zoneinfo import ZoneInfo  # Requires Python 3.9+

@lru_cache()
def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Add derived runtime values
    tz_name = cfg.get("project", {}).get("timezone", "UTC")
    cfg["TIMEZONE"] = ZoneInfo(tz_name)

    return cfg
