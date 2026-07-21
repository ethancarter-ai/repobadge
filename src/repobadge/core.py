from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

from . import parser

__all__ = ["RepoSummary", "compute_summary", "render_badge_svg", "compute_and_render"]


@dataclass(frozen=True)
class RepoSummary:
    repo: str
    stars: int
    forks: int
    open_issues: int
    language: Optional[str] = None


def compute_summary(repo: str, *, token: Optional[str] = None) -> RepoSummary:
    data = parser.fetch_repo_data(repo, token=token)
    return RepoSummary(
        repo=data["full_name"],
        stars=int(data.get("stargazers_count", 0)),
        forks=int(data.get("forks_count", 0)),
        open_issues=int(data.get("open_issues_count", 0)),
        language=data.get("language"),
    )


def _slug_color(label: str) -> str:
    table = {
        "Python": "#3572A5",
        "JavaScript": "#f1e05a",
        "TypeScript": "#2b7489",
        "Rust": "#dea584",
        "Go": "#00ADD8",
        "Java": "#b07219",
        "C++": "#f34b7d",
        "C": "#555555",
        "Shell": "#89e051",
        "Ruby": "#701516",
    }
    return table.get(label, "#cccccc")


def render_badge_svg(summary: RepoSummary, style: str = "flat") -> str:
    style = style.lower()
    if style not in {"flat", "flat-square", "plastic"}:
        raise ValueError(f"Unsupported badge style: {style}")

    left = "GitHub"
    right = f"★ {summary.stars}"
    if summary.language:
        right = f"{summary.language} • ★ {summary.stars}"

    bg_left = "#555555"
    bg_right = _slug_color(summary.language) if summary.language else "#4CAF50"

    if style == "flat":
        radius = "0"
        divider = "0"
    elif style == "flat-square":
        radius = "4"
        divider = "0"
    else:
        radius = "50"
        divider = "2"

    left_width = 96
    right_width = 76
    total_width = left_width + right_width
    height = 20
    text_x_left = 6
    text_x_right = left_width + 6
    middle_y = 14

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="{total_width}" height="{height}" rx="{radius}" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <path fill="#555" d="M0 0h{left_width}v{height}H0z"/>
    <path fill="{bg_right}" d="M{left_width} 0h{right_width}v{height}H{left_width}z"/>
    <path fill="url(#b)" d="M0 0h{total_width}v{height}H0z"/>
  </g>
  <g fill="#fff" text-anchor="start" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{text_x_left}" y="{middle_y}">{left}</text>
    <text x="{text_x_right}" y="{middle_y}" fill="#010101" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">{right}</text>
    <text x="{text_x_right}" y="{middle_y}" fill="#fff" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">{right}</text>
  </g>
</svg>"""
    return svg.strip()


def compute_and_render(
    repo: str,
    *,
    style: str = "flat",
    token: Optional[str] = None,
) -> str:
    summary = compute_summary(repo, token=token)
    return render_badge_svg(summary, style=style)
