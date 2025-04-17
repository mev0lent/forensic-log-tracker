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

if __name__ == "__main__":
    app()
