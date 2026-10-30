# Continue MadX Agent OS

Continue only `codex/linux-release-validation`; preserve the current working tree and history.
Do not restart the audit or modify Claude's separate workspace. Read ASTRA_PROGRESS.md and
REMAINING_ISSUES.md for evidence and open gates; VALIDATION_RESULTS.json records exact revisions.

## User's waiting preference

When CI, image creation or installer testing needs time, stop and report its run link. Do not
keep polling or waiting. Resume only when the user says to continue. Do not launch duplicate runs.

## Completed evidence

Last completed CI/image/VM source: `7f88d80a19d99e144fec97ee4ee8b8d3d86440ef`.

- CI 40898401729 attempt 2 passed: Linux system 2,347/two skips, aliases 19/19,
  desktop 5,835/two skips; macOS system 2,243/106 skips, desktop 5,833/four skips.
  Typechecks, production builds, branding, secret scan and pinned Hermes passed.
- Unpublished image 40899343029 built and inspected both default architectures and a real ISO.
  ISO SHA-256: `220db0a115b7869568779947a4bd44c2c942a2dd5260dbbd81eda68dc673a59d`.
- Installer 40945372298 completed against that exact image/source, account=madx-test.
  All three cases installed, rebooted (including encrypted unlock), passed SSH restrictions,
  captured privileged deployment status, resolved aliases and rendered the MadX welcome desktop.
  The protected synthetic GPT disk retained its hash. No GRUB failure was reproduced.
  All three failed systemd-remount-fs: Anaconda's Btrfs root fstab options cannot reconfigure
  the composefs overlay. The boot logs also show an unset HOME in the GPU helper.
- Installed Hermes revision is `67d47601bc5f8ed322451a672c843ed0e1a7c42c`; CI's unchanged pin is
  `f97608f178d1ffeca59860195ab7da295f7c8e5f`. Existing first-boot behavior tracks main. Do not silently
  switch it. Retry-install unit condition=false is not evidence of model-serving/chat.

## Repairs ready for fresh remote validation

CI 41000794337 at `c4300785cef44023c60c86d1623bbd0361eeeafd` completed with one failure on each
native platform: the account parser test still expected one post-install script, although the root
repair adds another. Linux system: 2,361 passed/one failed/two skips; macOS: 2,257/one/106. All 15 new
root-mount/GPU cases and all 19 alias cases passed in both full suites. Both desktop suites,
typechecks/builds, branding, secret scan and Hermes passed. The separate Linux alias job was skipped
after the suite failed. The corrected test checks both posts, error handling and execution contexts.
Its portable parser check, 23 focused tests, preparation fixtures and actionlint pass; full CI is next.
Do not retry the unchanged failing revision or dispatch an image before the corrected revision passes.

Code revision `21eda78b9f63c35da088090df3d6614d01af310f` includes `35fea98` (GPU HOME),
`c5dfa69` (offline root-options migration) and `21eda78` (LF checkout rules). The migration verifies
boot options before changing fstab, preserves other mounts/encryption arguments, and keeps the
remount failure gate enabled. Existing systems are not automatically migrated; custom layouts
remain unverified. No Hermes pin, release origin or host system configuration was changed.

23 focused local tests passed, plus both actual workflow preparation fixtures, actionlint, branding
and source parsing (79 Python, 44 Bash, six TOML). The wider Windows fixture run has 54 passes,
201 failures and 28 skips. All failures are WinError 1314 (missing symlink privilege); representative
unchanged fixtures reproduce it. These failures are documented, not counted as passes.

## Next execution sequence

1. Review the final diff and clean tree; push only the authorized branch. Record the full new
   HEAD and its triggered CI link, then stop. The docs commit after the code revision is part of
   the source to validate. Check live Git state to determine whether this push already happened.
2. On the user's next continuation, inspect that exact CI result and skips. Fix reproduced
   failures on the same branch. Only after CI passes, dispatch image.yml with publish=false,
   disks=true and that exact source revision. Report the link and stop.
3. On continuation, verify the built image's provenance/checksums. Dispatch installer-test.yml
   against that exact image run/source, account=madx-test, empty tag. Report its link and stop.
4. On continuation, inspect real installer logs, rootflags, fstab, /sysroot mount options,
   remount service, first reboot, screenshots and Hermes evidence. Do not claim repairs passed
   until these new VMs actually execute.

Remaining MVP gates include the repaired remount check, Hermes revision alignment and model chat,
interactive desktop operation, update/rollback and profile integrity. NVIDIA remains blocked by
missing upstream kernel modules; do not silently downgrade or change release origins.

Authorization covers only this branch's pushes, CI, unpublished images and disposable UEFI VMs.
No main merge, force push, tags, release, registry publication, paid infrastructure or new host
software. Never touch host Windows partitions, EFI or firmware. Preserve compatibility identifiers
and legal attribution. Do not begin LoRA, self-development or Phase 2 implementation.
