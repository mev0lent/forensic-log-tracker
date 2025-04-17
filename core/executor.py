# core/executor.py
import subprocess
from datetime import datetime
from pathlib import Path
import yaml
import hashlib
from core.logger import write_log
from core.legalizer import get_legal_explanation

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def sha256_from_string(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def execute_command(cmd: str, case: str):
    config = load_config()
    timestamp = datetime.utcnow().isoformat()
    case_dir = Path(f"logs/{case}")
    case_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"[ERROR] Command failed:\n{e.stderr}"

    output_hash = sha256_from_string(output) if config["output"].get("include_sha256", True) else ""

    first_segment = " ".join(cmd.split()[:4])
    explanation = get_legal_explanation(first_segment)

    preview_lines = config["output"].get("preview_lines", config["default_output_lines"])
    logfile = write_log(case_dir, cmd, output, explanation, output_hash, timestamp, preview_lines)
    return logfile
