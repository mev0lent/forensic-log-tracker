
# utils/reporting.py
from pathlib import Path
import subprocess
import re

def analyze_case(case):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Fall {case} existiert nicht.")
        return

    log_files = list(case_dir.glob("*.log"))
    sig_files = list(case_dir.glob("*.log.sig"))

    print(f"\n📂 Analyse von Fall: {case}")
    print(f"🗂️ {len(log_files)} Logdatei(en) gefunden:")
    for f in log_files:
        print(f" - {f.name}")

    if sig_files:
        print(f"\n🔐 Signaturen vorhanden für:")
        for f in sig_files:
            print(f" - {f.name}")
    else:
        print("\n⚠️ Keine GPG-Signaturen gefunden.")

def list_case_folders():
    cases = [d.name for d in Path("logs").iterdir() if d.is_dir()]
    if not cases:
        print("Keine Fälle gefunden.")
    else:
        print("📁 Vorhandene Fälle:")
        for c in cases:
            print(f" - {c}")

def show_case_description(case):
    desc_file = Path(f"logs/{case}/description.txt")
    if not desc_file.exists():
        print("[!] Keine Fallbeschreibung gefunden.")
        return

    content = desc_file.read_text()
    print(f"📝 Beschreibung von Fall {case}:\n\n{content}")

def extract_between_markers(lines, start_marker, end_marker):
    try:
        start = next(i for i, l in enumerate(lines) if start_marker in l) + 1
        end = next(i for i in range(start, len(lines)) if end_marker in lines[i])
        return "\n".join(lines[start:end]).strip()
    except StopIteration:
        return "*Nicht gefunden*"

def generate_report(case, verify=True):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Case '{case}' does not exist.")
        return

    description_file = case_dir / "description.txt"
    description = description_file.read_text().strip() if description_file.exists() else "*No description found.*"

    report_lines = [f"# 🕵️ Forensic Case Report: {case}\n", f"## 📝 Description\nFall-ID: {case}\nBeschreibung: {description}\n"]
    log_files = sorted(case_dir.glob("*.log"))
    if not log_files:
        print("[!] No log files found.")
        return

    report_lines.append("\n## 🧾 Executed Commands & Logs\n")

    for log_file in log_files:
        sig_file = log_file.with_suffix(log_file.suffix + ".sig")
        timestamp = log_file.stem.split("_")[0].replace("-", ":")
        log_text = log_file.read_text()
        lines = log_text.splitlines()

        # Initialize defaults
        cmd = "*Unbekannt*"
        sha = "*Nicht gefunden*"
        explanation = "*Nicht gefunden*"
        output_excerpt = "*Nicht gefunden*"

        # Extract values flexibly
        for line in lines:
            if "Befehl" in line and "`" in line:
                cmd = re.findall(r"`(.*?)`", line)[0] if re.findall(r"`(.*?)`", line) else cmd
            elif "SHA256" in line and "`" in line:
                sha = re.findall(r"`(.*?)`", line)[0] if re.findall(r"`(.*?)`", line) else sha

        explanation = extract_between_markers(lines, "### 🧾", "###")
        output_excerpt = extract_between_markers(lines, "### 📤", "```")

        sig_status = "⚠️ Nicht signiert"
        if verify and sig_file.exists():
            try:
                subprocess.run(["gpg", "--verify", str(sig_file)], capture_output=True, check=True)
                sig_status = "✅ Gültig"
            except subprocess.CalledProcessError:
                sig_status = "❌ Ungültig"
        elif sig_file.exists():
            sig_status = "✅ (nicht geprüft)"

        report_lines.append(f"### ✅ Command: `{cmd}`")
        report_lines.append(f"- Timestamp: `{timestamp}`")
        report_lines.append(f"- Signature: {sig_status}")
        report_lines.append(f"- SHA256: `{sha}`\n")
        report_lines.append(f"#### Output (excerpt):\n```\n{output_excerpt}\n```\n")
        report_lines.append(f"#### Legal Explanation:\n{explanation}\n---\n")

    report_lines.append("\n## 🔐 GPG Summary")
    report_lines.append("Each `.log` file is individually signed with GPG.")
    report_lines.append("Signature status is shown above for traceability.\n")

    report_path = case_dir / f"{case}_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"✅ Report written to: {report_path}")
