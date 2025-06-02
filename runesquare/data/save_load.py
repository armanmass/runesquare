import json
from typing import Dict

def save_skills(skills: Dict[str, int], path: str) -> None:
    """Save skills (name: xp) to a JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(skills, f)
    except OSError as e:
        raise RuntimeError(f"Failed to save skills: {e}")

def load_skills(path: str) -> Dict[str, int]:
    """Load skills (name: xp) from a JSON file. Returns empty dict if file not found."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid skills data format in save file.")
            return {str(k): int(v) for k, v in data.items()}
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        raise RuntimeError(f"Failed to load skills: {e}")
