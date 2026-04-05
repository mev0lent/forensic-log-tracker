# utils/pathing.py

import shutil
import importlib.resources
from pathlib import Path

_USER_CONFIG_DIR = Path.home() / ".config" / "forensic-log-tracker"

_BUNDLED = [
    ("config/config.yaml",       "config.yaml"),
    ("config/explanations.yaml", "explanations.yaml"),
    ("templates/legal.md.j2",    "templates/legal.md.j2"),
]

_bootstrapped = False


def _bootstrap():
    global _bootstrapped
    if _bootstrapped:
        return

    _USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    (_USER_CONFIG_DIR / "templates").mkdir(exist_ok=True)

    pkg = importlib.resources.files("forensic_log_tracker")
    initialized = []

    for bundled_rel, user_rel in _BUNDLED:
        dest = _USER_CONFIG_DIR / user_rel
        if not dest.exists():
            shutil.copy2(str(pkg.joinpath(bundled_rel)), dest)
            initialized.append(user_rel)

    if initialized:
        print(f"\n[+] flt: config initialized at {_USER_CONFIG_DIR}")
        print(f"    Edit config.yaml to set your analyst name and preferences.\n")

    _bootstrapped = True


def get_config_path(filename="config.yaml") -> Path:
    _bootstrap()
    return _USER_CONFIG_DIR / filename


def get_template_path(filename="legal.md.j2") -> Path:
    _bootstrap()
    return _USER_CONFIG_DIR / "templates" / filename


def get_log_dir() -> Path:
    path = Path.cwd() / "logs"
    path.mkdir(exist_ok=True)
    return path


def get_case_log_path(case_id: str, create: bool = False) -> Path:
    path = get_log_dir() / case_id
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def get_output_path() -> Path:
    path = Path.cwd() / "output"
    path.mkdir(exist_ok=True)
    return path
