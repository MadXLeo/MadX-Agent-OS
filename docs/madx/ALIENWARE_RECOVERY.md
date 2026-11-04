# Alienware m16 R2: recovery and NVIDIA image validation

Updated 2026-11-04 (Asia/Calcutta). Target: Core Ultra 7 155H / Intel Xe and RTX 4070
Laptop GPU, internal panel plus HDMI, Secure Boot enabled. **Hardware acceptance is open.**
This guide does not authorize modifying Windows partitions, EFI entries or firmware.

## Current evidence

The user's supplied hardware report says manual installation completed, Windows remained
bootable and Secure Boot was enabled. Intel rendering intermittently reached the desktop;
HDMI/Nouveau errors, freezes and a missing Hermes runtime remained. This is user-reported
evidence, not an independently repeated dual-boot or driver acceptance test. Current guest
configuration, journal and installed deployment identity have not yet been collected here.

Confirmed from source:

- The previous unpublished ISO path selected only the standard amd64 image. Building the
  separate NVIDIA container did not put its driver into that ISO.
- The NVIDIA initramfs preload list included i915 but omitted xe; the NVIDIA kernel arguments
  did not explicitly request DRM modesetting. These gaps alone do not prove the freeze's cause.
- The custom greetd wrapper bypassed niri-session's systemd lifetime integration. It did not
  activate graphical-session.target before starting portals or prevent a second managed session.
- Hermes is downloaded at first boot into the selected account, not bundled into the image.
  With no explicit installer account file, firstboot selects `hermes`; a manually created
  `dpatel` login may not see that account's installation. The report does not yet prove whether
  this, an offline/failed install, or runtime discovery caused the missing-runtime message.
- procps-ng was already in the image package list. Missing `pgrep` therefore still requires
  deployment/PATH inspection; adding a duplicate package entry would not diagnose it.

Unproven: the cause of `EACCES` during page flips, Intel/Nouveau cross-GPU presentation,
multiple manually started sessions, Electron's renderer, output refresh, and the `/usr/local/sbin`
tmpfiles warning. Do not change device permissions, disable security, ignore a GPU wholesale,
or mask tmpfiles rules based on those messages alone.

## Recover the currently installed system

The checks below run **inside MadX**, after rebooting out of Windows. Disconnect HDMI for the
first recovery attempt, press Ctrl+Alt+F3 and log in as the normal Linux account, not root.
Do not manually start niri on another VT. A reboot removes the extra experimental compositor
processes, but does not remove saved configuration overrides.

Read the current files before choosing a reversible repair:

```bash
whoami
cat ~/.config/niri/local.kdl
grep -E 'NIRI|COMPOSITOR|SOFTWARE_GPU|WLR_RENDERER|MESA_LOADER|GALLIUM_DRIVER|DRI_PRIME|LIBGL' ~/.config/herald-os/session.env 2>/dev/null
loginctl list-sessions
bootc status
systemctl status herald-os-hermes.service --no-pager -l
```

Additional diagnostics, if needed:

```bash
niri --version
niri validate --config ~/.config/niri/herald-os.kdl
ls -l /dev/dri/by-path
for gpu in /sys/class/drm/card[0-9]*; do
  test -f "$gpu/device/vendor" || continue
  printf '%s: ' "$gpu"
  cat "$gpu/device/vendor"
  readlink -f "$gpu/device/driver"
done
systemctl --user status graphical-session.target xdg-desktop-portal.service --no-pager
madx hermes-command
cat /etc/herald-os/install.conf 2>/dev/null
command -v pgrep lspci
rpm -q procps-ng pciutils
tail -n 100 ~/.local/state/herald-os/compositor.log
sudo journalctl -b -u greetd -u herald-os-hermes --no-pager -n 100
```

Review logs before sharing: omit credentials, provider configuration and private file contents.
Do not print shell environment wholesale. The exact `local.kdl` must be reviewed before replacing
or merging debug settings; its `.bak` is not known to be pristine. Back up the current config
before an agreed edit. Device numbers can change across boots; do not assume renderD128 is Intel.
The intended first recovery is one greetd session on the Intel-driven internal panel. That is a
limited recovery attempt, not acceptance of HDMI or the RTX driver.

Do not run a generic DNF/CUDA `.run` installer, `bootc switch` to a guessed registry tag, a
formatting command, or an EFI repair command. The validated development tag was unpublished.
Keep Secure Boot enabled. If the NVIDIA module's signing key is not trusted, enrolling a new
MOK changes boot trust and needs a separately reviewed, explicit user action. No enrollment,
Secure Boot disablement or firmware change has been performed by this work.

## Local source corrections

- `validation_variant=nvidia` builds the unpublished ISO from the NVIDIA image, gives it an
  NVIDIA filename and makes that selected build mandatory. Standard remains the default.
- The artifact manifest binds source SHA, image origin, variant and every packaged ISO byte
  checksum. Installer tests select and verify the same variant before extracting the ISO.
- Xe is loaded alongside the other integrated GPU drivers before NVIDIA; modesetting is
  explicit. The build retains pinned kernel/digest/key checks and additionally checks installed
  module signatures and driver version agreement. It records the package inventory.
- Image inspection requires diagnostic tools, the session lifetime unit, NVIDIA module set
  for each shipped kernel, the pinned enrollment certificate and modesetting configuration.
- The custom session has a per-user lock and a lifetime owner for systemd's graphical targets.
  Portals start after the display environment is imported. Session clipboard units stop with
  the graphical target. Unmanaged manually launched niri processes are not killed or adopted.
- Hybrid selection follows sysfs and chooses Intel only when its supported driver owns a
  connected internal panel. NVIDIA outputs stay available. Personal debug/include configuration
  takes precedence; invalid KDL is logged and refused without overwriting it.
- Image first boot queues the existing Hermes background installer without waiting for its
  downloads. Development VMs without that unit retain their original install path. Account
  selection and Hermes revisions are unchanged; this does not resolve the reported account's
  missing runtime until its actual service/deployment evidence is inspected.

These are candidate fixes until native CI, image boot and hardware testing pass. They do not
claim automatic recovery from every GPU failure. Hermes revision/installation policy, VM software
fallback, immutable tmpfiles handling and native interaction/performance remain separate work.

## Execute the next image milestone

Use the newly reviewed source commit on `codex/madx-desktop-redesign`, never the old image SHA.
Follow REDESIGN_EXECUTION.md for publication review, branch-only push, full native CI, source
verification and stop-on-failure. A remote push/build must have current user authorization.
After CI succeeds, these workflow inputs select the NVIDIA path (no publication):

```text
image.yml: publish=false, disks=true, validation_variant=nvidia
installer-test.yml: image_run=<verified run ID>, tag=, account=madx-test,
                    validation_variant=nvidia
```

Verify the full source SHA at every stage. The selected NVIDIA job must pass; absence of
signed modules for the selected Fedora kernel is a blocker, never a reason to bypass checks.
Inspect `image-packages.txt`, image validation, source manifest, ISO checksums and module
signer evidence. The new manifest intentionally rejects old artifacts without variant provenance;
old runs can be inspected using their original source, not treated as rebuilt evidence.
Return the Actions link and stop while a remote run is pending. Do not repeatedly poll.

Disposable UEFI VM tests can verify installation/reboot and image contents. A hosted VM with
virtio graphics cannot prove RTX 4070 display support or Secure Boot module enrollment.
Do not instruct a physical reinstall or modify the shared EFI partition to test this candidate.
An in-place recovery/update route needs the installed `bootc status` and a reviewed source;
there is currently no published update origin containing these corrections.

## Hardware acceptance checklist (all unverified for the candidate)

1. Record full deployment SHA, kernel, NVIDIA userspace/module versions, Secure Boot state,
   trusted module signer and actual DRM driver for both GPUs.
2. Cold boot internal-only three times: one compositor, working keyboard/mouse, usable shell,
   terminal, Files and settings; no frozen wallpaper-only success criterion.
3. Boot with HDMI attached; use both screens, unplug/replug HDMI, change resolution/scale.
4. Switch TTY1 -> TTY3 -> TTY1 repeatedly. Confirm fresh frames and input, active logind session,
   no persistent DRM-master/page-flip failures and functioning portals.
5. Measure resource use and interaction/frame pacing in graphics modes; record captures.
   Exercise suspend/resume, Wi-Fi, audio and a normal reboot separately.
6. Test desktop entry with Hermes missing, then installation for the **logged-in account**, real
   model-backed chat/tools, approve/deny/cancel and restart. Never reuse another user's runtime
   or credentials by pointing at their home directory.
7. Record both existing Windows and MadX boot paths after any separately authorized deployment.
   No assistant partition/EFI/firmware operations are part of this checklist.

Reference behavior: [niri startup/session integration](https://github.com/niri-wm/niri/wiki/Getting-Started),
[niri renderer overrides](https://github.com/niri-wm/niri/wiki/Configuration:-Debug-Options),
[systemd graphical-session target](https://github.com/systemd/systemd/blob/main/units/user/graphical-session.target),
[NVIDIA open kernel modules](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html).
Use the existing bootc image pipeline; NVIDIA's mutable-Fedora DNF guide is not an in-place
installation prescription for this image-based OS.
