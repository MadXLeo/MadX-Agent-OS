#!/usr/bin/env python3
"""Project-local Graphify, with no model backend or global assistant changes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[2]
ENV = ROOT / ".venv" / "graphify"
PYTHON = ENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
OUT = ROOT / "graphify-out"
GRAPH = OUT / "graph.json"
STAMP = OUT / "madx-index.json"
VERSION = "0.9.101"


def local_env():
    env = os.environ.copy()
    env.update(GRAPHIFY_BACKEND="none", GRAPHIFY_QUERY_LOG_DISABLE="1",
               GRAPHIFY_NO_CLOUD_CTA="1", PYTHONHASHSEED="0", PYTHONUTF8="1")
    # Do not inherit backend/remote graph configuration from another project.
    for name in list(env):
        if name.startswith("GRAPHIFY_") and name not in {
            "GRAPHIFY_BACKEND", "GRAPHIFY_QUERY_LOG_DISABLE", "GRAPHIFY_NO_CLOUD_CTA"
        }:
            del env[name]
    return env


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def fingerprint():
    """Include working edits and new nonignored files, not just commit identity."""
    names = sorted(set(git("ls-files", "-z", "--cached", "--others",
                           "--exclude-standard").split(b"\0")) - {b""})
    digest = hashlib.sha256()
    for name in names:
        path = ROOT / os.fsdecode(name)
        digest.update(name + b"\0")
        if path.is_symlink():
            digest.update(b"symlink:" + os.fsencode(os.readlink(path)))
        elif path.is_file():
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
        else:
            digest.update(b"missing")
        digest.update(b"\0")
    return digest.hexdigest()


def state():
    if not GRAPH.is_file() or not STAMP.is_file():
        return "missing"
    try:
        stamp = json.loads(STAMP.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return "stale"
    return "fresh" if (stamp.get("working_tree_sha256") == fingerprint()
                       and stamp.get("graphify_version") == VERSION) else "stale"


def run(*args):
    if not PYTHON.is_file():
        raise SystemExit("Run: python scripts/madx/graphify.py setup")
    version = subprocess.check_output(
        [str(PYTHON), "-c", "from importlib.metadata import version; print(version('graphifyy'))"],
        cwd=ROOT, env=local_env(), text=True).strip()
    if version != VERSION:
        raise SystemExit(f"Expected Graphify {VERSION}, found {version}; run setup.")
    subprocess.run([str(PYTHON), "-m", "graphify", *args], cwd=ROOT,
                   env=local_env(), check=True)


def build():
    before = fingerprint()
    # Invalidate old success evidence even if the new extraction fails halfway.
    STAMP.unlink(missing_ok=True)
    run("extract", str(ROOT), "--code-only", "--no-cluster", "--max-workers", "4")
    run("cluster-only", str(ROOT), "--no-label")
    if fingerprint() != before:
        raise SystemExit("Source changed during indexing. Run build again before trusting the graph.")
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    result = {
        "graphify_version": VERSION,
        "source_head": git("rev-parse", "HEAD").decode().strip(),
        "working_tree_sha256": before,
        "scope": "local code-only AST; no semantic model calls",
        "nodes": len(graph.get("nodes", [])),
        "edges": len(graph.get("links", graph.get("edges", []))),
    }
    STAMP.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("setup", "build", "status", "query", "explain", "path"))
    parser.add_argument("terms", nargs="*")
    args = parser.parse_args()
    if args.command == "setup":
        if not PYTHON.is_file():
            venv.EnvBuilder(with_pip=True).create(ENV)
        subprocess.run([str(PYTHON), "-m", "pip", "install", "--disable-pip-version-check",
                        "--only-binary=:all:", "--index-url", "https://pypi.org/simple",
                        "-r", str(ROOT / "scripts/madx/graphify-requirements.txt")], check=True)
        subprocess.run([str(PYTHON), "-m", "pip", "check"], check=True)
    elif args.command == "build":
        build()
    elif args.command == "status":
        status = state()
        print(f"Graphify index: {status}")
        print("Progress: docs/madx/PROJECT_STATUS.md; tasks: docs/madx/WORK_ITEMS.json")
        return 0 if status == "fresh" else 1
    else:
        expected = 2 if args.command == "path" else 1
        if len(args.terms) != expected or any(t.startswith("-") for t in args.terms):
            parser.error(f"{args.command} needs {expected} quoted search term(s), without flags")
        status = state()
        if status == "missing":
            raise SystemExit("No index. Run: python scripts/madx/graphify.py build")
        if status == "stale":
            print("WARNING: stale index; rebuild and verify source locations.", file=sys.stderr)
        run(args.command, *args.terms, "--graph", str(GRAPH))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
