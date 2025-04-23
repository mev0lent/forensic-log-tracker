# utils/pathing.py

from pathlib import Path
from functools import lru_cache
import os

# Path to persistent environment config file
FLT_ENV_PATH = Path.home() / ".flt_env"

# Attempt to load FLT_REPO from the config file
BASE_DIR = None

if FLT_ENV_PATH.exists():
    env_lines = FLT_ENV_PATH.read_text().splitlines()
    for line in env_lines:
        if line.startswith("FLT_REPO="):
            BASE_DIR = Path(line.split("=", 1)[1].strip().strip('"'))
            break

# Validate that BASE_DIR is usable
if not BASE_DIR or not BASE_DIR.exists():
    raise RuntimeError("❌ FLT_REPO is not set correctly in ~/.flt_env. Please run setup.sh to configure the project path.")

# Paths used throughout the app
@lru_cache()
def get_config_path(filename="config.yaml"):
    return BASE_DIR / "config" / filename

@lru_cache()
def get_template_path(filename="legal.md.j2"):
    return BASE_DIR / "templates" / filename

@lru_cache()
def get_log_dir():
    path = BASE_DIR / "logs"
    path.mkdir(exist_ok=True)
    return path

def get_case_log_path(case_id: str, create: bool = False) -> Path:
    path = get_log_dir() / case_id
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path

@lru_cache()
def get_output_path() -> Path:
    path = BASE_DIR / "output"
    path.mkdir(exist_ok=True)
    return path
