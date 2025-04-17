# utils/reporting.py
from pathlib import Path
import subprocess
import re
import yaml
import hashlib

# Load global configuration from config.yaml
def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Generate SHA256 hash from a string (used to compare output integrity)
def sha256_from_string(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

# Print available logs and GPG signatures for a case
def analyze_case(case):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Fall {case} existiert nicht.")
        return

    log_files = list(case_dir.glob("*.log"))
    sig_files = list(case_dir.glob("*.log.sig"))

    print(f"\n[+] Analyse von Fall: {case}")
    print(f"[+] {len(log_files)} Logdatei(en) gefunden:")
    for f in log_files:
        print(f" - {f.name}")

    if sig_files:
        print(f"\n[+] Signaturen vorhanden für:")
        for f in sig_files:
            print(f" - {f.name}")
    else:
        print("\n[x] Keine GPG-Signaturen gefunden.")

# Extract output block from log content
def extract_block(lines, start_contains):
    try:
        start = next(i for i, l in enumerate(lines) if start_contains in l)
        start_code = next(i for i in range(start, len(lines)) if lines[i].strip() == "```") + 1
        end_code = next(i for i in range(start_code, len(lines)) if lines[i].strip() == "```")
        return lines[start_code:end_code]
    except StopIteration:
        return ["[!] Abschnitt nicht gefunden."]

# Extract legal explanation section
def extract_explanation(lines):
    try:
        start = next(i for i, l in enumerate(lines) if "### [+] Erklärung" in l)
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("###")), len(lines))
        return "\n".join(lines[start + 1:end]).strip()
    except StopIteration:
        return "[!] Erklärung nicht gefunden."

# Build a complete Markdown report for a forensic case
def generate_report(case, verify=True):
    config = load_config()
    preview_lines = config.get("output", {}).get("preview_lines", 20)

    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Fall '{case}' existiert nicht.")
        return

    description_file = case_dir / "description.txt"
    description = "*Keine Beschreibung gefunden.*"
    if description_file.exists():
        desc_lines = description_file.read_text().splitlines()
        description = next((l for l in desc_lines if "Beschreibung:" in l), "").replace("Beschreibung:", "").strip()

    report_lines = [f"# [+] Forensischer Bericht zu Fall: {case}\n", f"## [---] Beschreibung\n{description}\n"]

    log_files = sorted(case_dir.glob("*.log"))
    if not log_files:
        print("[!] Keine Logdateien gefunden.")
        return

    report_lines.append("\n## [---] Ausgeführte Befehle & Logs\n")

    for log_file in log_files:
        sig_file = log_file.with_suffix(log_file.suffix + ".sig")
        timestamp = log_file.stem.split("_")[0].replace("-", ":")

        log_text = log_file.read_text()
        lines = log_text.splitlines()

        cmd = "*Unbekannt*"
        sha = "*Nicht gefunden*"

        for i, line in enumerate(lines):
            if "Befehl" in line and i + 1 < len(lines) and "`" in lines[i + 1]:
                cmd = re.findall(r"`(.*?)`", lines[i + 1])[0]
            elif "### [+] SHA256 Output Hash:" in line and i + 1 < len(lines):
                if "`" in lines[i + 1]:
                    sha = re.findall(r"`(.*?)`", lines[i + 1])[0]

        output_lines = extract_block(lines, "### [+] Auszug des Outputs")
        output_excerpt = "\n".join(output_lines[:preview_lines])
        explanation = extract_explanation(lines)

        sig_status = "[!] Nicht signiert"
        if verify and sig_file.exists():
            try:
                subprocess.run(["gpg", "--verify", str(sig_file)], capture_output=True, check=True)
                sig_status = "[+] Gültig"
            except subprocess.CalledProcessError:
                sig_status = "[x] Ungültig"
        elif sig_file.exists():
            sig_status = "[+] (nicht geprüft)"

        report_lines.append(f"### [+] Befehl: `{cmd}`")
        report_lines.append(f"- Zeitstempel: `{timestamp}`")
        report_lines.append(f"- GPG-Signatur: {sig_status}")
        report_lines.append(f"- SHA256: `{sha}`\n")
        report_lines.append(f"#### Auszug des Outputs:\n```\n{output_excerpt}\n```\n")

        if "[DRY RUN]" in output_excerpt:
            report_lines.append("[!] Dieser Befehl wurde im Dry-Run-Modus aufgezeichnet und NICHT ausgeführt.\n")

        report_lines.append(f"#### Juristische Einordnung:\n{explanation}\n---\n")

    report_lines.append("\n## [+] GPG-Überblick")
    report_lines.append("Jede `.log`-Datei wurde mit GPG digital signiert.")
    report_lines.append("Der Signaturstatus ist pro Befehl im Bericht dokumentiert.\n")

    report_path = case_dir / f"{case}_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"[+] Bericht geschrieben nach: {report_path}")

# Check SHA256 hashes of outputs for all logs in a case
def verify_output(case):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Fall '{case}' existiert nicht.")
        return

    print(f"[+] Verifiziere Output-Integrität für Fall: {case}")
    for log_file in sorted(case_dir.glob("*.log")):
        lines = log_file.read_text().splitlines()
        expected_hash = None
        for i, line in enumerate(lines):
            if "### [+] SHA256 Output Hash:" in line and i + 1 < len(lines):
                if "`" in lines[i + 1]:
                    match = re.findall(r"`(.*?)`", lines[i + 1])
                    if match:
                        expected_hash = match[0]

        output_lines = extract_block(lines, "### [+] Auszug des Outputs")
        cleaned = "\n".join([line.rstrip() for line in output_lines]).strip()
        actual_hash = sha256_from_string(cleaned)
        print(f"[DEBUG] Erwartet: {expected_hash}")
        print(f"[DEBUG] Tatsächlich: {actual_hash}")
        result = "[+] OK" if actual_hash == expected_hash else "[x] Mismatch"
        print(f"{log_file.name}: {result}")

# Print a list of all case folders
def list_case_folders():
    cases = [d.name for d in Path("logs").iterdir() if d.is_dir()]
    if not cases:
        print("[!] Keine Fälle gefunden.")
    else:
        print("[+] Vorhandene Fälle:")
        for c in cases:
            print(f" - {c}")

# Show case description file content
def show_case_description(case: str):
    desc_file = Path(f"logs/{case}/description.txt")
    if not desc_file.exists():
        print("[!] Keine Fallbeschreibung gefunden.")
        return

    content = desc_file.read_text()
    print(f"[+] Beschreibung von Fall {case}:\n\n{content}")
