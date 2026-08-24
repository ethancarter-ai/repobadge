# repobadge

Generate concise SVG badges summarizing GitHub repository statistics.

## About

`repobadge` turns live or cached GitHub repository metadata into compact SVG badges. It's designed for quick embedding in READMEs, dashboards, or status pages.

The current badge emphasizes repository stars, with optional language color tagging. It supports multiple visual styles.

- Source code: https://github.com/ethancarter-ai/repobadge

## Features

* Fetch repository metadata from GitHub or render from a local summary file.
* Language-aware right-side coloring for popular languages.
* Multiple badge styles: `flat`, `flat-square`, `plastic`.
* Deterministic offline rendering without network calls.
* Stdlib-only implementation with an optional MIT-licensed core.

## Installation

```bash
python -m pip install .
```

Source install:

```bash
git clone https://github.com/ethancarter-ai/repobadge.git
cd repobadge
python -m pip install -e .
```

## Usage

```bash
repobadge --summary-file path/to/repo.json --style flat
repobadge --summary-file path/to/repo.json --style plastic --output badge.svg
python -m repobadge --summary-file path/to/repo.json --style flat
```

Offline rendering from a cached summary file in JSON format:

```bash
repobadge --summary-file path/to/repo.json --style flat
```

### Exit codes

* `0` — success
* `1` — bad invocation or unsupported option

## Project structure

```text
repobadge/
  src/repobadge/
    __init__.py
    cli.py
    core.py
    parser.py
  tests/
    test_repobadge.py
  docs/
    usage.md
  pyproject.toml
  README.md
  .gitignore
```

## License

MIT
