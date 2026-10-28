"""Validation gates must reject incomplete evidence; no host installation is performed."""
import binascii
import importlib.util
from pathlib import Path
import struct

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


probe = load("installer_probe", "linux/vm/installer-probe.py")
windows = load("windows_fixture", "linux/vm/windows-fixture.py")
image = load("image_probe", "scripts/madx/check-image.py")
junit = load("junit_probe", "scripts/madx/check-junit.py")
hermes = load("hermes_probe", "scripts/madx/hermes-smoke.py")


def test_test_boot_preserves_the_iso_kernel_and_stage2_but_replaces_only_test_options():
    source = 'set timeout=60\nset default=1\nmenuentry "Install" {\n linuxefi /images/pxeboot/vmlinuz inst.stage2=hd:LABEL=MADX_AGENT_OS inst.ks=old quiet rhgb\n initrdefi /images/pxeboot/initrd.img\n}\n'
    result = probe.grub_for_test(source)
    assert result.startswith("set timeout=3\nset default=0\n")
    assert "inst.stage2=hd:LABEL=MADX_AGENT_OS" in result
    assert "/images/pxeboot/vmlinuz" in result and "initrdefi /images/pxeboot/initrd.img" in result
    assert "inst.ks=old" not in result and result.count("inst.ks=") == 1
    assert "console=ttyS0,115200" in result


def test_unknown_boot_layout_is_refused():
    with pytest.raises(ValueError, match="no installer kernel"):
        probe.grub_for_test("configfile /unrecognized-layout.cfg")


def test_missing_system_deployment_is_refused():
    with pytest.raises(ValueError, match="no system deployment"):
        probe.diagnostics("autopart --encrypted\npoweroff\n")


def test_diagnostics_preserve_the_deployment_and_capture_fatal_and_success_paths():
    original = "ostreecontainer --url=/run/install/repo/container --transport=oci\n"
    result = probe.diagnostics(original)
    assert result.startswith(original)
    assert "%onerror" in result and "%post --nochroot" in result
    assert result.count("/tmp/storage.log") == 2
    assert "MADX_INSTALLER_UEFI=1" in result and "*.origin" in result
    assert not any(command in result for command in ("grub2-mkconfig", "mkfs", "efibootmgr --create"))


def test_generated_diagnostics_and_vm_disk_scope_parse_with_real_kickstart_parser():
    parser_module = pytest.importorskip("pykickstart.parser")
    version = pytest.importorskip("pykickstart.version")
    source = """ostreecontainer --url=/run/install/repo/container --transport=oci
ignoredisk --only-use=vda
clearpart --all --initlabel --disklabel=gpt --drives=vda
autopart --type=btrfs --noswap --encrypted --passphrase=disposabletest
bootloader --boot-drive=vda
rootpw --lock
poweroff
"""
    handler = version.makeVersion()
    parser_module.KickstartParser(handler).readKickstartFromString(probe.diagnostics(source))
    assert handler.ignoredisk.onlyuse == ["vda"]
    assert handler.clearpart.drives == ["vda"]
    assert len(handler.scripts) == 2


def test_guard_disk_has_valid_primary_and_backup_gpt_and_distinct_partition_types(tmp_path):
    disk = windows.create(tmp_path)
    with disk.open("rb") as stream:
        assert stream.read(512)[510:] == b"\x55\xaa"
        primary = stream.read(512)
        entries = stream.read(128 * 128)
        stream.seek(-512, 2)
        backup = stream.read(512)
    for header in (primary, backup):
        assert header[:8] == b"EFI PART"
        expected = struct.unpack_from("<I", header, 16)[0]
        normalized = bytearray(header[:92])
        normalized[16:20] = b"\0" * 4
        assert binascii.crc32(normalized) == expected
        assert struct.unpack_from("<I", header, 88)[0] == binascii.crc32(entries)
    assert len({entries[n * 128:n * 128 + 16] for n in range(3)}) == 3
    assert disk.stat().st_size == 512 * 1024 * 1024
    with pytest.raises(FileExistsError):
        windows.create(tmp_path)
    with disk.open("rb") as stream:
        stream.seek(512)
        assert stream.read(512) == primary


@pytest.mark.parametrize("content", ["<testsuites/>", '<testsuite><testcase><skipped/></testcase></testsuite>', '<testsuite><testcase><failure/></testcase></testsuite>', '<testsuite><testcase><error/></testcase></testsuite>'])
def test_native_evidence_cannot_succeed_with_empty_failed_or_skipped_cases(tmp_path, content):
    report = tmp_path / "tests.xml"
    report.write_text(content)
    with pytest.raises(ValueError):
        junit.check(report)


def test_native_evidence_accepts_executed_cases(tmp_path):
    report = tmp_path / "tests.xml"
    report.write_text('<testsuites><testsuite><testcase name="real filesystem"/></testsuite></testsuites>')
    assert junit.check(report) == 1


def test_empty_image_cannot_pass_a_source_only_check(tmp_path):
    result = image.inspect(tmp_path, {"slug": "madx-agent-os", "version": "0.1.0-alpha"}, {"files": {}})
    assert not result["passed"]
    assert "no kernel/initramfs pair" in result["failures"]
    assert "MadX image identity missing" in result["failures"]


def test_runtime_smoke_does_not_inherit_credentials_or_profile_markers(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-reach-child")
    monkeypatch.setenv("HERMES_HOME", "existing-profile")
    monkeypatch.setenv("HERMES_PARENT_NONCE", "existing-parent")
    env = hermes.clean_environment(tmp_path, "test-token", tmp_path / "ready.json")
    assert "OPENAI_API_KEY" not in env and "HERMES_PARENT_NONCE" not in env
    assert env["HERMES_HOME"] == str(tmp_path)


def test_installer_uses_uefi_media_and_checks_a_real_guest_not_only_screenshots():
    workflow = yaml.safe_load((ROOT / ".github/workflows/installer-test.yml").read_text())
    job = workflow["jobs"]["install"]
    steps = {s.get("name"): s.get("run", "") for s in job["steps"]}
    install = steps["Install"]
    assert "-kernel" not in install and "-boot order=d" in install
    assert "OVMF_CODE_4M.fd" in install and "MADX_INSTALLER_UEFI=1" in install
    assert "guest-smoke.sh" in steps["Boot what was installed"]
    assert "--only-use=vda" in steps["The ISO's kickstart, unattended"]
    assert "--drives=vda" in steps["The ISO's kickstart, unattended"]
    assert any(case["preserve_disk"] for case in job["strategy"]["matrix"]["include"])
    assert "sha256sum -c mock-windows.sha256" in install
    assert "--bind 127.0.0.1 --directory installer-http" in install
    assert "file=mock-windows.raw" in steps["Boot what was installed"]


def test_manual_image_validation_cannot_publish_without_explicit_selection():
    workflow = yaml.safe_load((ROOT / ".github/workflows/image.yml").read_text())
    # PyYAML's YAML 1.1 loader treats 'on' as True.
    inputs = workflow[True]["workflow_dispatch"]["inputs"]
    assert inputs["publish"]["default"] is False
    steps = {s.get("name"): s for s in workflow["jobs"]["image"]["steps"]}
    assert steps["Push it"]["if"] == "env.PUBLISH == 'true'"
    assert "env.PUBLISH == 'true'" in steps["Sign it with the project's key"]["if"]
    assert "inputs.publish" in workflow["jobs"]["manifest"]["if"]
    assert "check-image.py" in steps["Inspect the actual image and systemd units"]["run"]
