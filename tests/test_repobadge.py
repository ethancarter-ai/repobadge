from __future__ import annotations
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, "src")
from repobadge.core import compute_and_render, render_badge_svg, compute_summary, RepoSummary
from repobadge.cli import main, _build_parser


def test_flat_badge_svg_contains_text():
    summary = RepoSummary(repo="octocat/Hello-World", stars=42, forks=7, open_issues=2, language="Python")
    svg = render_badge_svg(summary, style="flat")
    assert "GitHub" in svg
    assert "★ 42" in svg
    assert '<svg' in svg
    assert svg.strip().endswith("</svg>")


def test_flat_square_badge_svg_contains_rounded_corners():
    summary = RepoSummary(repo="octocat/Hello-World", stars=10, forks=3, open_issues=0, language=None)
    svg = render_badge_svg(summary, style="flat-square")
    assert '<svg' in svg
    assert "</svg>" in svg


def test_unsupported_style_raises():
    summary = RepoSummary(repo="octocat/Hello-World", stars=10, forks=3, open_issues=0)
    with pytest.raises(ValueError):
        render_badge_svg(summary, style="unsupported")


def test_summary_without_language():
    summary = RepoSummary(repo="octocat/Hello-World", stars=10, forks=3, open_issues=0)
    svg = render_badge_svg(summary)
    assert "★ 10" in svg
    assert "•" not in svg


def test_summary_with_language():
    summary = RepoSummary(repo="octocat/Hello-World", stars=10, forks=3, open_issues=0, language="Python")
    svg = render_badge_svg(summary)
    assert "Python" in svg
    assert "★ 10" in svg


def test_offline_cli_success_stdout():
    with tempfile.TemporaryDirectory() as tmp:
        summary_path = Path(tmp) / "summary.json"
        summary_path.write_text(
            json.dumps({"repo": "octocat/Hello-World", "stars": 5, "forks": 1, "open_issues": 0, "language": "Rust"}),
            encoding="utf-8",
        )
        rc = main(["--no-fetch", "--summary-file", str(summary_path)])
        assert rc == 0


def test_offline_cli_missing_summary_file_fails():
    rc = main(["--no-fetch", "--summary-file", "/tmp/_repobadge_nonexistent.json"])
    assert rc == 1


def test_offline_cli_invalid_summary_file_fails():
    with tempfile.TemporaryDirectory() as tmp:
        bad_path = Path(tmp) / "bad.json"
        bad_path.write_text("{not json}", encoding="utf-8")
        rc = main(["--no-fetch", "--summary-file", str(bad_path)])
        assert rc == 1


def test_offline_cli_writes_output_file():
    with tempfile.TemporaryDirectory() as tmp:
        summary_path = Path(tmp) / "summary.json"
        summary_path.write_text(
            json.dumps({"repo": "octocat/Hello-World", "stars": 0, "forks": 0, "open_issues": 0}),
            encoding="utf-8",
        )
        out_path = Path(tmp) / "badge.svg"
        rc = main(["--no-fetch", "--summary-file", str(summary_path), "--output", str(out_path)])
        assert rc == 0
        assert out_path.exists()
        assert out_path.read_text(encoding="utf-8").strip().startswith("<svg")


def test_offline_cli_unknown_style_fails():
    parser = _build_parser()
    with pytest.raises(argparse.ArgumentError):
        parser.parse_args(["--no-fetch", "--style", "bad"])
