#!/usr/bin/env python3
"""Bind an unpublished ISO artifact to its source, image variant and packaged bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def identity(revision, variant):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("expected a full source commit SHA")
    if variant not in ("standard", "nvidia"):
        raise ValueError("unknown image variant")
    return "ghcr.io/madxleo/madx-agent-os" + ("-nvidia" if variant == "nvidia" else "")


def create(directory, revision, variant, image):
    repo = identity(revision, variant)
    if not image.startswith(repo + ":"):
        raise ValueError("image origin differs from selected variant")
    files = sorted(p for p in directory.glob("madx-agent-os-*-x86_64.iso*") if p.is_file())
    if not any(p.name.endswith(".iso") or ".iso.part" in p.name for p in files):
        raise ValueError("no ISO or split ISO in artifact")
    return {"schema": 1, "revision": revision, "variant": variant, "image": image,
            "scope": "unpublished image; no hardware acceptance",
            "files": {p.name: digest(p) for p in files}}


def verify(path, revision, variant):
    repo = identity(revision, variant)
    data = json.loads(path.read_text(encoding="utf-8"))
    if (data.get("schema"), data.get("revision"), data.get("variant")) != (1, revision, variant):
        raise ValueError("artifact source or variant mismatch")
    if not data.get("image", "").startswith(repo + ":"):
        raise ValueError("artifact image origin mismatch")
    files = data.get("files", {})
    if not files or not any(n.endswith(".iso") or ".iso.part" in n for n in files):
        raise ValueError("artifact has no ISO bytes")
    for name, expected in files.items():
        if "/" in name or "\\" in name or not re.fullmatch(r"madx-agent-os-[A-Za-z0-9_.-]+-x86_64\.iso[A-Za-z0-9_.-]*", name):
            raise ValueError("unsafe artifact filename")
        candidate = path.parent / name
        if candidate.is_symlink() or not candidate.is_file() or digest(candidate) != expected:
            raise ValueError(f"artifact checksum failed: {name}")
    actual = {p.name for p in path.parent.glob("madx-agent-os-*-x86_64.iso*")}
    if actual != set(files):
        raise ValueError("unexpected ISO files in artifact")
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("write", "verify"))
    parser.add_argument("path", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--variant", choices=("standard", "nvidia"), required=True)
    parser.add_argument("--image")
    args = parser.parse_args()
    if args.action == "write":
        if not args.image:
            parser.error("write needs --image")
        result = create(args.path.parent, args.revision, args.variant, args.image)
        args.path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        verify(args.path, args.revision, args.variant)
    print(f"ISO artifact {args.action}: {args.variant} @ {args.revision}")
