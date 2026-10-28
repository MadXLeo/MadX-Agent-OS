# Phase 1 validation

## Continuation — awaiting authorized Linux execution

Started at `a486db3` on `codex/linux-release-validation`. The latest continuation repaired the
bridge CI runner regression, added full Linux skip accounting and image-run provenance checks,
and prepared exact remote invocations. Resumed at `310cfda` with all pending docs preserved. The
Git Bash path-spelling test defect was reproduced, then fixed using exact argument capture and
requirements-file identity. The expanded local run is **76 passed, 26 skipped, zero failed**.
Three installer workflow tests
pass; Actionlint, three YAML/46 Bash workflow blocks, branding and 72 Python/41 Bash/six TOML
source checks pass. TypeScript checks were rerun and pass. The native JUnit gate correctly rejects
the actual Windows report's 26 skipped cases. No desktop or Hermes runtime implementation changed;
their earlier full tests/build/smoke below were not repeated. Full details, logs, gates and approval scope are in
ASTRA_PROGRESS.md. No image/ISO/VM result is claimed.

## Astra Linux validation preparation — 2026-10-28

Started clean at `50dd6d4` on `codex/madx-foundation`; work continues on
`codex/linux-release-validation`. The original five commits remain intact. See
[ASTRA_PROGRESS.md](ASTRA_PROGRESS.md) for exact commands, artifacts, commits and the Linux handoff.

| Fresh check | Result |
| --- | --- |
| Initial Linux source baseline | 40 passed, 26 Windows/platform skips. |
| TypeScript checks and production desktop build | PASS; existing bundler warnings remain. |
| Full renderer/shared suite | 4,915 passed, 5 skipped, 0 failed; 351 files. |
| Focused main-process regressions | 89 passed in six files. |
| Release harness, installer parser, branding, window rules and disk tests | 60 passed, 26 skipped; includes real pykickstart parsing of generated diagnostics and disk restrictions. |
| Installer workflow/account tests | 3 passed, 218 deselected. |
| Branding synchronization and copy audit | PASS; compatibility exceptions retained. |
| Native source parsing | 71 Python, 41 Bash, 6 TOML files; PASS. |
| Edited workflows | Actionlint 1.7.12 PASS; YAML and Bash syntax checked separately. No Linux job execution implied. |
| Actual Hermes 0.21.5 server, pinned `f97608f178d1ffeca59860195ab7da295f7c8e5f` | PASS on Windows: two real process launches, API health, token rejection, bridge tool registration, memory, skills and persistence across restart. |

The Hermes smoke uses a disposable profile, isolated Python environment and no provider credentials.
It does not execute a model conversation, desktop tool, approval dialog or systemd service.
No configured provider was found; common local-provider ports 11434 and 1234 were closed.
The temporary profile lives outside `.venv`, because Hermes excludes skill paths containing that
component. Logs redact the throwaway session token; existing user profiles are untouched.

CI now retains desktop/Python reports, requires Linux alias tests without skips, runs the real
Hermes smoke on Ubuntu, inspects built-image contents/systemd/Electron, and supports unpublished
ISO artifacts. The installer harness boots actual UEFI media, captures Anaconda/OSTree diagnostics,
checks an installed desktop over SSH, and hashes an adjacent synthetic GPT disk before/after.
These are implemented checks awaiting Linux execution, not successful image/boot results.

No container image, native Linux app package, ISO or booted guest was produced here. WSL is not
installed; Podman/Docker/QEMU are unavailable. GitHub's branch search returned no matching
foundation branch; its limited PR-run query returned no runs for `50dd6d4`. No code was pushed
and no remote workflow was dispatched. Native runs cannot validate unpublished local changes.
The 128 previously reproduced Windows main-process failures remain open, not waived or rerun.
Claude's separate keyring/model-plan branch was neither inspected nor merged.

## Prior Phase 1 source evidence — 2026-10-27

Phase 1 source changes are implemented and checked locally; **Phase 1 is not yet complete**.
Supported-platform and VM release gates remain in [REMAINING_ISSUES.md](REMAINING_ISSUES.md).
No LoRA or self-development feature has been started. [BASELINE.md](BASELINE.md) preserves the
original audit; this report supersedes the earlier first-increment status.

Validated source commits: `cc829a8` (native identity, packaging and Linux aliases) and `9dd5ce9`
(desktop/bridge copy, compatibility fixes and branding audit). Earlier foundation commits
`5183b5c` and `2422689` are retained. The final documentation commit records evidence and open gates.

## Passing evidence

| Check | Result |
| --- | --- |
| `npm run typecheck` | PASS, all workspaces (renderer, Electron/preload and Hermes client). |
| `npm run build` | PASS, production renderer and Electron main/preload bundles. Existing large-chunk/dynamic-import warnings remain. |
| Renderer/shared Vitest (`src shared --maxWorkers=2`) | **351 files, 4,915 passed, 0 failed, 5 skipped**; 4,920 tests total. |
| Main-process migration regression recheck | **6 files, 89 passed**. Includes screen-recording permission copy, dictation, notes, templates, pet presentation detection and shared old/new title cases. |
| `npm run branding:check` | PASS, generated product metadata, native config and artwork hashes. |
| `node scripts/madx/audit-branding.mjs --check` | PASS, no unreviewed capitalized legacy product-copy candidates. Compatibility, attribution, fixtures and historical records are separately classified. Native packages are outside this check. |
| Linux branding, niri rules and VM-artifact source tests | **40 passed, 26 skipped** on this host. Three skips require symlinks; 23 require Linux. |
| `python scripts/madx/check-native.py` | PASS: parses 65 Python, 39 Bash and 6 TOML files; checks package helper checksums, names and registry agreement. Never executes installers. |
| Workflow syntax | PASS: five edited workflow YAML files and their shell blocks parse. Arch/release jobs now explicitly require MadX aliases, theme and migration resources; those jobs have not run here. |
| `git diff --check` | PASS. |
| Compatibility source comparison with `7ff5f81` | All 386 literal command IDs in 39 command modules retained; IPC/preload contract files, LICENSE, NOTICE and upstream lock unchanged. |
| Artwork | Original input SHA-256 retained: `4e85c43e3f147c256d314f5f2ab065fc04f77361089d04cde2d686be5ecc81cc`. PNG, ICO, ICNS and Plymouth exports checked by manifest; monogram visually inspected. |
| Visual fixture | Actual BootScreen rendered in headless Edge at 1280x800; supplied artwork and product text loaded with no page errors. This is a renderer fixture, not a native boot. |

## Main-process failures investigated

The broad main-process/scripts run (plus four renderer regression files and the shared title tests)
reported **840 passed, 148 failed, 17 skipped**, 1,005 total tests in 80 files. Running the 26 failing
files from the original `7ff5f81` source, in an isolated checkout with the same dependencies, reproduced
**128 failures** (427 passed, 12 skipped out of 567). File/test identity comparison isolated 20
additional failures: expected display strings and a source-level audience-title assertion. Those
were corrected; the six-file 89-test recheck passes. The earlier renderer failures also received a
complete clean rerun, reported above.

The remaining 128 main-process failures are **not waived or converted into passes**. Windows lacks
the Unix filesystem modes, symlink permissions, socket behavior and POSIX paths these tests assume.
Some native package tests need Electron/native tooling. The full supported Linux/macOS suites are
still required. The broader Python suite cannot collect CLI modules requiring `pwd` on Windows.
The new alias mutation tests also need a Linux filesystem run before release.

Local raw logs are ignored `madx-*.log` files; compact evidence is committed in
[VALIDATION_RESULTS.json](VALIDATION_RESULTS.json). Full local Vitest JSON reports are in `.venv/`.
The original source comparison was extracted under `.venv/validation-baseline`; it did not replace
or reset the working tree. Test runs use two workers to keep resource use bounded. Electron binary
auto-download was disabled for the main-process comparison/recheck.

Reproduce the passing desktop checks from the repository root:

```text
npm run typecheck
npm run build
npm exec --workspace apps/desktop -- vitest run src shared --maxWorkers=2
npm exec --workspace apps/desktop -- vitest run electron/calc/notes.test.ts electron/ipc/capture.test.ts electron/ipc/dictation.test.ts electron/office/templates.test.ts electron/pet/window.test.ts shared/product-windows.test.ts --maxWorkers=2
```

Set `ELECTRON_SKIP_BINARY_DOWNLOAD=1` for the last command on this Windows host. The full native
test suite must still run with Electron installed on supported Linux/macOS hosts.

## Regressions fixed

- A display constant narrowed a Canvas default argument to a literal type; callers can again pass
  arbitrary LUT titles.
- Spoken Calc requests recognize both names; legacy app-name aliases remain available to routines.
- Slides audience/fullscreen detection is shared between the pet and screensaver and accepts both
  identities. Niri also floats the renamed Canvas dialog correctly.
- Translation assertions exclude the actual product names; user-supplied text is never rewritten.
- macOS build/signature checks follow the configured app/executable and new artifact names.
- Release producers, package consumers, registry policy and both image detectors agree on MadX
  names while accepting installed legacy image IDs.
- Exact legacy Omarchy menu rows can be upgraded or removed; custom rows are preserved.

## Scope and limits

Generated assets, user-facing desktop/bridge/CLI copy, Linux service descriptions, launchers,
package names, release filenames, OCI/os-release/ISO metadata and fresh graphite/cyan defaults are
updated. Linux alias installation refuses conflicts, preflights every destination, rolls back links
created by a failed attempt and never moves user data or enables another service. Existing state,
Hermes APIs, app IDs, sockets, units and rollback directories remain compatible.

The ISO metadata follows the [Image Builder schema](https://osbuild.org/docs/user-guide/blueprint-reference/#iso-media-options-).
The encrypted interactive kickstart remains unchanged. Its Anaconda skin and boot-menu titles still
need inspection in an actual ISO; metadata is not proof of complete installer visual branding.

No native app, Hermes end-to-end connection, Linux package/image/ISO, Secure Boot, NVIDIA driver,
VM installation, system upgrade or rollback was executed successfully here. Source compilation is
not functional parity certification. There is no Docker/Podman or installed Linux VM in this host.

LICENSE, NOTICE, the pinned Hermes revision and dependency versions remain unchanged. Nothing was
pushed, published, installed onto the host, or written to host Windows partitions, EFI or firmware.
Local commits use `Codex <codex@localhost>` because no Git author was configured; Git settings stay
unchanged. Phase 2 has a gated plan, with no implementation started.
