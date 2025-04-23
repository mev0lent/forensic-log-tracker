# core/case_manager.py
from utils.pathing import get_case_log_path

def create_case_folder(case: str, description: str):
    base_path = get_case_log_path(case, create=True)
    base_path.mkdir(parents=True, exist_ok=True)
    desc_file = base_path / "description.txt"

    with desc_file.open("w", encoding="utf-8") as f:
        f.write(f"Case-ID: {case}\nDescription: {description}\n")
    print(f" [+] New case created: {base_path}")
