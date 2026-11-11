"""Offline first-boot behavior and the NVIDIA-only validation boundary."""
import importlib.util
import importlib.machinery
import os
from pathlib import Path
import re
import shutil
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("image_matrix", ROOT / "scripts/madx/image-matrix.py")
matrix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix)

loader = importlib.machinery.SourceFileLoader("local_model", str(ROOT / "linux/image/madx-local-model"))
local_model = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(local_model)


def test_fresh_account_has_private_offline_provider_that_survives_repeat_setup(tmp_path):
    home = tmp_path / "account"
    profile = home / ".hermes"
    assert local_model.configure(home, profile, 19000)
    keyfile = home / ".local/state/madx/local-model.key"
    key = keyfile.read_text().strip()
    cfg = profile / "config.yaml"
    original = cfg.read_bytes()
    assert len(key) >= 32
    if os.name != "nt":
        assert keyfile.stat().st_mode & 0o077 == 0
        assert cfg.stat().st_mode & 0o077 == 0
    model = yaml.safe_load(original)["model"]
    assert model["provider"] == "custom" and model["default"] == "madx-local"
    assert model["base_url"] == "http://127.0.0.1:19000/v1" and model["api_key"] == key
    assert local_model.configure(home, profile, 19000)
    assert cfg.read_bytes() == original and keyfile.read_text().strip() == key
    other = tmp_path / "second-account"
    assert local_model.configure(other, other / ".hermes", 19001)
    assert (other / ".local/state/madx/local-model.key").read_text().strip() != key


@pytest.mark.parametrize("existing", ["config.yaml", ".env", "auth.json", "hermes-agent", "profiles"])
def test_existing_hermes_profile_is_preserved(tmp_path, existing):
    home = tmp_path / "existing-account"
    profile = home / ".hermes"
    profile.mkdir(parents=True)
    original = profile / existing
    if existing in ("hermes-agent", "profiles"):
        original.mkdir()
        original = original / "sentinel"
    original.write_text("existing user settings")
    assert not local_model.configure(home, profile, 19000)
    assert original.read_text() == "existing user settings"
    assert set(profile.iterdir()) == {profile / existing}
    assert not (home / ".local/state/madx/local-model.key").exists()


def test_selected_scope_is_only_nvidia_amd64_and_full_scope_is_preserved():
    assert len(matrix.select()["include"]) == 3
    selected = matrix.select(True, False, "nvidia")["include"]
    assert len(selected) == 1
    assert selected[0]["arch"] == "amd64"
    assert selected[0]["image"] == "madx-agent-os-nvidia"
    assert selected[0]["runner"] == "ubuntu-24.04"


@pytest.mark.parametrize("publish,variant", [(True, "nvidia"), (False, "standard"), (True, "standard")])
def test_limited_scope_cannot_publish_or_build_a_different_variant(publish, variant):
    with pytest.raises(ValueError):
        matrix.select(True, publish, variant)


def run_boot(tmp_path, phase, found=True, setup_ok=True, command="/usr/bin/hermes"):
    source = (ROOT / "linux/image/firstboot.sh").read_text()
    functions = "\n".join(re.search(rf"^{name}\(\) \{{\n.*?^\}}$", source, re.M | re.S)[0]
                          for name in ("hermes_for_firstboot", "hermes_step", "hermes_phase", "apps_phase"))
    # Mirror the installed paths inside the fixture. Fedora's bin and sbin
    # spellings refer to the same executable, while a managed install is distinct.
    bundled = tmp_path / "usr/bin/hermes"
    bundled.parent.mkdir(parents=True)
    bundled.touch()
    discovered = tmp_path / command.lstrip("/")
    if discovered != bundled:
        discovered.parent.mkdir(parents=True)
        if command == "/usr/sbin/hermes":
            os.link(bundled, discovered)
        else:
            discovered.touch()
    functions = functions.replace("/usr/bin/hermes", '"$FIXTURE_BUNDLED"')
    bundle = tmp_path / "bundle.json"
    bundle.write_text("{}")
    pending = tmp_path / "pending"
    pending.write_text("offline\n")
    script = functions + r'''
step() { :; }
getent() { echo 'test:x:1000:1000::/home/test:/bin/bash'; }
online() { echo UNEXPECTED_NETWORK >&2; return 91; }
git() { echo UNEXPECTED_DOWNLOAD >&2; return 92; }
curl() { echo UNEXPECTED_DOWNLOAD >&2; return 93; }
uv() { echo UNEXPECTED_DOWNLOAD >&2; return 94; }
systemctl() {
  [[ "$*" == '--no-block start herald-os-hermes.service' ]] || { echo UNEXPECTED_SERVICE >&2; return 95; }
  echo LOCAL_REPAIR_QUEUED
}
as_user() {
  if [[ "$*" == 'herald-os hermes-command' ]]; then
    [[ "$FOUND" == 1 ]] || return 1
    printf '%s\n' "$FOUND_COMMAND"
  elif [[ "$*" == 'madx-local-model activate' ]]; then
    echo LOCAL_MODEL_ACTIVATED
  elif [[ "$*" == 'herald-os setup --yes' ]]; then
    echo SETUP_CALLED
    [[ "$SETUP_OK" == 1 ]] || return 17
  else
    echo "UNEXPECTED_USER_COMMAND: $*" >&2
    return 96
  fi
}
'''
    env = dict(os.environ, HERMES_BUNDLE=bundle.as_posix(), PENDING=pending.as_posix(),
               STATE=tmp_path.as_posix(), BRIDGE=tmp_path.as_posix(), HERMES_USER="test", HOME_DIR="/home/test",
               FOUND=str(int(found)), SETUP_OK=str(int(setup_ok)), FOUND_COMMAND=discovered.as_posix(),
               FIXTURE_BUNDLED=bundled.as_posix())
    result = subprocess.run([shutil.which("bash") or "bash", "-euc", script + "\n" + phase],
                            env=env, capture_output=True, text=True, timeout=10)
    assert "UNEXPECTED" not in result.stdout + result.stderr
    return result, pending


@pytest.mark.parametrize("phase", ["hermes_for_firstboot", "hermes_phase"])
@pytest.mark.parametrize("command", ["/usr/bin/hermes", "/usr/sbin/hermes", "/home/test/.hermes/hermes-agent/venv/bin/hermes"])
def test_bundle_sets_up_without_network_and_preserves_runtime_priority(tmp_path, phase, command):
    result, pending = run_boot(tmp_path, phase, command=command)
    assert result.returncode == 0, result.stderr
    assert "SETUP_CALLED" in result.stdout
    assert command in result.stdout
    assert ("LOCAL_MODEL_ACTIVATED" in result.stdout) == command.startswith("/usr/")
    assert not pending.exists()
    assert "LOCAL_REPAIR_QUEUED" not in result.stdout


@pytest.mark.parametrize("phase", ["hermes_for_firstboot", "hermes_phase"])
@pytest.mark.parametrize("found,setup_ok", [(False, True), (True, False)])
def test_broken_bundle_or_setup_fails_without_network_repair(tmp_path, phase, found, setup_ok):
    result, pending = run_boot(tmp_path, phase, found, setup_ok)
    assert pending.exists()
    if phase == "hermes_for_firstboot":
        assert result.returncode == 0 and pending.read_text().strip() == "setup-failed"
        assert "LOCAL_REPAIR_QUEUED" in result.stdout
    else:
        assert result.returncode != 0


def test_no_automatic_flatpak_downloads_on_bundled_image(tmp_path):
    result, _ = run_boot(tmp_path, "apps_phase")
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "firstboot-apps-done").exists()


def test_bundle_is_mandatory_and_native_acceptance_has_no_network():
    container = (ROOT / "linux/image/Containerfile").read_text()
    assert "BUNDLE_HERMES" not in container
    assert "&& bash /tmp/herald-os/linux/image/bundle-hermes.sh" in container
    image = yaml.safe_load((ROOT / ".github/workflows/image.yml").read_text())
    steps = image["jobs"]["image"]["steps"]
    probe = next(s for s in steps if s.get("name") == "Require built-in Hermes with networking disabled")
    assert "if" not in probe and "continue-on-error" not in probe
    assert "--network=none --read-only --user 65534:65534" in probe["run"]
    assert "offline-chat-smoke.py" in probe["run"]
    assert "madx setup --yes" in probe["run"] and "--launcher /usr/bin/hermes" in probe["run"]
    iso = next(s for s in steps if s.get("name") == "Build a validation ISO without publishing")
    assert steps.index(probe) < steps.index(iso)
    installer = yaml.safe_load((ROOT / ".github/workflows/installer-test.yml").read_text())
    scripts = {s.get("name"): s.get("run", "") for s in installer["jobs"]["install"]["steps"]}
    assert "-nic none" in scripts["Install"]
    assert "-map ks.cfg /madx-validation.ks" in scripts["Prepare the ISO's actual UEFI boot path"]
    assert "user,id=net0,restrict=on" in scripts["Boot what was installed"]


def test_workflow_scope_selection_executes_the_reviewed_selector():
    image = yaml.safe_load((ROOT / ".github/workflows/image.yml").read_text())
    inputs = image[True]["workflow_dispatch"]["inputs"]
    assert inputs["nvidia_only"]["default"] is False
    channel = image["jobs"]["channel"]
    select = next(s for s in channel["steps"] if s.get("id") == "matrix")
    assert "python3 scripts/madx/image-matrix.py" in select["run"]
    assert select["env"]["REQUEST_PUBLISH"] == "${{ inputs.publish }}"
    assert channel["outputs"]["matrix"] == "${{ steps.matrix.outputs.matrix }}"
    assert image["jobs"]["image"]["strategy"]["matrix"] == "${{ fromJSON(needs.channel.outputs.matrix) }}"
    assert image["jobs"]["image"]["continue-on-error"] == "${{ matrix.image == 'madx-agent-os-nvidia' && inputs.validation_variant != 'nvidia' }}"
