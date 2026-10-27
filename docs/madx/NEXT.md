# Continue MadX Agent OS

Work on `codex/madx-foundation`. Read DEVELOPMENT_BRIEF.md, BASELINE.md, VALIDATION.md and
MIGRATIONS.md first. The completed work is an audited baseline and the first desktop identity
increment, not a completed OS distribution. Preserve the existing upstream remote and pinned
Hermes revision. No authorization to push, publish, install to the host or change host boot state.

## Exact next implementation task

Finish Milestone 1's desktop copy and asset integration in a separate commit:

1. Run `npm run branding:audit -- --json`; migrate remaining product-copy literals in
   `apps/desktop/src/features`, `src/commands`, and Electron dialog/error messages to PRODUCT.
   Preserve command IDs, persisted formats, profile paths, environment aliases and tool names.
   Legal attribution stays explicit. Expand the existing translation catalogs rather than
   introducing runtime search-and-replace over user/agent content.
2. Export native launcher PNG/ICO/ICNS and Plymouth/lock assets from the supplied artwork; verify
   readability at small sizes. Retain provenance and verify package inclusion. The current favicon
   embeds a full-resolution raster and can be optimized with production exports.
3. Re-run the completed changed-area suite and full supported Linux/macOS CI. Investigate the
   Windows-only baseline failures separately without weakening supported-platform behavior.
4. Audit generated desktop bundles/packages for visible legacy copy. Keep compatibility/attribution
   findings separate and document unresolved ones. Only then claim the desktop identity complete.

## Following tasks and release gates

| Milestone | Remaining implementation |
| --- | --- |
| 0 | Full supported-host test baseline and native integration evidence; document any upstream failures. |
| 1 | Desktop leftovers above; coordinated Linux OS identity, graphical assets, safe namespace migration and docs/artifact naming. |
| 2 | Premium shell refinement, MadX Core controls, unified permissions, service health and emergency stop; real Hermes verification. |
| 3 | Main-process Ollama/llama.cpp/OpenAI-compatible adapters, typed IPC/UI, lifecycle/progress, secure credentials, hardware admission and real inference/tool tests. Verify primary API docs before implementation. |
| 4 | Safe LoRA registry/import, backend compatibility/activation, ComfyUI API workflow/output management, isolated training jobs. |
| 5 | Approved memory/skill provenance, versions and promotion; approved datasets, fixed-baseline evaluation and adapter rollback. |
| 6 | Extend existing Studio with sandboxed proposals, diffs/tests, approval broker and deployment monitoring/rollback. |
| 7 | Versioned Linux services/data cutover, independent verified registry/channels, installer reproduction and VM tests, image/ISO build/checksum/signature/release gates. |

For installer work use INSTALLER_INVESTIGATION.md. A Linux VM/runner with KVM/OVMF and isolated
virtual disks is required. Obtain the failing installation's logs before claiming a GRUB root cause.
Never use physical host disks for testing. Publishing signed release artifacts remains a separate
authorized step after reviewable artifacts and validation exist.

## Development commands

Node >=22.12; pinned Hermes sources in `upstream/hermes-agent` are required. `npm ci --ignore-scripts`
is enough for these source checks but does not install native Electron/PTY runtime components.
On a supported development system use the existing documented build/bootstrap workflow, reviewing
its Hermes configuration changes first. Python test dependencies are in `linux/tests/requirements.txt`.

```text
npm run branding:sync
npm run branding:check
npm run branding:audit
npm run typecheck
npm run build
npm run test --workspace apps/desktop -- --maxWorkers=2
python -m pytest linux/tests/test_window_rules.py -q
```

On this Windows checkout the isolated Python 3.12 interpreter used was
`.venv/py312/Scripts/python.exe`; that environment and local logs/builds are ignored by Git.
