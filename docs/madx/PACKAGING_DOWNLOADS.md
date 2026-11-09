# Linux packaging download correction — 2026-11-10

Image run [42572519127](https://github.com/MadXLeo/MadX-Agent-OS/actions/runs/42572519127),
attempt 2, source `42bcc70b1be621bb726b8c1647b538897aad39a7`, failed in the standard
amd64/arm64 Electron packaging jobs with HTTP 504 after ZIP download reached 100%.
The NVIDIA image/ISO job passed. The hosted error omitted the request URL, so the
exact earlier failing endpoint remains unconfirmed.

## Focused correction

`apps/desktop/scripts/electron-builder-linux.cjs` supplies the Linux x64/arm64 hashes
from the exact pinned Electron npm package's `checksums.json`. This is the same source
used by Electron's own installer, obtained through `npm ci` and the existing lockfile.
Both hashes were compared with the official Electron 44.5.1 release checksum manifest
retrieved on November 9. No version, dependency, binary origin or driver revision changed.

The actual pinned electron-builder 26.15.3 schema supports inline checksums. Its
`mirrorOptions` discriminator must be present to forward these options to its nested
`@electron/get` 3.1.0. The configuration keeps the default download origin, TLS and
checksum verification, preserves all existing packaging settings, and rejects missing
architecture hashes or an installed Electron version different from the exact pin.
Only `dist:linux` selects this configuration; publication remains explicitly disabled.
See the upstream [checksum option documentation](https://www.electron.build/v26/docs/api/electron-builder.interface.configuration/).

A controlled test using the real downloader reproduces the second SHASUMS256 request
and an injected HTTP 504 without inline hashes. With this configuration, the real
builder/downloader needs only the ZIP request on both architectures. Corrupted ZIP
bytes are rejected, with no online fallback. This establishes the corrected dependency
on a second network request, not the unlogged URL or root cause of the historical 504.

## Local validation and limits

- Eight focused tests passed: real builder schema, preserved configuration, simulated
  checksum-server failure, both architectures, corrupt bytes, version/missing hashes.
- TypeScript workspace checks and renderer/Electron production builds passed.
- Central branding synchronization/audit and actionlint passed.
- Release-validation suite: 43 passed, no skips.
- Broader packaging-test invocation: 11 passed, one existing Windows failure in
  `after-pack.test.ts:37` (backslashes versus expected POSIX separators). The test and
  production hook are byte-unchanged from the prior commit; no assertion was weakened.
- `test_image.py` could not collect on Windows because Linux's `pwd` module is absent.
  The CLI/test files are unchanged. Native Linux coverage remains required.
- Existing build chunk-size/dynamic-import warnings remain; no UI performance claim.

Fresh complete Linux/macOS CI must pass at the new commit before an unpublished image
build. Do not rerun the old source and claim this correction was tested. Keep the image
run-success/source/ISO checksum gates and all existing skip rules. No installer dispatch
while the complete image run fails.

## Retained NVIDIA artifact

The prior NVIDIA artifact 13660265466 passed independent archive/ZIP/part/full-ISO
integrity and source/variant review. Its ISO is
`madx-agent-os-validation-42bcc70-nvidia-x86_64.iso`, 4,767,723,520 bytes, SHA-256
`0e89ac5afdec40f69b198033324a73f56877371ed2287011975a118b93af84c6`.
It remains evidence for source `42bcc70`, not a build of this later packaging correction.
Candidate UEFI boot, installation, first reboot, desktop interaction, installed Hermes,
Secure Boot module trust and physical RTX/HDMI performance are unverified. No USB,
physical disk, host EFI/firmware, registry publication, release or tag is part of this fix.
