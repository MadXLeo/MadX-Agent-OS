#!/usr/bin/env bash
# Read-only acceptance checks inside the disposable installed guest, reached over its test SSH key.
set -euo pipefail
test -d /sys/firmware/efi
test -e /run/ostree-booted
test -s /var/lib/herald-os/firstboot-done
bootc status --format=json | python3 -c '
import json, sys
status = json.load(sys.stdin)
assert status.get("status", {}).get("booted"), "no booted deployment"
print(json.dumps(status, indent=2))'
ostree admin status
systemctl is-active NetworkManager firewalld greetd
for name in firstboot firstboot-apps hermes login reset; do
  old="$(systemctl show -p Id --value "herald-os-$name.service")"
  new="$(systemctl show -p Id --value "madx-agent-os-$name.service")"
  [[ "$old" == "herald-os-$name.service" && "$new" == "$old" ]]
done
[[ "$(readlink -f /usr/bin/madx-agent-os)" == "$(readlink -f /usr/bin/herald-os)" ]]
madx-agent-os commands >/dev/null
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
for suffix in service timer; do
  old="$(systemctl --user show -p Id --value "herald-os-update-check.$suffix")"
  new="$(systemctl --user show -p Id --value "madx-agent-os-update-check.$suffix")"
  [[ "$old" == "herald-os-update-check.$suffix" && "$new" == "$old" ]]
done
shopt -s nullglob
sockets=("$XDG_RUNTIME_DIR"/niri.*.sock)
(( ${#sockets[@]} == 1 ))
export NIRI_SOCKET="${sockets[0]}"
niri msg --json windows | python3 -c '
import json, sys
windows = json.load(sys.stdin)
assert any(w.get("app_id") in ("herald-os", "madx-agent-os", "MadX Agent OS", "Herald OS") for w in windows), "no desktop window"
print("MADX_DESKTOP_WINDOW=1")'
echo MADX_GUEST_CORE_PASSED=1
expected_hermes="${1:-}"
[[ -z "$expected_hermes" || "$expected_hermes" =~ ^[0-9a-f]{40}$ ]] || exit 2
echo "MADX_HERMES_TESTED_PIN=$expected_hermes"
if madx-agent-os hermes-command >/dev/null 2>&1; then
  echo MADX_HERMES_COMMAND_AVAILABLE=1
else
  echo MADX_HERMES_COMMAND_AVAILABLE=0
fi
if [[ -d "$HOME/.hermes/hermes-agent/.git" ]]; then
  installed_hermes="$(git -C "$HOME/.hermes/hermes-agent" rev-parse HEAD)"
  echo "MADX_HERMES_INSTALLED_REVISION=$installed_hermes"
  if [[ -n "$expected_hermes" && "$installed_hermes" != "$expected_hermes" ]]; then
    echo MADX_HERMES_REVISION_DRIFT=1
  fi
else
  echo MADX_HERMES_INSTALLED_REVISION=unknown
fi
# This does not certify model-backed Hermes chat or update/rollback. Those are separate gates.
