# Baseline results — 2026-10-27

Commit `7ff5f81`; original branch `feat/madx-branding`; clean before this task. Work branch:
`codex/madx-foundation`. Origin is `MadXLeo/MadX-Agent-OS`; upstream already points to
`iamlukethedev/Herald-OS`. No pushes, deployments or image publications were performed.

Environment: Windows, Node 22.23.3, npm 10.9.9. WSL is not installed; Docker/Podman were not found.
Windows is a stub platform in the upstream host adapters. No Linux VM or Hermes runtime is configured.

## Reproduction and results

| Command/check | Actual baseline result |
| --- | --- |
| `npm ci --ignore-scripts --no-audit --no-fund` | PASS, 861 packages; dependency lock unchanged. Native Electron/node-pty lifecycle scripts deliberately not run. This is not a native runtime validation. |
| Pinned Hermes client source | Checked out `f97608f178d1ffeca59860195ab7da295f7c8e5f` under ignored `upstream/hermes-agent`; no Hermes user configuration modified. |
| `npm run typecheck` | PASS, renderer/shared, Electron/preload and Hermes client. |
| `npm run build` | PASS, Vite renderer and esbuild main/preload. Existing large-chunk and ineffective-dynamic-import warnings. |
| `npm test` | ATTEMPTED, stopped after default concurrency produced Windows-specific failures and resource-contention timeouts. Not a passing full suite. |
| Full Vitest rerun with `--maxWorkers=2 --reporter=json` | ATTEMPTED, stopped after over six minutes without completion/report. No full-suite totals claimed. |
| Focused existing suite below | 150 passed, 2 failed in 8 files (9.36 s). Both failures in native-notification Linux/XDG path fixtures on Windows. |
| Python 3.15 + PyYAML 6.0.3 | Dependency setup failed: no compatible wheel, C++ compiler unavailable. Used bundled Python 3.12.14 in isolated `.venv/py312` instead. |
| Python 3.12 + pytest 9.1.1 / PyYAML 6.0.3 | Dependencies installed in repository-local ignored venv. |
| `python -m pytest plugins/herald-os-bridge/tests linux/tests -q --tb=short` | BLOCKED at collection: 9 errors including Unix-only `pwd`/`os.geteuid`. No claim that bridge/system tests pass. |
| Bridge config migration, permissions and scope subset | 28 passed, 6 failed; scope tests expect an available supported host, while Windows adapter is a stub. |
| Linux/macOS native integration, VM boot/install, NVIDIA, updates/rollback | NOT RUN; supported runtime required. |
| Packaged artifact signature/branding verification | NOT RUN; no release artifact produced. |

Focused command (from repository root):

```text
npm run test --workspace apps/desktop -- shared/i18n.test.ts electron/env.test.ts electron/migrate.test.ts electron/prefs.test.ts electron/paths.test.ts electron/main-wiring.test.ts electron/native-notification.test.ts src/features/setup/FirstRunSetup.test.tsx --maxWorkers=2 --reporter=verbose
```

Existing failures in this bounded, completed run:

- `desktopEntryFor > lets the other installed entry stand in when the launch's own is missing`
- `applicationDirs > follows the XDG data directories, the personal one first`

Both assert POSIX path strings using host-native `path.join`. Keep this evidence when comparing
post-change results; do not remove the Linux behavior to make Windows tests green.

Local raw output is in ignored root `baseline-*.log` files. Re-run supported-host CI before declaring
feature parity. These limitations mean Milestone 0's baseline is documented, but the full validation
gate is not green.
