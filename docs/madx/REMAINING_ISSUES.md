# Phase 1 release gates

Updated 2026-10-30. Native CI and unpublished image builds have run. Phase 1 is
**not declared complete**. No LoRA or self-development work has started.

Latest blocker: CI 41000794337 at `c430078` failed one stale installer-test assertion on each native
platform (Linux 2,361 passed/one failed/two skips; macOS 2,257 passed/one failed/106 skips). All 15
root-mount/GPU tests and all 19 aliases passed in both full suites. Desktop, typecheck/build, branding,
secret scan and pinned Hermes passed. The assertion is corrected to verify both post-install scripts
and their distinct execution contexts. 23 focused local tests, both preparation fixtures, actionlint
and a portable check of the exact parser assertions pass. The native fixture remains blocked on
Windows by symlink permissions; fresh CI is required before building the repaired image.

The user authorized the named validation branch and disposable Linux/UEFI workflows. The initial
approved commit `e062c0334dcb382236b18a60422eab0e46a0d8d2` was pushed and executed as
[CI 40684976475](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40684976475).
Linux desktop tests (5,835 passed, two optional spreadsheet-validator skips), TypeScript, branding,
production build, pinned Hermes runtime, native input checks and the full-history secret scan passed.
All 19 branding/alias cases in the full Linux report passed without skips. Both macOS jobs were
cancelled without execution.

The Linux bridge/system suite had eight failures and 27 skips. Stale documentation anchors,
misnamed package fixtures and self-app matching fixtures have been repaired in focused commits.
The runner now must enable and prove user namespaces instead of skipping 25 migration tests.
The two reviewed exclusions (macOS PDFKit and root-only nft syntax) remain explicitly unexecuted.
Repair revision `e8e6010b38a351f2dfa6f6ac553bd0a901bae955` passed
[CI 40741143041](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40741143041): Linux bridge/system
2,309 passed with two reviewed exclusions, dedicated aliases 19/19, Linux desktop 5,835 passed
(two skips), macOS desktop 5,833 passed (four skips), macOS bridge/system 2,205 passed (106 skips).
Typechecks, both desktop builds and real Linux Hermes passed. Skips are itemized in the progress log.
See ASTRA_PROGRESS.md for exact evidence, artifact checksums and subsequent results.

The image dispatch initially failed with 404 because GitHub had not registered the workflows.
Registration-only branch jobs fixed this in `606e1e1`; no main merge or publishing was needed.
Image run 40743693944 at `606e1e1be710451f80510d6d355518e20a023b95` built and inspected the default
amd64/arm64 images and produced an actual 3,883,882,496-byte ISO with publish=false and disks=true.
Systemd unit verification and packaged Electron execution passed. CI 40743566443 fully passed
after retrying the initially cancelled macOS jobs. All three jobs in installer run 40777283477
verified the full ISO checksum, then failed before boot because the harness did not resolve the
ISO's included deployment kickstart. Repair `da90688` passed full CI 40778418968. Actual ISO metadata
then exposed a separate appended-EFI-partition mismatch in the test setup, repaired in `2290c81`.
That repair passed 49 focused tests/actionlint and full CI 40780000937 (Linux bridge 2,328/two skips;
macOS bridge 2,224/106 skips; both desktop suites/builds and real Hermes passed). Unpublished image
40780003482 built and inspected both default architectures and a new ISO. Installer 40811638765
verified the ISO, then all cases failed before boot on the account include generated inside the
guest. Repair `161557f` moves deployment validation before test-account injection; 50 focused tests
and both workflow preparation-step fixtures pass. Full CI 40812157730 passed: Linux system
2,329/two skips, macOS system 2,225/106 skips, both desktop suites/builds and real Hermes passed.
Unpublished image 40812159188 completed at that source; both default images/inspections and ISO build
passed. Installer 40814588924 verified that ISO, booted it through UEFI and completed installation
in all three cases. Both unencrypted guests rebooted into the MadX graphical desktop; screenshots
were inspected. The adjacent synthetic GPT disk retained its hash. Overall acceptance failed:
Anaconda lacked the external base64 executable, dropping the SSH key, and the encrypted guest
remained at its unlock prompt. No GRUB installation failure was reproduced.
Commits `cb55130` and `448e85e` repair the key codec/error handling and serial input/readiness checks.
CI 40848022569 passed at exact source `448e85ea672fd4b00f6b581f5b27b5d858264a8e`:
Linux system 2,336/two reviewed skips, macOS system 2,232/106 platform skips, all 19 aliases,
both desktop suites/typechecks/builds, branding and pinned Hermes passed. New account regression
tests passed on both native platforms. Unpublished image 40848023781 completed with both default
images and a new ISO; NVIDIA remains blocked. Installer 40850572175 installed and rebooted all three
cases, including encrypted unlock; all accepted the test SSH key and displayed the MadX welcome
desktop. The protected synthetic GPT disk hash was unchanged. Overall acceptance still failed:
Fedora advertises GSSAPI beyond the documented managed keys-only policy, and the probe called
root-only bootc status as an ordinary user. Repairs `e9d8431`/`b2beb0a` enforce the authentication
method policy and capture privileged read-only status with a test-only boot unit (no sudo grant).
CI 40896115633 passed 2,346 Linux system cases, including all 11 new policy/status tests, but
failed the new test's parser dependency declaration. Commit `7f88d80` fixes it; seven affected
local tests pass. CI 40898401729 passed all Linux jobs at `7f88d80a19d99e144fec97ee4ee8b8d3d86440ef`
(system 2,347/two reviewed skips, aliases 19/19, desktop 5,835/two skips, build/typecheck/branding
and Hermes). Its macOS jobs were cancelled before execution because no hosted runner acquired them;
GitHub reports macOS arm64 capacity constraints. Attempt 2 passed: macOS system 2,243/106 skips,
desktop 5,833/four skips, typecheck/build passed. Overall CI is now success at `7f88d80`; all five
evidence archives were downloaded and SHA-256 verified. Skips are not counted as executed passes.
The superseded image run 40896705234 was cancelled. Image 40899343029 completed at `7f88d80`;
both default images and a real ISO passed build/inspection with publication disabled. Full source
labels and unchanged Hermes pin were verified. Installer 40945372298 completed against that exact
source/image. All three cases passed SSH restrictions, privileged deployment status,
core service/alias checks and desktop-window detection, but failed the root remount check. Journals
confirm that Btrfs options in Anaconda's root fstab entry cannot reconfigure the composefs overlay.
Repair `c5dfa69` moves physical root options into the installed boot entry, preserves other mounts
and keeps the service failure gate enabled. It applies only during fresh installation; custom
filesystem layouts retain their previous behavior and need separate testing. `35fea98` fixes the
observed GPU-check HOME error; `21eda78` prevents CRLF account-snippet parsing failures on Windows.
23 focused tests, both preparation fixtures, workflow/source and branding checks pass. All repairs
still require new native CI and image/VM evidence. The broader Windows fixture run is 54 passed,
201 failures (all WinError 1314, missing symlink privilege), 28 skipped; baseline fixtures reproduce
this limitation. Native tests remain enabled.
Superseded image run 40778438792 was deliberately cancelled. The exact-source gate is unchanged.
Encrypted first reboot is proven. Core acceptance remains blocked by the remount failure; interactive
desktop operation remains unverified. Installed Hermes is `67d47601bc5f8ed322451a672c843ed0e1a7c42c`,
different from CI pin `f97608f178d1ffeca59860195ab7da295f7c8e5f`, because existing first-boot behavior
tracks upstream main. No revision was changed by this repair. First-boot services report success; the Hermes retry-install unit
is inactive because its pending-install condition is false. This does not prove model-serving
operation. The earlier privilege-probe failure is fixed and confirmed in all three real VMs.
The NVIDIA image failed because the upstream akmods image for Fedora kernel
`7.2.13-200.fc44.x86_64` was unavailable; no downgrade or revision switch was made.
Image/installer provenance must match exactly. The Windows host still has no
Linux runtime; all native execution is on disposable GitHub runners. No new host software, registry
image, release, tag, main merge or physical installation was authorized or performed.

## Required before completion

1. Preserve passing full Linux/macOS desktop and bridge CI on each repair revision. On Windows, 128 main-process
   failures were reproduced against the original `7ff5f81` source. These involve Unix paths,
   permissions, symlinks, sockets and native runtime assumptions. They remain failures, not passes.
2. Real-filesystem alias migration checks now pass on Linux, including repeat install/remove,
   collision refusal, partial-write rollback and symlink-parent containment. Image systemd unit
   verification also passes. Confirm the booted guest resolves each MadX alias to the existing
   unit; do not enable duplicate units. Installed-service runtime remains unverified.
3. Build and inspect Linux tarballs, both Arch packages and macOS DMG/ZIP packages. Verify icons,
   executable names, source checksums, resource inclusion and the generated package audit. Exercise
   existing desktop notifications and macOS permissions with the retained application ID.
4. Default bootc image/ISO builds, os-release and ISO metadata inspections have passed. Verify
   Plymouth (including encrypted-disk password prompts), login, first boot,
   offline Hermes recovery and all compositor dialogs. Inspect the installer runtime branding and
   boot menu: ISO metadata alone does not prove Anaconda's visual skin or title is MadX-branded.
   A builder-specific installer branding layer may still be required after inspecting that ISO.
5. Complete fresh-install acceptance (all three installs and two unencrypted reboots ran), then
   test upgrade from an existing upstream install, reboot and rollback using isolated
   virtual disks. Hash preferences, browser profiles, Hermes memories, plugin settings and documents
   before/after. Verify old and new command names and service names address the same implementation.
6. Run actual Hermes chat, tools, approvals, routines and provider recovery against the pinned
   engine. Real Windows API health/authentication, bridge discovery, memory, skills and restart
   now pass. Linux service startup, host tools, desktop recovery and model-backed operation remain
   unvalidated. First boot currently installs Hermes from `main` unless an installation ref is set;
   capture that actual revision and validate it as well as the source/client pin before release.
7. Exercise NVIDIA image build/kernel matching, encrypted installation, recovery and dual-boot
   scenarios in disposable VMs only. The encrypted install and on-disk password checks passed,
   and automated first-boot unlock now passes. The remount service failure still needs diagnosis.
   The previously reported GRUB error was not reproduced;
   no GRUB root cause or fix has been claimed.
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
