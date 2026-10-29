"""The VM password input must be paced, complete, and never printed in logs."""
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASH = shutil.which(os.environ.get("HERALD_OS_TEST_BASH", "bash"))


def run_input(tmp_path, secret):
    script = (ROOT / "linux/vm/type-passphrase.sh").read_text()
    # A byte sink stands in for QEMU; no socket, VM, or storage operation is performed.
    fakes = 'sleep() { printf "%s\\n" "$1" >>"$DELAYS"; }; socat() { printf "%s\\n" "$*" >"$ARGS"; cat >"$BYTES"; };\n'
    paths = {key: (tmp_path / key.lower()).as_posix() for key in ("DELAYS", "ARGS", "BYTES")}
    result = subprocess.run([BASH, "-c", fakes + script, "test", "serial.sock"],
                            env={**os.environ, **paths, "PASSPHRASE": secret}, capture_output=True, text=True)
    return result, {key: Path(value) for key, value in paths.items()}


def test_complete_password_and_enter_are_paced_before_disconnect(tmp_path):
    secret = "testpassword123"
    result, files = run_input(tmp_path, secret)
    assert result.returncode == 0, result.stderr
    assert files["BYTES"].read_bytes() == b"\x15" + secret.encode() + b"\r"
    assert files["DELAYS"].read_text().splitlines() == ["0.15"] * len(secret) + ["2"]
    assert files["ARGS"].read_text().strip() == "- UNIX-CONNECT:serial.sock"  # Bidirectional draining.
    assert secret not in result.stdout + result.stderr


@pytest.mark.parametrize("secret", ["", "UPPER", "with space", "one\ntwo"])
def test_invalid_test_input_does_not_open_the_socket(tmp_path, secret):
    result, files = run_input(tmp_path, secret)
    assert result.returncode == 2
    assert not files["BYTES"].exists()
