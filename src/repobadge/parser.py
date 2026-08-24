from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

__all__ = ["fetch_repo_data"]

_API = "https://api.github.com/repos/{repo}"
_USER_AGENT = "repobadge/0.1 (+https://github.com/ethancarter-ai/repobadge)"


def fetch_repo_data(repo: str, *, token: Optional[str] = None) -> Dict[str, Any]:
    url = _API.format(repo=repo)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", _USER_AGENT)
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API error {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to reach GitHub API: {exc.reason}") from exc

    summary_fields = {
        "full_name",
        "stargazers_count",
        "forks_count",
        "open_issues_count",
        "language",
    }
    missing = summary_fields.difference(data)
    if missing:
        raise RuntimeError(f"GitHub API response missing fields: {sorted(missing)}")

    return {field: data[field] for field in sorted(summary_fields)}
