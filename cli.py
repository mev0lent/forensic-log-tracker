# cli.py
import typer
import yaml
from core.executor import execute_command
from core.case_manager import create_case_folder
from core.gpg_signer import sign_file
from utils.reporting import generate_report, analyze_case, list_case_folders, show_case_description
from pathlib import Path

app = typer.Typer()

def ensure_case_exists(case: str):
    case_dir = Path(f"logs/{case}")
    if not case_dir.exists():
        typer.echo(f"[!] Der Fall '{case}' existiert nicht. Bitte zuerst mit 'new-case' anlegen.")
        raise typer.Exit(code=1)

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@app.command()
def new_case(case: str, description: str = typer.Option("", help="Kurze Beschreibung des Falls")):
    create_case_folder(case, description)

@app.command()
def run(
    cmd: str = typer.Argument(..., help="Der auszuführende Befehl"),
    case: str = typer.Option(..., "--case", "-c", help="Fall-ID (Name des Logs)"),
    sign: bool = typer.Option(None, help="Erzeugte Logdatei GPG-signieren (Default laut config)"),
    dry_run: bool = typer.Option(False, help="Nur simulieren, Befehl nicht wirklich ausführen.")
):
    ensure_case_exists(case)
    config = load_config()
    use_signing = sign if sign is not None else config.get("gpg", {}).get("enabled", True)
    log_path = execute_command(cmd, case, dry_run=dry_run)
    if use_signing:
        sign_file(log_path)

@app.command()
def analyze(case: str = typer.Option(..., "--case", "-c", help="Fall-ID")):
    ensure_case_exists(case)
    analyze_case(case)

@app.command()
def list_cases():
    list_case_folders()

@app.command()
def case_info(case: str = typer.Option(..., "--case", "-c", help="Fall-ID")):
    ensure_case_exists(case)
    show_case_description(case)

@app.command()
def report(
    case: str = typer.Option(..., "--case", "-c", help="Case ID to summarize"),
    verify: bool = typer.Option(None, help="Verify GPG signatures for each log (Default laut config)")
):
    ensure_case_exists(case)
    config = load_config()
    verify = verify if verify is not None else config.get("gpg", {}).get("auto_verify", True)
    generate_report(case, verify)

@app.command()
def verify_output(
    case: str = typer.Option(..., "--case", "-c", help="Fall-ID für Output-Verifikation")
):
    """
    Verifiziert den SHA256-Hash der Log-Outputs gegen den gespeicherten Hash.
    """
    ensure_case_exists(case)
    from utils.reporting import verify_output
    verify_output(case)

if __name__ == "__main__":
    app()
