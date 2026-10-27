# Continue MadX Agent OS

Stay on `codex/madx-foundation`. Preserve the working implementation and the original baseline.
Read VALIDATION.md, REMAINING_ISSUES.md and MIGRATIONS.md. Do not repeat the initial inventory.

The next work is supported-platform Phase 1 validation: complete Linux/macOS suites, actual Hermes
integration, native packaging, staged aliases under Linux, then disposable-VM boot/install/upgrade
and rollback. Inspect the installer runtime branding before claiming Phase 1 complete. The source
copy audit and production desktop build pass; Windows-only failures and unrun gates remain explicit.

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
