# Usage

```bash
repobadge <owner/repo> [--style flat|flat-square|plastic] [--output badge.svg]
```

Offline from a cached summary:

```bash
repobadge --summary-file repo.json --style plastic --output badge.svg
```

## Summary file format

```json
{
  "repo": "octocat/Hello-World",
  "stars": 1234,
  "forks": 56,
  "open_issues": 7,
  "language": "Python"
}
```

## Notes

* Network access is needed only when `--summary-file` is omitted.
* `parser.py` requires no third-party dependencies; it uses `urllib`.
