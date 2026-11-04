# AI handoff — MadX Agent OS

Updated 2026-11-04, Asia/Calcutta. Start with this file; do not restart the migration.

## Read order

1. `AGENTS.md`: scope, compatibility and authorization boundaries.
2. [PROJECT_STATUS.md](PROJECT_STATUS.md): current progress, real evidence and limits.
3. [WORK_ITEMS.json](WORK_ITEMS.json): prioritized open tasks and acceptance conditions.
4. [PROJECT_MAP.md](PROJECT_MAP.md): source and test locations.
5. [GRAPHIFY.md](GRAPHIFY.md): local code graph setup, queries and freshness checks.
6. [ASTRA_PROGRESS.md](ASTRA_PROGRESS.md), [REMAINING_ISSUES.md](REMAINING_ISSUES.md),
   [FEATURE_PARITY.md](FEATURE_PARITY.md): detailed evidence and historical context.

## Worktree identity

The active worktree on Divanshu's PC is
`C:/Users/divan/Documents/MadX-Agent-OS-redesign`, branch `codex/madx-desktop-redesign`.
The original `C:/Users/divan/Documents/MadX-Agent-OS` is a separate worktree on
`codex/linux-release-validation` at `2e844ca74b87b04395bb6232b368edc5b8bea451`.
Do not edit the older checkout assuming it contains the redesign. Paths inside the
guides are repository-relative so a fresh clone can use them on other machines.

Validated code/image revision: `88d970167a9eb743a224a839491ec2631247f401`.
Evidence documentation was committed locally as `8c325286387cc11747d40decf1986211e72ae770`.
This handoff/Graphify change comes afterward. Check HEAD and remote state instead
of assuming documentation/tooling commits are included in the tested ISO or pushed.

## Immediate context

- New priority: Alienware m16 R2 / Intel Xe + RTX 4070 Laptop graphics recovery. The user's
  hardware report says installation and subsequent Windows boot succeeded with Secure Boot
  enabled, but graphical freezes/HDMI errors and missing Hermes remain. This supersedes the
  unknown installation outcome below; it is user-reported, not independently accepted.
  Read [ALIENWARE_RECOVERY.md](ALIENWARE_RECOVERY.md) for confirmed source defects, candidate
  fixes, exact console diagnostics and remaining hardware gates. Candidate source commit:
  `186681dd265a113d8f405877abacad4b7945329a`. No new ISO has been built.
- The LinkedIn screenshot-video work is paused while the hardware failure takes priority.
  Do not turn its earlier VM screenshots into claims of working physical RTX graphics.

- Native CI, image and all three isolated UEFI installer cases passed. Do not rerun
  the old failures at an obsolete SHA or claim that every feature is certified.
- VirtualBox with 3D disabled failed to start niri's renderer. A guest-only software
  fallback restored the graphical welcome screen. It is not a production fix.
- The user's encrypted VM looked stuck at the splash screen; a text console allowed
  unlocking. The graphical password prompt still needs diagnosis.
- Windows dual-boot testing was explicitly cancelled. A separate test VM was created
  but never booted. The user later reported only one disk visible in the physical
  installer and difficulty partitioning. No screenshot/result of that screen, completed
  install, partition preservation or Windows reboot is available. Treat all as unknown.
- No model-backed installed Hermes chat, performance benchmark or successful update/
  rollback cycle has been recorded. Preserve these release blockers.

## Continue without losing context

Use the task IDs in WORK_ITEMS, inspect the referenced source, reproduce one issue,
make a focused fix, run relevant tests, then record exact source/run/evidence details.
For native release validation use [REDESIGN_EXECUTION.md](REDESIGN_EXECUTION.md).
Do not dispatch workflows or publish new changes merely because old, exact-commit
authorization appears in historical notes. If work pauses, record the last completed
action, pending run link and concrete next action. Never put credentials in the handoff.

Graphify maps symbols and relationships; it does not know whether an installation
passed. Query results are navigation hints. Source code, current user instructions
and retained validation evidence remain authoritative.
