# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Removed

### Fixed

## [0.1.1] - 2026-08-03

**0.1.0 was not installable.** `iakg` crashed on import from a `pip install`, so
every command was dead. Two independent packaging defects, both invisible from a
source checkout, both fixed here.

### Fixed
- **`iakg` crashed with `ModuleNotFoundError: No module named 'download_ia'`.**
  The CLI's entire implementation — 1,588 lines across `download_ia.py` and
  `ingest.py` — lived in `scripts/`, which is not part of the package, and
  `cli/cmd_download.py` reached it by walking four directories up from `__file__`
  and injecting the result into `sys.path`. From a checkout that lands on the
  repo root; from `site-packages` it lands on nothing. Because `cli/main.py`
  imports `cmd_download` at module scope, *every* subcommand died, not just
  `download`.
- **`iakg ingest` failed with `ModuleNotFoundError: No module named 'kg_rag'`.**
  `kg-rag` was declared as a poetry git source, which PyPI strips from wheel
  metadata, so `pip install ia-kg` never installed it. It is now a normal
  `kg-rag>=0.11.0` dependency — kg-rag has been on PyPI since 0.6.0 and the
  comment claiming otherwise was stale.

### Changed
- **`download_ia.py` and `ingest.py` moved from `scripts/` into `src/ia_kg/`**,
  matching gutenberg_kg, where every module the CLI imports lives in the package
  and `scripts/` holds only dev one-offs. The `sys.path` manipulation in
  `cmd_download.py` and `cmd_ingest.py` is gone; both now use ordinary relative
  imports.
- **`REPO_ROOT` / `CORPUS_ROOT` / `discover_genres()` are defined once**, in
  `cli/options.py`, and imported by `download_ia` and `ingest` instead of each
  file deriving its own copy — again mirroring `gutenberg_kg.cli.options`.
- **The corpus root resolves from the working directory**, with an `IAKG_ROOT`
  override, rather than from `__file__`. Sibling tools can use
  `Path(__file__).parents[3]` because they are only ever run from a clone; ia-kg
  is on PyPI, where that expression points into `site-packages` and the corpus is
  nowhere near the installed code.
- Usage examples in both module docstrings now show real `iakg` commands
  (`iakg download book …`) instead of `python scripts/download_ia.py …`.

### Added
- **CI job that installs the built wheel into a clean venv and runs the console
  script.** The unit tests import from the source tree via `pythonpath = ["src"]`,
  so they passed on a wheel that was missing half its modules — nothing in CI
  ever exercised the artifact users receive. The job runs `--help` for every
  subcommand *and* executes `iakg ingest --list-genres` and `iakg download
  survey`: Click resolves `--help` before the command body, so a deferred import
  can pass `--help` and still fail when invoked, which is exactly how the kg_rag
  defect hid.

### Removed
- `scripts/test_download_ia.py`: standalone predecessor of
  `tests/test_download_ia.py`, superseded and orphaned by the module move.

## [0.1.0] - 2026-08-03

First published release. The `[0.1.0]` work was originally dated 2026-05-03 but
was never tagged or published, so everything developed since has been folded in
here rather than shipped as a phantom second version.

### Added
- `iakg download search --export-catalog FILE`: new flag writes all search results to a commented-out draft catalog `.txt` file. Every line is prefixed with `#` so nothing downloads accidentally; uncomment desired entries before running `iakg download catalog`.
- `docs/catalog-workflow.md`: step-by-step guide covering search → export-catalog → curate → test one book → bulk download → survey → ingest.
- `.github/workflows/release.yml`: tag-triggered release workflow mirroring the fleet standard (doc-kg, pycode-kg) — fires on `push: tags: ['v*']`, runs `poetry build`, and creates a GitHub Release from `dist/*`. It does **not** publish to PyPI; that stays a manual `poetry publish --build` step.
- `release-notes.md`: prose release notes, read by the workflow above via `--notes-file` out of the tagged commit. Rewritten at each release rather than appended to.
- `src/ia_kg/`: New package replacing `src/audel_kg/` — renamed to `ia_kg` with entry point `iakg` to reflect the project's general Internet Archive scope rather than Audel-specific use.
- `src/ia_kg/cli/main.py`, `cmd_download.py`, `cmd_ingest.py`, `options.py`: Click-based CLI with `download` (book / catalog / search / survey) and `ingest` subcommands. Genre is inferred from the catalog filename stem when `--genre` is omitted.
- `tests/test_download_ia.py`, `tests/conftest.py`: 9-test pytest suite covering `slugify`, ligature normalization, smart-quote cleaning, hyphen-join, page-number removal, index stripping, running-header removal, heading detection, and Markdown conversion.
- `.pre-commit-config.yaml`: Pre-commit hooks — trailing whitespace, EOF fixer, YAML/TOML check, merge-conflict check, large-file guard (`corpus/` excluded), `ruff` lint (auto-fix), and `ruff-format`.
- `.github/workflows/ci.yml`: GitHub Actions CI with `lint` (ruff format check + ruff check, dev deps only) and `test` (pytest, dev deps only) jobs.
- `README.md`: Project README following doc_kg conventions — badges, overview, features, quick start, installation, usage reference, corpus layout, and adding-a-new-genre guide.
- `.claude/skills/`: Copied `dockg`, `documentation-lookup`, `kgrag`, `kgrag-usage`, `new-kg-module`, `publish`, `pycodekg`, `pycodekg-thorough-analysis`, and `skill-creator` skills from pycode_kg.

### Changed
- **Dependency floors lifted to the currently published releases** — `kgmodule-utils>=0.10.0` (from a long-dead `>=0.2.0`), `doc-kg>=0.21.0` (from `>=0.12.3`), `pycode-kg>=0.21.4`; lock regenerated. Note the behavioural consequence of the doc-kg floor: from 0.20.0 `vector_backend` defaults to `"sqlite-vec"` outright rather than resolving per-store from whatever is on disk, and `lancedb` is no longer a core dependency — it moved to an opt-in `[lancedb]` extra needed only to read a pre-0.20.0 store via `dockg convert-index`.
- `scripts/download_ia.py`: Replaced hardcoded `ALL_GENRES = ["audel-electric"]` with `_discover_genres()` — scans `corpus/` subdirectories at runtime. `--genre` arguments changed from `choices=ALL_GENRES` to free-form strings. Genre auto-inferred from catalog filename stem in `cmd_catalog`. User-Agent updated to `IAKG/1.0`.
- `scripts/ingest.py`: Same dynamic genre discovery as `download_ia.py`. Removed genre validation against a hardcoded list. Summary header updated from "Audel KG" to "IA KG".
- `pyproject.toml`: Migrated from `[tool.poetry]` metadata to PEP 621 `[project]` table. Added `classifiers`, `[project.urls]`, `[project.optional-dependencies]` (`dev`, `kgdeps`). Moved `doc-kg` from git source to PyPI (`>=0.12.3`). Added `[tool.mypy]`, `[tool.pylint.messages_control]`, `[tool.pycodekg]`. Expanded `[tool.pytest.ini_options]` with `pythonpath`, `-v`, and markers. Added `ruff` excludes for `corpus/` and `.claude/`.
- `.gitignore`: Replaced minimal gitignore with comprehensive pycode_kg-style template. Added full KG artifact exclusions (`.pycodekg/`, `.dockg/`, `**/.dockg/`), KGRAG model cache wiring (`.kgrag/`, `.dockg/models` with comment documenting `~/.kgrag/models/` shared cache and `KGRAG_MODEL_DIR` override), and `.claude/` exclusion.

### Removed
- `src/audel_kg/`: Deleted old package (replaced by `src/ia_kg/`).

### Fixed
- `.github/workflows/ci.yml`: replaced invalid `poetry install --only dev` with `poetry install --extras dev` in both `lint` and `test` jobs. `--only` targets Poetry dependency *groups*; `dev` is a PEP 621 *extra*, so the old command errored in CI.
