#!/usr/bin/env python3
"""Inspect a built MadX root filesystem. Read-only; does not boot or install it."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

SYSTEM_UNITS = ("firstboot", "firstboot-apps", "hermes", "login", "reset")
COMMANDS = ("herald-os", "herald-os-app", "herald-os-session", "herald-os-compositor",
            "herald-os-update", "herald-os-tarball", "herald-os-gpu-check")
REQUIRED = (
    "usr/share/herald-os/app/resources/app.asar",
    "usr/share/herald-os/app/resources/herald-os-bridge/plugin.yaml",
    "usr/share/herald-os/niri/config.kdl",
    "usr/share/herald-os/themes/madx-graphite/theme.json",
    "usr/share/wayland-sessions/herald-os.desktop",
    "usr/share/plymouth/themes/herald-os/herald-os.plymouth",
    "usr/share/plymouth/themes/herald-os/logo.png",
    "usr/lib/systemd/system/greetd.service.d/herald-os-login.conf",
    "usr/lib/bootc/kargs.d/10-herald-os.toml",
)


def inspect(root: Path, product: dict, assets: dict, nvidia: bool = False) -> dict:
    failures = []
    def require(ok, message):
        if not ok:
            failures.append(message)
    for name in REQUIRED:
        require((root / name).is_file(), f"missing file: {name}")
    executable = [f"usr/bin/{name}" for name in COMMANDS] + [
        "usr/share/herald-os/app/herald-os", "usr/libexec/herald-os/firstboot.sh",
        "usr/libexec/herald-os/reset-helper",
    ]
    for name in executable:
        require((root / name).is_file() and os.access(root / name, os.X_OK), f"missing executable: {name}")
    for name in COMMANDS:
        alias = root / "usr/bin" / name.replace("herald-os", product["slug"], 1)
        require(alias.is_symlink() and os.readlink(alias) == name, f"wrong command alias: {alias.name}")
    for location, names in (
        ("system", [f"herald-os-{name}.service" for name in SYSTEM_UNITS]),
        ("user", ["herald-os-update-check.service", "herald-os-update-check.timer"]),
    ):
        for name in names:
            unit = root / f"usr/lib/systemd/{location}" / name
            alias = unit.with_name(name.replace("herald-os", product["slug"], 1))
            require(unit.is_file(), f"missing unit: {name}")
            require(alias.is_symlink() and os.readlink(alias) == name, f"wrong unit alias: {alias.name}")
    for name in SYSTEM_UNITS:
        require((root / f"etc/systemd/system/multi-user.target.wants/herald-os-{name}.service").is_symlink(),
                f"unit not enabled: herald-os-{name}.service")
    release = root / "usr/lib/os-release"
    values = dict(line.split("=", 1) for line in release.read_text().splitlines() if "=" in line) if release.is_file() else {}
    require(values.get("ID", "").strip('"') == "fedora", "Fedora identity missing")
    require(values.get("IMAGE_ID", "").strip('"') == product["slug"], "MadX image identity missing")
    require(values.get("IMAGE_VERSION", "").strip('"') == product["version"], "image version differs from source")
    kernels = root / "usr/lib/modules"
    require(any(p.is_file() and (p.parent / "initramfs.img").is_file() for p in kernels.glob("*/vmlinuz")),
            "no kernel/initramfs pair")
    sandbox = root / "usr/share/herald-os/app/chrome-sandbox"
    require(sandbox.is_file() and sandbox.stat().st_uid == 0 and bool(sandbox.stat().st_mode & 0o4000),
            "Chromium sandbox is not setuid root")
    for installed, source in (
        ("usr/share/icons/hicolor/512x512/apps/herald-os.png", "apps/desktop/build/icon.png"),
        ("usr/share/plymouth/themes/herald-os/logo.png", "linux/plymouth/herald-os/logo.png"),
    ):
        path = root / installed
        require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == assets["files"][source],
                f"artwork hash differs: {installed}")
    if nvidia:
        require(any(kernels.glob("**/nvidia.ko*")), "NVIDIA kernel module missing")
    return {"scope": "built image filesystem; no boot or hardware proof", "passed": not failures,
            "nvidia": nvidia, "failures": failures}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True, help="source branding directory")
    parser.add_argument("--nvidia", action="store_true")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("actual image inspection requires Linux; unit fixtures can run elsewhere")
    result = inspect(args.root, json.loads((args.metadata / "product.json").read_text()),
                     json.loads((args.metadata / "assets.json").read_text()), args.nvidia)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
