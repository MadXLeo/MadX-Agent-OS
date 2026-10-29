# Continue MadX Agent OS

Continue `codex/linux-release-validation`, based on `codex/madx-foundation` at `50dd6d4`.
Read ASTRA_PROGRESS.md, VALIDATION.md, REMAINING_ISSUES.md and MIGRATIONS.md. Preserve existing
work and do not repeat the initial inventory. Do not merge or modify Claude's separate workspace.

The user authorized this branch's pushes, Linux CI, unpublished image build and disposable UEFI
installer tests. The approved initial revision `e062c0334dcb382236b18a60422eab0e46a0d8d2` was
pushed and ran as CI 40684976475. Linux desktop (5,835 passed, two optional-tool skips), build,
real Hermes runtime and secret scan passed; eight bridge/system test failures and 25 unexpected
namespace skips required repairs. Repair revision `e8e6010b38a351f2dfa6f6ac553bd0a901bae955`
passed CI 40741143041. Registration fix `606e1e1` also passed full CI 40743566443; its image run
40743693944 built both default architectures and an actual ISO. All three installer cases in
40777283477 verified the ISO checksum but failed before VM boot because the test harness ignored
the ISO's included deployment kickstart. Fix `da90688` passed full CI 40778418968. Inspection of the
actual ISO then identified a separate appended-EFI-partition mismatch in the test setup. Repair
`2290c818e34fed73b45dadc085aabb66f1ec20a5` is pushed; 49 focused tests/actionlint pass. CI 40780000937
passed; unpublished image 40780003482 built and inspected both default architectures and a new ISO.
Installer 40811638765 verified the ISO in all three cases but failed before boot: the strict
deployment validator also tried to read the account include generated later inside the guest.
Repair `161557f9da021d0c7b44024260bc75448c5cc083` validates the original ISO before adding that account
fragment. It passed 50 focused tests, workflow/shell checks and both full preparation-step fixture
checks. Full CI 40812157730 passed (Linux system 2,329/two skips, macOS system 2,225/106 skips).
Unpublished image 40812159188 completed at this new source; both default architectures and the ISO
passed their build/inspection steps. Installer 40814588924 booted the ISO through UEFI and installed
all three cases. Both unencrypted guests rebooted to the graphical MadX welcome screen; the
protected synthetic GPT disk remained unchanged. Acceptance failed because Anaconda lacked base64
and lost the SSH key, while the encrypted guest remained at its unlock prompt. No GRUB failure
was reproduced. Repairs `cb55130` (Python key codec/error handling) and `448e85e` (paced serial input
and accurate SSH readiness reporting) are pushed. Current source is
`448e85ea672fd4b00f6b581f5b27b5d858264a8e`; CI 40848022569 passed (Linux system 2,336/two skips,
macOS system 2,232/106 skips, all aliases, both desktop suites/builds and real Hermes).
Unpublished image 40848023781 completed; both default images and a new ISO passed build/inspection.
Installer 40850572175 is running against that exact image/source with account=madx-test.
Superseded image 40778438792 was deliberately cancelled; NVIDIA still fails on missing upstream modules.
See ASTRA_PROGRESS.md for current outcomes and exact artifact checksums.
The host has no Linux runtime; the branch's proven push trigger runs CI without a merge.
Follow installer 40850572175. Preserve the previous logs/screenshots and compare the SSH and
encrypted-unlock results. Fix only confirmed failures and preserve matching full source revisions.
Never reuse a mismatched image or claim boot from a build pass.
Inspect the first real Anaconda/GRUB diagnostics,
boot screenshots and guest checks before any installer fix. Source and Windows Hermes runtime
checks pass; installed Linux, model-backed chat and update/rollback gates remain open. See ASTRA_PROGRESS.md
for the exact sequence, evidence limits and the isolated update/rollback procedure. Keep image
and installer revisions identical: the installer rejects mismatched image-run evidence.

Do not start LoRA Studio, self-development or Phase 2 implementation until these gates pass.
PHASE2_PLAN.md is planning only. Keep all compatibility identifiers listed in MIGRATIONS.md and
REMAINING_ISSUES.md. Authorization covers only the named validation branch; no merge, tag, release,
registry publication, paid infrastructure or new host system software is permitted. Never use host Windows disks,
EFI entries or firmware for testing.

Useful local checks:

```text
npm run branding:check
node scripts/madx/audit-branding.mjs --check
npm run typecheck
npm run build
npm exec --workspace apps/desktop -- vitest run src shared --maxWorkers=2
python scripts/madx/check-native.py --bash <bash-executable>
python -m pytest linux/tests/test_branding.py linux/tests/test_window_rules.py linux/tests/test_vm_disks.py -q
```

The complete native suites remain enabled in CI; do not disable failing tests to manufacture a
passing release. Credentials, signing keys and publishing are separate from local source validation.
