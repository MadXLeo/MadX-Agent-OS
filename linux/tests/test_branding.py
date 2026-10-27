"""Phase 1 identity migration: isolated roots only; never install onto the host."""
import importlib.util
import json
import os
from pathlib import Path
import re
import tomllib

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "linux/branding" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


identity = load("madx_identity", "install.py")
release = load("madx_os_release", "os-release.py")


def put(root, name, text="original"):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def can_symlink(tmp_path):
    target = put(tmp_path, "probe-target")
    link = tmp_path / "probe-link"
    try:
        link.symlink_to(target)
    except OSError as exc:
        pytest.skip(f"host cannot create symlinks: {exc}")
    link.unlink()
    target.unlink()


@pytest.mark.parametrize("layout,prefix", [("image", "usr"), ("arch", "usr"), ("dev", "usr/local"), ("tarball", "usr/local")])
def test_alias_plan_shares_implementation_without_duplicate_units(tmp_path, layout, prefix):
    put(tmp_path, f"{prefix}/bin/herald-os")
    put(tmp_path, "usr/lib/systemd/system/herald-os-firstboot.service")
    put(tmp_path, "usr/lib/systemd/user/herald-os-update-check.timer")
    plan = identity.alias_plan(tmp_path, layout)
    assert plan[tmp_path / prefix / "bin/madx-agent-os"] == "herald-os"
    assert plan[tmp_path / "usr/lib/systemd/system/madx-agent-os-firstboot.service"] == "herald-os-firstboot.service"
    assert plan[tmp_path / "usr/lib/systemd/user/madx-agent-os-update-check.timer"] == "herald-os-update-check.timer"
    assert not any(".wants" in str(path) for path in plan)


def test_conflict_prevents_every_write_and_preserves_existing_data(tmp_path):
    old = put(tmp_path, "usr/bin/herald-os", "working command")
    put(tmp_path, "usr/bin/herald-os-app")
    conflict = put(tmp_path, "usr/bin/madx-agent-os-app", "user-owned command")
    with pytest.raises(ValueError, match="existing file"):
        identity.install(tmp_path, "image")
    assert not (tmp_path / "usr/bin/madx-agent-os").exists()
    assert old.read_text() == "working command"
    assert conflict.read_text() == "user-owned command"


def test_alias_is_idempotent_and_removes_only_its_own_links(tmp_path):
    can_symlink(tmp_path)
    old = put(tmp_path, "usr/bin/herald-os", "working command")
    assert identity.install(tmp_path, "image") == 1
    alias = old.with_name("madx-agent-os")
    assert os.readlink(alias) == "herald-os"
    assert alias.read_text() == "working command"
    assert identity.install(tmp_path, "image") == 0
    assert identity.remove(tmp_path, "image") == 1
    assert old.read_text() == "working command"
    assert not alias.exists()


def test_install_rolls_back_new_links_after_io_failure(tmp_path, monkeypatch):
    can_symlink(tmp_path)
    put(tmp_path, "usr/bin/herald-os")
    put(tmp_path, "usr/bin/herald-os-app")
    original = Path.symlink_to
    calls = []
    def fail_second(self, *args, **kwargs):
        calls.append(self)
        if len(calls) == 2:
            raise OSError("injected write failure")
        return original(self, *args, **kwargs)
    monkeypatch.setattr(Path, "symlink_to", fail_second)
    with pytest.raises(OSError, match="injected"):
        identity.install(tmp_path, "image")
    assert not any(path.is_symlink() for path in (tmp_path / "usr/bin").iterdir())
    assert (tmp_path / "usr/bin/herald-os").read_text() == "original"


def test_symlinked_parent_cannot_escape_staging(tmp_path):
    can_symlink(tmp_path)
    outside = tmp_path / "outside"
    put(outside, "bin/herald-os")
    staged = tmp_path / "stage"
    staged.mkdir()
    (staged / "usr").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlinked parent"):
        identity.install(staged, "image")
    assert not (outside / "bin/madx-agent-os").exists()


def test_os_release_preserves_fedora_contract_and_is_idempotent():
    before = 'NAME="Fedora Linux"\nID=fedora\nID_LIKE="fedora"\nVERSION_ID=44\nIMAGE_ID=herald-os\n'
    after = release.branded_release(before)
    assert 'ID=fedora\nID_LIKE="fedora"\nVERSION_ID=44\n' in after
    assert 'IMAGE_ID="madx-agent-os"' in after
    assert 'PRETTY_NAME="MadX Agent OS 0.1.0-alpha"' in after
    assert "Herald" not in after
    assert release.branded_release(after) == after


@pytest.mark.parametrize("image,accepted", [("herald-os", True), ("madx-agent-os", True), ("bazzite", False), ("silverblue", False)])
@pytest.mark.parametrize("quoted", [False, True])
def test_updaters_recognize_both_identities_and_reject_unrelated_systems(image, accepted, quoted):
    line = f'IMAGE_ID="{image}"' if quoted else f"IMAGE_ID={image}"
    for script in ("herald-os-update", "herald-os-gpu-check"):
        source = (ROOT / "linux/bin" / script).read_text(encoding="utf-8")
        pattern = re.search(r"'(IMAGE_ID=[^']+)'", source).group(1)
        assert bool(re.fullmatch(pattern, line)) == accepted


def test_assets_and_distribution_resources_are_shipped():
    product = json.loads((ROOT / "branding/product.json").read_text(encoding="utf-8"))
    assert product == json.loads((ROOT / "linux/branding/product.json").read_text(encoding="utf-8"))
    pkg = json.loads((ROOT / "apps/desktop/package.json").read_text(encoding="utf-8"))
    resource = next(item for item in pkg["build"]["linux"]["extraResources"] if item["to"] == "herald-os-linux")
    assert "branding/**" in resource["filter"]
    assert pkg["build"]["linux"]["executableName"] == "herald-os"
    splash = (ROOT / "linux/plymouth/herald-os/herald-os.script").read_text(encoding="utf-8")
    assert "Plymouth.SetDisplayPasswordFunction(display_password_callback)" in splash
    assert 'prompt + "  " + text' in splash


def test_iso_identity_preserves_the_interactive_encrypted_installer():
    config = tomllib.loads((ROOT / "linux/image/iso.toml").read_text(encoding="utf-8"))["customizations"]
    assert config["iso"] == {"volume_id": "MADX_AGENT_OS", "application_id": "MadX Agent OS", "publisher": "MadXCore"}
    kickstart = config["installer"]["kickstart"]["contents"]
    assert "autopart --type=btrfs --encrypted" in kickstart
    assert not any(command in kickstart for command in ("clearpart", "ignoredisk", "bootloader", "zerombr"))
