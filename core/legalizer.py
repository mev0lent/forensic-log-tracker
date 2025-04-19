# core/legalizer.py
import yaml
from jinja2 import Template
from pathlib import Path
from core.legal_parser import PARSERS

def get_legal_explanation(tool: str) -> str:
    with open("config/explanations.yaml", "r", encoding="utf-8") as f:
        explanations = yaml.safe_load(f)

    template_file = Path("templates/legal.md.j2")
    if not template_file.exists():
        return "[x] No template found."

    with template_file.open("r", encoding="utf-8") as f:
        template = Template(f.read())

    parts = tool.strip().split()
    command = parts[0]
    args = parts[1:]

    parser = PARSERS.get(command)
    flags = parser(args) if parser else args

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
                # z. B. bei "mount -o ro" → findet Erklärung zu -o und ro
                explanation_text += "\n\n" + cmd_entry.get(flag, "")

    return template.render(tool=tool, explanation=explanation_text)
