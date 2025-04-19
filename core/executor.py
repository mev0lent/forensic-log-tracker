# core/executor.py
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import yaml
from core.hasher import compute_hash
from core.logger import write_log
from core.legalizer import get_legal_explanation
from utils.log import logger
from utils.shared_config import load_config

config = load_config()


def execute_command(cmd: str, case: str, dry_run: bool = False):
    timestamp = datetime.now(timezone.utc).isoformat()
    case_dir = Path(f"logs/{case}")
    case_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Executing command: {cmd}")
    if dry_run:
        output = "[!] DRY RUN: Command not executed."
    else:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"[!] Command failed:\n{e.stderr}"

    explanation = get_legal_explanation(" ".join(cmd.split()[:4]))
    preview_lines = config["output"].get("preview_lines", config["default_output_lines"])
    hash_algo = config["output"].get("hash_algorithm", "sha256")
    output_hash = compute_hash(output, hash_algo)

    logfile = write_log(case_dir, cmd, output, explanation, timestamp, preview_lines, dry_run, output_hash)
    return logfile