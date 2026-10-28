# Astra progress — 2026-10-28

## Continuation: execution prepared, remote authorization required

Started clean at `a486db3d851ad8f6eea6a5917773841857dc9d8d` on
`codex/linux-release-validation`. Windows still has no installed WSL, Podman, Docker or QEMU;
`gh` is also absent. No system software was installed. GitHub read-only checks confirm a public
repository, default branch `main`, and no remote validation branch. Account access does not
override the user's requirement for approval before pushing. No remote run was started.

Resumed the interrupted work at `310cfda`, retaining the committed CI/provenance improvements
and all five pending documentation changes. The user explicitly repeated **do not push yet**.
The Git Bash test defect is now fixed and validated below; no host software or remote state changed.
Source commits: `310cfda` (CI runner, strict Linux evidence and image provenance, retained from the
interrupted session) and `9444c6d` (Git Bash/native Python test-path identity fix). The evidence
commit follows these; the final response records its ID and final working-tree state.

### Repairs and safeguards

- Reproduced and fixed a previous-session CI regression: the bridge job bypassed
  `scripts/test-bridge.sh`, breaking its existing dependency/runner assertion. CI again uses the
  established runner and Python selection, explicitly passes both suites, and retains JUnit.
- Remote main lacks CI's manual trigger. This validation branch now has a CI push trigger, so an
  authorized push can test the branch without merging into main. Image/installer workflows
  already have manual triggers on remote main; invoke their **branch versions** as shown below.
  Read-only checks reconfirmed this after resumption. Manual CI API dispatch has not been attempted
  (the branch is not remote); the execution plan does not depend on branch-only manual dispatch.
- Full Linux JUnit now rejects unreviewed skips. Only macOS PDFKit and root-only nft syntax have
  named exclusions with review reasons. Alias tests remain strictly zero-skip. Missing namespaces,
  loop devices or prerequisites must produce incomplete validation, not a green release claim.
  Root nft validation remains a separate gate; the general suite stays unprivileged.
- Validation ISO downloads require a successful completed manual image run from this repository
  at the exact checked-out commit. Wrong revisions/workflows/repositories, forks and incomplete
  or failed runs are rejected. Original ISO checksums are retained in installer artifacts.
- Images carry an OCI source-revision label; inspection checks architecture and revision.
  Artifacts retain UPSTREAM.lock. Guest observations record Hermes command availability, installed
  Git revision and drift from the tested pin, without changing first-boot versions. This is not
  proof of model-backed functionality.

### Executed checks and resolved test defect

Initial selected baseline: **60 passed, 26 skipped**. The expanded run first exposed two failures;
restoring the bridge runner fixed the CI regression. Before interruption the result was **75
passed, 26 skipped, one failed**. Resumption reproduced the last failure in
`test_test_deps.py::test_the_runner_falls_back_to_uv_with_the_requirements_when_pyyaml_is_missing`:
Git Bash returned `/c/Users/.../requirements.txt`, while the test expected the spelling `C:\Users\...`.
The test now records NUL-separated arguments, converts the Git Bash path on Windows, and checks
the actual requirements file with `Path.samefile`. It also checks the invocation's arguments;
neither file selection nor missing-dependency fallback was relaxed. The production runner is
unchanged. All four dependency-runner tests now pass.

Final expanded result: **76 passed, 26 skipped, zero failed**. The skips remain three filesystem
symlink cases and 23 Linux-only packaging cases. Running the native JUnit gate on this actual
Windows report correctly rejected those skips. Provenance acceptance/rejection and explicit-skip
accounting tests pass. The earlier 128 Windows main-process failures are separate and remain open.

Three installer workflow tests pass (218 deselected). Actionlint passes for three edited workflows;
three YAML files and 46 Bash blocks parse. Native parsing passes 72 Python, 41 Bash and six TOML
files. TypeScript checks for all workspaces, branding and whitespace checks pass. Desktop code
and the Hermes smoke implementation are unchanged; their earlier full test/build/runtime results
below remain historical, not new runs.

Executed commands, with Git Bash on PATH and PYTHONUTF8=1:

```text
.venv/py312/Scripts/python.exe -m pytest linux/tests/test_release_validation.py linux/tests/test_installer.py linux/tests/test_branding.py linux/tests/test_window_rules.py linux/tests/test_vm_disks.py -q
.venv/py312/Scripts/python.exe -m pytest linux/tests/test_release_validation.py linux/tests/test_installer.py linux/tests/test_branding.py linux/tests/test_window_rules.py linux/tests/test_vm_disks.py linux/tests/test_test_deps.py -q
.venv/py312/Scripts/python.exe -m pytest linux/tests/test_unattended.py -k installer_test -q
.venv/actionlint/actionlint.exe -shellcheck= -pyflakes= .github/workflows/ci.yml .github/workflows/image.yml .github/workflows/installer-test.yml
.venv/py312/Scripts/python.exe scripts/madx/check-native.py --bash "C:\Program Files\Git\bin\bash.exe"
npm run typecheck
npm run branding:check
node scripts/madx/audit-branding.mjs --check
git diff --check
```

The interrupted run's ignored logs remain `madx-continuation-*.log`. The resumed evidence is
`madx-resume-{baseline-deps,deps,tests,installer-workflow,typecheck,workflows,workflow-shells,native,
branding,skip-rejection}.log`, with `.venv/madx-resume-tests.xml`. The expanded run added
`--junitxml=.venv/madx-resume-tests.xml` to the command above. Native skip detection was also run as
`python scripts/madx/check-junit.py .venv/madx-resume-tests.xml --allow-skipped linux/tests/expected-linux-skips.json`;
its rejection is an expected validation result, not another product failure. Compact evidence and
hashes are appended to VALIDATION_RESULTS.json.

### Exact remote execution proposal — not executed

Separate approval is required to push **only** `codex/linux-release-validation` to the public
repository and run CI plus the nonpublishing image/installer workflows. Neither is approved in
this resumed session. No merge, release, registry push or host
software installation is included. Keep the branch fixed between build and installation.

```text
git rev-parse HEAD
git status --short
git push origin HEAD:refs/heads/codex/linux-release-validation
```

The push triggers CI. These commands require an already authenticated GitHub CLI environment,
or equivalent GitHub API/UI operations; installing CLI on Windows is not presumed authorized.
Replace placeholders with the recorded full SHA and returned run IDs. Verify every `headSha`.
No `gh workflow run ci.yml` is needed. Image and release push triggers exclude this branch, so
pushing it does not publish images or tags. Do not push if the working tree is unexpectedly dirty.

```text
gh run list --repo MadXLeo/MadX-Agent-OS --workflow ci.yml --branch codex/linux-release-validation --commit <full-SHA> --event push --json databaseId,headSha,status,conclusion,url
gh run watch <CI-run-ID> --repo MadXLeo/MadX-Agent-OS --exit-status
gh workflow run image.yml --repo MadXLeo/MadX-Agent-OS --ref codex/linux-release-validation -f publish=false -f disks=true
gh run list --repo MadXLeo/MadX-Agent-OS --workflow image.yml --branch codex/linux-release-validation --commit <full-SHA> --event workflow_dispatch --json databaseId,headSha,status,conclusion,url
gh run watch <image-run-ID> --repo MadXLeo/MadX-Agent-OS --exit-status
gh run download <image-run-ID> --repo MadXLeo/MadX-Agent-OS --name image-evidence-madx-agent-os-amd64 --dir <new-evidence-directory>
gh workflow run installer-test.yml --repo MadXLeo/MadX-Agent-OS --ref codex/linux-release-validation -f image_run=<image-run-ID> -f tag= -f account=madx-test
```

Inspect CI failures, each image leg and checksums, then all three installer artifacts and screenshots.
Image building can diagnose packaging separately, but failed CI remains a release blocker. Do not
run the old default-branch publishing workflow. GitHub documents manual triggers in
[manual workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow),
and branch/input/SHA selectors in [workflow run](https://cli.github.com/manual/gh_workflow_run)
and [run list](https://cli.github.com/manual/gh_run_list).

### Milestone evidence and separate readiness estimates

| Required runtime result | Evidence |
| --- | --- |
| Built Linux image | Blocked: no local builder; remote execution needs authorized push. |
| Generated bootable ISO | Blocked; no ISO or ISO checksum available. |
| UEFI media boot | Unverified; harness not run. |
| Isolated installation | Unverified; no new Anaconda logs. |
| First reboot | Unverified. |
| Running graphical desktop | Unverified on Linux; prior production bundles are not boot evidence. |
| Required systemd services | Unverified; source checks only. |
| Basic Linux Hermes integration | Unverified; prior Windows smoke supplies partial evidence only. |
| Update/rollback | Unverified; the two-image VM procedure below remains required. |
| No critical installer failure | Unproven; original GRUB failure still lacks reproduction/logs. |

| Area | Readiness estimate |
| --- | --- |
| Source migration | Substantially implemented and previously desktop-tested; native appearance/compatibility need execution. |
| Linux image build readiness | Execution prepared; no successful build yet. |
| VM installation readiness | Harness prepared with provenance checks; no successful boot/install yet. |
| Hermes Linux integration | Not validated; pinned Windows server smoke passed previously. |
| Release readiness | Not ready: native, update/rollback, signing/security and hardware gates remain. |
| Overall MadX v0.1 | Source foundation and validation tooling; installability unproven. Claude's later provider/keyring/LoRA integration and combined verification remain dependencies. |

NVIDIA remains source-reviewed only. Real laptop checklist: GPU detection, CUDA/container GPU,
hybrid graphics, Wi-Fi, Bluetooth, audio, suspend/resume, external display, battery/thermal behavior
and Secure Boot. No Alienware installation is authorized. Claude's workspace and host disks, EFI,
firmware and encryption were not changed. Session commit IDs are recorded in the final response.

## Prior session evidence

MadX source validation and a real Hermes server smoke pass. **MadX v0.1 is not yet proven
installable; Phase 1 remains open.** No Linux image, ISO, installed desktop, update or rollback
was run on this Windows host. The next step is to execute the extended existing workflows on
Linux, then inspect their actual artifacts and failures.

## A. Repository state and boundaries

- Original workspace: `C:\Users\divan\Documents\MadX-Agent-OS`.
- Initial state: clean `codex/madx-foundation` at `50dd6d42a3212203dcd30e901b497896e7a4e39d`.
- Confirmed retained commits: `5183b5c`, `2422689`, `cc829a8`, `9dd5ce9`, `50dd6d4`.
- New branch: `codex/linux-release-validation`, based on that HEAD. No reset or project restart.
- Origin: `https://github.com/MadXLeo/MadX-Agent-OS`; upstream remains Herald's repository.
- Final source commits are listed below. No push, release publication or remote dispatch.
- Claude's reported `claude/ecc-upstream-integration` / `3b28ee7` was not accessed or merged.
  Keyring/Secret Service and model-plan work remain that branch's dependency, not Astra changes.
- No host partitions, EFI entries, Windows Boot Manager, encryption or firmware were changed.
  No LoRA, model routing, Cognitive Core or self-development implementation was started.

## B. Implemented validation

The existing CI workflow retains desktop and Python JUnit reports, runs the Linux alias tests
with a zero-skip requirement, installs the real Kickstart parser, and runs the pinned Hermes
server smoke on Ubuntu. Existing full desktop, bridge and Linux tests remain enabled.

The existing image workflow inspects the actual built filesystem: app/bridge resources, kernel
and initramfs, product/artwork hashes, commands and aliases, enabled units and Chromium sandbox
ownership/mode. It runs systemd unit verification and the packaged Electron executable in Node
mode. This is packaging evidence, not graphical-session evidence. The NVIDIA leg additionally
requires its kernel module. That leg remains optional in the upstream matrix; assess its own
result rather than treating overall workflow success as NVIDIA success.

Manual image runs now default to `publish=false`; `disks=true` produces an unpublished x86_64
validation ISO artifact. Normal main/tag publishing behavior is retained. A shared, pinned
`build-disk.sh` builds only into a new directory below the working directory on Linux.

The existing installer workflow consumes either a release ISO or a validation image run ID.
It boots through the ISO's UEFI loader instead of bypassing the media with `-kernel/-initrd`.
GRUB test arguments and both EFI configuration copies are changed while replaying the media's
boot setup. Unknown media layouts fail explicitly. A required disposable SSH account verifies
key-only access, core services, booted deployment, first boot, aliases and a real niri desktop
window. An adjacent synthetic Windows-style GPT disk is hashed before installation and after
installation/reboot. Only VM `vda` is selected by the unattended storage configuration.

The HTTP kickstart server binds to loopback and serves only a dedicated directory, excluding the
test SSH private key. Retained evidence includes redacted kickstart, installation/boot logs,
screenshots, guest checks, image source revision and protected-disk hash. The fixture contains
ESP/MSR/basic-data partition types and sentinels, **not Windows or formatted filesystems**.
Shared-ESP coexistence and actual Windows boot are separate pending tests.

## C–D. Commands and observed results

Commands below were executed from the repository root on Windows. For Python/Bash tests, Git Bash
was prepended to PATH and `PYTHONUTF8=1`. Node is 22.23.3, npm 10.9.9, Python 3.12; pykickstart
3.78 was installed in the existing validation environment. Raw local logs are ignored
`madx-astra-*.log` files; compact evidence and report hashes are in VALIDATION_RESULTS.json.

| Executed command | Result |
| --- | --- |
| `git status --short`; `git log -6 --oneline`; `git remote -v`; `git switch -c codex/linux-release-validation` | Confirmed clean starting state; dedicated branch created. |
| `.venv/py312/Scripts/python.exe -m pytest linux/tests/test_branding.py linux/tests/test_window_rules.py linux/tests/test_vm_disks.py -q` | Initial baseline: 40 passed, 26 skipped. |
| `npm run typecheck` | PASS before changes and on final source. |
| `npm run build` | PASS; renderer and main/preload bundles generated; existing bundler warnings. |
| `npm exec --workspace apps/desktop -- vitest run src shared --maxWorkers=2` | 4,915 passed, five skipped; 351 files. |
| `npm exec --workspace apps/desktop -- vitest run electron/calc/notes.test.ts electron/ipc/capture.test.ts electron/ipc/dictation.test.ts electron/office/templates.test.ts electron/pet/window.test.ts shared/product-windows.test.ts --maxWorkers=2` | 89 passed; `ELECTRON_SKIP_BINARY_DOWNLOAD=1`. |
| `npm run branding:check`; `node scripts/madx/audit-branding.mjs --check` | PASS; no unreviewed product-copy candidate. |
| `.venv/py312/Scripts/python.exe scripts/madx/check-native.py --bash "C:\Program Files\Git\bin\bash.exe"` | PASS: 71 Python, 41 Bash, six TOML files. |
| `.venv/py312/Scripts/python.exe -m pytest linux/tests/test_release_validation.py linux/tests/test_installer.py linux/tests/test_branding.py linux/tests/test_window_rules.py linux/tests/test_vm_disks.py -q` | 60 passed, 26 skipped: three symlink and 23 Linux-only cases. |
| `.venv/py312/Scripts/python.exe -m pytest linux/tests/test_unattended.py -k installer_test -q` | Three passed, 218 deselected. |
| `.venv/actionlint/actionlint.exe -shellcheck= -pyflakes= .github/workflows/ci.yml .github/workflows/image.yml .github/workflows/installer-test.yml` | PASS, official actionlint 1.7.12 archive checksum verified; shell blocks also checked with Bash. |
| `git diff --check` | PASS. |

The original 128 Windows main-process failures were reproduced upstream in the previous session;
they were not rerun, suppressed or declared passed. Full Python CLI collection needs Unix `pwd`.
The native suites, systemd, native packages and all VM execution remain pending. Windows lacks
an installed WSL distribution and Podman/Docker/QEMU; these tools were not installed on the host.
Read-only GitHub lookup found no matching foundation branch and no PR-triggered runs in its
limited first-page query for `50dd6d4`. This is not a complete repository CI-history audit.

## E–F. Artifacts and real Hermes result

The production build generated `apps/desktop/dist`; it was not launched as a native Linux app.
The only disk created locally was a temporary 512 MiB sparse GPT unit-test fixture. It was not
booted and contains no OS. No container/ISO/QCOW2 release artifact or VM screenshots exist from
this session. CI artifact names above describe expected outputs, not completed runs.

Executed runtime setup and test:

```text
.venv/py312/Scripts/python.exe -m venv .venv/hermes-runtime
.venv/hermes-runtime/Scripts/python.exe -m pip install --disable-pip-version-check -e ./upstream/hermes-agent
.venv/hermes-runtime/Scripts/python.exe -m pip freeze
.venv/hermes-runtime/Scripts/python.exe scripts/madx/hermes-smoke.py
```

Installation and smoke **passed** against Hermes 0.21.5 at the repository's locked revision
`f97608f178d1ffeca59860195ab7da295f7c8e5f`. Report:
`.venv/astra-hermes-runtime.json`; sanitized logs: `.venv/astra-runtime/hermes-smoke-{0,1}.log`;
dependency snapshot: `.venv/astra-hermes-dependencies.txt`. The source pin is checked; resolved
transitive dependencies are captured rather than presented as a fully locked environment.

Observed: actual MemoryStore write, two actual server launches, healthy HTTP API, rejection of
missing/invalid session tokens, `herald_os`/`system_info` discovery, skill creation/listing, memory
and skill persistence after restart, unknown-route 404, and cleanup of owned child processes.
Initial harness failures were Windows child-process cleanup and placing skills beneath `.venv`
(a directory Hermes intentionally excludes). Both harness issues were corrected before the pass.

Not tested: model-backed messages, model tool choice, desktop host execution, interactive
approval/denial, routines, provider errors, native desktop recovery, or systemd startup. No model
credentials were supplied; no provider was configured and neither common local endpoint was
listening. HTTP proxy settings block accidental normal outbound requests from the smoke; this
is not a network sandbox. User profiles and pinned Hermes source were not modified.

First boot still installs Hermes from `main` unless `/etc/herald-os/ref` selects a ref. Therefore
the passing pinned test does not certify whichever runtime a future online install downloads.
Record and test the actual installed revision; selecting a release pin needs an explicit
compatibility decision, not a silent architecture change.

## G. Installer, image and hardware findings

The reported `grub2-mkconfig: Child process exited with code 1` and absent OSTree deployment have
not been reproduced. Original Anaconda logs were not available. No guessed GRUB fix was applied.
New `%onerror` and `%post --nochroot` diagnostics retain storage/program/Anaconda/package logs,
UEFI state, mount/partition information, read-only EFI listing, deployment origins and GRUB config
locations. The harness refuses kickstarts with no system deployment command. Inspect the first
actual failing phase and complete logs before choosing a fix. The media repack itself also needs
execution against the pinned builder's output; parsing it does not establish bootability.

Source base: Fedora bootc 44; normal image tag floats, while the NVIDIA workflow resolves base
and Universal Blue akmods digests and matches the kernel. The disk builder remains pinned to
`sha256:2b52843ea2bfda73b0a08d97e76b734393b1d3a804681b9fabb26723bd3a2f0b`.
No blind migration to a newer builder was made. Product metadata changes retain Fedora ID and
the existing immutable `/usr` app layout; user/configuration state remains under existing paths.

Packages cover Intel/other Wi-Fi firmware, Bluetooth, Intel GPU firmware, kernel modules,
SOF/ALSA audio and PipeWire. NVIDIA source includes open kernel modules, driver/CUDA libraries,
container toolkit, signature and kernel checks, and initramfs regeneration. None proves actual
RTX 4070 operation. Alienware m16 R2 testing still needs hybrid graphics, external displays,
NVIDIA/CUDA and VRAM checks, suspend/resume, Wi-Fi/Bluetooth, speakers/microphone, battery/thermal
behavior and Secure Boot. VMs cannot establish these laptop results. Existing SELinux permissive
mode and unconfigured project signing remain explicit release/security limitations.

## H–J. Blockers and progress estimate

**Source migration is substantially implemented; native release readiness is unproven.** Of the
nine requested installability criteria, zero are fully closed with Linux release evidence here:
image/ISO creation, UEFI boot, isolated install, reboot, desktop, core services, complete Hermes,
update/rollback and absence of critical installer/security regressions all require execution.
Hermes has useful partial evidence from the real Windows process test. A percentage would confuse
source completion with release readiness. The retained-name contracts and all open platform gates
remain in REMAINING_ISSUES.md; the feature register records this session's evidence.

Focused commits for this session are recorded in the final section below. Phase 2's desktop and
Hermes plan remains in PHASE2_PLAN.md and is not started.

## K. Next Astra engineering task

After an authorized transfer of this branch to a supported Linux environment:

1. Run existing `ci.yml` at the exact source commit. Require full desktop/bridge suites, zero-skip
   Linux alias report and the real Hermes job. Keep test reports and dependency snapshot.
2. Run `image.yml` with `publish=false`, `disks=true`. Inspect per-architecture and NVIDIA evidence,
   packaged Electron, systemd errors, os-release and ISO checksums. No registry switch is needed.
3. Run `installer-test.yml` at the same source with `image_run=<that run ID>`, empty `tag`, and
   `account=madx-test`. Require all three cases and review logs/screenshots as well as exit status.
   Inspect graphical installer branding separately: unattended text mode does not test that UI.
4. Fix the first reproduced image/installer failure, rerun the affected gate, then check Linux
   Hermes chat/tool approval/denial and desktop recovery using an authorized configured provider.
5. Complete the isolated update/rollback procedure below before declaring Phase 1 complete.

### Update/rollback procedure — not executed

Use disposable VM disks only, with a stopped-VM snapshot and two known image revisions A/B.
Start from both an existing Herald-derived image and MadX A. Record `bootc status --format=json`,
`rpm-ostree status --json`, `ostree admin status`, image digests, enabled units and alias targets.
Seed deterministic sample preferences, a browser profile, Hermes memory/skill/plugin settings and
documents; close the app/server and hash those files. Preserve the manifest outside the guest.

For a clean deployment, stage B using the already configured **test** source and the existing
updater (`madx-agent-os-update --no-hermes`); for an rpm-ostree-layered copy verify the existing
rpm-ostree upgrade branch retains its layering. Do not silently rebase a real installation to a
new registry. Reboot the VM, assert B is booted, run `guest-smoke.sh` over SSH, verify both command
names and every service alias, then compare the closed-profile hashes and reopen each profile.
Run `madx-agent-os rollback` inside the guest, reboot, prove A is booted and repeat those checks.
The current rollback command calls bootc; a layered deployment must be tested explicitly before
assuming that path works. Tarball rollback separately retains `/opt/herald-os.previous`.

For failed-update recovery, disconnect the VM's test update source, attempt staging, and verify
the command fails without changing the booted deployment or data. Test an unbootable B only on
another snapshot and recover A through the VM's boot menu. Capture all statuses and logs; a failed
network check alone does not certify failed-boot recovery. Channel selection derives its repository
from the current deployment, while normal update uses bootc/rpm-ostree's configured origin.

## Source references

- [Kickstart directives](https://pykickstart.readthedocs.io/en/latest/kickstart-docs.html) support
  the diagnostic sections and disk restrictions; parsing is covered locally.
- [xorriso manual](https://www.gnu.org/software/xorriso/man_1_xorriso.html) describes boot setup
  replay; actual repacked-media boot remains pending.
- [bootc status documentation](https://github.com/bootc-dev/bootc/blob/main/docs/src/man/bootc-status.8.md)
  defines the machine-readable deployment check.
- [Actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12) was used for workflow validation.

## Session commits

- `09f0d5a` — real pinned Hermes smoke in an isolated profile.
- `d08d5e3` — Linux CI evidence, image inspection and actual-UEFI installer acceptance harness.
- The documentation/evidence commit containing this file follows those source commits; its ID is
  recorded in the session's final response and Git log. Final working-tree verification is clean.

Local commits use command-scoped `Codex <codex@localhost>`; global Git identity is unchanged.
