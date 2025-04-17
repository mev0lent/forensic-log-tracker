# utils/reporting.py
from pathlib import Path
import subprocess

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

def generate_report(case, verify=True):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Case '{case}' does not exist.")
        return

    description_file = case_dir / "description.txt"
    description = description_file.read_text().strip() if description_file.exists() else "*No description found.*"

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
        cmd = "N/A"
        sha = "N/A"
        explanation = "*Missing*"
        output_excerpt = "*No output found*"
        lines = log_text.splitlines()

        try:
            cmd = next(l for l in lines if l.startswith("### 🧩 Befehl:")).split("`")[1]
            sha = next(l for l in lines if l.startswith("### 🔐 SHA256")).split("`")[1]
            explanation_idx = lines.index("### 🧾 Juristische Erklärung:") + 1
            explanation = "\n".join(lines[explanation_idx:]).strip()
            output_start = lines.index("### 📤 Output (Auszug):") + 2
            output_end = lines.index("```", output_start)
            output_excerpt = "\n".join(lines[output_start:output_end])
        except Exception:
            explanation = "*Could not parse log structure*"

        sig_status = "⚠️ Missing"
        if verify and sig_file.exists():
            try:
                subprocess.run(["gpg", "--verify", str(sig_file)], capture_output=True, check=True)
                sig_status = "✅ Valid"
            except subprocess.CalledProcessError:
                sig_status = "❌ Invalid"
        elif sig_file.exists():
            sig_status = "✅ (Not Verified)"

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
