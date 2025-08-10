# New helper module to load prompt text from external files
import importlib.resources as pkg_resources
from pathlib import Path
from typing import Optional

def load_prompt(file_name: str, fallback: str, subdir: str = "files") -> str:
    """Return prompt text from app/templates/<subdir>/<file_name> if exists, else fallback.

    This lets non-developers edit prompt wording without changing Python code.
    """
    try:
        pkg_path = Path(__file__).resolve().parent / subdir / file_name
        if pkg_path.exists():
            return pkg_path.read_text(encoding="utf-8")
    except Exception:
        # Any problem just fall back
        pass
    return fallback
