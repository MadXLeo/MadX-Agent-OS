# Astra progress — updated 2026-10-29 (Asia/Calcutta)

## Current repair source and actual VM results

Current code HEAD is **`448e85ea672fd4b00f6b581f5b27b5d858264a8e`**, pushed only to
`codex/linux-release-validation`. [CI 40848022569](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40848022569)
passed at that exact revision: Linux system **2,336 passed/two reviewed skips**, macOS system
**2,232 passed/106 platform skips**, aliases **19/19**, desktop **5,835/two skips on Linux** and
**5,833/four skips on macOS**. Typechecks, production builds, branding, scripts, signing policy,
secret scanning and pinned real Hermes passed. All five CI evidence ZIPs were downloaded and
SHA-256 verified. Both new account regression tests passed on Linux and macOS; no unexpected Linux
skips were accepted. Unpublished [image 40848023781](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40848023781)
completed with publish=false/disks=true. Both default images passed inspection, systemd verification
and packaged Electron execution (44.5.1); NVIDIA failed on the same missing upstream module image.
The manual installer rerun [40850572175](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40850572175)
is running against this exact image/source with account=madx-test and no tag. Its outcome is pending.

| Current object at `448e85e` | Digest / checksum |
| --- | --- |
| amd64 OCI image | `sha256:a1e5c33066b525062d3752259a71dae844d7316cd191fff88996284d30eb51dc` |
| arm64 OCI image | `sha256:f7013331587eebedabb3397d908206235b794687b772cc49ee568a47dab704f2` |
| ISO `madx-agent-os-validation-448e85e-x86_64.iso` (3,883,677,696 bytes) | `c0bacb3f36409678b9de091022cb0eea85c9ec88e47ffdbf9b9988fd7c5a9357` |
| ISO part0 | `b506d0642cd415280bfc4e455097852c327e7eb320542a09273a4573704b50b7` |
| ISO part1 | `cbf2b479f4e8a080884ac471b87d8adae71b1c7371102bb1e05ca5039b6f9c1f` |
| amd64 Actions archive 12885819367 | `10920e99e4bba4922be3ef40d776fb6c26f1cac88ea4c679fdf796f2aa9d229b` |
| arm64 Actions archive 12886635879 | `be30d0595bab179154c1329350e234c50459778c4bf4cb4373ecaafc9dcf3a5a` |

Both full source labels and the unchanged Hermes pin were checked. The arm64 evidence ZIP was
downloaded/hash-verified. The amd64 metadata was range-read and ZIP CRC-checked; its full archive
digest is GitHub-reported and ISO/part hashes come from its checksum files. The installer must
verify the reconstructed ISO. Registry pushes/signing, manifests and release steps were skipped.

Installer [40814588924](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40814588924), using image
40812159188 at `161557f`, **booted the actual ISO through UEFI and completed Anaconda installation
in all three cases**. The reconstructed ISO checksum, actual EFI partition replacement/verification
and expected encrypted/unencrypted disk layouts passed. The encrypted disk accepted the correct
test password and rejected an incorrect password. The adjacent synthetic Windows-style GPT disk
retained its exact hash after installation and after the acceptance failure.

Both unencrypted VMs then booted the installed deployment and displayed the MadX desktop, dock and
"Welcome to MadX Agent OS" screen. The retained `shots/boot-18min.png` images were visually inspected.
This proves first reboot and graphical rendering; interactive application acceptance is still open.
The encrypted VM remained at the disk-unlock prompt. **The overall installer run failed**, and no
GRUB installation failure was reproduced.

The unencrypted installation log identifies a concrete product defect: `base64: command not found`
in the minimal Anaconda runtime. Account setup continued with an empty key file, so first boot
correctly left SSH off (`no SSH keys from the install: SSH stays off`). Commit `cb55130` uses the
already-required Python base64 codec, refuses encoding failures before generating the account
fragment, and makes the generated post-install script fail on errors. A portable reproduction
confirmed the original empty-key failure and verified exact key preservation with the fix.

Commit `448e85e` paces serial password bytes, clears partial input and keeps the connection open
after Enter. Incomplete serial input is the current hypothesis for the encrypted boot failure,
not a confirmed UART root cause. The workflow now distinguishes SSH readiness failure from an
authentication-policy failure and runs acceptance only after readiness succeeds. **55 focused
tests and actionlint pass locally**. Two new native account tests could not run locally because
Windows refused test-fixture symlinks (WinError 1314); both subsequently passed in native CI.

First-boot logs show Hermes installation and bridge setup completing in the unencrypted guests.
Installed service state, the installed Hermes revision, guest acceptance and model-backed operation
remain unverified because SSH was unavailable. The source/client Hermes pin was not changed.

All three failure-evidence ZIPs were downloaded and SHA-256 verified:

| Artifact | SHA-256 |
| --- | --- |
| 12873530720, unencrypted | `f940f2352b71444f49ebd3acd1e8117ece4f7cac83123de71e7284dc1b8ac3ba` |
| 12873083407, unencrypted/protected disk | `81d757bbc1377a55a37740915f912aa52241da054ea0b18429e47de2810f447f` |
| 12872898816, encrypted | `e89af999e4483f72d4a35cab14a839db9e7342f355a338262d4d5551716d195b` |

They retain install/boot/SSH logs, screenshots, redacted kickstarts, source provenance, EFI layout
verification and the protected-disk checksum. No host disks, EFI entries or firmware were touched.

### Last fully validated CI and completed image source

Previous code source is **`161557f9da021d0c7b44024260bc75448c5cc083`**, pushed on the authorized
branch. It fixes the second real preparation failure described below. Full CI
[40812157730](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40812157730) passed: Linux system
**2,329 passed/two reviewed skips**, macOS system **2,225 passed/106 platform skips**, aliases 19/19,
both desktop suites (Linux 5,835/two skips; macOS 5,833/four skips), typechecks/builds, scripts,
signing, secrets and real Hermes passed. All five CI archives were downloaded and SHA-256 verified.
Unpublished image [40812159188](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40812159188)
completed at this revision with publish=false/disks=true. Both default architectures passed
filesystem inspection, systemd unit verification and packaged Electron execution. NVIDIA hit the
same upstream module blocker; no registry/release/tag publication occurred.

| Current object at `161557f` | Digest / checksum |
| --- | --- |
| amd64 OCI image | `sha256:b615b4597990049ae3931132832099749d5db22bda599017b05dd74b63f9fc12` |
| arm64 OCI image | `sha256:5a0e3543016d488c3ed7edc501055dd47055f59002898169eb538d6e7a89e2df` |
| ISO `madx-agent-os-validation-161557f-x86_64.iso` (3,883,671,552 bytes) | `d1ac64f36cfebe34718ad90d3b693ae1d738a961c09151f86e3c581bc8875a20` |
| ISO part0 | `9abfeb36c794746745a7c8bb5ec4a1ac731b86459866a3944167929cf9283782` |
| ISO part1 | `d0f07e05d2c3183b8eb4d55d844614458174780d58f3225cc4284fb84f80ea72` |
| amd64 Actions archive 12871138762 | `49d3cdb946fb9f0ae09df6b0dab97b75b3903bcb0fd4468b85d3ae8873f001a0` |
| arm64 Actions archive 12870978034 | `e0ab05e4e1b8ba431b0e09312df5b6fb28f7899755f3da8c78e179aa7f259eff` |

Both source labels match the complete source revision. The small arm64 archive was fully
downloaded/hash-verified; amd64 metadata members were range-read and ZIP CRC-checked. ISO/part
checksums come from those metadata files; the full archive was not downloaded to the Windows host.
[Installer 40814588924](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40814588924) was dispatched
against this exact image run/source with account=madx-test, no tag. All three cases verified the
reconstructed ISO; their actual installation and first-boot outcomes are recorded above.

### Previous validated source and second preparation failure

Source **`2290c818e34fed73b45dadc085aabb66f1ec20a5`** is committed and pushed only to
`codex/linux-release-validation`. Full [CI 40780000937](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40780000937)
passed: Linux bridge/system **2,328 passed, two reviewed skips**, aliases **19/19**, macOS
bridge/system **2,224 passed, 106 platform skips**, Linux desktop **5,835 passed/two skips**,
macOS desktop **5,833 passed/four skips**. Both typechecks/production builds, scripts, signing
policy, secret scan and real pinned Hermes runtime passed. The five CI evidence archives were
downloaded and their SHA-256 digests verified.

[Image 40780003482](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40780003482) built and
inspected both default architectures and a fresh ISO at that source. Filesystem inspections,
systemd unit verification and packaged Electron 44.5.1 execution passed. Both labels match the
full source SHA; Hermes remains pinned to `f97608f178d1ffeca59860195ab7da295f7c8e5f`.
NVIDIA failed again on the same unavailable upstream akmods tag; default-image success does not
waive that failure. Registry push/sign, manifest, published disk and release steps were skipped.

| Object at `2290c81` | Digest / checksum |
| --- | --- |
| amd64 OCI image | `sha256:f401d553d303346a9ddb393e2ea36a1aefc9ebd3d0cfe557549efe5e8c054c1e` |
| arm64 OCI image | `sha256:8538ccf53c54df097b9426ea9cec9baa99614a68facf1ee3b1667f414b42e625` |
| ISO `madx-agent-os-validation-2290c81-x86_64.iso` (3,883,870,208 bytes) | `02d343cafcde2eb5201a146625e033dc6ca98be0f2612619eb2e16206476a472` |
| ISO part0 | `52efa608094c993eb8941a26d2f1ec8f116f86cb36761666087c98f8fd251bcc` |
| ISO part1 | `3dda98641f02f5d56e3969a27d4aa6e672ebba450f811f8101349a8687fdd81d` |
| amd64 Actions archive 12858305397 | `0bbf8df2f827020361a11adfab5a5b8d14c7663056d4be7df6a2ddec949a9542` |
| arm64 Actions archive 12856404610 | `6b0c8b6923b4340e9319433ff81ad29b5edadc40a6ab1f1fa1eed83883a30050` |

The arm64 evidence archive was fully downloaded/hash-verified. The amd64 archive's small metadata
members were read by HTTPS byte ranges and ZIP CRC-checked. Its archive digest is GitHub-reported;
the large ISO was not downloaded to the host. ISO checksums above come from the artifact files;
all three jobs in installer 40811638765 verified the reconstructed ISO (`.iso: OK`).

[Installer 40811638765](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40811638765) was dispatched
against image **40780003482**, exact source `2290c81`, `account=madx-test`, no release tag. All three
cases failed before QEMU started. The ISO include was resolved successfully, but the deployment
validator then rejected `/tmp/herald-os-account.ks`, which the existing account `%pre` generates
later inside Anaconda. Its absence on the runner is expected. Failure artifacts were downloaded
and SHA-256 verified; no guest logs/screenshots exist from this attempt.

Repair `161557f` moves strict ISO deployment validation before appending the guest-generated
account fragment. It does not allow host paths or relax include/source checks. Guest smoke also
records first-boot/Hermes service state before later acceptance checks. **50 focused tests,
actionlint and shell syntax checks pass.** Additionally, the actual workflow preparation shell
step was executed locally for encrypted and unencrypted layouts with a fixture ISO reader and
real account generator; both generated kickstarts passed pykickstart parsing. That fixture test
did not boot or install an OS. The subsequent native run is recorded at the top; installed Hermes
service acceptance and interactive graphical operation remain **unverified**.

## Actual image and installer milestone — 2026-10-29

Image run [40743693944](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40743693944)
completed at source `606e1e1be710451f80510d6d355518e20a023b95`. Default **amd64 and arm64 images
built and passed inspection**, systemd unit verification and packaged Electron execution
(44.5.1). The amd64 job built an actual ISO, volume label `MADX_AGENT_OS`, totaling
**3,883,882,496 bytes**. No registry push, manifest publication, release or tag occurred.

| Built object | Digest / checksum |
| --- | --- |
| amd64 OCI image | `sha256:1727dc630a4462d57cfdecacade0b8195af9718b7f32d99ace92148db9da2873` |
| arm64 OCI image | `sha256:b8f05b9417d09034e409e0a5662a1f38df27a020d8fd72b764de7eba145b5ca5` |
| ISO `madx-agent-os-validation-606e1e1-x86_64.iso` | `3bab771854c6d2e811f9100761c15c860ba1c341b8e0d144d7f81dc4919d7d95` |
| ISO part0 | `c2c44acb3b00e68afa47236f8a178b27f2cb8dc14ab16d7ec33ca346298d7df7` |
| ISO part1 | `60d2e221264be4afd5651ab4779f7c25727b058cfe3069acddacdb3388d4c82d` |
| amd64 Actions archive 12840979501 | `40a3b611e23d3c9a4a70fb4238b7ea07edf7ae98ca3c6a63b54e175ec178aa8a` |
| arm64 Actions archive 12841541120 | `450eb75d9182023a2bca1ec0c5d13d7672245f78637c2314ebc3760baa9ac56f` |

The small arm64 archive was downloaded and its SHA-256 verified. The 3.81 GB amd64 archive was
inspected through HTTPS byte ranges: its small members passed ZIP CRC checks, both image labels
match the exact source revision, filesystem inspections report no failures, and UPSTREAM.lock
retains Hermes `f97608f178d1ffeca59860195ab7da295f7c8e5f`. The table's ISO/part checksums are
from the packaged checksum files; all three installer jobs subsequently rejoined the parts and
verified the full ISO against that SHA-256 (`.iso: OK`).
The large host download was stopped after 4 MiB because it was too slow; the partial file remains
ignored and is not claimed as a downloaded or verified ISO. OCI repository-shaped names in the
inspection describe local build tags, not published registry availability.

**NVIDIA did not build.** Its job failed because Universal Blue has not published
`ghcr.io/ublue-os/akmods:main-44-7.2.13-200.fc44.x86_64`. The selected Fedora base was
`quay.io/fedora/fedora-bootc@sha256:e541eab24374e2d35d91ec0b2b3edd71eb7880b50b73329e4116102a751c0e99`.
The workflow marks NVIDIA optional, so overall success does not establish NVIDIA readiness.
No kernel/base downgrade or Hermes revision change was made to bypass this failure.

CI 40743566443 at this exact image revision passed every Linux job: bridge/system **2,316
passed, two reviewed exclusions**, dedicated aliases **19/19**, desktop/build/typecheck and real
Hermes passed. Both macOS jobs were initially cancelled before execution, then passed in attempt 2
at the same source: bridge/system **2,212 passed, 106 skipped**, desktop **5,833 passed, four skipped**,
TypeScript and production build passed. The workflow is now fully successful. Its five evidence
archives were downloaded and their GitHub SHA-256 digests verified.

Installer run [40777283477](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40777283477)
was actually dispatched against image run **40743693944**, with `account=madx-test` and no release
tag, at the same source revision. All three cases (encrypted, unencrypted and protected adjacent
disk) failed **before VM boot** in kickstart preparation. The ISO's top-level `osbuild.ks` delegates
deployment to `%include /run/install/repo/osbuild-base.ks`; the test harness incorrectly demanded
an inline deployment command. This is a reproduced harness defect, not a reproduced GRUB error.
The three small failure artifacts were downloaded and SHA-256 verified. No guest logs or screenshots
exist because QEMU had not started.

Repair `da9068836bc7c0dfea424751825e8d6f63e5ff3c` follows includes only within kickstart files extracted
from the already verified ISO, refuses missing/escaping/cyclic includes, ignores commands inside
script sections, and preserves the original deployment configuration. **42 focused tests passed**;
actionlint and whitespace checks passed. Only the authorized branch was pushed. CI
[40778418968](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40778418968) passed: Linux bridge/system
**2,321 passed, two reviewed exclusions**, macOS bridge/system **2,217 passed, 106 skipped**, both
desktop suites, typechecks/builds and real Hermes passed. Unpublished image build
[40778438792](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40778438792) was started
at this exact revision (`publish=false`, `disks=true`). That build was deliberately cancelled
after the additional boot-layout defect below was found; it is not a completed image-build result.
The image must be rebuilt to preserve the strict image/installer source match; the provenance gate
was not relaxed to reuse the previous ISO.
At that cancelled attempt, UEFI boot and installation remained unverified. Later actual VM
results are recorded at the top; installed Hermes service acceptance remains **unverified**.

### Boot partition inspection and second harness repair

Reading the first MiB of the actual `606e1e1` ISO through artifact byte ranges exposed a second
test-harness mismatch. Its ISO directory places `/images/efiboot.img` at 2,048-byte LBA **1,408,823**,
but the El Torito EFI entry boots LBA **1,886,021**. That is GPT partition 2, beginning at 512-byte
sector **7,544,084**: an appended 20 MiB EFI image. Replacing only the ISO directory file does not
replace those appended bytes. This is artifact-layout evidence, not a claimed GRUB runtime failure.

Repair `2290c818e34fed73b45dadc085aabb66f1ec20a5` extracts the actual boot partition, checks GPT
header/table checksums and agreement with the El Torito EFI entry, patches the test arguments,
replaces that appended partition after xorriso replay, and verifies that the resulting ISO's
bootable partition exactly matches the patched image. The
[xorriso manual](https://man.archlinux.org/man/xorriso.1) documents replay ordering and overriding
appended partitions. The helper accepts ordinary test files only, bounds metadata reads, and
refuses unknown or inconsistent boot layouts. It does not address host devices or firmware.
**49 focused tests and actionlint pass locally.** This repair was pushed only to the authorized
branch. CI [40780000937](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40780000937) and unpublished
image [40780003482](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40780003482) subsequently passed
at `2290c818e34fed73b45dadc085aabb66f1ec20a5`, with the separate NVIDIA exception above.
The installer rerun is recorded at the top.

## Authorized Linux execution — initial run and repairs

The user authorized the isolated Linux validation milestone on
`codex/linux-release-validation`, starting at the verified full commit
`e062c0334dcb382236b18a60422eab0e46a0d8d2`. Only that branch was pushed; main, tags,
releases, registries, Windows disks/EFI/firmware and the separate workspace were not changed.
Git Credential Manager was already installed. Its sign-in was completed by the user after the
first push attempt reported missing credentials; no credentials were passed through chat.

Pre-push review covered the clean working tree, commit history, workflow permissions/publication
guards, all 1,817 tracked files and 543 newly introduced historical blobs. Pattern matches were
test fixtures or UI labels, with no actual credentials found. Large tracked files were branding
assets, not disk images or build output. This local review was followed by the real CI Gitleaks
scan: **461 commits scanned, no leaks found**.

[CI run 40684976475](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40684976475)
is a `push` run on the exact approved commit. The branch push trigger works without a main merge.
Results retained so far:

- Linux desktop: **5,835 passed, zero failed, two skipped**, across 426 passing test files.
  TypeScript, branding and the production build passed. The two skips are the existing chart
  validation tests that require the optional openpyxl interpreter and xmllint; neither tool was
  configured in that job. These remain unexecuted checks, not passes.
- Real Linux Hermes runtime: passed using pin
  `f97608f178d1ffeca59860195ab7da295f7c8e5f`. Actual server launches verified health, authentication
  rejection, bridge discovery, memory/skills and restart persistence. This does not establish
  systemd startup, graphical integration or model-backed behavior.
- Scripts/native inputs, signing policy and secret scan passed. The Linux bridge/system suite
  finished with **2,275 passed, eight failed and 27 skipped**. Both macOS jobs were cancelled
  without executing. At this initial-run checkpoint no image or installer had been dispatched;
  subsequent actual executions are recorded above.
- Local rechecks: **52 passed, three skipped** (Windows symlink privilege), TypeScript, actionlint
  and both branding checks passed. No new host software was installed.

Downloaded evidence archives match GitHub's SHA-256 digests:

| Artifact | ID | SHA-256 |
| --- | --- | --- |
| desktop-tests-Linux | 12815105374 | `31f255bbb9777e3a96647f4807cc066846dda36231a793fad5dbb6415599557e` |
| hermes-runtime-evidence | 12813939066 | `31f710b0117c9b6ff8c476905e336bc24b95bf65fd139e811eb8b2e80f0fd3cf` |
| bridge-tests-Linux | 12815146225 | `3acf729695e6256f01e5b9375174a97a17ee6bd523e50131762f2675e8429e16` |

### Repairs from actual Linux results

- `cf9cd9f`: repaired documentation links whose headings had been renamed. A focused check of
  49 linked documentation pages passes; this also caught three additional stale anchors in the
  image-building guide outside the original failing test's page list.
- `417300e`: repaired the stale checksum URL expectation and made the corruption test alter the
  actual published MadX package, asserting the file exists first. The self-quit regression test
  now exercises matching MadX and legacy app fixtures; direct self-protection recognizes both
  display names and the retained application ID. No update origin or Hermes pin changed.
- `e8e6010`: the Linux runner must successfully enter an unprivileged user namespace. If Ubuntu's
  AppArmor namespace restriction blocks it, the workflow changes that runtime setting only on
  its disposable GitHub runner, then verifies the namespace before testing. This follows the
  [Ubuntu 24.04 release notes](https://documentation.ubuntu.com/release-notes/24.04/).
  The 25 migration skips remain forbidden; the two separately reviewed exclusions are unchanged.

Actionlint, branding audit, Python compilation and 31 provenance/runner tests pass locally.
Attempting the affected Unix test files on Windows failed at collection (`os.getuid` / `pwd`
unavailable), so that is not counted as a passing rerun. The repaired branch was pushed at full
revision `e8e6010b38a351f2dfa6f6ac553bd0a901bae955` and triggered
[CI run 40741143041](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40741143041).
That run **completed successfully** on the exact repair revision:

| Job | Executed result |
| --- | --- |
| Linux desktop | 5,835 passed, two optional spreadsheet-validator skips; typecheck and production build passed |
| Linux bridge/system | 2,309 passed, two reviewed exclusions; all 25 previously skipped namespace tests executed |
| Dedicated Linux aliases | 19 passed, zero skipped |
| macOS desktop | 5,833 passed, four skips; typecheck and production build passed |
| macOS bridge/system | 2,205 passed, 106 skips |
| Real Linux Hermes | Passed at the unchanged pin |
| Scripts, signing policy, secrets | Passed; Gitleaks scanned 464 commits |

The macOS desktop skips are three Linux-specific filesystem cases and the optional openpyxl
chart validator. Its XML chart check ran. The macOS bridge skips comprise cryptsetup (28), loop
device (1), root nft (1), setsid/proc (15), shellcheck (5), util-linux terminal (9), namespaces
(24) and Linux disk packaging (23). Linux executed those applicable native cases. macOS executed
the PDFKit case excluded on Linux. Root nft syntax remains a separate unexecuted release gate.

All five repair-run archives were downloaded and their digests checked:

| Artifact | ID | SHA-256 |
| --- | --- | --- |
| desktop-tests-Linux | 12839867223 | `b0e357c9f665411fea9e4358593c40e9a6443b1a2966cfa9a03e4c2ec7fef181` |
| bridge-tests-Linux | 12839833956 | `b18a68b58308e36b40c72de0a22ed8df2aa4a198f1c1b9d14830c59b7ef38be6` |
| hermes-runtime-evidence | 12839712352 | `6c15a950d64e1f2adec2c411287210bfc6e873363e5989fed958799182d3bc10` |
| desktop-tests-macOS | 12839702905 | `270313f593f347bd5223beb21edf7f4a33119e77007fcaae0795e0c809aba50d` |
| bridge-tests-macOS | 12839428084 | `75a01023bd39a301682070578c3004b3cd6872577afb4a91e49ac9fb0ae2eccf` |

### Manual workflow dispatch: actual failure and registration repair

The first image dispatch returned HTTP 404. API inspection showed only CI registered in Actions,
although both manual workflow files exist on main. File presence alone did not prove dispatch
availability. GitHub documents the initial-run registration requirement in its
[workflow_dispatch reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch).

Commit `606e1e1be710451f80510d6d355518e20a023b95` adds registration-only jobs for pushes on the
authorized branch. The image build chain is skipped on those pushes; installation remains manual.
Publishing is explicitly disabled on this branch, even with a manual publish=true input. The
existing main/tag release behavior is preserved. Seven event/ref/input cases test these guards;
37 focused validation/installer tests and actionlint pass locally.

The branch-only push registered both workflows successfully. Image registration run 40743566536
ran only its registration job: channel, image, manifest, disks and release were skipped. Installer
registration run 40743566760 ran only its registration job: installation was skipped. **These runs
are registration evidence, not image or installation evidence.** No main merge was needed.

Actual manual image dispatch then returned HTTP 204 with publish=false and disks=true:
[image run 40743693944](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/40743693944),
at source `606e1e1be710451f80510d6d355518e20a023b95`. That image build and full CI 40743566443
subsequently passed for the default architectures; the actual installer result and repair are
recorded at the top. Do not advance the remote source while image/installer provenance is being checked.

The later UEFI boot, installation and unencrypted desktop evidence is recorded at the top;
installed Hermes service acceptance remains **unverified**. The image and installer must use the same CI-validated
revision; the initially approved base and every repair revision are recorded above.

## Historical continuation: execution prepared, remote authorization required

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

### Historical milestone evidence before remote authorization

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
  replay; actual repacked-media UEFI boot passed in installer 40814588924.
- [bootc status documentation](https://github.com/bootc-dev/bootc/blob/main/docs/src/man/bootc-status.8.md)
  defines the machine-readable deployment check.
- [Actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12) was used for workflow validation.

## Session commits

- `09f0d5a` — real pinned Hermes smoke in an isolated profile.
- `d08d5e3` — Linux CI evidence, image inspection and actual-UEFI installer acceptance harness.
- The documentation/evidence commit containing this file follows those source commits; its ID is
  recorded in the session's final response and Git log. Final working-tree verification is clean.

Local commits use command-scoped `Codex <codex@localhost>`; global Git identity is unchanged.
