# core/executor.py
import subprocess
import platform
from datetime import datetime, timezone
from pathlib import Path
import yaml
from core.hasher import compute_hash
from core.logger import write_log
from core.legalizer import get_legal_explanation
from utils.log import logger
from utils.shared_config import load_config
from utils.pathing import get_case_log_path
config = load_config()


def execute_command(cmd: str, case: str, dry_run: bool = False):
    from datetime import datetime
    from pathlib import Path
    import subprocess
    import platform

    timestamp = datetime.now(config["TIMEZONE"]).isoformat()
    case_dir = get_case_log_path(case, create=False)

    logger.info(f"Executing command: {cmd}")

    if dry_run:
        output = "[!] DRY RUN: Command not executed."
    else:
        try:
            # Check if we're on Windows or Linux
            if platform.system() == "Windows":
                # Use PowerShell on Windows
                result = subprocess.run(
                    ["powershell", "-Command", cmd],
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                # Use bash on Linux/Unix, without the -i flag to avoid interactive mode
                result = subprocess.run(
                    ["bash", "-c", cmd],
                    capture_output=True,
                    text=True,
                    check=True
                )
            output = f"[STDOUT]\n{result.stdout}\n[STDERR]\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            output = f"[!] Command failed:\n{e.stderr}"

    explanation = get_legal_explanation(" ".join(cmd.split()[:4]))
    preview_lines = config.get("output", {}).get("preview_lines", 20)
    hash_algo = config["output"].get("hash_algorithm", "sha256")
    output_hash = compute_hash(output, hash_algo)

    logfile = write_log(case_dir, cmd, output, explanation, timestamp, preview_lines, dry_run, output_hash)
    return logfile, output
