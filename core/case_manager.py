# core/case_manager.py
from pathlib import Path

def create_case_folder(case: str, description: str):
    base_path = Path("logs") / case
    base_path.mkdir(parents=True, exist_ok=True)
    desc_file = base_path / "description.txt"

    with desc_file.open("w", encoding="utf-8") as f:
        f.write(f"Fall-ID: {case}\nBeschreibung: {description}\n")
    print(f" [+] New case created: {base_path}")
