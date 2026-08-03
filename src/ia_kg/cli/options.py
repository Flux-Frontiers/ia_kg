"""Shared constants and helpers for the iakg CLI.

This module is the single definition of the corpus location; ``download_ia`` and
``ingest`` import ``REPO_ROOT``/``CORPUS_ROOT`` from here rather than deriving
their own, mirroring ``gutenberg_kg.cli.options``.
"""

import os
from pathlib import Path

# Deliberately NOT derived from __file__. Sibling corpus tools (gutenberg_kg)
# can use Path(__file__).parents[3] because they are only ever run from a clone;
# ia-kg is published to PyPI, where that expression resolves into site-packages
# and the corpus is nowhere near the installed code. The working directory is
# the corpus repo you are operating on, so resolve from there, with an explicit
# override for callers that need to run from elsewhere.
REPO_ROOT = Path(os.environ.get("IAKG_ROOT") or Path.cwd()).resolve()
CORPUS_ROOT = REPO_ROOT / "corpus"


def discover_genres() -> list[str]:
    """Return genre names from corpus/ subdirectories."""
    if not CORPUS_ROOT.exists():
        return []
    return sorted(
        p.name for p in CORPUS_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
