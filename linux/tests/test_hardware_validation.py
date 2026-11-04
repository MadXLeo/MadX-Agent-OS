"""Hybrid renderer policy and exact-variant unpublished ISO provenance; no host GPU changes."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(ROOT / path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


graphics = load("madx_graphics_device", "linux/session/madx-render-device")
artifact = load("madx_validation_artifact", "scripts/madx/validation-artifact.py")


def hybrid(tmp_path, driver="xe", internal="connected"):
    drm, dev = tmp_path / "sys", tmp_path / "dev"
    dev.mkdir()
    # Deliberately nonstandard numbering: selection must follow sysfs, not renderD128.
    for number, vendor, module, render in ((7, "0x8086", driver, 132), (2, "0x10de", "nouveau", 129)):
        device = drm / f"card{number}/device"
        (device / f"drm/renderD{render}").mkdir(parents=True)
        (device / "vendor").write_text(vendor)
        (device / "uevent").write_text(f"DRIVER={module}\nPCI_ID=test\n")
        (dev / f"renderD{render}").touch()
    panel = drm / "card7-eDP-1"
    panel.mkdir()
    (panel / "status").write_text(internal)
    return drm, dev, tmp_path / "local.kdl"


@pytest.mark.parametrize("driver", ["xe", "i915"])
def test_hybrid_uses_actual_intel_node_without_disabling_nvidia_outputs(tmp_path, driver):
    args = hybrid(tmp_path, driver)
    result = graphics.configuration(*args)
    assert f'render-drm-device "{(args[1] / "renderD132").as_posix()}"' in result
    assert "ignore-drm-device" not in result


@pytest.mark.parametrize("personal", ['debug { render-drm-device "/dev/dri/renderD129"; }',
                                      'debug { disable-direct-scanout; }', 'include "custom.kdl"'])
def test_personal_gpu_policy_is_never_overridden_or_rewritten(tmp_path, personal):
    args = hybrid(tmp_path)
    args[2].write_text(personal)
    assert "render-drm-device" not in graphics.configuration(*args)
    assert args[2].read_text() == personal


@pytest.mark.parametrize("case", ["disconnected", "no-nvidia", "unknown-driver", "missing-node"])
def test_no_speculative_gpu_override_without_connected_supported_hybrid(tmp_path, case):
    args = hybrid(tmp_path, driver="unknown" if case == "unknown-driver" else "xe",
                  internal="disconnected" if case == "disconnected" else "connected")
    if case == "no-nvidia":
        (args[0] / "card2/device/vendor").write_text("0x1002")
    if case == "missing-node":
        (args[1] / "renderD132").unlink()
    assert "render-drm-device" not in graphics.configuration(*args)


def fixture(tmp_path, variant="nvidia"):
    name = "madx-agent-os-validation-abcdef0-nvidia-x86_64.iso.part0"
    (tmp_path / name).write_bytes(b"disposable fixture, not an ISO")
    image = "ghcr.io/madxleo/madx-agent-os" + ("-nvidia" if variant == "nvidia" else "") + ":dev-abcdef0"
    data = artifact.create(tmp_path, "a" * 40, variant, image)
    manifest = tmp_path / "validation-source.json"
    manifest.write_text(json.dumps(data))
    return manifest, name


@pytest.mark.parametrize("variant", ["standard", "nvidia"])
def test_manifest_verifies_variant_source_and_actual_split_bytes(tmp_path, variant):
    manifest, _ = fixture(tmp_path, variant)
    assert artifact.verify(manifest, "a" * 40, variant)["variant"] == variant


@pytest.mark.parametrize("change", ["revision", "variant", "image", "bytes", "missing", "extra", "traversal"])
def test_invalid_or_mixed_artifact_is_refused(tmp_path, change):
    manifest, name = fixture(tmp_path)
    data = json.loads(manifest.read_text())
    if change in ("revision", "variant", "image"):
        data[change] = {"revision": "b" * 40, "variant": "standard", "image": "other:tag"}[change]
    elif change == "bytes":
        (tmp_path / name).write_bytes(b"changed")
    elif change == "missing":
        (tmp_path / name).unlink()
    elif change == "extra":
        (tmp_path / "madx-agent-os-other-x86_64.iso").touch()
    else:
        data["files"] = {"../escape.iso": "0" * 64}
    manifest.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        artifact.verify(manifest, "a" * 40, "nvidia")


def test_no_iso_means_no_manifest(tmp_path):
    with pytest.raises(ValueError, match="no ISO"):
        artifact.create(tmp_path, "a" * 40, "nvidia", "ghcr.io/madxleo/madx-agent-os-nvidia:dev")


@pytest.mark.parametrize("selected", ["standard", "nvidia"])
def test_only_selected_amd64_image_builds_the_iso_and_selected_nvidia_cannot_soft_fail(selected):
    workflow = yaml.safe_load((ROOT / ".github/workflows/image.yml").read_text())
    inputs = workflow[True]["workflow_dispatch"]["inputs"]
    assert inputs["validation_variant"]["options"] == ["standard", "nvidia"]
    assert inputs["publish"]["default"] is False
    job = workflow["jobs"]["image"]
    iso = next(s for s in job["steps"] if s.get("name") == "Build a validation ISO without publishing")
    context = {"github": SimpleNamespace(event_name="workflow_dispatch"),
               "inputs": SimpleNamespace(publish=False, disks=True, validation_variant=selected)}
    chosen = []
    for leg in job["strategy"]["matrix"]["include"]:
        context["matrix"] = SimpleNamespace(**leg)
        def enabled(expr):
            expr = expr.removeprefix("${{").removesuffix("}}").strip()
            return eval(expr.replace("&&", " and ").replace("!inputs.publish", "not inputs.publish"),
                        {"__builtins__": {}}, context)
        if enabled(iso["if"]):
            chosen.append(leg["image"])
            assert not enabled(job["continue-on-error"])
    assert chosen == ["madx-agent-os" + ("-nvidia" if selected == "nvidia" else "")]
    installer = yaml.safe_load((ROOT / ".github/workflows/installer-test.yml").read_text())
    download = next(s["run"] for s in installer["jobs"]["install"]["steps"]
                    if s.get("name") == "The installer, from the release")
    assert "image-evidence-madx-agent-os-nvidia-amd64" in download
    assert download.index("validation-artifact.py verify") < download.index("find installer-input")


def test_image_enables_xe_before_nvidia_and_keeps_modesetting_and_diagnostics():
    assert "i915 xe amdgpu nvidia" in (ROOT / "linux/image/nvidia.sh").read_text()
    assert '"nvidia-drm.modeset=1"' in (ROOT / "linux/image/kargs-nvidia.toml").read_text()
    packages = (ROOT / "linux/image/packages.txt").read_text().splitlines()
    assert all(name in packages for name in ("pciutils", "procps-ng", "mokutil", "intel-gpu-firmware"))


def test_session_target_has_a_lifetime_owner_and_portals_start_after_it():
    unit = (ROOT / "linux/session/madx-graphical-session.service").read_text()
    assert "BindsTo=graphical-session.target" in unit and "RemainAfterExit=yes" in unit
    session = (ROOT / "linux/session/herald-os-session").read_text()
    assert session.index("start madx-graphical-session.service") < session.index("start xdg-desktop-portal.service")
    assert "--property=PartOf=graphical-session.target" in session
    compositor = (ROOT / "linux/session/herald-os-compositor").read_text()
    assert "stop madx-graphical-session.service graphical-session.target" in compositor
    assert "trap cleanup_session EXIT" in compositor


@pytest.mark.parametrize("unit_present,queue_exit", [(True, 0), (True, 1), (False, 0)])
def test_firstboot_downloads_are_deferred_only_when_the_image_has_a_background_service(tmp_path, unit_present, queue_exit):
    bash = shutil.which(os.environ.get("HERALD_OS_TEST_BASH", "bash"))
    assert bash, "Bash is required for the firstboot contract test"
    unit, pending = tmp_path / "hermes.service", tmp_path / "hermes-pending"
    if unit_present:
        unit.touch()
    pending.write_text("old")
    script = (ROOT / "linux/image/firstboot.sh").read_text()
    function = re.search(r"^hermes_for_firstboot\(\) \{\n.*?^\}", script, re.M | re.S).group(0)
    body = (f"HERMES_UNIT={shlex.quote(unit.as_posix())}\nPENDING={shlex.quote(pending.as_posix())}\n"
            f'systemctl() {{ echo "queued $*"; return {queue_exit}; }}\n'
            'hermes_step() { echo synchronous-install; }\n'
            'hermes_later() { echo later; }\n'
            'online() { echo unexpected-network; return 99; }\n'
            + function + "\nhermes_for_firstboot\n")
    result = subprocess.run([bash, "-c", body], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0, result.stderr
    assert "unexpected-network" not in result.stdout
    if unit_present:
        assert "queued --no-block start herald-os-hermes.service" in result.stdout
        assert "synchronous-install" not in result.stdout
        assert pending.read_text().strip() == "pending"
    else:
        assert "synchronous-install" in result.stdout and "queued" not in result.stdout
        assert not pending.exists()
