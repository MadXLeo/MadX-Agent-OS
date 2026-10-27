# Feature parity register

Baseline: commit `7ff5f81`, upstream version `0.1.0-alpha.5`, clean checkout on 2026-10-27.
The repository has 1,767 tracked files, 423 desktop test files and 38 bridge/Linux test files.
Inventory derived from the app/command registries, source layout, architecture/build/security
documentation, bridge registrations, session scripts and workflows. This is a feature-family
inventory; it is not a claim that every line has received a security review.

Validation codes: **T** = included in attempted desktop suite (see BASELINE.md for actual results);
**P** = Python suite attempted but Windows collection is blocked; **H** = requires supported-host
integration; **V** = requires disposable-VM validation; **N** = new capability, not implemented.
Typecheck/build success alone does not establish functional parity. No existing feature is removed.

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
| Memory search, categories, editing, deletion, providers | `src/features/memory`, `electron/ipc/memory*` if present; store uses existing file API | MadX Intelligence foundation | T + H; new approval/provenance/export work remains |
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
| bootc image, OSTree updates and rollback | `linux/image`, `linux/bin/herald-os-update`, `linux/migrations` | MadX distribution migration pending | P + V |
| Tarball, Arch, Hyprland and Omarchy integrations | `packaging/arch`, `linux/bin/herald-os-tarball`, `linux/session` | Preserve non-bootc installation paths | P + H |
| NVIDIA image, kernel/driver consistency | `linux/image/Containerfile.nvidia`, `nvidia.sh` | Retain separate NVIDIA build | P + V |
| ISO, encrypted install, UEFI, recovery | `linux/image/iso.toml`, `unattended.ks`, installer workflow | Investigate reported GRUB failure; not fixed | P + V |
| QCOW2, VHDX, UTM and VM helpers | `linux/vm`, `linux/tests/test_vm_disks.py` | Preserve virtual disk artifacts | P + V |
| Release signing, checksums, OCI, macOS packaging | `.github/workflows`, `apps/desktop/scripts`, `build/licenses` | Independent MadX channels pending | T + P + V |
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
