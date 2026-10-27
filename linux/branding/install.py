#!/usr/bin/env python3
"""Add MadX aliases to an existing installation, without moving data or enabling units.

All changes are below an explicitly supplied root. Run during image/package creation,
or from the tarball installer. Existing names remain the implementation and rollback
anchor. Conflicting files are never replaced. This script never touches disks or EFI.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRODUCT = json.loads((HERE / "product.json").read_text(encoding="utf-8"))


def alias_plan(root: Path, layout: str) -> dict[Path, str]:
    prefix = "usr/local" if layout in ("dev", "tarball") else "usr"
    paths: dict[Path, str] = {}
    # Read names from the shipped sources, not arbitrary executables on the host.
    names = [p.name for p in (HERE.parent / "bin").glob("herald-os*") if p.is_file()]
    names += ["herald-os-session", "herald-os-compositor", "herald-os-niri-nested"]
    for name in names:
        old = root / prefix / "bin" / name
        if old.exists() or old.is_symlink():
            paths[old.with_name(name.replace("herald-os", PRODUCT["slug"], 1))] = name
    shares = [(f"{prefix}/share/{PRODUCT['slug']}", "herald-os-linux" if layout == "dev" else "herald-os"),
              (f"opt/{PRODUCT['slug']}", "herald-os")]
    for relative, target in shares:
        dest = root / relative
        if (dest.parent / target).exists():
            paths[dest] = target
    for location in ("usr/lib/systemd/system", "usr/lib/systemd/user", "usr/local/lib/systemd/user"):
        for unit in (HERE.parent / "session").glob("herald-os-*.*"):
            if unit.suffix in (".service", ".timer") and (root / location / unit.name).is_file():
                paths[root / location / unit.name.replace("herald-os", PRODUCT["slug"], 1)] = unit.name
        for name in ("firstboot", "firstboot-apps", "hermes", "login", "reset"):
            old = root / location / f"herald-os-{name}.service"
            if old.is_file():
                paths[old.with_name(f"{PRODUCT['slug']}-{name}.service")] = old.name
    for prefix in ("usr", "usr/local"):
        old = root / prefix / "share/icons/hicolor/512x512/apps/herald-os.png"
        if old.is_file():
            paths[old.with_name(f"{PRODUCT['slug']}.png")] = old.name
    return paths


def validate(root: Path, plan: dict[Path, str]) -> None:
    """Preflight the whole plan so a conflict cannot leave a partial migration."""
    for dest, target in plan.items():
        # Never traverse a symlinked parent out of a staged root (or into another user's data).
        for parent in dest.relative_to(root).parents:
            if (root / parent).is_symlink():
                raise ValueError(f"refusing symlinked parent: {root / parent}")
        if dest.is_symlink():
            if os.readlink(dest) != target:
                raise ValueError(f"conflicting alias: {dest}")
        elif dest.exists():
            raise ValueError(f"existing file or directory: {dest}")


def install(root: Path, layout: str) -> int:
    root = root.absolute()
    plan = alias_plan(root, layout)
    validate(root, plan)
    created = []
    try:
        for dest, target in plan.items():
            if not dest.is_symlink():
                dest.symlink_to(target, target_is_directory=(dest.parent / target).is_dir())
                created.append(dest)
    except OSError:
        # Roll back only links created by this invocation. Never touch existing state.
        for dest in reversed(created):
            if dest.is_symlink() and os.readlink(dest) == plan[dest]:
                dest.unlink()
        raise
    return len(created)


def remove(root: Path, layout: str) -> int:
    root = root.absolute()
    plan = alias_plan(root, layout)
    validate(root, plan)
    removed = 0
    for dest, target in plan.items():
        if dest.is_symlink() and os.readlink(dest) == target:
            dest.unlink()
            removed += 1
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--layout", required=True, choices=("image", "dev", "arch", "tarball"))
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("installation is supported only on Linux; use isolated tests on other hosts")
    count = (remove if args.remove else install)(args.root, args.layout)
    print(f"{PRODUCT['name']}: {count} compatibility aliases {'removed' if args.remove else 'added'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
