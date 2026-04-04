from pathlib import Path
import subprocess
import re
import yaml
from core.hasher import compute_hash
from utils.log import logger
from utils.shared_config import load_config
from utils.pathing import get_case_log_path, get_log_dir

config = load_config()


def analyze_case(case):
    case_dir = get_case_log_path(case)
    if not case_dir.exists():
        logger.error(f"Case {case} does not exist")
        return

    log_files = list(case_dir.glob("*.log"))
    sig_files = list(case_dir.glob("*.log.sig"))

    logger.info(f"Analysis of case: {case} — {len(log_files)} logfile(s) found")
    for f in log_files:
        logger.info(f"  - {f.name}")

    if sig_files:
        logger.info("Signatures found:")
        for f in sig_files:
            logger.info(f"  - {f.name}")
    else:
        logger.warning("No signatures found.")


def extract_block(lines, label="Output excerpt"):
    label_variants = [
        label,
        "Output excerpt",
        "Output preview",
        "Output section",
    ]

    try:
        start = next(
            i for i, l in enumerate(lines)
            if any(variant.lower() in l.lower() for variant in label_variants)
        )

        start_block = next(
            i for i in range(start, len(lines))
            if lines[i].strip().startswith("```")
        )

        end_block = next(
            i for i in range(start_block + 1, len(lines))
            if lines[i].strip().startswith("```")
        )

        return "\n".join(lines[start_block + 1:end_block]).strip()
    except StopIteration:
        return "[!] Output not found."


def extract_explanation(lines):
    header_patterns = [
        "### [+] Erklärung",
        "### [+] Legal Context",
    ]
    try:
        start = next(
            i for i, l in enumerate(lines)
            if any(header.lower() in l.lower() for header in header_patterns)
        )
        end = next(
            (i for i in range(start + 1, len(lines)) if lines[i].startswith("###")),
            len(lines)
        )
        return "\n".join(lines[start + 1:end]).strip()
    except StopIteration:
        return "[!] Explanation not found."


def generate_report(case, verify=True):
    logger.info(f"Generating report for case: {case}")

    case_dir = get_case_log_path(case)
    if not case_dir.exists():
        logger.error(f"Case {case} does not exist")
        return

    description_file = case_dir / "description.txt"
    description = "*No description found.*"
    if description_file.exists():
        desc_lines = description_file.read_text().splitlines()
        description = next((l for l in desc_lines if "Description:" in l), "").replace("Description:", "").strip()

    report_lines = [f"# [++] Forensic report of case: {case}\n", f"## [++] Description\n{description}\n"]

    log_files = sorted(case_dir.glob("*.log"))
    if not log_files:
        logger.warning(f"No log files found in {case_dir}")
        return

    report_lines.append("\n## [++] Timeline of Commands and Comments\n")

    for log_file in log_files:
        sig_file = log_file.with_suffix(log_file.suffix + ".sig")
        timestamp = log_file.stem.split("_")[0]

        log_text = log_file.read_text()
        lines = log_text.splitlines()

        meta_file = log_file.with_suffix(".meta.json")

        if log_file.name.endswith("_command.log"):
            cmd = "*Unknown*"
            sha = "*Not found*"

            if meta_file.exists():
                import json
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                cmd = meta.get("command", cmd)
                sha = meta.get("output_hash", sha)
            else:
                for i, line in enumerate(lines):
                    if "Command" in line:
                        for offset in range(1, 4):
                            if i + offset < len(lines):
                                content_line = lines[i + offset].strip()
                                if "`" in content_line:
                                    matches = re.findall(r"`(.*?)`", content_line)
                                    if matches:
                                        cmd = matches[0]
                                        break
                                elif content_line:
                                    cmd = content_line
                                    break
                        if cmd == "*Unknown*":
                            logger.warning(f"No valid command found after 'Command:' in {log_file.name} (line {i})")

                    elif "### [+] SHA256 Output Hash:" in line:
                        for offset in range(1, 4):
                            if i + offset < len(lines):
                                content_line = lines[i + offset].strip()
                                matches = re.findall(r"`(.*?)`", content_line)
                                if matches:
                                    sha = matches[0]
                                    break
                        if sha == "*Not found*":
                            logger.warning(f"No SHA256 hash found after 'SHA256 Output Hash' in {log_file.name} (line {i})")

            output_lines = extract_block(lines, "### [+] Output")
            output_excerpt = output_lines if isinstance(output_lines, str) else "\n".join(output_lines)
            from core.legalizer import get_legal_explanation
            explanation = get_legal_explanation(cmd)

            sig_status = "[!] Not Signed"
            if verify and sig_file.exists():
                try:
                    subprocess.run(["gpg", "--verify", str(sig_file)], capture_output=True, check=True)
                    sig_status = "[+] Valid"
                except subprocess.CalledProcessError:
                    sig_status = "[x] Invalid"
            elif sig_file.exists():
                sig_status = "[+] (not checked)"

            report_lines.append(f"### [+] Command: `{cmd}`")
            report_lines.append(f"- Timestamp: `{timestamp}`")
            report_lines.append(f"- GPG-signature: {sig_status}")
            report_lines.append(f"- SHA256: `{sha}`\n")
            report_lines.append(f"#### Output:\n```shell\n{output_excerpt}\n```\n")

            if "[DRY RUN]" in output_excerpt:
                report_lines.append("[!] This command was logged in dry-run mode and NOT executed.\n")

            report_lines.append(f"#### Context:\n{explanation}\n")
            report_lines.append("---\n")

        elif log_file.name.endswith("_comment.log"):
            report_lines.append(f"### [+] Timestamp: `{timestamp}`")
            report_lines.append(log_text)
            report_lines.append("---\n")

    report_lines.append("\n## [+] GPG-Overview")
    report_lines.append("Each `.log`-file was digitally signed with GPG where applicable.")
    report_lines.append("The signature status is documented per command.\n")

    report_path = case_dir / f"{case}_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    logger.info(f"Report written to: {report_path}")


def verify_output(case):
    case_dir = get_case_log_path(case)
    if not case_dir.exists():
        logger.error(f"Case {case} does not exist")
        return

    logger.info(f"Verifying output integrity for case: {case}")
    for log_file in sorted(case_dir.glob("*.log")):
        lines = log_file.read_text().splitlines()
        expected_hash = None
        for i, line in enumerate(lines):
            if "### [+] SHA256 Output Hash:" in line and i + 1 < len(lines):
                if "`" in lines[i + 1]:
                    match = re.findall(r"`(.*?)`", lines[i + 1])
                    if match:
                        expected_hash = match[0]

        output_lines = extract_block(lines, "### [+] Output excerpt")
        cleaned = "\n".join([line.rstrip() for line in output_lines]).strip()
        hash_algo = config.get("output", {}).get("hash_algorithm", "sha256")
        actual_hash = compute_hash(cleaned, algorithm=hash_algo)
        result = "[+] OK" if actual_hash == expected_hash else "[x] Mismatch"
        logger.info(f"{log_file.name}: {result} — expected={expected_hash} actual={actual_hash}")


def list_case_folders():
    cases = [d.name for d in get_log_dir().iterdir() if d.is_dir()]
    if not cases:
        logger.warning("No cases found.")
    else:
        logger.info("Existing cases:")
        for c in cases:
            logger.info(f"  - {c}")


def show_case_description(case: str):
    desc_file = get_case_log_path(case) / "description.txt"
    if not desc_file.exists():
        logger.warning("No case description found.")
        return

    content = desc_file.read_text()
    logger.info(f"Description of case {case}:\n\n{content}")
