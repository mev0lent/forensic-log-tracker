# cli.py
import typer
from utils.log import logger
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
        typer.echo(f"[!] The case '{case}' does not exist. Please create it first using 'new-case'.")
        raise typer.Exit(code=1)

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@app.command()
def new_case(case: str, description: str = typer.Option("", help="Short description of the case")):
    try:
        create_case_folder(case, description)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")

@app.command()
def run(
    cmd: str = typer.Argument(..., help="The command to be executed"),
    case: str = typer.Option(..., "--case", "-c", help="Case ID (log name)"),
    sign: bool = typer.Option(None, help="Sign the generated log file with GPG (default as per config)"),
    dry_run: bool = typer.Option(False, help="Simulate only, do not actually execute the command.")
):
    ensure_case_exists(case)
    config = load_config()
    use_signing = sign if sign is not None else config.get("gpg", {}).get("enabled", True)

    try:
        log_path = execute_command(cmd, case, dry_run=dry_run)
        if dry_run:
            answer = " not"
        else:
            answer = ""
        logger.info(f"Command{answer} executed, logged: {cmd}")
    except Exception as e:
        logger.error(f"[run] Command failed: {e}")
        raise typer.Exit(code=2)

    if use_signing:
        try:
            sign_file(log_path)
            logger.info(f"Log file signed: {log_path}")
        except Exception as e:
            logger.error(f"[run] Signing failed: {e}")

@app.command()
def analyze(case: str = typer.Option(..., "--case", "-c", help="Case ID")):
    ensure_case_exists(case)
    analyze_case(case)

@app.command()
def list_cases():
    list_case_folders()

@app.command()
def case_info(case: str = typer.Option(..., "--case", "-c", help="Case ID")):
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
    case: str = typer.Option(..., "--case", "-c", help="Case ID for output verification")
):
    """
    Verifies the output hash (e.g., SHA256) of log files against the stored hash value.
    Hash algorithm is configurable in config.yaml (output.hash_algorithm).
    """
    ensure_case_exists(case)
    from utils.reporting import verify_output
    verify_output(case)

if __name__ == "__main__":
    app()
