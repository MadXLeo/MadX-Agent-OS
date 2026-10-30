"""The test VM captures root-only status without granting the SSH account root access."""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASH = shutil.which(os.environ.get("HERALD_OS_TEST_BASH", "bash"))


def test_status_fragment_is_a_post_install_test_unit_with_no_privilege_grant():
    # Match the existing installer tests: CI installs this parser and rejects missing-parser
    # skips on Linux; local environments without it can still run the other test families.
    parser_module = pytest.importorskip("pykickstart.parser")
    from pykickstart.version import makeVersion
    made = subprocess.run([BASH, str(ROOT / "linux/vm/status-kickstart.sh")],
                          capture_output=True, text=True, check=True).stdout
    handler = makeVersion()
    parser_module.KickstartParser(handler, followIncludes=False).readKickstartFromString(made)
    assert len(handler.scripts) == 1 and handler.scripts[0].inChroot
    script = handler.scripts[0].script
    assert subprocess.run([BASH, "-n"], input=script, text=True).returncode == 0
    assert "After=herald-os-firstboot.service" in script
    assert "ConditionVirtualization=yes" in script
    assert "RuntimeDirectory=madx-validation" in script
    assert "systemctl enable madx-validation-status.service" in script
    assert "sudoers" not in script and "NOPASSWD" not in script and "PermitRootLogin" not in script


@pytest.mark.parametrize("bootc_fails", [False, True])
def test_capture_retains_diagnostics_and_marks_complete_only_after_success(tmp_path, bootc_fails):
    script = (ROOT / "linux/vm/capture-guest-status.sh").read_text()
    # Replace root-only commands and fixed guest paths with byte-producing fixture functions.
    script = script.replace("/run/madx-validation", '"$EVIDENCE"')
    script = script.replace("/usr/bin/bootc", "bootc").replace("/usr/bin/ostree", "ostree")
    script = script.replace("/etc/fstab", '"$FIXTURE_FSTAB"')
    script = script.replace("/proc/cmdline", '"$FIXTURE_CMDLINE"')
    fakes = """
systemctl() { printf 'test service evidence\\n'; }
journalctl() { printf 'test remount journal\\n'; }
findmnt() { printf '{}\\n'; }
ostree() { printf 'booted deployment\\n'; }
bootc() {
  if [[ "$BOOTC_FAILS" == 1 ]]; then echo 'status failure' >&2; return 1; fi
  printf '{"status":{"booted":{"image":"test"}}}\\n'
}
"""
    fstab = tmp_path / "fstab"
    fstab.write_text("test mount table\n")
    cmdline = tmp_path / "cmdline"
    cmdline.write_text("rootflags=subvol=root,compress=zstd:1\n")
    result = subprocess.run([BASH, "-c", fakes + script], capture_output=True, text=True,
                            env={**os.environ, "EVIDENCE": tmp_path.as_posix(),
                                 "FIXTURE_FSTAB": fstab.as_posix(), "FIXTURE_CMDLINE": cmdline.as_posix(),
                                 "BOOTC_FAILS": str(int(bootc_fails))})
    assert (tmp_path / "remount-journal.txt").read_text() == "test remount journal\n"
    assert (tmp_path / "fstab.txt").read_text() == "test mount table\n"
    assert (tmp_path / "kernel-command-line.txt").read_text() == cmdline.read_text()
    if bootc_fails:
        assert result.returncode != 0
        assert not (tmp_path / "complete").exists()
        assert "status failure" in (tmp_path / "errors.log").read_text()
    else:
        assert result.returncode == 0, result.stderr
        assert json.loads((tmp_path / "bootc.json").read_text())["status"]["booted"]
        assert (tmp_path / "ostree.txt").read_text() == "booted deployment\n"
        assert (tmp_path / "complete").read_text() == "complete\n"
