# Einstiegspunkt mit Typer: https://typer.tiangolo.com/

# cli.py
import typer
from core.executor import execute_command
from core.case_manager import create_case_folder

app = typer.Typer()

@app.command()
def new_case(case: str, description: str = typer.Option("", help="Kurze Beschreibung des Falls")):
    create_case_folder(case, description)

@app.command()
def run(cmd: str, case: str):
    execute_command(cmd, case)

@app.command()
def analyze(case: str):
    """Zeigt eine Übersicht aller Logs und Hashes eines Falls."""
    from pathlib import Path

    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        print(f"[!] Fall {case} existiert nicht.")
        raise typer.Exit()

    log_files = list(case_dir.glob("*.log"))
    manifest_file = case_dir / "SHA256-MANIFEST.txt"

    print(f"\n📂 Analyse von Fall: {case}")
    print(f"🗂️ {len(log_files)} Logdatei(en) gefunden:\n")
    for f in log_files:
        print(f" - {f.name}")

    if manifest_file.exists():
        print(f"\n🧾 SHA256-MANIFEST:\n{manifest_file.read_text()}")
    else:
        print("\n⚠️ Kein Manifest gefunden.")

if __name__ == "__main__":
    app()
