# core/logger.py
from pathlib import Path
from utils.log import logger

def write_log(case_dir: Path, cmd: str, output: str, explanation: str, timestamp: str, max_lines: int = 20, dry_run: bool = False, output_hash: str = "") -> Path:
    safe_time = timestamp.replace(":", "-").replace(".", "-")
    logfile = case_dir / f"{safe_time}_command.log"

    if dry_run:
        preview = "[!] DRY RUN: the command wasn't executed."
    else:
        preview = "\n".join(output.strip().splitlines()[:max_lines])

    with logfile.open("w", encoding="utf-8") as f:
        f.write(f"# [+] Timestamp: {timestamp}\n")
        f.write(f"## [+] Case: {case_dir.name}\n\n")
        f.write(f"### [+] Command:\n`{cmd}`\n\n")
        f.write("### [+] Output excerpt (number of lines as in config):\n```\n")
        f.write(preview)
        f.write("\n```\n\n")
        f.write(f"### [+] Explanation:\n{explanation}\n\n")
        f.write(f"### [+] SHA256 Output Hash:\n`{output_hash}`\n")
        logger.info(f"Log written to: {logfile}")

    return logfile



