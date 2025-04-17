# core/legalizer.py
import yaml
from jinja2 import Template
from pathlib import Path

def get_legal_explanation(tool: str) -> str:
    with open("config/explanations.yaml", "r", encoding="utf-8") as f:
        explanations = yaml.safe_load(f)

    template_file = Path("templates/legal.md.j2")
    if not template_file.exists():
        return "[x] Kein juristisches Template gefunden."

    with template_file.open("r", encoding="utf-8") as f:
        template = Template(f.read())

    # Erkennung von Tool und Flags
    parts = tool.strip().split()
    command = parts[0]
    flags = parts[1:] if len(parts) > 1 else []

    cmd_entry = explanations.get(command, None)
    if not cmd_entry:
        print(f"[x] Keine Erklärung für '{command}' gefunden – bitte explanations.yaml ergänzen.")
        explanation_text = "[x] Keine spezifische Erklärung vorhanden."
    else:
        if isinstance(cmd_entry, str):
            explanation_text = cmd_entry
        else:
            explanation_text = cmd_entry.get("default", "")
            for flag in flags:
                # z. B. bei "mount -o ro" → findet Erklärung zu -o und ro
                explanation_text += "\n\n" + cmd_entry.get(flag, "")

    return template.render(tool=tool, explanation=explanation_text)
