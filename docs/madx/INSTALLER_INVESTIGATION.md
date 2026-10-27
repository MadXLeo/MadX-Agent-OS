# Installer investigation — open, not fixed

Reported failure: `Bootloader write config: grub2-mkconfig: Child process exited with code 1`.
There are no installation logs or failing VM disk attached to this checkout. Leftover Ubuntu files
are not an established cause. Do not claim this issue resolved from a source audit.

## Evidence in this revision

- `linux/image/Containerfile`: Fedora bootc 44, followed by `bootc container lint`.
- `linux/image/iso.toml`: interactive Anaconda kickstart, `autopart --type=btrfs --encrypted`,
  no embedded passphrase, `xconfig --startxonboot`, no `clearpart` or forced first disk selection.
- `linux/image/unattended.ks`: separate, explicitly unattended configuration; must never be run
  against the development host.
- `.github/workflows/installer-test.yml`: QEMU/KVM + OVMF installer and reboot tests for encrypted
  and unencrypted virtual disks; optional throwaway-account SSH check. Existing release-download
  requirements mean this workflow is not evidence that this checkout has booted.
- `linux/tests/test_installer.py`, `test_image.py`, `test_unattended.py`, `test_disk_password.py`,
  `test_vm_disks.py`: configuration/fixture checks, with some Linux-only execution.
- `linux/image/Containerfile.nvidia`, `nvidia.sh`: separate NVIDIA build and kernel compatibility
  requirements; these need separate image testing.

## Reproduction matrix still required

Use only disposable image files in a dedicated VM workspace. Never pass through physical drives,
host EFI partitions, firmware variables or Windows boot configuration. Validate resolved paths
and require explicit virtual-image selection in any new harness.

| Fixture | Evidence to capture |
| --- | --- |
| Empty UEFI disk, encrypted / unencrypted | Anaconda storage plan, deployment creation, grub configuration, reboot and unlock. |
| Existing test ESP plus Windows-like partitions | Partition identifiers/hashes before and after; preservation of unrelated contents and boot entries. |
| Existing test ESP with multiple Linux loaders | Actual grub stderr and selected target; do not assume a particular loader causes failure. |
| Insufficient ESP/free space, cancelled install | Actionable failure, preserved unrelated partitions, cancellation before destructive changes. |
| Interrupted installation and recovery | State of the deployment/ESP, recovery instructions and successful second boot. |
| Secure Boot enabled / disabled | Signed shim/kernel chain and NVIDIA module acceptance; state unsupported combinations explicitly. |
| Update and rollback after install | Verified image source/digest, boot success, recovery to previous deployment. |

Preserve `/tmp/anaconda.log`, `/tmp/storage.log`, `/tmp/program.log`, installer journal, exact image
digest, bootc-image-builder/Anaconda/OSTree/GRUB versions and VM firmware configuration. Inspect the
actual stderr of grub2-mkconfig and deployment paths before proposing a bootloader change. Derive
a regression test from the reproduced cause. Review Fedora/Anaconda/bootc primary documentation
at that point because these interfaces change. Partition preview and cancel behavior still need
interactive VM verification; static kickstart checks cannot prove them.

No disk installation, firmware, bootloader or partition command was run on the Windows host.
