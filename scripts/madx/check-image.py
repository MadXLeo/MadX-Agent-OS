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
    "usr/lib/systemd/user/madx-graphical-session.service",
    "usr/share/herald-os/hermes-bundled.json",
    "usr/lib/hermes-agent/uv.lock",
    "usr/lib/hermes-agent/dependencies.txt",
    "usr/lib/hermes-agent/hermes_cli/subcommands/dashboard.py",
    "usr/share/madx-model/LICENSE", "usr/libexec/madx-model/llama.cpp-LICENSE",
    "usr/lib/systemd/user/madx-local-model.service",
)


def inspect(root: Path, product: dict, assets: dict, nvidia: bool = False) -> dict:
    failures = []
    def require(ok, message):
        if not ok:
            failures.append(message)
    for name in REQUIRED:
        require((root / name).is_file(), f"missing file: {name}")
    executable = [f"usr/bin/{name}" for name in COMMANDS] + [
        "usr/bin/madx-render-device", "usr/bin/pgrep",
        "usr/share/herald-os/app/herald-os", "usr/libexec/herald-os/firstboot.sh",
        "usr/libexec/herald-os/reset-helper",
        "usr/bin/hermes", "usr/lib/hermes-agent/venv/bin/python",
        "usr/bin/madx-local-model", "usr/libexec/madx-model/llama-server",
    ]
    for name in executable:
        require((root / name).is_file() and os.access(root / name, os.X_OK), f"missing executable: {name}")
    for tool in ("lspci", "mokutil"):
        require(any((root / directory / tool).is_file() and os.access(root / directory / tool, os.X_OK)
                    for directory in ("usr/bin", "usr/sbin")), f"missing diagnostic tool: {tool}")
    try:
        runtime = root / "usr/lib/hermes-agent"
        bundle = json.loads((root / "usr/share/herald-os/hermes-bundled.json").read_text())
        pin = next(line[4:] for line in (Path(__file__).resolve().parents[2] / "upstream/UPSTREAM.lock").read_text().splitlines() if line.startswith("sha="))
        require(bundle["revision"] == pin == (runtime / ".herald-os-upstream-sha").read_text().strip(),
                "bundled Hermes revision differs from source pin")
        require(bundle["lockSha256"] == hashlib.sha256((runtime / "uv.lock").read_bytes()).hexdigest(),
                "bundled Hermes dependency lock hash differs")
        require(bundle["automaticDependencyDownloads"] is False, "bundled Hermes permits automatic dependency downloads")
        require(bundle["modelWeightsBundled"] is True, "offline model missing from bundle manifest")
        model_dir = root / "usr/share/madx-model"
        model = json.loads((model_dir / "model.json").read_text())
        pinned_model = json.loads((Path(__file__).resolve().parents[2] / "linux/image/offline-model.json").read_text())
        require(model == pinned_model, "offline model manifest differs from source")
        weights = model_dir / pinned_model["file"]
        with weights.open("rb") as stream:
            require(weights.stat().st_size == pinned_model["bytes"] and
                    hashlib.file_digest(stream, "sha256").hexdigest() == pinned_model["sha256"],
                    "offline model file does not match its pinned size and SHA-256")
    except (OSError, ValueError, KeyError, StopIteration):
        require(False, "bundled Hermes provenance missing or invalid")
    for name in COMMANDS:
        alias = root / "usr/bin" / name.replace("herald-os", product["slug"], 1)
        require(alias.is_symlink() and os.readlink(alias) == name, f"wrong command alias: {alias.name}")
    primary = root / "usr/bin" / product["command"]
    require(primary.is_symlink() and os.readlink(primary) == "herald-os",
            f"wrong primary command alias: {primary.name}")
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
        for kernel in kernels.glob("*/vmlinuz"):
            for module in ("nvidia", "nvidia-drm", "nvidia-modeset", "nvidia-uvm"):
                require(any(kernel.parent.glob(f"**/{module}.ko*")), f"{kernel.parent.name}: {module} module missing")
        require(any(kernels.glob("**/nvidia.ko*")), "NVIDIA kernel module missing")
        cert = root / "etc/pki/akmods/certs/akmods-ublue.der"
        require(cert.is_file() and hashlib.sha256(cert.read_bytes()).hexdigest() ==
                "4e5c68474cb133fd8984d9599762cece9100c3e6cd8a9709aeaabd85dd9e70d1",
                "NVIDIA Secure Boot enrollment certificate missing or changed")
        kargs = root / "usr/lib/bootc/kargs.d/20-herald-os-nvidia.toml"
        require(kargs.is_file() and '"nvidia-drm.modeset=1"' in kargs.read_text(),
                "NVIDIA DRM modesetting argument missing")
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
