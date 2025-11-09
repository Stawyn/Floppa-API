"""Helpers for interacting with files."""
from __future__ import annotations

from pathlib import Path


def ensure_file_exists(path: Path) -> None:
    """Create an empty file if it does not yet exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
