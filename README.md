# repobadge

Generate concise SVG badges summarizing GitHub repository statistics.

## About

`repobadge` turns live or cached GitHub repository metadata into compact SVG badges. It’s designed for quick embedding in READMEs, dashboards, or status pages.

The current badge emphasizes repository stars, with optional language color tagging. It supports multiple visual styles.

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
git clone <repo_url>
cd repobadge
PYTHONPATH=src python -m repobadge.cli .
```

## Usage

```bash
repobadge octocat/Hello-World --style flat
repobadge octocat/Hello-World --style plastic
python -m repobadge.cli octocat/Hello-World
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

## Tags

github, badge, svg, cli, developer-tools, static-analysis, oss

## License

MIT
