# core/legalizer.py
import yaml
from jinja2 import Template
from pathlib import Path
from core.legal_parser import PARSERS
from utils.log import logger
from utils.shared_config import load_config
from datetime import datetime
from utils.pathing import get_template_path, get_config_path

config = load_config()


def get_legal_explanation(tool: str) -> str:
    if not tool or not tool.strip():
        return "[x] Skipped: command was empty or malformed."

    parts = tool.strip().split()
    if not parts:
        return "[x] Skipped: command string could not be parsed."

    used_sudo = parts[0] == "sudo"
    if used_sudo:
        parts = parts[1:]

    if not parts:
        return "[x] Skipped: command after sudo was empty."

    command = parts[0].lower()
    args = parts[1:]

    parser = PARSERS.get(command)
    flags = parser(args) if parser else args

    with get_config_path("explanations.yaml").open("r", encoding="utf-8") as f:
        explanations = yaml.safe_load(f)

    cmd_entry = explanations.get(command, None)
    if not cmd_entry:
        print(f"[x] No explanation for '{command}' found – please extend explanations.yaml.")
        explanation_text = "[x] No specific explanation found."
    else:
        if isinstance(cmd_entry, str):
            explanation_text = cmd_entry
        else:
            explanation_text = cmd_entry.get("default", "")
            for flag in flags:
                explanation_text += "\n\n" + cmd_entry.get(flag, "")

    if used_sudo:
        explanation_text = (
            "**[!] Note:** This command was executed with administrative rights (`sudo`).\n"
            + explanation_text
        )

    template_file = get_template_path()
    if not template_file.exists():
        logger.error("[x] No template found at templates/legal.md.j2.")
        return "[x] Legal explanation unavailable – missing template."

    try:
        with template_file.open("r", encoding="utf-8") as f:
            template = Template(f.read())
    except Exception as e:
        logger.error(f"[x] Template loading failed: {e}")
        return "[x] Legal explanation rendering failed."

    return template.render(
        tool=tool.strip(),
        explanation=explanation_text.strip(),
        analyst=config["project"]["analyst"],
        timestamp=datetime.now(config["TIMEZONE"]).isoformat()
    ).strip()
