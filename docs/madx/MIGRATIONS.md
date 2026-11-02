# Namespace and data migration register

This register deliberately separates product text from compatibility identifiers. Phase 1 adds
MadX aliases and identity metadata while retaining canonical systemd units, bridge tools, disk
layouts and user state. The table records original contracts and the cutover requirements.

## Phase 1 implementation update

### Primary CLI and appearance increment — 2026-11-01

`93fdc9c` adds `madx -> herald-os` to image/dev/Arch/tarball alias plans. The existing preflight
checks every destination, rejects foreign files and symlinked parents, is idempotent, and removes
only newly created links if a write fails. `madx-agent-os`, `herald-os`, existing helper names and
canonical service units remain usable. The packaged-image validator now requires the exact primary
symlink. Help/docs teach `madx`; older images retain their existing command until updated.
CLI dispatch, options and exit status are unchanged. SSH's JSON error path strips either public
or legacy diagnostic prefix, preserving the existing JSON contract (both cases tested).

`517d72f` adds optional `visualQuality` and `dockMagnification` preferences. Missing/unknown
quality means Automatic; missing magnification retains enabled behavior. Existing profile and
theme/wallpaper selections stay in place. Automatic chooses Performance for software rendering,
Balanced otherwise; Full Glass is an explicit selection, not a GPU-brand guess or FPS promise.
The added environment capability field is optional for older adapters. No storage directory,
browser partition, IPC/tool ID, plugin ID, service name, update origin or Hermes revision is moved.
Native install/update/rollback and old-profile acceptance remain required for this increment.

`linux/branding/install.py` creates relative MadX command, install/share/icon and service aliases
under an explicit root. It checks all destinations before writing, refuses existing foreign files
or symlinked parents, is idempotent, and rolls back only links it created when a write fails. It
never copies/moves settings, changes partitions, enables units or redirects an existing update
deployment. Image, development, Arch and tarball installers invoke it; old tarballs without the
helper remain supported on rollback. Symlink mutation tests still require Linux.

Native display metadata, service descriptions, icons, new-install theme and ISO metadata use MadX.
Artifact producers/consumers and registry signature scopes were changed together. Alpha tags target
edge, not stable. Both old and new IMAGE_ID values are accepted; Fedora ID/ID_LIKE remain intact.
Existing bootc deployments continue following their configured reference; there is no automatic
upstream-to-MadX registry rebase. Omarchy only rewrites exact previously generated menu rows and
recognizes both markers on removal. Historical migration recognizers remain unchanged.

The retained names and required native checks are listed in REMAINING_ISSUES.md. Installer runtime
branding and real package/upgrade/rollback validation are still open gates.

| Identifier | Current contract | Planned cutover and validation |
| --- | --- | --- |
| Product/app labels | Herald OS, Herald Office apps | Central MadX product manifest; check translated copy and packaged metadata. |
| Electron profile | `appData/Herald OS` | v1: reuse an existing legacy profile in place; fresh installs use `madx-agent-os`. Never merge Chromium databases. Explicitly set userData and sessionData before ready. |
| Hermes shell store | `$HERMES_HOME/herald-os` | Retain until shell, plugin, CLI and migrations switch together; preserve preferences, policy, audit and file undo. |
| Browser partitions | `herald-web`, `herald-viewer`, `herald-preview` | Retain persisted partitions, including cookies; no cosmetic renaming. |
| Renderer storage keys | `herald-*`, legacy Hermes keys | Keep current reader/writer and legacy-storage migration. Add versioned copy/verification only when necessary. |
| Preload and IPC | `window.heraldOS`, existing channels/types | Retain wire API. Future MadX alias may reference the same capability object; no second permissive API. |
| Runtime environment | `HERALD_OS_*`, older `HERMES_OS_*` | Electron accessor accepts `MADX_OS_*` first, then legacy aliases. Direct process/CLI/plugin consumers remain explicitly legacy until audited. |
| Hermes toolset/session source | `herald_os`, `source: herald_os` | Retain upstream integration contracts and approvals; do not masquerade as Hermes Desktop. |
| Bridge install and skill IDs | `herald-os-bridge`, `herald-*` skills | Retain enabled-plugin configuration and skill links until versioned migration can test discovery and rollback. |
| Window titles | `Herald OS · …`, Slides Audience | Match MadX and legacy titles during cutover in niri and shell identification; never change just the renderer label. |
| Desktop IDs/executables | `herald-os`, `dev.iamluke.heraldos` | Keep executable and desktop IDs during first UI increment; later migrate packaging, notifications, niri/Hyprland and macOS permissions together. |
| Linux share/install paths | `/usr/share/herald-os`, `/opt/herald-os` | Versioned install migration, old command aliases and atomic rollback required. |
| User session config | `~/.config/herald-os`, niri include files | Preserve customized settings; backup/merge only managed entries and do not overwrite overrides. |
| systemd units/timers | `herald-os-*` | Update dependencies, enablement, first boot, provisioner and recovery as one change; VM boot test first. |
| Control socket | `…/herald-os/control.sock`, launch token | Keep path and token agreement across CLI, main and bridge. Preserve socket permissions. |
| Protocols/file formats | `herald-plugin:`, `herald-model:`, Office custom XML, Canvas format | Keep persisted documents and content security policy compatible. Display name is independent. |
| bootc image detection | `IMAGE_ID=herald-os` | Change updater detection and os-release together; keep Fedora ID/ID_LIKE compatibility. |
| Registry/release artifacts | Upstream defaults and repository-derived GHCR paths | Configure verified MadX channels, signature policy and artifacts together. No upstream-to-MadX switch without rollback test. |
| Firewall zone/Plymouth | `herald-os`, theme resource paths | Update references and initramfs, test network services and splash in a VM. |
| Legal attribution | LICENSE, NOTICE, bundled third-party notices | Preserve required names/copyrights; explain fork provenance in About. Not branding defects. |

## Profile selection v1

Reuse `appData/Herald OS` if it is a real existing directory, even if a new MadX directory also
exists; this prevents an upgrade silently abandoning the user's previous settings. Otherwise use
`appData/madx-agent-os`. Reject symlink/non-directory profile candidates and propagate permission
errors instead of claiming a fresh profile. This policy performs no copy, deletion or database
merge. A later explicit profile migration needs closed applications, backup, verification and
rollback. The existing pre-Herald `Hermes OS` migration remains responsible for its older format.

Electron documents the [userData/sessionData initialization contract](https://www.electronjs.org/docs/latest/api/app/).
