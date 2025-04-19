# core/logger.py
from pathlib import Path

def write_log(case_dir: Path, cmd: str, output: str, explanation: str, timestamp: str, max_lines: int = 20, dry_run: bool = False) -> Path:
    safe_time = timestamp.replace(":", "-").replace(".", "-")
    logfile = case_dir / f"{safe_time}_command.log"

    if dry_run:
        preview = "[!] DRY RUN: the command wasn't executed."
    else:
        preview = "\n".join(output.strip().splitlines()[:max_lines])

    # 🔐 Hier den Hash vom Preview erzeugen (nicht vom kompletten Output)
    from hashlib import sha256
    output_hash = sha256(preview.encode("utf-8")).hexdigest()

    with logfile.open("w", encoding="utf-8") as f:
        f.write(f"# [+] Timestamp: {timestamp}\n")
        f.write(f"## [+] Case: {case_dir.name}\n\n")
        f.write(f"### [+] Command:\n`{cmd}`\n\n")
        f.write("### [+] Output excerpt (number of lines as in config):\n```\n")
        f.write(preview)
        f.write("\n```\n\n")
        f.write(f"### [+] Explanation:\n{explanation}\n\n")
        f.write(f"### [+] SHA256 Output Hash:\n`{output_hash}`\n")

    return logfile



