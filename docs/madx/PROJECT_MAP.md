# MadX source map

All paths below are relative to the repository root. Start with `AGENTS.md` and
`docs/madx/AI_HANDOFF.md`. For symbol-level links, use the local Graphify index;
for completion evidence, use PROJECT_STATUS and WORK_ITEMS instead.

| Area | Main locations | Checks / supporting context |
| --- | --- | --- |
| Product identity | `branding/product.json`, `branding/legacy-allowlist.json`, `scripts/madx/branding.mjs`, `apps/desktop/shared/product.ts` | `linux/tests/test_branding.py`, `scripts/madx/audit-branding.mjs` |
| Electron entry / machine access | `apps/desktop/electron/main.ts`, `apps/desktop/electron/ipc/`, `apps/desktop/electron/platform/` | `apps/desktop/README.md`, `docs/ARCHITECTURE.md`; tests beside implementation |
| Preload / IPC contract | `apps/desktop/preload/index.ts`, `apps/desktop/shared/ipc.ts` | Preserve `window.heraldOS` and versioned tool/IPC contracts |
| Shell / app registry | `apps/desktop/src/shell/App.tsx`, `apps/desktop/src/shell/apps.ts`, `apps/desktop/src/shell/MainWindow.tsx`, `apps/desktop/src/shell/Dock.tsx` | Shell tests beside implementation; `docs/madx/REDESIGN.md` |
| Graphite/glass styles | `apps/desktop/src/madx-design.css`, `apps/desktop/src/styles.css`, `apps/desktop/src/components/`, `linux/themes/madx-graphite/theme.json` | `apps/desktop/DESIGN.md`, `docs/madx/REDESIGN.md` |
| Home | `apps/desktop/src/features/overview/OverviewPage.tsx`, `apps/desktop/src/features/overview/` | Uses real stores; Home is named overview in source |
| Hermes conversation / output | `apps/desktop/src/features/hermes/HermesPage.tsx`, `apps/desktop/src/features/hermes/Conversation.tsx`, `apps/desktop/src/features/hermes/ArtifactPane.tsx` | `apps/desktop/src/features/hermes/HermesPage.test.tsx`, state in `apps/desktop/src/store/` |
| Hermes lifecycle | `apps/desktop/electron/backend/manager.ts`, `apps/desktop/electron/backend/resolve.ts`, `apps/desktop/electron/backend/bridge-plugin.ts` | Adjacent tests, `scripts/madx/hermes-smoke.py`, `upstream/UPSTREAM.lock` |
| Hermes protocol client | `packages/hermes-client/src/`, `packages/hermes-client/README.md` | Workspace TypeScript checks; preserve upstream wire contracts |
| Hermes native tools / permissions | `plugins/herald-os-bridge/bridge/`, `plugins/herald-os-bridge/tests/` | `docs/SYSTEM-BRIDGE.md`, `scripts/test-bridge.sh` |
| Existing app workflows | `apps/desktop/src/features/`, `apps/desktop/src/commands/`, `apps/desktop/src/store/` | `docs/madx/FEATURE_PARITY.md`; tests beside each feature |
| Visual quality choices | `apps/desktop/shared/visual-quality.ts`, `apps/desktop/src/features/settings/sections/VisualQualitySettings.tsx` | `apps/desktop/shared/visual-quality.test.ts`; not a compositor fallback fix |
| Linux compositor / desktop startup | `linux/session/herald-os-compositor`, `linux/session/herald-os-niri-nested`, `linux/session/herald-os-session`, `linux/session/greetd-config.toml` | `linux/tests/test_session.py`; guest compositor.log and shell.log |
| Boot splash / encrypted prompt | `linux/plymouth/herald-os/herald-os.script` | Real guest screenshot and journal required; unattended encryption test is insufficient |
| CLI / compatibility | `linux/bin/herald-os`, `linux/bin/herald-os-update`, `linux/image/Containerfile` | `linux/tests/test_cli.py`, `linux/tests/test_madx_entrypoint.py`, `linux/tests/test_update.py`; `madx` is an installed alias |
| Image / dependencies | `linux/image/Containerfile`, `linux/image/Containerfile.nvidia`, `linux/image/packages.txt` | `scripts/madx/check-image.py`, `linux/tests/test_image.py`, `.github/workflows/image.yml` |
| Interactive installer | `linux/image/iso.toml`, `linux/image/finalize-root-mount.py` | `linux/tests/test_root_mount.py`, `linux/tests/test_branding.py`; no Windows dual-boot certification |
| Unattended installer testing | `linux/image/unattended.ks`, `linux/vm/efi-boot.py`, `linux/vm/guest-smoke.sh`, `linux/vm/windows-fixture.py` | `.github/workflows/installer-test.yml`, `linux/tests/test_release_validation.py`; fixture is not Windows |
| First boot / Hermes install | `linux/image/firstboot.sh`, `linux/image/herald-os-firstboot.service`, `linux/image/herald-os-hermes.service` | `linux/tests/test_firstboot.py`; record installed Hermes revision |
| Build / test entrypoints | `package.json`, `apps/desktop/package.json`, `.github/workflows/ci.yml`, `scripts/test-bridge.sh` | `docs/madx/REDESIGN_EXECUTION.md`, `docs/madx/VALIDATION.md` |
| Evidence / open work | `docs/madx/PROJECT_STATUS.md`, `docs/madx/WORK_ITEMS.json`, `docs/madx/ASTRA_PROGRESS.md`, `docs/madx/REMAINING_ISSUES.md` | `docs/madx/evidence/redesign-linux-2026-11-02/validation.json` |
| Graphify developer tooling | `scripts/madx/graphify.py`, `scripts/madx/graphify-requirements.txt`, `.graphifyignore` | `docs/madx/GRAPHIFY.md`; generated files in ignored `graphify-out/` |

Common traps: the Home page lives under `overview`; the current primary CLI is
`madx` but its implementation is still `herald-os`; Hermes installation/retry services
are not proof that `hermes serve` is healthy; the real upstream runtime is not vendored
into the tracked code graph. Legacy names often represent compatibility contracts.
