"""Shared constants and helpers for the iakg CLI."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # src/ia_kg/cli/ -> repo root
CORPUS_ROOT = REPO_ROOT / "corpus"


def discover_genres() -> list[str]:
    """Return genre names from corpus/ subdirectories."""
    if not CORPUS_ROOT.exists():
        return []
    return sorted(
        p.name for p in CORPUS_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
