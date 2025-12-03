import json
from pathlib import Path

def load_last_values(file: Path):
    """Load last entered values if available."""
    if file.exists():
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_last_values(file: Path, data: dict):
    """Save last entered values to disk."""
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
