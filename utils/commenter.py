# utils/commenter.py
from datetime import datetime
from pathlib import Path
from utils.pathing import get_case_log_path
from utils.shared_config import load_config
from core.gpg_signer import sign_file

def write_comment(case: str, text: str) -> Path:
    """
    Create a comment log for a case and optionally sign it.
    """
    config = load_config()
    case_dir = get_case_log_path(case, create=False)
    if not case_dir.exists():
        raise FileNotFoundError(f"Case folder '{case}' does not exist.")

    timestamp = datetime.now(config["TIMEZONE"]).isoformat()
    safe_time = timestamp.replace(":", "-").replace(".", "-")
    comment_file = case_dir / f"{safe_time}_comment.log"

    analyst = config.get("project", {}).get("analyst", "Unknown Analyst")

    content = [
        f"#### [+] Comment from analyst: {analyst}",
        "",
        f"#### [+] Content:",
        text,
        ""
    ]

    comment_file.write_text("\n".join(content), encoding="utf-8")

    # Sign the comment file if configured
    if config.get("gpg", {}).get("enabled", True):
        sign_file(comment_file)

    return comment_file
