# Catalog Workflow: Discovering and Curating IA Books

This guide walks through the full process of building a catalog for a new genre,
from initial search to a downloaded and ingested corpus.

---

## Overview

A **catalog file** is a tab-separated text file that tells `iakg` which Internet
Archive items to download for a given genre.  You build it manually from search
results — curating identifiers and optionally overriding titles — before
committing to a bulk download.

```
scripts/catalogs/<genre>.txt   →   iakg download catalog   →   corpus/<genre>/
```

---

## Step 1 — Search for identifiers

Use the `search` command to find items on the Internet Archive:

```bash
iakg download search "audels electric library" -n 25
```

Output:

```
Searching Internet Archive: 'audels electric library'

Identifier                        Year   Title
-----------------------------------------------------------------------
audels-electric-library-vol-1    1929   Audels Electric Library Vol. 1
audels-electric-library-vol-2    1929   Audels Electric Library Vol. 2
...
```

Tip: try multiple queries — IA metadata is inconsistent.  Narrow with year or
author terms (`"audels plumbers guide" author:graesser`).

---

## Step 2 — Export a draft catalog

Add `--export-catalog` to write results directly to a catalog file:

```bash
iakg download search "audels electric library" -n 25 \
    --export-catalog scripts/catalogs/audel-electric.txt
```

Every result is written as a **commented-out line** so nothing downloads
accidentally:

```
# Catalog draft — IA search: audels electric library
# Review identifiers before downloading.
# Format: <identifier>[TAB<title>]  (comment lines start with #)

# audels-electric-library-vol-1	Audels Electric Library Vol. 1
# audels-electric-library-vol-2	Audels Electric Library Vol. 2
# audels-electric-library-vol-3	Audels Electric Library Vol. 3
```

Run multiple searches and append results to the same file to collect from
different query terms before curating.

---

## Step 3 — Curate the catalog

Open the draft in any editor and:

1. **Uncomment** lines you want to download (remove the leading `# `).
2. **Delete or leave commented** lines you don't want.
3. **Override titles** by editing the text after the tab — the directory name
   in `corpus/` is derived from the title.
4. **Add notes** as comment lines for future reference.

Example after curation:

```
# Audel Electric Library — curated 2026-05-03
# Vols 5 and 6 not available on IA.

audels-electric-library-vol-1	Audels Electric Library Vol. 1
audels-electric-library-vol-2	Audels Electric Library Vol. 2
# audels-electric-library-vol-5   ← not available
```

### Verifying an identifier

Before downloading, confirm an identifier exists and check its files:

```bash
curl -s "https://archive.org/metadata/audels-electric-library-vol-1" | python -m json.tool | head -40
```

Or do a targeted search:

```bash
iakg download search "audels electric library vol 1" -n 5
```

---

## Step 4 — Test one book

Download a single item to verify the output before committing to the full catalog:

```bash
iakg download book audels-electric-library-vol-1 --genre audel-electric
```

Check the result in `corpus/audel-electric/` — confirm the Markdown looks clean
and the `reference.md` metadata sidecar is present.

---

## Step 5 — Download the full catalog

Once satisfied, download everything in the catalog:

```bash
iakg download catalog scripts/catalogs/audel-electric.txt
```

Genre is inferred from the filename stem (`audel-electric.txt` → genre
`audel-electric`).  Override with `--genre` if needed.

Use `--dry-run` to preview actions without writing files:

```bash
iakg download catalog scripts/catalogs/audel-electric.txt --dry-run
```

Use `--force` to re-download items that already exist in `corpus/`.

---

## Step 6 — Survey and ingest

Check what was downloaded:

```bash
iakg download survey --genre audel-electric
```

Then ingest into DocKG / KGRAG:

```bash
iakg ingest --genre audel-electric
```

---

## Catalog file format reference

```
# Comment lines are ignored (leading #)
<identifier>
<identifier><TAB><title override>
```

- **Identifier** — the Internet Archive item identifier (slug in the IA URL).
- **Title override** (optional) — used as the directory name under `corpus/<genre>/`.
  If omitted, the title is fetched from IA metadata at download time.
- Place the file at `scripts/catalogs/<genre>.txt` — genre is inferred from the
  filename stem.

---

## Adding a new genre

1. Run `iakg download search` with relevant terms.
2. Export a draft: `--export-catalog scripts/catalogs/<genre>.txt`
3. Curate, verify, test one book.
4. Download: `iakg download catalog scripts/catalogs/<genre>.txt`
5. Ingest: `iakg ingest --genre <genre>`

No code changes are needed — genre discovery is fully dynamic.
