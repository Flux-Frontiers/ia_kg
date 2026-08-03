# Release Notes — v0.1.0

> Released: 2026-05-03

**IAKG is the Audel toolchain generalised.** What began as a set of scripts for
one specific collection is now a package with a scope that matches what it
actually does: download books from the Internet Archive, clean the OCR text into
Markdown, and ingest the result into a DocKG knowledge graph. The package is
`ia_kg`, the command is `iakg`, and nothing about it assumes a particular
collection any more.

## What changed

**The Audel assumption is gone, in the name and in the code.** `src/audel_kg/`
became `src/ia_kg/`, and the hardcoded `ALL_GENRES = ["audel-electric"]` that sat
at the top of both `download_ia.py` and `ingest.py` was replaced with
`_discover_genres()`, which scans the `corpus/` subdirectories at runtime.
`--genre` accepts free-form strings rather than a fixed choice list, and is
inferred from the catalog filename stem when omitted — so adding a genre means
creating a directory, not editing source.

**A real CLI.** The scripts are now a Click application with two subcommands:
`download`, covering single books, catalogs, search, and survey; and `ingest`,
which builds the knowledge graph. Both are reachable as `iakg <subcommand>`.

**The text pipeline is under test.** Nine tests cover the parts most likely to
silently corrupt a corpus: slug generation, ligature normalisation, smart-quote
cleaning, hyphen-joining across line breaks, page-number removal, index
stripping, running-header removal, heading detection, and the final Markdown
conversion. These are the transformations that make OCR output usable, and they
were previously unverified.

**Repository hygiene brought in line with the rest of the fleet.** Pre-commit
hooks (whitespace, EOF, YAML/TOML validation, merge-conflict and large-file
guards, `ruff` lint and format), a GitHub Actions CI workflow with separate lint
and test jobs, a README following the doc_kg conventions, and a `.gitignore` that
actually excludes the KG artifacts (`.pycodekg/`, `.dockg/`) and wires up the
shared KGRAG model cache. Packaging moved from `[tool.poetry]` metadata to the
PEP 621 `[project]` table, and `doc-kg` moved from a git source to PyPI.

## Upgrading

This is the first release under the new name, so for most people it is an
install rather than an upgrade:

```bash
pip install ia-kg
iakg --help
```

If you were running the old `audel_kg` package, two things change. The import
path is `ia_kg`, not `audel_kg` — the old package is deleted, not aliased. And
the genre list is no longer compiled in: `corpus/` is the source of truth, so any
genre you want available needs a directory there. Existing `corpus/` layouts are
discovered as-is and need no migration.

---

_Full changelog: [CHANGELOG.md](CHANGELOG.md)_
