# Feature parity register

## Alienware follow-up — 2026-11-04

The user reports physical installation, Windows boot and Secure Boot enabled; graphical
stability failed on Intel Xe + RTX 4070 Laptop with Nouveau/HDMI errors. Hermes was missing
for the logged-in account. These results supersede the unknown installation outcome below
and do not certify stable dual boot or hardware parity. Candidate session, NVIDIA ISO and
background-install changes are tracked in [ALIENWARE_RECOVERY.md](ALIENWARE_RECOVERY.md).
Native CI, rebuilt ISO, RTX module loading, responsive applications/input, HDMI/VT switching
and measured performance remain required; no preserved feature is declared accepted merely
because its old unit tests pass.

## Local follow-up — 2026-11-03

Hosted results below remain valid for their exact source and scenarios. The user's
VirtualBox guest required a manual nested/pixman/software-GPU override to reach the
welcome desktop with 3D disabled; automatic compositor fallback is not accepted.
Encrypted splash prompt visibility is also unresolved. No new installed Hermes chat
or performance acceptance is claimed. Actual Windows dual-boot testing was cancelled,
and the later physical installer attempt has no confirmed outcome. Current tasks and
acceptance conditions are in [WORK_ITEMS.json](WORK_ITEMS.json).

## Native redesign evidence — 2026-11-02

At `88d970167a9eb743a224a839491ec2631247f401`, CI 41400903428 passed both desktop/system
matrices, TypeScript/builds, branding and pinned Hermes smoke. Image 41413455726 built inspected
amd64/arm64/NVIDIA images and a checksum-verified unpublished ISO. Installer 41438712212 passed
all three disposable UEFI cases: installation, first reboot, encryption/unlock, SSH restrictions,
core services, compatibility aliases and preservation of a synthetic second disk.

Real 1280x800 screenshots show the welcome desktop/top bar/dock. Full Home/Hermes operation,
graphics fallback/latency/FPS, manual installer and hardware compatibility remain unverified.
The primary `madx` alias passes image and CI checks; the installed smoke invokes `madx-agent-os`.
Installed Hermes `0aab6dc` differs from tested `f97608f`; no running model-backed chat is certified.
The booted update origin names an intentionally unpublished tag; updates/rollback remain open.
See [retained evidence](evidence/redesign-linux-2026-11-02/validation.json) and REMAINING_ISSUES.md.

## Redesign increment — original local assessment, 2026-11-01

Implementation: `93fdc9c` (public identity/CLI), `517d72f` (desktop).
These statuses supplement, rather than replace, the OS evidence and baseline inventory below.

| Milestone | Implemented and checked locally | Remaining native acceptance |
| --- | --- | --- |
| A — design system | Shared graphite surfaces, spacing, focus, motion; four graphics choices, capability-based Automatic; optional saved preferences and reduced motion | GPU/software rendering, frame pacing, manual override persistence across a real restart |
| B — shell | Launcher/top bar/dock/chrome, responsive sidebar and command strip; compact Add space and five-column launcher keyboard navigation exercised | niri panel placement, focus/drag/resize, shortcuts, dock behavior and compositor fallbacks |
| C — Home/Hermes | Distinct activity/workspace layout using real stores, unavailable/stale statistics; history/output toggles preserve mounted editor state; startup recovery | Real engine streaming, tools, approvals/deny/cancel, provider switching and reconnect |
| D — applications/settings | Shared headers/surfaces/navigation across existing apps; responsive settings; working existing model-settings entry | Interactive Files/Office/Missions/Automations/Memory/Connections/onboarding/system panels; not every application has a bespoke redesign |
| E — identity/CLI | Primary madx alias in all four install layouts, public help/docs, legacy aliases/storage preserved; generated identity and source/built-JS audit | Native alias mutation/rollback, packaged boot/login/installer appearance, retained old-profile behavior |
| F — validation | 4,963 desktop passes/5 skips; 149 portable passes/3 skips; typecheck/build/lint/branding; paired renderer images | New branch CI, exact-source image/ISO, isolated UEFI install/reboot, native performance and actual VirtualBox resolution |

No existing application/command is removed. Runtime protocol, permissions, storage and updater
origins are preserved; native parity is an open acceptance gate, not inferred from visual previews.
One broader Windows bridge test fails identically on the original checkout (unsupported process
inspection). See REDESIGN.md for commands, skips, screenshots and limits.

Baseline: commit `7ff5f81`, upstream version `0.1.0-alpha.5`, clean checkout on 2026-10-27.
The repository has 1,767 tracked files, 423 desktop test files and 38 bridge/Linux test files.
Inventory derived from the app/command registries, source layout, architecture/build/security
documentation, bridge registrations, session scripts and workflows. This is a feature-family
inventory; it is not a claim that every line has received a security review.

Validation codes: **T** = included in attempted desktop suite (see BASELINE.md for actual results);
**P** = Python suite attempted but Windows collection is blocked; **H** = requires supported-host
integration; **V** = requires disposable-VM validation; **N** = new capability, not implemented.
Typecheck/build success alone does not establish functional parity. No existing feature is removed.

## Astra runtime and release evidence — updated 2026-10-31

Continuation: CI again uses the established bridge runner; unexpected Linux skips are rejected;
image architecture/source labels and installer run provenance are checked. Guest Hermes revision
drift is observed without altering the installed version. After correcting the Git Bash test's
path comparison, expanded local checks report 76 passes, 26 skips and zero failures; three
installer workflow tests and all TypeScript checks also pass.
Linux CI has now actually run at `e062c0334dcb382236b18a60422eab0e46a0d8d2` (run 40684976475):
the desktop suite reports **5,835 passed, two optional spreadsheet-validator skips, zero failures**;
TypeScript, branding and the production build passed. The real Linux Hermes process smoke passed.
The bridge/system suite reports **2,275 passed, eight failed, 27 skipped**. Repairs and a runner
namespace preflight passed in `e8e6010`, CI run 40741143041: Linux bridge/system 2,309 passed
with two reviewed exclusions, dedicated aliases 19/19, macOS desktop 5,833 passed/four skipped,
macOS bridge/system 2,205 passed/106 skipped. Both desktop builds passed. CI 40743566443 at
`606e1e1` subsequently passed (Linux bridge 2,316/two skips; macOS bridge 2,212/106 skips).
Image run 40743693944 built and inspected both default architectures and an actual amd64 ISO.
All three installer jobs verified the ISO checksum but failed before VM boot on an included
kickstart validation defect. Fix `da90688` passed full CI. Actual ISO inspection then found an
appended-EFI-partition mismatch in the test setup; `2290c81` repairs it and passes 49 focused tests.
Full CI then passed at `2290c81` (Linux bridge 2,328/two skips; macOS bridge 2,224/106 skips;
both desktop suites/builds passed). Image 40780003482 built both default architectures and a new ISO;
installer 40811638765 verified it but failed before boot because deployment validation tried to
read an account include generated later inside the guest. Repair `161557f` reorders validation
before account injection; 50 focused tests and both preparation-step fixtures pass. Full CI at
`161557f` passed (Linux system 2,329/two skips, macOS system 2,225/106 skips, desktop suites/builds and
real Hermes passed); image 40812159188 built and inspected both default architectures and the ISO.
Installer 40814588924 booted the ISO through UEFI and installed all three cases. Both unencrypted
guests rebooted into the graphical MadX welcome screen; the adjacent synthetic GPT disk retained
its hash. Acceptance failed on lost SSH keys (Anaconda lacked base64) and encrypted unlock input.
Fixes `cb55130`/`448e85e` passed full native CI 40848022569: Linux system 2,336/two skips,
macOS system 2,232/106 skips, aliases 19/19, desktop suites/typechecks/builds and pinned Hermes.
Image 40848023781 built both default images and a new ISO. Installer 40850572175 installed and
rebooted all three cases, unlocked encryption, accepted SSH keys and rendered the MadX desktop.
Acceptance failed on GSSAPI outside the documented managed policy and the probe's root-only bootc
command. All 11 new cases for repairs `e9d8431`/`b2beb0a` passed Linux CI, but a new parser import
failed its dependency guard; `7f88d80` fixes it and passes all Linux CI 40898401729 jobs (system
2,347/two skips; desktop 5,835/two skips; aliases/build/typecheck/branding/Hermes passed). macOS
was initially cancelled by hosted runner capacity constraints; attempt 2 passed (system 2,243/106
skips, desktop 5,833/four skips, typecheck/build passed). Overall CI at `7f88d80` is success.
Image 40899343029 built/inspected both default architectures and a real ISO at `7f88d80`, with
publication disabled and source labels/pin verified. Installer 40945372298 completed against
that exact image/source: all three cases installed/rebooted, passed SSH restrictions and deployment/
alias checks, and rendered the MadX desktop. All failed on the composefs root remount conflict,
now confirmed by journal and fstab evidence. Repair `c5dfa69` migrates physical root options during
fresh installation; `35fea98` fixes the GPU check's missing HOME, and `21eda78` preserves shell LF
endings on Windows. 23 focused tests, preparation fixtures, workflow/source and branding checks pass;
CI 41000794337 passed all 15 root-mount/GPU cases and all 19 alias cases on both platforms, but failed
one stale post-script-count assertion in each system suite. The test now verifies both execution
contexts; the subsequent CI and image/VM results are recorded below. Installed Hermes revision drift is recorded in
ASTRA_PROGRESS.md; model-backed operation and interactive desktop acceptance remain open.
NVIDIA initially failed on missing upstream kernel modules; the later build succeeds as recorded below.

Latest CI 41093321542 at `5b704d6` confirms the corrected parser test on Linux: system 2,362 passed,
two reviewed skips; dedicated aliases 19/19; desktop 5,835/two skips; typecheck/build/branding/Hermes
passed. Attempt 2 resolved the macOS hosted-runner issue: system 2,258 passed/106 skips, desktop
5,833/four skips, typecheck/build passed. Overall CI is successful. Image 41098826626 also passed
at the same source: default amd64/arm64 and NVIDIA filesystem/systemd/Electron checks passed and
a new ISO was produced. Installer 41172111127 passed all three cases at that exact source/image:
UEFI boot, installation, first reboot, encrypted unlock, SSH restrictions, aliases and core services.
The remount service succeeds with physical Btrfs options preserved; the GPU HOME error is absent.
All three final screenshots show the MadX welcome desktop. Installed Hermes `78077b2` differs from
the tested pin `f97608f`; model-backed and interactive desktop acceptance remain open.

Earlier Windows desktop results were 4,915 renderer/shared passes (five skips) and 89 focused main-process
passes. Typecheck/build and branding checks pass. Selected Python validation now passes 60 tests
with 26 Windows/platform skips, plus three installer workflow tests. Later full native suite results
are recorded above; the earlier Windows limitations remain documented.

| Area | New implemented check / observed evidence | Remaining gate |
| --- | --- | --- |
| Hermes process, health/auth, bridge discovery | Real pinned server executed twice on both Windows and Linux; missing/wrong tokens rejected; bridge tools registered | Installed Linux service and host adapter, model chat/tools/approvals, desktop recovery |
| Memory and skills | Real MemoryStore and skills API; contents survive server restart in an isolated profile | Existing-profile OS upgrade and user-facing integration |
| Linux alias/filesystem behavior | All 19 cases passed without skips in Linux CI; installed system/user unit aliases and commands resolved in all three VMs | VM upgrade behavior |
| Image packaging | Default amd64/arm64 and NVIDIA images built and passed filesystem/systemd/Electron checks at `5b704d6`; exact amd64 ISO checksum verified and booted through UEFI | Native package variants, arm64 boot and NVIDIA hardware |
| UEFI installation | All three `5b704d6` cases passed: installation/reboot, encrypted unlock, SSH restrictions, deployment evidence, aliases, core services, root remount and desktop window; final screenshots viewed | Interactive operation, custom storage and existing-profile upgrades remain open |
| Adjacent Windows-style disk | Actual VM install and acceptance attempt preserved the synthetic GPT/sentinel disk hash | No actual Windows/shared-ESP certification |
| Update/rollback and NVIDIA | Existing implementation reviewed; validation sequence documented, identifiers retained | Two deployment transitions, data integrity, GPU/laptop testing |

The H/V gates below remain open. See ASTRA_PROGRESS.md for the precise scope and next execution.

## Phase 1 evidence update — 2026-10-27

The full renderer/shared suite now passes **4,915 tests in 351 files**, with five skips and no
failures. This covers the existing shell, commands, Office, Canvas, Calc, settings, voice, pet/room,
gateway stores and translation behavior. Main-process migration regressions pass their 89-test
recheck; 128 other main-process failures reproduce on the original source under Windows. Linux
source/configuration checks pass 40 tests, with 26 environment skips. See VALIDATION.md for exact
scope. H and V gates below remain open, including actual Hermes integration.

| Migration area | Implemented preservation | Evidence / remaining gate |
| --- | --- | --- |
| Desktop display and command routing | Product constants; old spoken names still resolve; all 386 literal IDs across 39 command modules retained | Renderer suite and source comparison pass; native interaction H |
| Slides, pet and screensaver | Shared old/new presentation detection; no privacy leak during presentation | New title tests and renderer tests pass; compositor V |
| Profile and preferences | Legacy Chromium profile reused; original storage keys and saved themes retained | Profile tests pass; real existing-profile upgrade H |
| Linux commands and services | MadX aliases target existing files/units; no second service enabled | Conflict/plan tests pass; real symlink and systemd V |
| Packaging and release identity | Coordinated filenames, metadata, checksums, registry policy; legacy executable/data layout retained | Static checks pass; package/image build V |
| Upgrades and rollback | Both IMAGE_ID values accepted; tarball's original swap directories unchanged | Detector tests pass; actual upgrade/rollback V |
| Installer and splash | ISO identity, graphite Plymouth and supplied wordmark; encrypted interactive storage unchanged | Source/config tests pass; visual branding, unlock and boot V |
| Hermes tool permissions and persisted files | Bridge IDs, schemas, plugin identity and engine pin retained | Renderer/client checks pass; complete Python suite and real gateway P + H |

| Discovered feature | Implementation (repository-relative) | MadX mapping | Validation / status |
| --- | --- | --- | --- |
| Single-window desktop, windows, focus, resize, spaces | `src/shell/`, `src/store/windows.ts` in `apps/desktop` | Retain, MadX shell identity | T + H |
| Multi-window Linux panels, docking and compositor focus | `electron/shell/`, `electron/wm/`, `linux/niri/config.kdl` | Retain; titles are matching contracts | T + H + V |
| Launcher, installed/native applications | `src/features/applications`, `electron/ipc/apps.ts`, `electron/platform/` | MadX application launcher | T + H |
| Command palette, voice commands, agent UI commands | `src/commands/`, `src/store/os-commands.ts`, `electron/shell/os-control.ts` | Preserve commands/tiers, MadX display labels | T + P + H |
| Notification center, history, D-Bus notifications | `src/shell/Toasts.tsx`, `electron/notifications-history.ts`, `electron/shell/notification-daemon.ts` | Retain, MadX sender identity | T + H |
| Wi-Fi, Bluetooth, audio, display, power, battery | `src/features/status`, `electron/ipc/controls.ts`, `linux/bin/herald-os` | Preserve quick settings | T + P + H |
| Themes, wallpaper, fonts, light/dark infrastructure | `shared/theme.ts`, `electron/theme/`, `src/styles.css`, `linux/themes/` | MadX graphite/cyan defaults, keep user themes | T + H |
| Reduced motion, keyboard shortcuts, translations | `src/styles.css`, `shared/locales/`, `shared/i18n.ts` | Preserve English, Portuguese and Chinese catalogs | T + H |
| First-run identity, provider, Wi-Fi and password setup | `src/features/setup`, `electron/ipc/setup.ts`, `linux/image/firstboot.sh` | MadX welcome copy, unchanged account operations | T + P + V |
| Hermes runtime resolution, restart, error recovery | `electron/backend/`, `src/features/status` | MadX Core uses real Hermes | T + H |
| Pinned JSON-RPC types, reconnect, REST gateway | `packages/hermes-client`, `upstream/UPSTREAM.lock` | Preserve unchanged upstream client contract | T + H |
| Chat, sessions, profile bots, context, history | `src/features/chat`, `src/features/hermes`, `src/store/chat.ts`, `src/store/bots.ts` | MadX Core interface; Hermes engine identity retained | T + H |
| Tool calls, approval/clarify/sudo/secret prompts | `src/store/gateway.ts`, `src/features/chat`, `plugins/herald-os-bridge/bridge` | Preserve explicit request/approval/execution states | T + P + H |
| Provider settings, auth, custom endpoints | `src/features/auth`, `settings/sections/ProviderRow.tsx`, `electron/backend` | Preserve configured Hermes providers | T + H; not a local model lifecycle manager |
| Multi-engine voice, wake, interruption, dictation | `src/lib/voice`, `src/features/voice`, `electron/ipc/voice.ts`, `dictation.ts` | Preserve voice and permission controls | T + H |
| Missions, task steps, tool history | `src/features/missions`, `src/store/missions.ts` | Retain agent task monitor | T + H |
| Scheduled/event automations and hooks | `src/features/automations`, `electron/events`, `shared/events.ts` | Retain; new controls must use existing approvals | T + H |
| Memory search, categories, editing, deletion, providers | `src/features/memory`, `memory-store.ts`; store uses existing file API | MadX Intelligence foundation | T + H; new approval/provenance/export work remains |
| Hermes skill configuration/development | `settings/sections/`, `plugins/herald-os-bridge/skills`, Hermes runtime | Retain skills; add version/promotion UI later | P + H; managed proposal workflow N |
| MCP/connections and environment settings | `src/features/connections`, `src/features/settings` | Retain integration settings | T + H |
| Files, search, previews, watches, system editor | `src/features/files`, `electron/ipc/fs.ts`, `edit.ts`, `electron/platform` | Retain safe filesystem boundaries | T + P + H |
| Native applications and desktop automation | `electron/platform`, `plugins/herald-os-bridge/host` | Keep platform adapters and permission tiers | T + P + H |
| Terminal/PTYS, paste and output buffering | `src/features/terminal`, `electron/ipc/terminal.ts` | Retain terminal functionality | T + H; native module not installed in baseline |
| Web views, external links, isolated preview | `src/features/web`, `electron/ipc/web.ts`, `electron/external-url.ts` | Preserve partitions and navigation restrictions | T + H |
| Studio code tree, diffs, terminal, live preview | `src/features/studio`, `src/store/studio.ts` | Retain developer Studio; new self-development layer later | T + H |
| System process/resource monitor | `src/features/system`, `electron/ipc/system.ts`, `electron/platform` | Retain; GPU admission and backend metrics N | T + H |
| Overview, continuity, recents and calendar | `src/features/overview`, `electron/context`, `src/store/continuity.ts` | Preserve opt-in context sharing | T + H |
| Screenshots, recording, camera, markup, OCR/QR | `src/features/capture`, `electron/ipc/capture.ts`, `src/features/emoji` | Preserve capture permissions and shortcuts | T + H |
| Clipboard history, emoji insertion | `src/shell/surfaces`, `electron/shell/emoji-panel.ts`, `linux/session` | Retain platform integrations | T + H |
| Layered image editor, PSD, masks, effects, undo | `src/features/canvas`, `shared/canvas`, `electron/canvas` | MadX Canvas; preserve file formats | T + H |
| Existing Canvas verified on-device model downloads | `shared/canvas/models.ts`, `electron/canvas/model-*` | Preserve; separate from future LLM manager | T + H |
| Documents, DOCX, pages, tables, comments, templates, PDF | `src/features/office/docs`, `shared/office`, `electron/office` | MadX Docs; preserve custom XML and formats | T + H |
| Sheets, XLSX/CSV, formulas, charts, cleaning, comments | `src/features/office/sheets`, `src/features/office/univer` | MadX Sheets; preserve workbook/agent operations | T + H |
| Slides, PPTX, masters, transitions, presenter and audience | `src/features/office/slides`, `electron/office/presenter.ts` | MadX Slides; audience window requires compositor migration | T + H |
| Exact calculator, units, currency, dates, plots/history | `src/features/calc`, `shared/calc*`, `electron/calc` | MadX Calc | T + H |
| Desktop pet, Petdex and activity room | `src/features/pet`, `petdex`, `room`, `electron/pet`, `electron/room` | Preserve companion and task visualization | T + H |
| Screensaver, lock, idle, night light, stay awake | `src/features/screensaver`, `electron/switches.ts`, `linux/session` | Keep controls, later MadX Linux assets | T + P + V |
| Widget plugins, hooks, catalog, enable/disable | `src/features/plugins`, `electron/plugins`, `linux/catalog` | Preserve plugin isolation; generated plugins need review | T + P + H |
| Crash reporting/diagnosis, logs, audit | `electron/crash`, `electron/log.ts`, bridge audit module | Preserve diagnostics; do not rename stores independently | T + P + H |
| Bridge information/process/network/document tools | `plugins/herald-os-bridge/tools`, `host`, `bridge` | Preserve tool names and permissions | P + H |
| Bridge file batches, dry run, undo, destructive prompts | `plugins/herald-os-bridge`, `SECURITY.md` | Preserve policy/protected paths and audit | P + H |
| Login, user session, first boot, offline Hermes recovery | `linux/session`, `linux/image/*service`, `firstboot.sh` | Retain bootable shell when AI is absent | P + V |
| Package catalog, Flatpak, omakase and Linux app discovery | `linux/catalog`, `linux/omakase`, `linux/bin` | Retain app installation and permissions | P + V |
| bootc image, OSTree updates and rollback | `linux/image`, `linux/bin/herald-os-update`, `linux/migrations` | MadX identity and dual image detection; existing rollback path retained | Source checks pass; P + V |
| Tarball, Arch, Hyprland and Omarchy integrations | `packaging/arch`, `linux/bin/herald-os-tarball`, `linux/session` | Preserve non-bootc installation paths | P + H |
| NVIDIA image, kernel/driver consistency | `linux/image/Containerfile.nvidia`, `nvidia.sh` | Retain separate NVIDIA build | P + V |
| ISO, encrypted install, UEFI, recovery | `linux/image/iso.toml`, `unattended.ks`, installer workflow | Investigate reported GRUB failure; not fixed | P + V |
| QCOW2, VHDX, UTM and VM helpers | `linux/vm`, `linux/tests/test_vm_disks.py` | Preserve virtual disk artifacts | P + V |
| Release signing, checksums, OCI, macOS packaging | `.github/workflows`, `apps/desktop/scripts`, `build/licenses` | MadX artifact/channel configuration; alpha tags follow edge | Static inputs checked; signing/publication and T + P + V remain |
| Licenses, copyright, notices and upstream updates | `LICENSE`, `NOTICE`, `SECURITY.md`, `upstream/` | Preserve attribution, add MadX provenance | Audited source; package audit pending |
| Local/cloud model lifecycle and tool-calling probes | Proposed Models adapters | MadX Models | N |
| Hardware-aware GPU reservations and NPU probing | Proposed resource admission | MadX AI Studio | N |
| Safe LLM/image LoRA import, presets and activation | Proposed LoRA registry/adapters | MadX LoRA Studio | N |
| ComfyUI workflows, progress and output management | Proposed ComfyUI adapter | MadX LoRA Studio | N |
| Approved datasets, isolated training/evaluation/promotion | Proposed training workers | MadX Intelligence + LoRA Studio | N |
| Sandboxed improvement proposals, reviews, deployment/rollback | Proposed Studio extension | MadX Self-Development | N |

The implementation directories above retain upstream names until their individual migrations are
tested. `BASELINE.md` and `VALIDATION.md` record commands/results, including failures and missing
environments. An H/V item cannot be marked complete by source-only testing on Windows.
