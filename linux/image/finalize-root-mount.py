#!/usr/bin/env python3
"""Move physical root options to rootflags in a fresh offline Anaconda target.

The installed / is a composefs overlay, which rejects Btrfs remount options.
See https://github.com/bootc-dev/bootc/issues/971 and Fedora bug 2332319.
This helper never selects, partitions or formats a disk.
"""
import argparse
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile


class CustomLayout(ValueError):
    """Keep existing installer behavior for layouts outside the reproduced Btrfs case."""


def boot_args(root: Path) -> list[str]:
    entries = list((root / "boot/loader/entries").glob("*.conf"))
    if len(entries) != 1:
        raise ValueError("expected one boot entry in a fresh installation")
    entry = entries[0].resolve()
    if not entry.is_relative_to(root):
        raise ValueError("boot entry escapes the installation target")
    options = [line[8:] for line in entry.read_text().splitlines() if line.startswith("options ")]
    if len(options) != 1:
        raise ValueError("expected one boot options line")
    return shlex.split(options[0])


def plan(fstab: str, args: list[str]) -> tuple[str, str] | None:
    lines = fstab.splitlines(keepends=True)
    roots = [(i, line.split()) for i, line in enumerate(lines)
             if line.strip() and not line.lstrip().startswith("#")
             and len(line.split()) >= 2 and line.split()[1] == "/"]
    if not roots:
        return None
    if len(roots) != 1:
        raise ValueError("ambiguous root mount entries")
    index, fields = roots[0]
    if len(fields) != 6 or fields[2] != "btrfs" or not fields[0].startswith("UUID="):
        raise CustomLayout("only the verified Anaconda Btrfs root layout is supported")
    if [arg for arg in args if arg.startswith("root=")] != ["root=" + fields[0]]:
        raise ValueError("boot entry and fstab name different root filesystems")
    if not any(arg.startswith("ostree=") for arg in args):
        raise ValueError("boot entry is not an OSTree deployment")
    existing = [arg.partition("=")[2] for arg in args if arg.startswith("rootflags=")]
    if len(existing) > 1:
        raise ValueError("ambiguous rootflags arguments")
    flags = {}
    for option in (existing[0].split(",") if existing else []) + fields[3].split(","):
        if option == "defaults" or option.startswith("x-systemd."):
            continue
        if option in {"auto", "noauto", "nofail", "user", "users", "nouser", "_netdev"}:
            raise ValueError("unexpected policy option on the root filesystem")
        if not re.fullmatch(r"[A-Za-z0-9_./:=+-]+", option):
            raise ValueError("unsupported root mount option")
        key = option.partition("=")[0]
        if key in flags and flags[key] != option:
            raise ValueError("conflicting root mount options")
        flags[key] = option
    if "subvol" not in flags or not flags["subvol"].startswith("subvol="):
        raise ValueError("missing Btrfs root subvolume")
    if "ro" in flags and "rw" in flags:
        raise ValueError("conflicting root access modes")
    lines[index] = "# MadX: physical root options are preserved in rootflags; / uses composefs.\n# " + lines[index]
    return "".join(lines), "rootflags=" + ",".join(flags.values())


def finalize(root: Path, run=subprocess.run) -> bool:
    root = root.resolve()
    if root == Path(root.anchor):
        raise ValueError("an explicit offline installation target is required")
    release = (root / "usr/lib/os-release").read_text()
    if not re.search(r'^IMAGE_ID="?(madx-agent-os|herald-os)"?$', release, re.M):
        raise ValueError("target is not a MadX installation")
    if not (root / "sysroot/ostree/deploy").is_dir():
        raise ValueError("target has no mounted OSTree sysroot")
    fstab = root / "etc/fstab"
    if fstab.is_symlink() or not fstab.resolve().is_relative_to(root):
        raise ValueError("fstab escapes the installation target")
    original = fstab.read_text()
    if not any(line.split()[1:2] == ["/"] for line in original.splitlines()
               if line.strip() and not line.lstrip().startswith("#")):
        return False
    before = boot_args(root)
    try:
        updated, argument = plan(original, before)
    except CustomLayout as error:
        print(f"Root mount finalization not applied to this custom layout: {error}")
        return False
    # Anaconda uses this installed ostree command in the same target chroot.
    # Merge retains root=, rd.luks.uuid=, console= and unrelated kernel arguments.
    run(["chroot", str(root), "/usr/bin/ostree", "admin", "instutil", "set-kargs",
         "--merge", "--replace=" + argument], check=True)
    after = boot_args(root)
    retained = lambda values: [value for value in values if not value.startswith(("rootflags=", "ostree="))]
    if [arg for arg in after if arg.startswith("rootflags=")] != [argument] or retained(after) != retained(before):
        raise ValueError("boot options were not preserved; fstab remains unchanged")
    backup = fstab.with_name("fstab.madx-before-rootflags")
    if not backup.exists():
        shutil.copy2(fstab, backup)
    fd, name = tempfile.mkstemp(prefix=".fstab-madx-", dir=fstab.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(updated)
        os.chmod(name, fstab.stat().st_mode & 0o777)
        os.replace(name, fstab)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    print("MADX_ROOT_OPTIONS_MIGRATED=" + argument)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    finalize(parser.parse_args().root)
