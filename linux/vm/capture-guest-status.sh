#!/usr/bin/env bash
# Read-only deployment evidence, run as root by a test-only unit in the disposable VM.
set -euo pipefail
umask 022
exec 2>/run/madx-validation/errors.log
systemctl --failed --no-legend --no-pager >/run/madx-validation/failed-units.txt
systemctl show systemd-remount-fs.service -p ActiveState -p SubState -p Result -p ExecMainStatus >/run/madx-validation/remount-status.txt
journalctl -b -u systemd-remount-fs.service --no-pager -n 150 >/run/madx-validation/remount-journal.txt
findmnt --json / >/run/madx-validation/root-mount.json
if [[ -f /etc/fstab ]]; then
  cat /etc/fstab >/run/madx-validation/fstab.txt
else
  printf 'No /etc/fstab\n' >/run/madx-validation/fstab.txt
fi
/usr/bin/bootc status --format=json >/run/madx-validation/bootc.json
/usr/bin/ostree admin status >/run/madx-validation/ostree.txt
printf 'complete\n' >/run/madx-validation/complete
