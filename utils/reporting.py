
# utils/reporting.py
from pathlib import Path
import subprocess
import re
import yaml
import hashlib

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def sha256_from_string(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

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

def extract_block(lines, start_marker):
    try:
        start = next(i for i, l in enumerate(lines) if start_marker in l)
        start_code = next(i for i in range(start, len(lines)) if lines[i].strip() == "```") + 1
        end_code = next(i for i in range(start_code, len(lines)) if lines[i].strip() == "```")
        return lines[start_code:end_code]
    except StopIteration:
        return ["*Nicht gefunden*"]

def extract_explanation(lines):
    try:
        start = next(i for i, l in enumerate(lines) if "### 🧾" in l)
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("###")), len(lines))
        return "\n".join(lines[start + 1:end]).strip()
    except StopIteration:
        return "*Nicht gefunden*"

def generate_report(case, verify=True):
    config = load_config()
    preview_lines = config.get("output", {}).get("preview_lines", 20)

    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Case '{case}' does not exist.")
        return

    description_file = case_dir / "description.txt"
    description = "*No description found.*"
    if description_file.exists():
        desc_lines = description_file.read_text().splitlines()
        description = next((l for l in desc_lines if "Beschreibung:" in l), "").replace("Beschreibung:", "").strip()

    report_lines = [f"# 🕵️ Forensic Case Report: {case}\n", f"## 📝 Description\n{description}\n"]
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

        cmd = "*Unbekannt*"
        sha = "*Nicht gefunden*"

        for i, line in enumerate(lines):
            if "Befehl" in line and i + 1 < len(lines) and "`" in lines[i + 1]:
                cmd = re.findall(r"`(.*?)`", lines[i + 1])[0]
            elif "SHA256" in line and "`" in line:
                sha = re.findall(r"`(.*?)`", line)[0]

        output_lines = extract_block(lines, "### 📤 Output")
        output_excerpt = "\n".join(output_lines[:preview_lines])
        explanation = extract_explanation(lines)

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

def verify_output(case):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Case '{case}' does not exist.")
        return

    print(f"📦 Verifiziere Outputs für Fall: {case}")
    for log_file in sorted(case_dir.glob("*.log")):
        lines = log_file.read_text().splitlines()
        expected_hash = None
        for line in lines:
            if "SHA256" in line and "`" in line:
                match = re.findall(r"`(.*?)`", line)
                if match:
                    expected_hash = match[0]

        output_lines = extract_block(lines, "### 📤 Output")
        actual_hash = sha256_from_string("\n".join(output_lines))
        result = "✅ OK" if actual_hash == expected_hash else "❌ Mismatch"
        print(f"{log_file.name}: {result}")

def list_case_folders():
    cases = [d.name for d in Path("logs").iterdir() if d.is_dir()]
    if not cases:
        print("Keine Fälle gefunden.")
    else:
        print("📁 Vorhandene Fälle:")
        for c in cases:
            print(f" - {c}")

def show_case_description(case: str):
    desc_file = Path(f"logs/{case}/description.txt")
    if not desc_file.exists():
        print("[!] Keine Fallbeschreibung gefunden.")
        return

    content = desc_file.read_text()
    print(f"📝 Beschreibung von Fall {case}:\n\n{content}")
