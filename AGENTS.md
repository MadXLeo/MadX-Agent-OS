# MadX Agent OS — start here

Read `docs/madx/AI_HANDOFF.md`, then `docs/madx/PROJECT_STATUS.md` and
`docs/madx/WORK_ITEMS.json` before changing this project. Use
`docs/madx/PROJECT_MAP.md` to find the implementation and tests.

## Evidence and scope

- Inspect `git status --short --branch`, HEAD and `git worktree list` first. Preserve
  existing changes. The active redesign branch is `codex/madx-desktop-redesign`;
  `codex/linux-release-validation` is a separate, older OS worktree.
- Distinguish implemented, locally tested, native CI tested, VM tested and unverified.
  The validated image source is `88d970167a9eb743a224a839491ec2631247f401`.
  Later documentation/tooling commits do not rebuild that image.
- Windows dual-boot verification was cancelled by the user. The subsequent physical
  installation attempt has no confirmed outcome. Do not mark either as passed or
  resume VM installation without a new request.
- Do not touch physical disks, Windows partitions, host EFI/firmware, or Claude's
  LoRA/ECC work. No merging, releases, tags, registry publishing or broad pushes.
  Check the current user's authorization before remote changes.
- Preserve Hermes protocols, permissions, stored data and legacy aliases. Never
  silently change the Hermes revision or update origin. LoRA/self-development is
  outside this workstream. Do not weaken tests to get a green result.
- When a remote run or OS installation is pending, return its link/state and stop;
  the user prefers to check completion and ask to continue.

## Graphify and handoff maintenance

Graphify is a development-only code index, not an OS dependency or acceptance test.
Use `python scripts/madx/graphify.py status` to check freshness, then
`python scripts/madx/graphify.py query "<code question>"` for scoped file/symbol
locations. Setup/build instructions are in `docs/madx/GRAPHIFY.md`. Missing or stale
graphs must not block source inspection: use `rg` and verify the actual files.

The project wrapper disables model backends and query logging. Do not enable cloud
upload, API-backed extraction, global assistant configuration or automatic hooks
as part of ordinary indexing. Read progress from the status documents, not graph
inferences. Update WORK_ITEMS, PROJECT_STATUS and ASTRA_PROGRESS with real evidence
after meaningful work. Keep unresolved failures and skip reasons visible.
