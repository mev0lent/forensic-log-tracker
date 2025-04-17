# core/legalizer.py
import yaml
from jinja2 import Template
from pathlib import Path

def get_legal_explanation(tool: str) -> str:
    with open("config/explanations.yaml", "r", encoding="utf-8") as f:
        explanations = yaml.safe_load(f)

    template_file = Path("templates/legal.md.j2")
    if not template_file.exists():
        return "[Warnung] Kein juristisches Template gefunden."

    with template_file.open("r", encoding="utf-8") as f:
        template = Template(f.read())

    explanation_text = explanations.get(tool, "Keine spezifische Erklärung vorhanden.")
    return template.render(tool=tool, explanation=explanation_text)
