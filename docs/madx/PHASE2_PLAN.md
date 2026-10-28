# Phase 2 — desktop experience and Hermes integration

Planning only. Implementation is gated on the Phase 1 checks in REMAINING_ISSUES.md. LoRA Studio,
self-development, training and model lifecycle services are outside this phase.

2026-10-28: native release gates remain open; see ASTRA_PROGRESS.md. Claude's separately reported
`claude/ecc-upstream-integration` at `3b28ee7` contains keyring/Secret Service and a read-only model
plan. Do not recreate or merge those changes in this Astra session. After explicit integration
authorization, review that dependency and rerun portal, credential and Hermes acceptance before
building desktop experience work on it. Its reported test results are not Astra evidence.

## 1. Establish native acceptance evidence

Capture desktop and panels sessions on Linux, plus the macOS application. Test keyboard-only use,
focus, multi-monitor placement, scaled displays and reduced motion. Record startup time, idle CPU,
memory and frame stability before adding visual effects. Resolve Phase 1 failures first.

## 2. Refine the existing shell

Apply the graphite/silver/cyan design consistently to launcher, search, dock, quick settings,
notifications and window controls. Preserve command IDs, menus, Linux controls and current keyboard
bindings. Extend the existing theme and translation systems; avoid a second UI framework. Validate
readability, focus visibility, contrast and low-power performance on the native session.

## 3. Make Hermes state understandable

Build MadX Core around the existing backend manager and gateway stores. Show connected, starting,
busy, waiting for permission, unavailable and recovering states from real events. Surface the
configured provider and model only when the gateway confirms them. Keep credentials in existing
protected stores and make reconnect/restart errors actionable. Do not imply unsupported backends.

## 4. Improve task and permission controls

Reuse Missions, activity and approval stores for a coherent task view. Keep approval, rejection,
clarification, secret and sudo interactions distinct. Add cancellation and an emergency stop only
through verified Hermes cancellation/process controls; test what can and cannot be stopped. Never
grant permission because a task appears in an activity panel.

## 5. Exercise functional parity

Use controlled provider fixtures and one real configured Hermes provider to test chat, tool calls,
memory and skills, automations, file operations, Office/Canvas/Calc, voice interruption, recovery
and permissions. Include an unavailable/offline engine and a failed tool. UI changes ship in small
commits only after their relevant tests and native acceptance checks pass.

## Exit evidence

Passing supported-platform suites, native interaction recordings/screenshots, before/after
performance results, updated FEATURE_PARITY.md and reproducible package builds. No new feature is
marked available solely because a screen or product label exists.
