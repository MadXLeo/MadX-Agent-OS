# First implementation increment — validation

Date: 2026-10-27. This increment begins Milestone 1 after the recorded baseline; **Milestone 1 is
not complete**. Milestones 2–7 remain outstanding. No local LLM/LoRA/training/ComfyUI/self-development
capability is represented as implemented merely because its name exists in the product manifest.

## Implemented

- Central `branding/product.json`, generated typed constants, metadata/version synchronization,
  niri compatibility rules, favicon generation and a CI synchronization gate.
- Supplied metallic artwork in boot, setup, menu and About components. Original bytes preserved:
  SHA-256 `4e85c43e3f147c256d314f5f2ab065fc04f77361089d04cde2d686be5ecc81cc`.
- Product copy in English, Portuguese and Chinese catalogs, application labels, notification sender,
  window titles and legal attribution. Other untranslated hardcoded strings remain in the audit.
- Graphite/ice defaults in main and renderer; saved themes are not overwritten.
- Profile selection v1: existing Herald profile reused in place, fresh MadX profile otherwise;
  both Chromium profile paths set before startup; file/link collisions refused.
- `MADX_OS_*` precedence in the existing Electron environment accessor, keeping both legacy prefixes.
- Niri accepts MadX and legacy app IDs/titles; dock/main/renderer title agreement is tested.
- Read-only branding audit distinguishes review candidates, compatibility identifiers, notices,
  comments, fixtures, migration documentation and legacy assets. It does not claim a clean audit.

## Executed checks

| Check | Result |
| --- | --- |
| `npm run branding:check` | PASS; generated identity and metadata synchronized. |
| `npm run typecheck` | PASS across workspaces, including main/preload/renderer/shared. |
| `npm run build` | PASS; renderer + Electron main/preload emitted. Existing chunk warnings remain. |
| Changed-area Vitest suite (command below) | 190 passed, 2 failed in 13 files. Both failures are the same native-notification POSIX-path fixtures seen in the baseline; no newly failing test remains in this suite. |
| `python -m pytest linux/tests/test_window_rules.py -q` | 10 passed, including old/new identity placement equivalence. Static rules validation, not a running compositor. |
| Browser visual inspection | Actual BootScreen component rendered with a waiting-state fixture in headless Edge, 1280×800: supplied artwork loaded, copy legible, no page errors. No Electron/Hermes/OS runtime claim. Temporary harness removed. |
| `git diff --check` | PASS. |
| Input artwork integrity | Source and supplied PNG SHA-256 match. |
| Dependency diff | Only root/desktop identity/version lock metadata changed; dependency versions unchanged. |

Completed Vitest command:

```text
npm run test --workspace apps/desktop -- shared/product.test.ts shared/i18n.test.ts electron/product-profile.test.ts electron/env.test.ts electron/migrate.test.ts electron/prefs.test.ts electron/paths.test.ts electron/main-wiring.test.ts electron/native-notification.test.ts electron/shell/dock-menu.test.ts electron/office/presenter.test.ts src/shell/surfaces/dock-menu.test.ts src/features/setup/FirstRunSetup.test.tsx --maxWorkers=2 --reporter=verbose
```

The two remaining baseline failures are `desktopEntryFor > lets the other installed entry stand
in when the launch's own is missing` and `applicationDirs > follows the XDG data directories, the
personal one first`. They compare POSIX paths against host-native Windows joins. They are retained,
not disabled to claim success. Full-suite attempts and Python platform blockers are in BASELINE.md.

## Not validated / not complete

No Electron native launch, Hermes end-to-end run, native packaging, OS image, installer ISO, VM boot,
Secure Boot, NVIDIA driver, live model inference, adapter activation/training, update or rollback
was validated. Existing LICENSE/NOTICE were preserved. Native launcher PNG/ICNS, Plymouth, Linux
CLI/service labels, release artifact filenames, registries, installer identity and much inherited
documentation still carry legacy references. `npm run branding:audit -- --json` gives locations.
Legacy lowercase identifiers require migration review; some are visible in error/help output.

The desktop build in `apps/desktop/dist` is a local compiled development artifact, not a bootable
distribution or signed release. No host disk, EFI, firmware or Windows boot configuration was touched.
Nothing was pushed, merged, published or deployed. Local commits use `Codex <codex@localhost>` because
the checkout had no configured author; global/repository author settings were not changed.
