#!/usr/bin/env python3
"""Reject validation ISOs from a different source revision or workflow before downloading them."""
import argparse
import json
import re
from pathlib import Path


def verify(run: dict, revision: str, repository: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("expected a full source commit SHA")
    expected = {
        "head_sha": revision,
        "path": ".github/workflows/image.yml",
        "event": "workflow_dispatch",
        "status": "completed",
        "conclusion": "success",
    }
    for key, value in expected.items():
        if run.get(key) != value:
            raise ValueError(f"image run {key}: expected {value!r}, got {run.get(key)!r}")
    for key in ("repository", "head_repository"):
        if (run.get(key) or {}).get("full_name", "").lower() != repository.lower():
            raise ValueError(f"image run {key} is not the requested repository")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--repository", required=True)
    args = parser.parse_args()
    verify(json.loads(args.report.read_text(encoding="utf-8")), args.revision, args.repository)
    print(f"Validated image workflow source: {args.repository}@{args.revision}")
