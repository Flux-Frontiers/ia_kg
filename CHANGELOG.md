# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Removed

### Fixed

## [0.1.0] - 2026-05-03

### Added
- `src/ia_kg/`: New package replacing `src/audel_kg/` — renamed to `ia_kg` with entry point `iakg` to reflect the project's general Internet Archive scope rather than Audel-specific use.
- `src/ia_kg/cli/main.py`, `cmd_download.py`, `cmd_ingest.py`, `options.py`: Click-based CLI with `download` (book / catalog / search / survey) and `ingest` subcommands. Genre is inferred from the catalog filename stem when `--genre` is omitted.
- `tests/test_download_ia.py`, `tests/conftest.py`: 9-test pytest suite covering `slugify`, ligature normalization, smart-quote cleaning, hyphen-join, page-number removal, index stripping, running-header removal, heading detection, and Markdown conversion.
- `.pre-commit-config.yaml`: Pre-commit hooks — trailing whitespace, EOF fixer, YAML/TOML check, merge-conflict check, large-file guard (`corpus/` excluded), `ruff` lint (auto-fix), and `ruff-format`.
- `.github/workflows/ci.yml`: GitHub Actions CI with `lint` (ruff format check + ruff check, dev deps only) and `test` (pytest, dev deps only) jobs.
- `README.md`: Project README following doc_kg conventions — badges, overview, features, quick start, installation, usage reference, corpus layout, and adding-a-new-genre guide.
- `.claude/skills/`: Copied `dockg`, `documentation-lookup`, `kgrag`, `kgrag-usage`, `new-kg-module`, `publish`, `pycodekg`, `pycodekg-thorough-analysis`, and `skill-creator` skills from pycode_kg.

### Changed
- `scripts/download_ia.py`: Replaced hardcoded `ALL_GENRES = ["audel-electric"]` with `_discover_genres()` — scans `corpus/` subdirectories at runtime. `--genre` arguments changed from `choices=ALL_GENRES` to free-form strings. Genre auto-inferred from catalog filename stem in `cmd_catalog`. User-Agent updated to `IAKG/1.0`.
- `scripts/ingest.py`: Same dynamic genre discovery as `download_ia.py`. Removed genre validation against a hardcoded list. Summary header updated from "Audel KG" to "IA KG".
- `pyproject.toml`: Migrated from `[tool.poetry]` metadata to PEP 621 `[project]` table. Added `classifiers`, `[project.urls]`, `[project.optional-dependencies]` (`dev`, `kgdeps`). Moved `doc-kg` from git source to PyPI (`>=0.12.3`). Added `[tool.mypy]`, `[tool.pylint.messages_control]`, `[tool.pycodekg]`. Expanded `[tool.pytest.ini_options]` with `pythonpath`, `-v`, and markers. Added `ruff` excludes for `corpus/` and `.claude/`.
- `.gitignore`: Replaced minimal gitignore with comprehensive pycode_kg-style template. Added full KG artifact exclusions (`.pycodekg/`, `.dockg/`, `**/.dockg/`), KGRAG model cache wiring (`.kgrag/`, `.dockg/models` with comment documenting `~/.kgrag/models/` shared cache and `KGRAG_MODEL_DIR` override), and `.claude/` exclusion.

### Removed
- `src/audel_kg/`: Deleted old package (replaced by `src/ia_kg/`).
