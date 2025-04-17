
# cli.py
import typer
from core.executor import execute_command
from core.case_manager import create_case_folder
from core.gpg_signer import sign_file
from utils.reporting import generate_report, analyze_case, list_case_folders, show_case_description

from pathlib import Path

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
    analyze_case(case)

@app.command()
def list_cases():
    list_case_folders()

@app.command()
def case_info(case: str = typer.Option(..., "--case", "-c", help="Fall-ID")):
    show_case_description(case)

@app.command()
def report(
    case: str = typer.Option(..., "--case", "-c", help="Case ID to summarize"),
    verify: bool = typer.Option(True, help="Verify GPG signatures for each log")
):
    generate_report(case, verify)

if __name__ == "__main__":
    app()
