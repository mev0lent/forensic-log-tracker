# shared_config.py
import yaml
from functools import lru_cache

@lru_cache()
def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
