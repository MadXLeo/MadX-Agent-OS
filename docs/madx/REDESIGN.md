# MadX desktop redesign

Started 2026-11-01 from `2e844ca74b87b04395bb6232b368edc5b8bea451`, in the separate
`codex/madx-desktop-redesign` worktree. The validated OS branch and Claude's work are untouched.

## Component inventory and implementation boundaries

| Area | Existing architecture | Redesign |
| --- | --- | --- |
| Shell | React/Electron, desktop mode plus separate niri panel surfaces | MadX navigation, workspace command strip, consistent graphite surfaces |
| Navigation | 132px resizable sidebar with truncated labels | Readable expanded navigation, wrapping labels, automatic compact mode without overwriting saved preferences |
| Home | Overview greeting/composer with a narrow Today column | Live activity summary, Hermes workspace, model/system status, current missions and recent work; retain calendar, memory and plugin widgets |
| Hermes | Fixed 380px conversation beside an always-open artifact pane | Conversation-led layout, explicit output toggle, direct history access, task/cancellation status; preserve transcript and artifact stores |
| Shared applications | Files, Missions, Automations, Memory, Connections and Settings use glass primitives | Shared spacing, headers, focus, surface and motion tokens; application-specific workflows retained |
| Search/launcher | Existing command registry and floating surfaces | Restyled search/launcher using the same executable commands and permissions |
| Startup | Full-screen Hermes startup/failure overlay | Explicit desktop access during engine outage; retry/log controls remain available |
| Models | Existing provider/model settings and session controls | MadX Models entry points to the working provider settings; no placeholder manager |
| CLI | `herald-os` implementation plus `madx-agent-os` aliases | `madx` points to the same implementation; preserve all old commands, state paths and service units |
| Boot/login/installer | Validated bootc/Anaconda/niri implementation | Preserve storage/encryption/install behavior; visual changes need a separately rebuilt image and VM inspection |

The design uses graphite surfaces, restrained cyan, silver hierarchy, local system fonts,
shared radii, visible keyboard focus and reduced-motion support. No new animation dependency.
Hermes runtime, IPC/tool identifiers, history, permissions and storage are compatibility contracts.
The user's existing VirtualBox chat/file/hardware demonstrations are reported baseline evidence;
they are not automatically evidence for this new revision.

## Validation boundaries

Browser renderer previews use isolated empty/offline adapters, not the user's data or credentials.
They can establish layout and navigation behavior, not native services or real model chat.
Linux image/VM tests must use this branch's exact source and remain unpublished. The earlier push
authorization named only `codex/linux-release-validation`; obtain authorization before publishing
this separate feature branch. Do not merge it into the validation branch to bypass that boundary.

VirtualBox resolution and application layout are separate: compare compositor output mode/scale
and guest display integration with the renderer's available CSS pixels. Do not change Windows
display drivers, partitions, EFI or firmware. Native guest scaling remains unverified until tested.
LoRA Studio remains owned by its separate branch; no LoRA engine or UI placeholder is added here.

## Implemented revisions

| Revision | Scope |
| --- | --- |
| `93fdc9c539b07f34fd3905787a019ff4d449a82d` | Primary CLI, generated MADXCORE identity, public guides, installer alias/check-image guards and compatibility tests |
| `517d72fce3f4c066187030038084e6a3db72e841` | Desktop design system, graphics preferences, shell/Home/Hermes/settings and regression tests |
| `c5d03cf499701547127580133cd23952908775c2` | CI trigger and image/manifest publication guards with regression coverage |

Key design files: `apps/desktop/src/madx-design.css`, `shared/visual-quality.ts`,
`features/settings/sections/VisualQualitySettings.tsx`, `shell/WorkspaceHeader.tsx`,
`features/overview/OverviewPage.tsx`, `features/overview/SystemHealth.tsx` and
`features/hermes/HermesPage.tsx` (desktop-relative paths). Existing shell surfaces, UI primitives,
locales and preference readers/writers were updated together. No new package dependency.

## Local validation evidence

Executed on Windows on 2026-11-01. Commands are relative to the repository root unless noted.

| Check | Result and limits |
| --- | --- |
| `npx vitest run src shared electron/prefs.test.ts` in apps/desktop | 4,963 passed; 5 skipped; 355 passed files and 1 skipped file. Renderer/shared plus preferences, not the full native Electron suite |
| Final focused locale/i18n/Hermes/SystemHealth run | 40 passed, no skips; overlapping coverage after the last localized-copy adjustment |
| `python -m pytest linux/tests/test_manual.py linux/tests/test_branding.py linux/tests/test_release_validation.py linux/tests/test_madx_entrypoint.py linux/tests/test_branding_inventory.py linux/tests/test_catalog.py -q -rs` | 149 passed; 3 skipped (Windows cannot create required symlinks) |
| `npm run typecheck` at root | Renderer, Electron and client workspace TypeScript checks passed |
| `npm run build` in apps/desktop | Renderer and Electron production bundles passed; existing nonfatal ineffective-dynamic-import warnings |
| `npm run branding:check`; `node scripts/madx/audit-branding.mjs --check` | Generated product files match; zero remaining unreviewed product-copy candidates |
| actionlint for ci.yml, image.yml, installer-test.yml | Passed with external shellcheck/pyflakes disabled; those tools remain CI checks |
| Bash syntax for changed gpu-check/idle scripts; `git diff --check` | Passed |
| Broader portable identity/bridge attempt | 101 passed, 3 skipped, 1 failure: WindowsHost.find_processes is unsupported. Same test fails on unchanged baseline 2e844ca; not a redesign regression |

The five desktop skips are two optional spreadsheet XML/openpyxl validators and three memory
cross-process tests requiring POSIX flock. The three portable skips are alias idempotence/removal,
rollback after write failure and symlink-parent escape prevention. Native Linux CI must run these
guards; Windows success does not substitute for them. Full CLI/SSH tests require Linux.

Regression repairs during implementation included honest offline activity counts, stale system
readings, preserving output-editor state when hidden, compact Add space access, long sidebar
labels, responsive launcher arrow navigation, preference application after capability discovery,
and SSH JSON prefix compatibility. Preview-only adapter errors were fixed in the ignored harness;
no mock backend is shipped in the application.

The final workflow regression test reproduced the missing redesign exclusion in the multi-arch
manifest job (1 failed/8 passed before repair). The corrected guard blocks both image and manifest
publication with publish=true as well as false on this branch; all nine guard cases now pass.

## Visual review and performance boundaries

See [renderer evidence](evidence/redesign-2026-11-01/README.md) and its SHA-256 manifest.
Paired Home previews use the original source at 2e844ca and the redesigned source at 517d72f.
They show 1920x1080 and 1366x768 target layouts plus a representative 1024x768 layout.
Browser CSS rounding/padding is explicitly recorded. The actual VirtualBox resolution has not
been measured, and no native guest screenshot is included in this redesign evidence.

Interactive renderer checks: Home navigation, Hermes history/output switching, compact sidebar
Add space focus/cancel, graphics selection and five-column launcher keyboard navigation at 640px.
Performance mode's computed top-bar backdrop-filter is `none`; CSS disables continuous motion
and the JS motion helper respects that choice. This is behavior evidence, not frame pacing or
latency measurement. Native GPU/compositor behavior and sustained interaction performance remain
open. Existing app-specific workflows and permissions are retained; full interactive acceptance
of every major application in the installed OS is still required.

## Branding and publication review

`python scripts/madx/inventory-branding.py --write` produces HERALD_INVENTORY.csv/JSON from every
tracked/non-ignored UTF-8 source file and matching filenames, including the lockfile. It lists
binary/undecodable content separately. Classifications are triage, not a promise that every
lowercase identifier is invisible. The remaining terminal-classified MENU_LINE is an internal
legacy Omarchy menu identifier with a MadX label and compatible legacy action.

The final built JS/CSS/HTML/JSON scan found 1,281 case-insensitive legacy-name occurrences in 91
files (source maps excluded). This includes required identifiers, not 1,281 branding defects.
Product-name matches were manually
reviewed: retained old profile names; old presentation-title recognizers and command synonyms;
implementation comments; and required About attribution. Lowercase IPC, paths, plugin/package
names and document formats remain by design. Source maps and native packages were not declared
free of old names. A rebuilt Linux package plus installed login/installer/desktop audit remains
required before claiming zero unintended public branding.

Outgoing changes were reviewed for private-key blocks, GitHub/provider credentials, private
host-user paths and accidental disk/archive/environment files: no findings. Screenshots use
empty offline data and contain no real account, model output or credentials. Full gitleaks is
not installed on this host and remains a native CI gate. Workflow permissions were not expanded;
image publishing is forcibly false on this feature branch. Existing package-write and installer
contents-write scopes remain in the shared publishing workflows, but publishing steps are gated
off for this validation path. No remote mutation has been performed for the redesign.

Next execution: [branch approval and native validation procedure](REDESIGN_EXECUTION.md).
