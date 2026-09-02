> # ⚠️ Deprecated — superseded by `gutenberg_kg`
>
> **This project is no longer maintained.** Everything it did now lives in
> [gutenberg_kg](https://github.com/Flux-Frontiers/gutenberg_kg) under the
> `gutenkg ia` subcommands, which are a strict superset.
>
> | instead of | use |
> |---|---|
> | `iakg download search "<q>"` | `gutenkg ia search "<q>"` |
> | `iakg download book <id> --genre <g>` | `gutenkg ia download <id> --genre <g>` |
> | `iakg download catalog <file>` | `gutenkg ia catalog <file>` |
> | `iakg download survey --genre <g>` | `gutenkg ia survey --genre <g>` |
> | `iakg ingest --genre <g>` | `gutenkg ingest --genre <g>` |
>
> **Why.** The two projects had drifted into the same shape: the OCR and
> Markdown code is byte-identical between `ia_kg/download_ia.py` and
> `gutenberg_kg/ia.py` (`clean_ocr`, `_is_heading`, `text_to_markdown`,
> `_detect_running_headers`, `_find_toc_range`), and both parse the same IA
> items to the same bytes. Maintaining two copies bought nothing and cost
> correctness: `gutenberg_kg` has since gained fixes this repo never got --
> most importantly, downloads keyed on the **IA identifier** rather than the
> output path, so a changed `--title` no longer writes a second directory
> holding the same item.
>
> **What moved.** The Audels Electric Library corpus was consolidated into
> `gutenberg_kg` (8 of 10 volumes, all the 1929 public-domain edition), and
> `docs/catalog-workflow.md` was ported to
> [`docs/IA_CATALOG_WORKFLOW.md`](https://github.com/Flux-Frontiers/gutenberg_kg/blob/main/docs/IA_CATALOG_WORKFLOW.md)
> there, expanded with a rights-checking step this version lacked. The two CLI
> features `gutenberg_kg` was missing -- `--export-catalog` and genre inference
> from a catalog's filename -- were ported before retirement rather than lost.
>
> **If you installed `ia-kg` from PyPI:** it still works, but will receive no
> further releases. Switch to `gutenberg-kg`.
>
> The code below is left as-is for reference. Its corpus is redundant with
> `gutenberg_kg`'s and should not be rebuilt from here.

[![CI](https://github.com/Flux-Frontiers/ia_kg/actions/workflows/ci.yml/badge.svg)](https://github.com/Flux-Frontiers/ia_kg/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: Elastic-2.0](https://img.shields.io/badge/License-Elastic%202.0-blue.svg)](https://www.elastic.co/licensing/elastic-license)
[![Version](https://img.shields.io/badge/version-0.1.1-blue.svg)](https://github.com/Flux-Frontiers/ia_kg/releases)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

**ia-kg** — Internet Archive Book Downloader and Knowledge Graph Ingestion Pipeline

*Author: Eric G. Suchanek, PhD*
*Flux-Frontiers, Liberty TWP, OH*

---

## Overview

**ia-kg** downloads books from the [Internet Archive](https://archive.org) as structured Markdown and ingests them into [DocKG](https://github.com/Flux-Frontiers/doc_kg)-backed knowledge graphs, ready for retrieval via [KGRAG](https://github.com/Flux-Frontiers/KGRAG).

Books are organized by genre into a local corpus. Each volume is cleaned of OCR artifacts, segmented by chapter and section headings, and converted to well-structured Markdown — making it directly ingestible by `dockg build`. After ingestion, each book's knowledge graph is registered in the KGRAG registry and added to genre and global corpora for federated semantic retrieval.

ia-kg pairs naturally with [doc-kg](https://github.com/Flux-Frontiers/doc_kg) and [KGRAG](https://github.com/Flux-Frontiers/KGRAG) to form a complete pipeline from raw scanned text to queryable knowledge graph.

---

## Features

- **Internet Archive integration** — search, fetch metadata, and download DjVu text layers by identifier
- **OCR cleaning** — normalizes Unicode ligatures, smart quotes, hyphenated line-breaks, running headers, page numbers, and table-of-contents blocks
- **Heading-aware Markdown conversion** — detects CHAPTER / PART / SECTION / ALL-CAPS / Q&A headings and maps them to `##` / `###` / `####` nodes
- **Catalog-driven batch download** — tab-separated catalog files with identifier and optional title override; genre inferred from filename
- **Dynamic genre discovery** — no hardcoded genre lists; scans `corpus/` at runtime
- **DocKG ingestion** — builds per-book `.dockg/` indices and registers each in the KGRAG registry
- **Corpus and genre management** — adds each book to a genre corpus (`ia-<genre>`) and a global `ia-all` corpus
- **Survey command** — tabular status showing MD / reference / KG presence per book per genre
- **Dry-run support** — all download and ingest commands accept `--dry-run`

---

## Quick Start

```bash
# Search Internet Archive for texts
iakg download search "audels electric library"

# Download all books in a catalog
iakg download catalog scripts/catalogs/audel-electric.txt

# Show corpus status
iakg download survey

# Ingest into DocKG / KGRAG
iakg ingest --genre audel-electric
```

---

## Installation

**Requirements:** Python ≥ 3.12, < 3.14

```bash
# pip (runtime only)
pip install ia-kg

# pip (with dev tools)
pip install 'ia-kg[dev]'

# pip (with PyCodeKG for codebase analysis)
pip install 'ia-kg[kgdeps]'

# Poetry
poetry add ia-kg
```

> **Note:** `kg-rag` is not yet on PyPI. Install it from GitHub before using the ingest command:
> ```bash
> pip install git+https://github.com/Flux-Frontiers/KGRAG.git
> ```

---

## Usage

### Download

```bash
# Search for texts on Internet Archive
iakg download search "audels electric library" -n 10

# Download a single item by identifier
iakg download book audels-electric-library-vol-1 --genre audel-electric

# Download from a catalog file (genre inferred from filename)
iakg download catalog scripts/catalogs/audel-electric.txt

# Force re-download even if already present
iakg download catalog scripts/catalogs/audel-electric.txt --force

# Dry run — print actions without writing files
iakg download catalog scripts/catalogs/audel-electric.txt --dry-run

# Survey corpus status (MD / reference / KG)
iakg download survey
iakg download survey --genre audel-electric
```

### Ingest

```bash
iakg ingest --list-genres                         # list genres found in corpus/
iakg ingest                                       # ingest all genres
iakg ingest --genre audel-electric                # ingest one genre
iakg ingest --genre audel-electric --force-build  # rebuild even if .dockg exists
iakg ingest --push                                # git commit + push after each genre
iakg ingest --dry-run                             # print actions without executing
```

### Catalog format

Catalog files are tab-separated, one item per line, with optional title override:

```
# Comments are ignored
audels-electric-library-vol-1	Audels Electric Library Vol. 1
audels-electric-library-vol-2
```

Place catalogs in `scripts/catalogs/<genre>.txt` — the genre is inferred from the filename stem.

---

## Corpus Layout

```
corpus/
  <genre>/                        # e.g. audel-electric
    <Title>/                      # e.g. Audels Electric Library Vol. 1
      <slug>.md                   # structured Markdown (headings, Q&A, body)
      reference.md                # Internet Archive metadata sidecar
      .dockg/                     # DocKG knowledge graph index (after ingest)
        graph.sqlite
        lancedb/
```

Each book directory is a self-contained DocKG repository. Run `dockg build` inside any book directory to rebuild its index independently.

---

## Adding a New Genre

1. Create a catalog file at `scripts/catalogs/<genre>.txt`
2. Add identifiers (verify with `iakg download search`)
3. Download: `iakg download catalog scripts/catalogs/<genre>.txt`
4. Ingest: `iakg ingest --genre <genre>`

No code changes are needed — genre discovery is fully dynamic.

---

## License

[Elastic License 2.0](LICENSE) — free for non-commercial and internal use; commercial redistribution requires a license from Flux-Frontiers.
