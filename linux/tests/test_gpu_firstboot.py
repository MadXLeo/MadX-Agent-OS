"""A system unit can inspect the GPU without a user HOME or notification state."""
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASH = shutil.which(os.environ.get("HERALD_OS_TEST_BASH", "bash"))


@pytest.mark.parametrize("vendor", ["0x8086", "0x10de"])
def test_firstboot_gpu_check_without_home_or_state(tmp_path, vendor):
    device = tmp_path / "sys/bus/pci/devices/test"
    device.mkdir(parents=True)
    (device / "vendor").write_text(vendor + "\n")
    (device / "class").write_text("0x030000\n")
    release = tmp_path / "os-release"
    release.write_text("IMAGE_ID=madx-agent-os\n")
    env = {**os.environ, "HERALD_OS_SYSFS": (tmp_path / "sys").as_posix(),
           "HERALD_OS_MODULES": (tmp_path / "modules").as_posix(),
           "HERALD_OS_OS_RELEASE": release.as_posix(), "HERALD_OS_ARCH": "x86_64"}
    result = subprocess.run([BASH, "-c", 'unset HOME XDG_STATE_HOME HERALD_OS_STATE; exec bash "$1"',
                             "gpu-firstboot", (ROOT / "linux/bin/herald-os-gpu-check").as_posix()],
                            env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert "unbound variable" not in result.stderr
    assert ("NVIDIA graphics found" in result.stdout) == (vendor == "0x10de")
