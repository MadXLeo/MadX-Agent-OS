#!/usr/bin/env python3
"""Prepare disposable-VM installer diagnostics; never runs storage or firmware commands."""
import argparse
from pathlib import Path, PurePosixPath
import re
import shlex


def grub_for_test(source: str) -> str:
    """Boot the ISO through its own UEFI loader, with only test arguments changed."""
    lines, changed = [], 0
    for line in source.splitlines():
        if re.match(r"\s*(linux|linuxefi)\s+", line):
            line = re.sub(r"\s+inst\.ks=\S+", "", line)
            line = re.sub(r"\s+(quiet|rhgb)(?=\s|$)", "", line)
            line += " inst.ks=http://10.0.2.2:8000/ks.cfg inst.text console=ttyS0,115200"
            changed += 1
        elif re.match(r"\s*set\s+(timeout|default)=", line):
            continue
        lines.append(line)
    if not changed:
        raise ValueError("no installer kernel entry in ISO GRUB configuration")
    return "set timeout=3\nset default=0\n" + "\n".join(lines) + "\n"


def has_deployment(source: str, iso_root: Path | None = None, active: tuple[Path, ...] = ()) -> bool:
    """Check real kickstart directives, including files extracted from this ISO only."""
    found, section = False, False
    for line in source.splitlines():
        line = line.strip()
        if line == "%end":
            section = False
            continue
        if section or not line or line.startswith("#"):
            continue
        words = shlex.split(line, comments=True)
        if not words:
            continue
        command = words[0]
        if command == "%include":
            if iso_root is None or len(words) != 2:
                raise ValueError("kickstart include requires extracted ISO files")
            path = PurePosixPath(words[1])
            try:
                relative = path.relative_to("/run/install/repo")
            except ValueError as error:
                raise ValueError("kickstart include is outside the ISO repository") from error
            if ".." in relative.parts:
                raise ValueError("kickstart include escapes the ISO repository")
            root = iso_root.resolve()
            included = root.joinpath(*relative.parts).resolve()
            if not included.is_relative_to(root) or not included.is_file():
                raise ValueError("kickstart include is missing or outside the extracted ISO")
            if included in active or len(active) >= 32:
                raise ValueError("cyclic or excessive kickstart includes")
            found = has_deployment(included.read_text(encoding="utf-8"), root, (*active, included)) or found
        elif command.startswith("%"):
            section = True
        elif command in ("ostreecontainer", "ostreesetup", "liveimg") and len(words) > 1:
            found = True
    return found


def diagnostics(source: str, iso_root: Path | None = None) -> str:
    if not has_deployment(source, iso_root):
        raise ValueError("ISO kickstart has no system deployment command; refuse an empty install")
    body = r'''
exec >/dev/ttyS0 2>&1
echo MADX_INSTALLER_DIAGNOSTICS_BEGIN
test -d /sys/firmware/efi && echo MADX_INSTALLER_UEFI=1
lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS
findmnt
efibootmgr -v || true
for file in /tmp/anaconda.log /tmp/storage.log /tmp/program.log /tmp/packaging.log /tmp/dnf.log; do
  if test -f "$file"; then echo "MADX_LOG=$file"; tail -n 3000 "$file"; fi
done
for target in /mnt/sysroot /mnt/sysimage; do
  if test -d "$target/ostree/deploy"; then
    echo "MADX_DEPLOYMENTS=$target"
    find "$target/ostree/deploy" -maxdepth 4 -name '*.origin' -print
    find "$target/boot" -maxdepth 5 -name grub.cfg -print
  fi
done
echo MADX_INSTALLER_DIAGNOSTICS_END
'''
    return source.rstrip() + "\n\n%onerror\n" + body + "%end\n\n%post --nochroot\n" + body + "%end\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("grub", "diagnostics"))
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--iso-root", type=Path, help="Kickstart files extracted from the verified ISO")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    value = grub_for_test(source) if args.mode == "grub" else diagnostics(source, args.iso_root)
    args.destination.write_text(value, encoding="utf-8")
