#!/usr/bin/env python3
"""Prepare disposable-VM installer diagnostics; never runs storage or firmware commands."""
import argparse
from pathlib import Path
import re


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


def diagnostics(source: str) -> str:
    if not re.search(r"^(ostreecontainer|ostreesetup|liveimg)\s", source, re.M):
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
    args = parser.parse_args()
    value = (grub_for_test if args.mode == "grub" else diagnostics)(args.source.read_text())
    args.destination.write_text(value, encoding="utf-8")
