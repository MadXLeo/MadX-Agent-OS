#!/usr/bin/env python3
"""Exhaustive case-insensitive source inventory. Classification is triage, not an exemption.

One row per text occurrence and per matching filename. Binary content is not decoded or
claimed to be audited. Generated reports are excluded to prevent recursive self-counting.
No source excerpts are copied to the report. Run from any directory; never edits source.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = {"docs/madx/HERALD_INVENTORY.csv", "docs/madx/HERALD_INVENTORY.json"}
RULES = json.loads((ROOT / "branding/legacy-allowlist.json").read_text(encoding="utf-8"))["rules"]
CATEGORIES = {
    "1": "Public-facing product branding",
    "2": "Terminal commands and help output",
    "3": "Internal implementation names",
    "4": "Compatibility-sensitive APIs and persisted data",
    "5": "Tests, fixtures and documentation",
    "6": "Historical records and legally required attribution",
}


def classify(path, line, token):
    if path in ('branding/legacy-allowlist.json', 'scripts/madx/inventory-branding.py'): return "5", "audit recognizer and its rationale; not displayed product copy"
    if path == 'docs/madx/VALIDATION_RESULTS.json': return "6", "historical test evidence; preserve original test names"
    for rule in RULES:
        if path in rule['files'] and re.search(rule['pattern'], line):
            return ("6" if rule['category'] in ('required-attribution', 'historical-migration') else "4"), rule['reason']
    if re.search(r"(^|/)(LICENSE[^/]*|NOTICE|COPYING[^/]*)$|build/licenses/|^docs/(adr/|internal/|DECISIONS\.md)|^upstream/README\.md", path, re.I):
        return "6", "retain attribution or historical record"
    if re.search(r"(^|/)(tests?|fixtures?)/|\.test\.[cm]?[jt]sx?$|\.md$", path):
        return "5", "test/guide reference; current instructions must match shipped behavior"
    if token == "herald-os" and re.search(r"\b(print|die|raise|description)\b", line):
        return "2", "review diagnostic/help text; do not rename the referenced runtime blindly"
    if re.search(r"heraldOS|herald_os|HeraldOS|@herald|[/\\]|:|HERALD_|herald-os-|herald-(ocean|graphite)", token):
        return "4", "API/path/command identifier; preserve consumers or provide tested migration"
    if re.match(r"\s*(#|//|/\*|\*)", line):
        return "3", "implementation comment; no automatic public-copy exemption"
    if re.search(r"Herald\s+(OS|Office|Canvas|Docs|Sheets|Slides|Calc)|[\"']Herald[\"']", line):
        return "1", "review potential product copy in its actual display context"
    if token.lower() == "herald-os" and re.search(r"\b(exec|spawn|which|command|Exec=)\b", line):
        return "4", "legacy executable consumer shares the same MadX implementation"
    return "3", "implementation/configuration reference; inspect consumers before renaming"


def occurrences(path, source):
    for number, line in enumerate(source.splitlines(), 1):
        for match in re.finditer("herald", line, re.I):
            start, end = match.span()
            while start > 0 and re.match(r"[\w@./\\:-]", line[start - 1]): start -= 1
            while end < len(line) and re.match(r"[\w@./\\:-]", line[end]): end += 1
            category, reason = classify(path, line, line[start:end])
            yield {"file": path, "line": number, "column": match.start() + 1,
                   "kind": "text", "category": category, "reason": reason}


def inventory(root):
    files = sorted(set(subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root).decode().split("\0")) - {""})
    rows, binaries, unreadable = [], [], []
    for name in files:
        if name in OUTPUTS: continue
        path = root / name
        if not path.is_file(): continue
        for match in re.finditer("herald", name, re.I):
            rows.append({"file": name, "line": 0, "column": match.start() + 1, "kind": "filename",
                         "category": "4", "reason": "filename contract; verify packaging and consumers before moving"})
        raw = path.read_bytes()
        if b"\0" in raw:
            binaries.append(name)
            continue
        try: source = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            unreadable.append(name)
            continue
        rows.extend(occurrences(name, source))
    return rows, binaries, unreadable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the source inventory into docs/madx")
    args = parser.parse_args()
    rows, binaries, unreadable = inventory(ROOT)
    summary = {
        "schema": 1, "scope": "Tracked and non-ignored working-tree files; every UTF-8 text match plus matching filenames",
        "classification": "Rule-based triage; categories are not automatic approval to retain user-visible branding",
        "textOccurrences": sum(row["kind"] == "text" for row in rows),
        "filesWithTextOccurrences": len({row["file"] for row in rows if row["kind"] == "text"}),
        "filenameOccurrences": sum(row["kind"] == "filename" for row in rows),
        "categories": {key: {"name": value, "textOccurrences": sum(row["category"] == key and row["kind"] == "text" for row in rows)} for key, value in CATEGORIES.items()},
        "excludedGeneratedReports": sorted(OUTPUTS), "binaryContentNotAudited": binaries,
        "undecodableContentNotAudited": unreadable,
        "remainingGates": ["Review lowercase identifiers in actual public diagnostic output", "Inspect newly built Linux package and image", "Visual review of installed boot/login/desktop"]
    }
    if args.write:
        (ROOT / "docs/madx/HERALD_INVENTORY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=["file", "line", "column", "kind", "category", "reason"])
        writer.writeheader()
        writer.writerows(rows)
        (ROOT / "docs/madx/HERALD_INVENTORY.csv").write_text(stream.getvalue(), encoding="utf-8", newline="")
    print(json.dumps({key: value for key, value in summary.items() if key not in ("binaryContentNotAudited",)}, indent=2))


if __name__ == "__main__": main()
