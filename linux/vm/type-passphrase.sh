#!/usr/bin/env bash
# Type the disposable test password at the observed serial prompt without a bulk UART write.
set -euo pipefail
socket="${1:?serial socket required}"
[[ "${PASSPHRASE:-}" =~ ^[a-z0-9]{1,128}$ ]] || { echo 'test passphrase must be lowercase letters/digits' >&2; exit 2; }
[[ "$socket" =~ ^[a-zA-Z0-9_./-]+$ ]] || { echo 'invalid serial socket path' >&2; exit 2; }
{
  # Clear any partial input. Keep the connection open while the emulated UART consumes each byte.
  printf '\025'
  for (( i=0; i<${#PASSPHRASE}; i++ )); do
    printf '%s' "${PASSPHRASE:i:1}"
    sleep 0.15
  done
  printf '\r'
  sleep 2
} | socat - "UNIX-CONNECT:$socket" >/dev/null
