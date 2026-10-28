# Phase 1 release gates

Updated 2026-10-28. Source implementation is ready for supported-platform validation. Phase 1 is
**not declared complete**. No LoRA or self-development work has started.

The current Astra work adds executable Linux/image/VM gates to existing workflows and passes a
real Windows Hermes server smoke. None of the native jobs has executed on this source. Follow
ASTRA_PROGRESS.md after an authorized transfer to Linux; do not publish an image to obtain a test
ISO. Manual image builds now default to `publish=false`.

## Required before completion

1. Run the complete desktop and bridge suites on Linux and macOS. On Windows, 128 main-process
   failures were reproduced against the original `7ff5f81` source. These involve Unix paths,
   permissions, symlinks, sockets and native runtime assumptions. They remain failures, not passes.
2. Run the three real-filesystem alias migration tests on Linux: repeat install/remove, collision
   refusal, partial-write rollback and symlink-parent containment. Windows cannot create the
   required symlinks here. Confirm systemd resolves each MadX alias to the existing unit; do not
   enable duplicate units. Run `systemd-analyze verify` on the installed units.
3. Build and inspect Linux tarballs, both Arch packages and macOS DMG/ZIP packages. Verify icons,
   executable names, source checksums, resource inclusion and the generated package audit. Exercise
   existing desktop notifications and macOS permissions with the retained application ID.
4. Build the pinned bootc image and ISO in a disposable Linux environment. Verify os-release,
   ISO volume metadata, Plymouth (including encrypted-disk password prompts), login, first boot,
   offline Hermes recovery and all compositor dialogs. Inspect the installer runtime branding and
   boot menu: ISO metadata alone does not prove Anaconda's visual skin or title is MadX-branded.
   A builder-specific installer branding layer may still be required after inspecting that ISO.
5. Test fresh install, upgrade from an existing upstream install, reboot and rollback using isolated
   virtual disks. Hash preferences, browser profiles, Hermes memories, plugin settings and documents
   before/after. Verify old and new command names and service names address the same implementation.
6. Run actual Hermes chat, tools, approvals, routines and provider recovery against the pinned
   engine. Real Windows API health/authentication, bridge discovery, memory, skills and restart
   now pass. Linux service startup, host tools, desktop recovery and model-backed operation remain
   unvalidated. First boot currently installs Hermes from `main` unless an installation ref is set;
   capture that actual revision and validate it as well as the source/client pin before release.
7. Exercise NVIDIA image build/kernel matching, encrypted installation, recovery and dual-boot
   scenarios in disposable VMs only. The previously reported GRUB failure still needs its logs;
   no root cause or fix has been claimed.
8. Validate MadX registry ownership, signing and release downloads. No image or release was
   published. Current registry references are build configuration, not a claim that tags exist.
9. Replace historical documentation screenshots with captures from the validated native build.
   They are explicitly labeled as upstream references, not passed off as current MadX screenshots.

The simulated Windows GPT case checks an adjacent disk only: shared-ESP installation, boot-menu
coexistence and an actual Windows boot remain untested. Installer UI/branding and Plymouth prompts
also need visual inspection; unattended text mode does not cover the interactive storage UI.
NVIDIA remains an optional CI leg upstream; an overall workflow success is insufficient proof
that the NVIDIA image passed. Require that leg's own build/inspection report for laptop readiness.

Existing source uses SELinux permissive mode (ADR-012), and this checkout has no committed project
cosign public key. Preserve these explicit upstream/release limitations; source validation does
not certify a hardened or signed release. Secret Service/keyring work is a separate Claude branch
dependency and must be reviewed after an authorized integration, not duplicated here.

## Intentionally retained names

| Contract | Reason and removal condition |
| --- | --- |
| `@herald-os/*`, `window.heraldOS`, IPC/tool IDs and `herald-os-bridge` | Keep Hermes and plugin API compatibility. A future versioned API migration needs integration and rollback tests. |
| Existing `Herald OS` profile, `herald-*` storage keys and browser partitions | Existing data is reused, never silently merged or discarded. Fresh profiles use `madx-agent-os`. |
| `herald-os` executable, desktop IDs and `dev.iamluke.heraldos` | Keep shell scripts, notifications, compositor matching and permission history working. MadX aliases and visible labels are added. |
| `/opt/herald-os`, `/usr/share/herald-os`, user config/state and control sockets | Preserve atomic tarball swaps, paths used by older versions and active settings. Aliases point to the same installation. |
| `herald-os-*.service/timer`, first-boot markers and firewall zone ID | Keep ordering, enablement and completion state. Alias unit files do not start a second instance. |
| Legacy theme IDs, file-format namespaces and Omarchy keys | Existing preferences and saved files still load. New defaults use `madx-graphite`; old theme colors remain intact. |
| Plymouth directory, signing-key path and resource filenames | These are shared installation contracts. Artwork and display labels are MadX. |
| Historical migration markers and development VM checkout | Readers still recognize older installations; old VM provisioning paths remain valid. |
| LICENSE, NOTICE, About provenance and historical design records | Preserve legal obligations and accurate authorship. |

The source copy audit has explicit reviewed exceptions in `branding/legacy-allowlist.json`.
Lowercase identifier findings are not automatically exempted; the table above records their
contract families. Native packages still need inspection.

## Installer references

ISO volume/application/publisher fields use the upstream
[Image Builder ISO metadata schema](https://osbuild.org/docs/user-guide/blueprint-reference/#iso-media-options-).
The [Anaconda customization documentation](https://anaconda-installer.readthedocs.io/en/latest/anaconda-webui/docs/customization.html)
describes a separate installer runtime branding layer. The pinned ISO builder must be inspected
before selecting that layer; do not replace its storage workflow merely to change the logo.

No host Windows partition, EFI entry, firmware setting or bootloader was modified.
