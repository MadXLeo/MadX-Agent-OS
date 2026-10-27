# MadX Agent OS architecture

Status: implementation in progress; this is a target architecture, not a list of shipped capabilities.
Baseline: `7ff5f81`, Herald OS `0.1.0-alpha.5`. MadX distribution version: `0.1.0-alpha`.

## Existing boundaries to preserve

The Fedora 44 bootc image boots through greetd and niri (cage fallback). The Electron shell has a
single-window mode and a multi-window panels mode. Main owns native capabilities, sandboxed React
renderers use the typed preload contract, and Hermes owns conversations, providers, tools, skills,
memory and scheduling. Windows currently has a generic platform adapter, not a supported OS session.

| Layer | Existing implementation | MadX evolution |
| --- | --- | --- |
| Distribution | `linux/image/`, `.github/workflows/image.yml` | Keep bootc; migrate identity, image references and signing together after VM validation. |
| Login/session | `linux/session/`, `linux/niri/`, `linux/image/firstboot.sh` | Keep first boot, account/password handling, encrypted disks and compositor hotkeys. |
| Electron main | `apps/desktop/electron/` | Keep process, filesystem, IPC, credential and navigation boundaries. Add narrowly scoped backend adapters. |
| Preload | `apps/desktop/preload/index.ts`, `shared/ipc.ts` | Add typed request/response APIs with runtime validation in main; no renderer shell execution. |
| Desktop | `apps/desktop/src/shell/`, `src/features/` | MadX identity, graphite/cyan appearance and connected AI panels without removing existing apps. |
| Hermes integration | `packages/hermes-client`, `electron/backend/`, `plugins/herald-os-bridge` | Preserve pinned upstream wire contract, source identifiers, policy, approval prompts and audit history. |
| Product identity | `branding/` (new) | One source for product/app names, version, assets and provenance; generated consumers checked in CI. |

## AI services to implement

These services are planned and must not appear operational until connected and tested. Keep them
separate from Hermes's own implementation and reuse existing Settings, Memory, Missions and Studio.

**MadX Models.** Main-process backend adapters expose capabilities, health, list, inspect, pull,
import, load, unload, delete and inference tests. Ollama and llama.cpp are distinct adapters;
OpenAI-compatible endpoints are another adapter, not an assumption that every server implements
every operation. Use cancellation, bounded timeouts/response sizes and progress events. Only
explicitly configured endpoints are contacted. Model downloads require source, size, digest where
available and disk-space checks. Backend errors must remain errors. Cloud credentials remain in
Hermes-supported secret storage or an OS-backed vault, never preferences, renderer state or logs.

**Resource admission.** Detect CPU/RAM through the existing system adapter; probe NVIDIA with a
bounded subprocess, distinguish total/free VRAM and account for ComfyUI. Start conservatively with
3B–4B quantized models and modest contexts on 8 GB VRAM / 16 GB RAM. Serialize GPU-heavy loads,
offer unloading and refuse unsafe estimates. Report estimates separately from measurements.
Advertise Intel NPU only after an installed runtime and a real inference check succeed.

**MadX LoRA Studio.** A versioned adapter manifest records hash, base-model identity, architecture,
format, backend compatibility, provenance, tags and activation history. Import only bounded,
validated formats into private storage using atomic writes; never execute imported Python/pickle
or follow archive traversal/symlinks. Safetensors validation includes header bounds, offsets and
tensor metadata. GGUF adapters require backend-specific inspection. Strength and multiple-adapter
controls appear only when a backend supports them. Presets do not imply model retraining.

**ComfyUI integration.** Use its supported API for checkpoint/LoRA discovery, workflow submission,
progress, cancellation/history and output retrieval. Validate workflow node requirements and file
references; do not treat arbitrary workflow JSON as a trusted shell command. Keep previews and
output deletion scoped to the configured output store. Verify the actual API version before coding.

**Training.** Isolated LoRA/QLoRA workers consume explicitly approved, versioned datasets. Validate
examples, deduplicate and flag sensitive data before enqueueing. Jobs expose resource estimates,
progress/loss, checkpoints, cancellation, export and fixed-baseline evaluation. No automatic
conversation harvesting. Promotion requires measured improvement and user approval; retain the
previous adapter and evaluation report for rollback. Selecting a training backend requires an
actual hardware/runtime compatibility check, not a decorative queue.

**MadX Intelligence.** Extend Hermes's existing memory CRUD and skill toolset, preserving stores
and locking. Add fact/assumption status, approval, provenance, export and deletion; version skill
proposals with dependencies and validation reports. Activation is separate from generation.
Memory, reusable procedures and weight training remain separate mechanisms in the UI and storage.

**Self-development.** Extend existing Studio, Missions and plugin infrastructure with an isolated
workspace per proposal. States: observed → planned → sandboxed implementation → tested → evaluated
→ awaiting approval → deployed → monitored (or failed/cancelled/rolled back). Keep diffs, test reports,
source revision and rollback artifact together. A separate approval broker owns deployment;
generated code cannot modify that broker, audit policy, privileged service definitions or boot
infrastructure. Privileged deployments always need review. Tests and dependency resolution run in
a constrained worker with explicit network/filesystem grants; Git pushes and PR publication are
separate authorized actions. The shell stays usable when any AI service is absent.

## Compatibility and release boundaries

See [MIGRATIONS.md](MIGRATIONS.md). Display names are not service names. In particular, window titles
are compositor matching contracts; profile names determine Chromium cookies/local storage; bridge
identifiers determine permission routing. Keep old readers/writers aligned until each migration
has a tested cutover and rollback.

Independent images require MadX-owned registry/channel configuration, matching OCI metadata,
verified signatures, shell artifact naming and updater changes in one release. Never point an
updater at a registry that has not been provisioned and verified. Keep the upstream remote and
pinned Hermes revision; merge upstream security fixes on dedicated branches with parity tests.

## Validation gates

1. Pure modules, renderer components, IPC/security, bridge and Linux static tests.
2. Renderer/main/preload build and package metadata/asset/branding audits.
3. Linux/macOS native integration and Hermes end-to-end tests on supported hosts.
4. Local model inference/tool-calling, adapter activation and training evaluation with real backends.
5. Disposable VM install/reboot, encrypted and unencrypted disks, shared ESP/dual boot fixture,
   update/rollback and failure recovery. Never attach host disks to test VMs.
6. Signed, checksummed release artifacts; explicit authorization to publish.

No gate is satisfied by a UI screenshot or a successful TypeScript build alone.
