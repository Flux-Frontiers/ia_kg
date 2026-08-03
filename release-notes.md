# Release Notes — v0.1.1

> Released: 2026-08-03

**0.1.0 was not installable — install this instead.** `pip install ia-kg==0.1.0`
produced a package whose `iakg` command crashed on import, so every subcommand
was dead on arrival. Two independent packaging defects caused it, neither of
which is visible from a source checkout, which is why the tests and CI were green
throughout. Both are fixed, and CI now installs the built wheel and runs the real
command so this cannot recur.

## What changed

**The CLI's implementation was not in the package.** All 1,588 lines of it —
`download_ia.py` and `ingest.py` — lived in `scripts/`, which the wheel does not
ship. `cli/cmd_download.py` bridged the gap by walking four directories up from
its own `__file__` and injecting the result into `sys.path`. From a clone that
lands on the repo root and everything works; from `site-packages` it lands on
nothing. And because `cli/main.py` imports `cmd_download` at module scope, the
failure took out every command, not just `download`. Both modules now live in
`src/ia_kg/` and are imported normally, matching how gutenberg_kg is laid out:
everything the CLI needs is in the package, and `scripts/` holds only dev
one-offs.

**`iakg ingest` had a dependency that was never installed.** `kg-rag` was
declared as a poetry git source, and PyPI strips direct URLs from wheel metadata
— so `pip install ia-kg` resolved no kg-rag at all and `ingest` died on
`ModuleNotFoundError: No module named 'kg_rag'`. It is a genuine runtime
dependency: ingest registers each per-book DocKG in the KGRAG registry and adds
it to genre corpora, and those primitives (`KGRegistry`, `CorpusRegistry`,
`KGEntry`) exist only in kg-rag — kgmodule-utils covers embedding, extraction,
storage and retrieval, not the cross-KG registry. It is now declared as
`kg-rag>=0.11.0`, which has been on PyPI since 0.6.0.

**The corpus root no longer depends on where the code is installed.**
`REPO_ROOT` and `CORPUS_ROOT` were each derived from `__file__` in three separate
files. They are now defined once in `cli/options.py` and resolved from the
working directory, with an `IAKG_ROOT` environment override. Deriving them from
`__file__` is fine for a tool you only ever run from a clone; for a published
package it points into `site-packages`, nowhere near your corpus.

**CI now tests the artifact, not just the source tree.** The unit tests import
`ia_kg` via `pythonpath = ["src"]`, so they passed happily against a wheel
missing half its modules. A new job builds the wheel, installs it into a clean
virtualenv with no source tree in sight, and runs the console script from
`/tmp` — every subcommand's `--help`, plus `iakg ingest --list-genres` and `iakg
download survey`, which execute real code. That last part matters: Click resolves
`--help` before the command body runs, so a subcommand with deferred imports can
pass `--help` and still fail the moment it is actually invoked. That is precisely
how the kg_rag defect stayed hidden.

## Upgrading

```bash
pip install --upgrade ia-kg
iakg --help
```

If you installed 0.1.0, nothing you did was wrong — the package was broken.
Upgrading is the whole fix; there is no migration and no data to convert.

One behavioural note if you scripted around the old layout: the corpus is now
located relative to your working directory rather than to the installed code.
Run `iakg` from your corpus repo, or set `IAKG_ROOT=/path/to/repo` to point it
elsewhere. `iakg ingest --list-genres` will tell you what it can see.

---

_Full changelog: [CHANGELOG.md](CHANGELOG.md)_
