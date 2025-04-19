# utils/log.py
import logging
import yaml
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Fallback default
log_level = "INFO"

# Try reading config.yaml
try:
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        log_level = config.get("logging", {}).get("level", "INFO").upper()
except Exception:
    print("[!] Failed to load logging config from config.yaml. Using default INFO level.")

# Setup logger
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "tracker.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("forensic_tracker")
