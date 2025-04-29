# utils/pathing.py

from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parents[1]

@lru_cache()
def get_config_path(filename="config.yaml"):
    return BASE_DIR / "config" / filename

@lru_cache()
def get_template_path(filename="legal.md.j2"):
    return BASE_DIR / "templates" / filename

@lru_cache()
def get_log_dir():
    path = BASE_DIR / "logs"
    try:
        path.mkdir(exist_ok=True)
    except OSError as e:
        # Handle the error, e.g., log it or raise a custom exception
        print(f"Error creating directory: {e}")
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
