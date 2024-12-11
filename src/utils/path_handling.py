from pathlib import Path
import os

def get_project_root() -> Path:
    """Get the absolute path to the project root directory"""
    return Path(__file__).parent.parent.parent

def resolve_path(relative_path: str) -> Path:
    """Convert a path relative to project root into absolute path"""
    root = get_project_root()
    # Remove './' from the start if present
    clean_path = relative_path.lstrip('./')
    return root / clean_path

def ensure_path_exists(path: Path, create: bool = True) -> Path:
    """Ensure a path exists, optionally creating it"""
    if create and not path.exists():
        if path.suffix:  # If it's a file, create parent directories
            path.parent.mkdir(parents=True, exist_ok=True)
        else:  # If it's a directory, create it
            path.mkdir(parents=True, exist_ok=True)
    return path