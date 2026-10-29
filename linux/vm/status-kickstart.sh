#!/usr/bin/env bash
# Append a test-only unit that captures privileged read-only status after first boot.
# It grants no sudo access and is never added to production installer configuration.
set -euo pipefail
capture="$(dirname "${BASH_SOURCE[0]}")/capture-guest-status.sh"
cat <<'KICKSTART'
%post --interpreter=/usr/bin/bash --erroronfail
set -euo pipefail
install -d -m 0755 /etc/madx-validation
cat >/etc/madx-validation/capture-status.sh <<'MADX_STATUS_SCRIPT'
KICKSTART
cat "$capture"
cat <<'KICKSTART'
MADX_STATUS_SCRIPT
chmod 0755 /etc/madx-validation/capture-status.sh
cat >/etc/systemd/system/madx-validation-status.service <<'MADX_STATUS_UNIT'
[Unit]
Description=Disposable VM deployment evidence
Requires=herald-os-firstboot.service
After=herald-os-firstboot.service
ConditionVirtualization=yes
ConditionPathExists=/run/ostree-booted

[Service]
Type=oneshot
User=root
RuntimeDirectory=madx-validation
RuntimeDirectoryMode=0755
RuntimeDirectoryPreserve=yes
ExecStart=/usr/bin/bash /etc/madx-validation/capture-status.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
MADX_STATUS_UNIT
systemctl enable madx-validation-status.service
%end
KICKSTART
