# Führt Befehle aus und loggt alles

# core/executor.py
import subprocess
from datetime import datetime
from pathlib import Path
import yaml

from core.logger import write_log
from core.legalizer import get_legal_explanation
from core.hasher import sha256_from_string

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_manifest(case_dir: Path, files_with_hashes: dict, manifest_name: str):
    manifest_file = case_dir / manifest_name
    with open(manifest_file, "w", encoding="utf-8") as f:
        for file, hash_val in files_with_hashes.items():
            f.write(f"{hash_val}  {file}\n")

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

    output_hash = sha256_from_string(output)
    explanation = get_legal_explanation(cmd.split()[0])

    logfile = write_log(case_dir, cmd, output, explanation, output_hash, timestamp, config["default_output_lines"])

    # SHA256-MANIFEST aktualisieren
    files_with_hashes = {logfile.name: sha256_from_string(Path(logfile).read_text(encoding="utf-8"))}
    write_manifest(case_dir, files_with_hashes, config["manifest_name"])
