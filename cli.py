# cli.py
import typer
from core.executor import execute_command
from core.case_manager import create_case_folder
from core.gpg_signer import sign_file

from pathlib import Path
import os

app = typer.Typer()

@app.command()
def new_case(case: str, description: str = typer.Option("", help="Kurze Beschreibung des Falls")):
    create_case_folder(case, description)

@app.command()
def run(
    cmd: str = typer.Argument(..., help="Der auszuführende Befehl"),
    case: str = typer.Option(..., "--case", "-c", help="Fall-ID (Name des Logs)"),
    sign: bool = typer.Option(True, help="Erzeugte Logdatei GPG-signieren")
):
    log_path = execute_command(cmd, case)
    if sign:
        sign_file(log_path)

@app.command()
def analyze(case: str = typer.Option(..., "--case", "-c", help="Fall-ID")):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Fall {case} existiert nicht.")
        raise typer.Exit()

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

@app.command()
def list_cases():
    """Listet alle vorhandenen Fälle auf."""
    cases = [d.name for d in Path("logs").iterdir() if d.is_dir()]
    if not cases:
        print("Keine Fälle gefunden.")
    else:
        print("📁 Vorhandene Fälle:")
        for c in cases:
            print(f" - {c}")

@app.command()
def case_info(case: str = typer.Option(..., "--case", "-c", help="Fall-ID")):
    """Zeigt Beschreibung und Erstellungsdatum eines Falls."""
    desc_file = Path(f"logs/{case}/description.txt")
    if not desc_file.exists():
        print("[!] Keine Fallbeschreibung gefunden.")
        raise typer.Exit()

    content = desc_file.read_text()
    print(f"📝 Beschreibung von Fall {case}:\n\n{content}")

@app.command()
def report(
    case: str = typer.Option(..., "--case", "-c", help="Case ID to summarize"),
    verify: bool = typer.Option(True, help="Verify GPG signatures for each log")
):
    """
    Generates a full report (Markdown) for a given case.
    """
    from pathlib import Path
    import subprocess

    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Case '{case}' does not exist.")
        raise typer.Exit()

    description_file = case_dir / "description.txt"
    if description_file.exists():
        description = description_file.read_text().strip()
    else:
        description = "*No description found.*"

    report_lines = []
    report_lines.append(f"# 🕵️ Forensic Case Report: {case}\n")
    report_lines.append(f"## 📝 Description\n{description}\n")

    log_files = sorted(case_dir.glob("*.log"))
    if not log_files:
        print("[!] No log files found.")
        raise typer.Exit()

    report_lines.append("\n## 🧾 Executed Commands & Logs\n")

    for log_file in log_files:
        sig_file = log_file.with_suffix(log_file.suffix + ".sig")
        timestamp = log_file.stem.split("_")[0].replace("-", ":")

        # Try extracting the command, output excerpt, explanation and hash
        log_text = log_file.read_text()
        cmd = "N/A"
        sha = "N/A"
        explanation = ""
        output_excerpt = ""
        lines = log_text.splitlines()

        try:
            cmd = next(l for l in lines if l.startswith("### 🧩")).split("`")[1]
            sha = next(l for l in lines if l.startswith("### 🔐")).split("`")[1]
            explanation_idx = lines.index("### 🧾 Juristische Erklärung:") + 1
            explanation = "\n".join(lines[explanation_idx:]).strip()
            output_start = lines.index("### 📤 Output (Auszug):") + 2
            output_end = lines.index("```", output_start)
            output_excerpt = "\n".join(lines[output_start:output_end])
        except Exception:
            explanation = "*Could not parse log structure*"

        # Optional GPG verification
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

    # Write final report
    report_path = case_dir / f"{case}_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"✅ Report written to: {report_path}")


if __name__ == "__main__":
    app()
