"""Reproduce the installed Btrfs/composefs conflict using offline fixture files only."""
import importlib.util
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("root_mount", ROOT / "linux/image/finalize-root-mount.py")
mount = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mount)
FSTAB = """# Created by Anaconda
UUID=test-root / btrfs subvol=root,compress=zstd:1,x-systemd.device-timeout=0 0 0
UUID=test-boot /boot ext4 defaults 1 2
UUID=test-efi /boot/efi vfat umask=0077,shortname=winnt 0 2
UUID=test-root /home btrfs subvol=home,compress=zstd:1 0 0
# preserve a user's other mount exactly
UUID=test-data /data ext4 noatime 0 2
"""
ARGS = "root=UUID=test-root rd.luks.uuid=luks-test console=tty0 console=ttyS0,115200 rootflags=subvol=root rw ostree=/ostree/boot.0/test/0"


def target(tmp_path):
    for directory in ("usr/lib", "etc", "boot/loader/entries", "sysroot/ostree/deploy"):
        (tmp_path / directory).mkdir(parents=True, exist_ok=True)
    (tmp_path / "usr/lib/os-release").write_text('IMAGE_ID="madx-agent-os"\n')
    (tmp_path / "etc/fstab").write_text(FSTAB)
    entry = tmp_path / "boot/loader/entries/test.conf"
    entry.write_text("title MadX Agent OS\noptions " + ARGS + "\n")
    return entry


def test_migrates_root_options_preserves_other_mounts_encryption_and_repeated_runs(tmp_path):
    entry = target(tmp_path)
    calls = []
    def run(argv, check):
        calls.append(argv)
        assert check and argv[:6] == ["chroot", str(tmp_path.resolve()), "/usr/bin/ostree", "admin", "instutil", "set-kargs"]
        assert argv[6:] == ["--merge", "--replace=rootflags=subvol=root,compress=zstd:1"]
        entry.write_text(entry.read_text().replace("rootflags=subvol=root", "rootflags=subvol=root,compress=zstd:1"))
    assert mount.finalize(tmp_path, run)
    after = (tmp_path / "etc/fstab").read_text()
    assert not any(line.split()[1:2] == ["/"] for line in after.splitlines() if not line.startswith("#"))
    for line in FSTAB.splitlines()[2:]:
        assert line in after.splitlines()
    assert (tmp_path / "etc/fstab.madx-before-rootflags").read_text() == FSTAB
    assert "rd.luks.uuid=luks-test" in entry.read_text()
    assert not mount.finalize(tmp_path, run) and len(calls) == 1


@pytest.mark.parametrize("failure", ["command", "no change", "lost encryption"])
def test_fstab_is_retained_when_boot_options_cannot_be_verified(tmp_path, failure):
    entry = target(tmp_path)
    def run(argv, check):
        if failure == "command":
            raise subprocess.CalledProcessError(1, argv)
        if failure == "lost encryption":
            entry.write_text(entry.read_text().replace("rd.luks.uuid=luks-test ", "").replace("rootflags=subvol=root", "rootflags=subvol=root,compress=zstd:1"))
    with pytest.raises((ValueError, subprocess.CalledProcessError)):
        mount.finalize(tmp_path, run)
    assert (tmp_path / "etc/fstab").read_text() == FSTAB
    assert not (tmp_path / "etc/fstab.madx-before-rootflags").exists()


@pytest.mark.parametrize("source,args", [
    (FSTAB + "UUID=other / btrfs subvol=root 0 0\n", ARGS),
    (FSTAB.replace("/ btrfs", "/ ext4"), ARGS),
    (FSTAB, ARGS.replace("root=UUID=test-root", "root=UUID=other")),
    (FSTAB, ARGS + " rootflags=subvol=other"),
    (FSTAB.replace("subvol=root,", "subvol=other,"), ARGS),
    (FSTAB.replace("compress=zstd:1", "noauto"), ARGS),
    (FSTAB, ARGS.replace("ostree=", "unrelated=")),
])
def test_rejects_ambiguous_or_unsupported_layouts_before_writing(source, args):
    with pytest.raises(ValueError):
        mount.plan(source, args.split())


def test_refuses_the_running_host_and_non_madx_targets(tmp_path):
    with pytest.raises(ValueError, match="offline"):
        mount.finalize(Path(tmp_path.anchor))
    target(tmp_path)
    (tmp_path / "usr/lib/os-release").write_text("IMAGE_ID=another-os\n")
    with pytest.raises(ValueError, match="MadX"):
        mount.finalize(tmp_path)
    assert (tmp_path / "etc/fstab").read_text() == FSTAB


def test_other_filesystem_layout_keeps_its_existing_install_behavior(tmp_path):
    entry = target(tmp_path)
    custom = FSTAB.replace("/ btrfs", "/ ext4")
    (tmp_path / "etc/fstab").write_text(custom)
    def forbidden(*args, **kwargs):
        pytest.fail("custom layout must not invoke a bootloader update")
    assert not mount.finalize(tmp_path, forbidden)
    assert (tmp_path / "etc/fstab").read_text() == custom
    assert "options " + ARGS in entry.read_text()
