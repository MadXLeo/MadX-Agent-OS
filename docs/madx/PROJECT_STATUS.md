# MadX Agent OS progress — 2026-11-11

**Current result: a bootable, installable Linux alpha with a redesigned desktop.
It is not yet a release-ready, Windows-dual-boot-verified MVP.** There is no honest
single completion percentage: implementation and runtime acceptance are different.

## New hardware report and recovery work

November 11, updated scope: Fedora NVIDIA with built-in offline Hermes and a local model is implemented in the image recipe. The new ISO and disconnected VM acceptance are pending. See [OFFLINE_NVIDIA.md](OFFLINE_NVIDIA.md). macOS and ARM validation are deferred at the user's request.

The user reports a completed Alienware m16 R2 install, successful return to Windows and
Secure Boot enabled. Intel Xe rendering intermittently reaches the desktop; Nouveau/HDMI
errors, frozen interaction and a missing Hermes runtime remain. This supersedes the earlier
unknown physical-install outcome, but does not establish stable hardware/dual-boot acceptance.

Candidate source fixes now select an actual NVIDIA validation ISO, bind artifact variant/source
and checksums, require the selected NVIDIA job, preload Xe, request NVIDIA DRM modesetting,
check modules/certificate/tools, prevent duplicate managed sessions, own graphical-session
target lifetime, prefer an Intel-driven internal panel without disabling NVIDIA outputs,
and defer Hermes downloads to the background service. See
[ALIENWARE_RECOVERY.md](ALIENWARE_RECOVERY.md). No candidate ISO, hardware repair, HDMI success
or new native CI result is claimed. Existing installed user overrides need inspection first.

## What is implemented

| Area | Progress | What the evidence establishes |
| --- | --- | --- |
| MadX identity | Logos, product metadata, icons, themes, boot assets, package/release naming, public help and guides migrated | Branding checks pass; some updater wording remains |
| Compatibility | `madx` and `madx-agent-os` command aliases, legacy commands/services/settings and Hermes identifiers retained | Native CI, image checks and installed legacy alias smoke pass; old-profile upgrade still open |
| Desktop redesign | Graphite/glass design system, shell/top bar/dock/launcher, responsive navigation, redesigned Home and Hermes layouts | Unit tests/builds and real welcome-desktop screenshots; full native interaction not yet accepted |
| Graphics preferences | Automatic and explicit graphics choices, saved preferences, reduced motion | Implemented/tested in source; automatic VirtualBox fallback defect and performance testing remain |
| Existing applications | Files, Office/Docs/Sheets/Slides, Canvas, Calc, Missions, Automations, Memory, Connections, settings and command registry retained | Broad automated regression coverage; no claim every installed app has been exercised |
| Hermes | Existing runtime client, backend lifecycle, bridge/tools, authentication and permission contracts retained | Real pinned Hermes smoke passed CI; installed model-backed chat and revision alignment remain |
| Linux packaging | Fedora bootc images, niri/greetd session, services, installer, first boot and encrypted disk path | Default amd64/arm64 and NVIDIA images built/inspected; actual amd64 UEFI install/reboot passed |
| Release validation | Exact-source checks, unpublished build path, ISO checksums, skip detection, guest logs/screenshots and synthetic-disk preservation | Reproducible evidence retained; no public release or registry publication |
| AI continuity | Project entry instructions, source map, task register and local Graphify integration | Development tooling; does not change the shipped OS |

## Passed native milestone

All runs below use source **`88d970167a9eb743a224a839491ec2631247f401`**.

| Run | Recorded result |
| --- | --- |
| [CI 41400903428](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/41400903428) | All eight jobs passed. Linux desktop **5,855 passed / 2 skipped**, Linux bridge/system **2,385 / 2**; dedicated alias suite **20 / 0** (overlaps system suite). macOS desktop **5,853 / 4**, bridge/system **2,281 / 106**. TypeScript, production builds, branding, security/signing configuration and pinned Hermes smoke passed. |
| [Image 41413455726](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/41413455726) | amd64, arm64 and NVIDIA built and inspected. `publish=false`, `disks=true`; no registry/release publication. Actual x86_64 ISO produced. |
| [Installer 41438712212](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/41438712212) | All three cases passed: encrypted, unencrypted, unencrypted with protected synthetic second disk. Actual UEFI/GRUB ISO boot, installation, first reboot, encrypted unlock, SSH restrictions, core services and desktop window. No failed system units in retained diagnostics. |

The ISO is `madx-agent-os-validation-88d9701-x86_64.iso`, 3,883,409,408 bytes.
SHA-256: `785488e0be1895046d7820df748806e8d221c75d65b177ac596dcd77544f1d58`.
On this PC it was saved in `C:/Users/divan/Downloads/`. The three actual 1280x800
screenshots and machine-readable provenance are under
[evidence/redesign-linux-2026-11-02](evidence/redesign-linux-2026-11-02/validation.json).

Skips were reviewed, not counted as passes: Linux PDFKit/root-only nft and optional
spreadsheet validators; macOS platform/tool exclusions. The documented Windows bridge
process-inspection failure reproduced on the original checkout; the corresponding
native Linux/macOS tests pass. Windows preview is not full Windows host support.
Build logs retain dracut copy and overlay-unmount messages even though later checks
and boot passed. The earlier reported GRUB failure was not reproduced; no speculative
GRUB fix is claimed.

## Latest local observations and user installation

The user's VirtualBox guest had a render node but no usable 3D renderer. Logs reported
`software EGL renderers are skipped` and `no allocator available for device`.
The guest-only session override `MADX_OS_NIRI_NESTED=1`, `WLR_RENDERER=pixman`,
`MADX_OS_SOFTWARE_GPU=1` restored the welcome desktop. This was not committed to OS
production code and is not a verified automatic fallback. Hermes was still in setup
at the last observed welcome screen. No FPS/latency measurements were taken.

The encrypted guest also hid the unlock prompt behind the splash; text-console
unlock succeeded. The graphical prompt's root cause is still unknown.

**Independent Windows/shared-ESP, Secure Boot and hardware acceptance remain open.**
The cancelled dual-boot VM was never booted. The later 2026-11-04 user report says
manual installation completed and both systems boot, with Secure Boot enabled;
graphics are unstable and Hermes is missing. This user report supersedes the
earlier unknown installation outcome, without certifying stable dual boot or RTX
driver trust. The assistant made no host partition, EFI or firmware changes.

## Work remaining before v0.1 can be called a working MVP

1. Resolve/validate manual installation and recovery, with real partition proposals.
   Actual Windows/shared-ESP and Secure Boot tests require a renewed isolated test
   request; never assume the synthetic second-disk test covers them.
2. Fix and test automatic software-renderer fallback and the encrypted splash prompt.
3. Explicitly resolve the Hermes revision policy. Installed guests used
   `0aab6dcf8b7869acbab06507c34881b53036c09a`; CI tested
   `f97608f178d1ffeca59860195ab7da295f7c8e5f`. Test real chat/streaming, tools,
   approve/deny/cancel, filesystem permissions, reconnect and recovery in installed Linux.
4. Exercise Home/Hermes and the retained apps on installed Linux. Measure frame pacing,
   input latency and resource use across graphics modes/resolutions; inspect real screenshots.
5. Test existing-profile upgrade and rollback, with preferences/history/memory/documents
   preserved. The current `dev-88d9701-amd64` update tag is intentionally unpublished;
   delivery cannot be claimed. Do not publish or change origin to bypass that restriction.
6. Finish user-facing legacy updater text and manual packaging/boot/login branding review.
   Keep legally required attribution and compatibility identifiers.
7. Validate hardware/driver/network/audio/suspend behavior, arm64 boot and NVIDIA hardware.
   Resolve release signing/trust and the existing SELinux-permissive limitation before
   making security/release claims.

Detailed acceptance conditions and file pointers are in [WORK_ITEMS.json](WORK_ITEMS.json).
Phase 1 is not fully closed. Phase 2 desktop work is implemented in part, but native
Hermes/desktop acceptance is incomplete. LoRA/self-development has not been started
in this workstream; no assertion is made about a separate Claude-owned workspace.
