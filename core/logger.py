# core/logger.py
from pathlib import Path

def write_log(case_dir: Path, cmd: str, output: str, explanation: str, output_hash: str, timestamp: str, max_lines: int = 20) -> Path:
    safe_time = timestamp.replace(":", "-").replace(".", "-") # Zwei Logs pro Sekunde möglich
    logfile = case_dir / f"{safe_time}_command.log"

    with logfile.open("w", encoding="utf-8") as f:
        f.write(f"# 🕒 {timestamp}\n")
        f.write(f"## 🧪 Fall: {case_dir.name}\n\n")
        f.write(f"### 🧩 Befehl:\n`{cmd}`\n\n")
        f.write("### 📤 Output (Auszug):\n```\n")
        f.write("\n".join(output.strip().splitlines()[:max_lines]))
        f.write("\n```\n\n")
        f.write(f"### 🧾 Erklärung:\n{explanation}\n\n")
        f.write(f"### 🔐 SHA256 Output Hash:\n`{output_hash}`\n")

    return logfile

