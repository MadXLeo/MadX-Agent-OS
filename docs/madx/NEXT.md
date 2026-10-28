# Continue MadX Agent OS

Continue `codex/linux-release-validation`, based on `codex/madx-foundation` at `50dd6d4`.
Read ASTRA_PROGRESS.md, VALIDATION.md, REMAINING_ISSUES.md and MIGRATIONS.md. Preserve existing
work and do not repeat the initial inventory. Do not merge or modify Claude's separate workspace.

The next work requires approval to push this branch and run existing CI/image/installer workflows.
The host has no Linux runtime, and remote main lacks CI's manual trigger; the branch's push trigger
now runs CI without a merge. Use the exact commands in ASTRA_PROGRESS.md. Run the image workflow
on this branch with publish=false and disks=true, then
pass its run ID to installer-test's image_run. Inspect the first real Anaconda/GRUB diagnostics,
boot screenshots and guest checks before any installer fix. Source and Windows Hermes runtime
checks pass; Linux, model-backed chat and update/rollback gates remain open. See ASTRA_PROGRESS.md
for the exact sequence, evidence limits and the isolated update/rollback procedure. Keep image
and installer revisions identical: the installer rejects mismatched image-run evidence.

Do not start LoRA Studio, self-development or Phase 2 implementation until these gates pass.
PHASE2_PLAN.md is planning only. Keep all compatibility identifiers listed in MIGRATIONS.md and
REMAINING_ISSUES.md. Do not publish or push without authorization. Never use host Windows disks,
EFI entries or firmware for testing.

Useful local checks:

```text
npm run branding:check
node scripts/madx/audit-branding.mjs --check
npm run typecheck
npm run build
npm exec --workspace apps/desktop -- vitest run src shared --maxWorkers=2
python scripts/madx/check-native.py --bash <bash-executable>
python -m pytest linux/tests/test_branding.py linux/tests/test_window_rules.py linux/tests/test_vm_disks.py -q
```

The complete native suites remain enabled in CI; do not disable failing tests to manufacture a
passing release. Credentials, signing keys and publishing are separate from local source validation.
