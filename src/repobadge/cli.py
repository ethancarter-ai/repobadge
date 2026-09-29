from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from . import render_badge_svg, RepoSummary

__all__ = ["main"]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repobadge",
        description="Generate SVG GitHub repo summary badges.",
        exit_on_error=False,
    )
    parser.add_argument("repo", nargs="?", default=None, help="Repository in owner/repo form.")
    parser.add_argument(
        "--style",
        default="flat",
        choices=["flat", "flat-square", "plastic"],
        help="Badge visual style.",
    )
    parser.add_argument("--token", default=None, help="Optional GitHub personal access token.")
    parser.add_argument("--no-fetch", action="store_true", help="Skip GitHub fetch; require --summary-file.")
    parser.add_argument("--summary-file", default=None, help="Path to JSON summary for offline rendering.")
    parser.add_argument("--output", default=None, help="Write SVG to file instead of stdout.")
    parser.add_argument("--lang-color-only", action="store_true", help="Render language color as badge body.")
    return parser


def _load_summary_from_file(path: str) -> RepoSummary:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"unable to read summary file: {exc}") from exc

    try:
        return RepoSummary(
            repo=data["repo"],
            stars=int(data["stars"]),
            forks=int(data["forks"]),
            open_issues=int(data["open_issues"]),
            language=data.get("language"),
        )
    except (TypeError, KeyError, ValueError) as exc:
        raise RuntimeError(f"invalid summary file contents: {exc}") from exc


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # pragma: no cover - exercised via tests
        return int(exc.code or 0)

    if not args.summary_file:
        print("repobadge: either default fetch or --summary-file is required", file=sys.stderr)
        return 1

    try:
        summary = _load_summary_from_file(args.summary_file)
    except RuntimeError as exc:
        print(f"repobadge: {exc}", file=sys.stderr)
        return 1

    try:
        svg = render_badge_svg(summary, style=args.style)
    except ValueError as exc:
        print(f"repobadge: {exc}", file=sys.stderr)
        return 1

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(svg)
        except OSError as exc:
            print(f"repobadge: unable to write output: {exc}", file=sys.stderr)
            return 1
    else:
        print(svg)

    return 0
