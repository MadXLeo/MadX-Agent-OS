# Continue MadX Agent OS

Continue only `codex/linux-release-validation`; preserve the current working tree and history.
Do not restart the audit or modify Claude's separate workspace. Read ASTRA_PROGRESS.md and
REMAINING_ISSUES.md for evidence and open gates; VALIDATION_RESULTS.json records exact revisions.

## User's waiting preference

When CI, image creation or installer testing needs time, stop and report its run link. Do not
keep polling or waiting. Resume only when the user says to continue. Do not launch duplicate runs.

## Completed boot/install milestone

Validated source: `5b704d64d7c154138515b60a26f20ad7f75a1690`.

- CI 41093321542 attempt 2 passed: Linux system 2,362/two reviewed skips, aliases 19/19,
  desktop 5,835/two skips; macOS system 2,258/106 platform skips, desktop 5,833/four skips.
  Both typechecks/builds, branding, scripts, secret scan and pinned Hermes passed.
- Unpublished image 41098826626 passed with publish=false/disks=true. Default amd64/arm64 and
  NVIDIA passed filesystem/systemd/Electron checks. The actual ISO is 3,883,495,424 bytes,
  SHA-256 `3d4b96047443788737abf318a4ff178354714bcdcec53000f9a63f20a65da853`.
- Installer 41172111127 passed all three cases against that exact source/image, account=madx-test,
  empty tag. Each verified the full ISO checksum, booted through UEFI, installed, rebooted and
  passed core acceptance. Encrypted unlock, SSH restrictions and system/user aliases passed.
  The synthetic adjacent GPT disk checksum was unchanged after install and acceptance.
- The root-remount repair is proven: service success, Btrfs rootflags/compression preserved,
  other fstab mounts/encryption arguments retained. The GPU unset-HOME error is absent.
  No GRUB installation error was reproduced. All three final screenshots show the MadX welcome
  desktop; interactive onboarding/use is not tested.
- All five CI archives and three installer archives were downloaded and SHA-256/CRC verified.
  Small image archives were verified; amd64 ISO verification ran in the installer jobs. The
  full amd64 image ZIP digest remains GitHub-reported. Exact hashes are in VALIDATION_RESULTS.json.

Evidence documentation is committed locally after the milestone. Remote tested source remains
`5b704d6`; check live Git state before a later push. A later documentation commit is not the source
of the executed ISO. Do not rerun this completed repair merely because older historical records
describe its earlier failures.

## Remaining MVP work, in order

1. Resolve the installed Hermes validation gap explicitly. All guests installed
   `78077b2b8f83ac7d9293d3269df7ef20e3a9a994` via existing upstream-main behavior; CI tests unchanged
   pin `f97608f178d1ffeca59860195ab7da295f7c8e5f`. The command is available and retry-install unit
   condition=false is expected, but model-backed chat, tools and approvals are unverified. Review
   installation/ref handling and define the exact installed/tested revision before changing it;
   do not silently switch revisions, use credentials or add paid infrastructure.
2. Exercise interactive onboarding, desktop controls, host tools and provider recovery inside a
   disposable VM. Inspect interactive installer branding and graphical boot/password prompts;
   the unattended serial harness disables Plymouth for encrypted unlock and does not prove its UI.
3. Validate upgrade and rollback from an existing upstream profile on disposable virtual disks,
   comparing preferences, browser profiles, memories, plugins and documents before/after. The
   root helper only handles fresh supported Btrfs installs; existing/custom layouts need coverage.
   The configured dev registry origin is unpublished and rollback is null. Prepare an isolated
   upgrade path within current boundaries; do not silently switch origin or publish images.
4. Complete native package checks and remaining hardware/branding gates in REMAINING_ISSUES.md.
   NVIDIA builds now pass; actual GPU/hardware and arm64 boot are unverified. An adjacent mock
   Windows disk is not shared-ESP, Windows-boot or physical laptop certification.

For any substantive fix, run focused checks, review/commit on this branch, then use the established
CI -> unpublished image -> isolated installer path with matching full source revisions. Stop at
each remote run link and resume only on user instruction. Preserve all successful acceptance gates.

The Windows fixture limitation is unchanged: 54 passes, 201 WinError 1314 failures and 28 skips
in the wider local fixture run; representative baseline cases reproduce missing symlink privilege.
These are not passed tests. Linux/macOS suites subsequently passed on their supported hosts.

Phase 1 and a working agent MVP remain incomplete. Authorization covers this branch's pushes,
CI, unpublished images and disposable UEFI VMs only. No main merge, force push, tags, release,
registry publication, paid infrastructure or new host software. Never touch host Windows
partitions, EFI or firmware. Preserve compatibility identifiers and legal attribution. Do not
begin LoRA, self-development or Phase 2 implementation.
