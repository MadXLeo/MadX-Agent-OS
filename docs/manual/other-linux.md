# Arch and other Linux

MadX Agent OS Linux, the whole system, is built and tested on Fedora. On other distributions MadX Agent OS
comes as a package or a tarball: as the full MadX Agent OS session you pick at the login screen, or as an
app inside the desktop you already use.

| You run | Install | The full session | As an app |
| --- | --- | --- | --- |
| Arch Linux | The Arch package | Yes, with niri | Yes |
| Omarchy | The Arch package, then [`herald-os omarchy install`](omarchy.md) | Yes, with niri | Yes, the usual way there |
| Another Linux | The release tarball | Yes, with niri | Yes |

The full session needs [niri](https://github.com/YaLTeR/niri) and the tools its menu bar and panels
use. As an app, MadX Agent OS works best in niri or Hyprland, where it can see and arrange windows ("ask
about this window"); GNOME and KDE are not supported yet
([#20](https://github.com/MadXLeo/MadX-Agent-OS/issues/20)).

## Arch Linux

```bash
git clone https://github.com/MadXLeo/MadX-Agent-OS.git
cd MadX-Agent-OS/packaging/arch/herald-os-bin && makepkg -si
herald-os setup        # once per account: Hermes Agent and MadX's system tools
```

The package downloads the release build for x86_64 or aarch64. It is not on the AUR yet
([#54](https://github.com/MadXLeo/MadX-Agent-OS/issues/54)). Its optional dependencies list what each
panel and feature uses.

## Another Linux: the tarball

Download `madx-agent-os-<version>-linux-x64.tar.gz` (or `-linux-arm64`) and its `.sha256` from the
[releases page](https://github.com/MadXLeo/MadX-Agent-OS/releases), then:

```bash
VERSION=0.1.0-alpha.4    # replace with the version you downloaded
sha256sum -c "madx-agent-os-$VERSION-linux-x64.tar.gz.sha256"
sudo mkdir -p /opt/herald-os
sudo tar -xzf "madx-agent-os-$VERSION-linux-x64.tar.gz" -C /opt/herald-os --strip-components=1
sudo /opt/herald-os/resources/herald-os-linux/bin/herald-os-tarball install
herald-os setup        # once per account
```

This puts the `herald-os` commands in `/usr/local/bin`, MadX Agent OS in your application menu and, if
niri is installed, on your login screen. `sudo herald-os-tarball remove` takes them out again.

## Starting it

- **The full session:** log out and pick MadX Agent OS on the login screen.
- **As an app:** run `herald-os-app`, or open MadX Agent OS from your application menu. It opens full
  screen; your desktop's own bar and keys stay as they are.

## Try it from a second account

The full session applies MadX's theme to the account that runs it: GTK apps, the foot terminal and
GNOME's colour scheme, which your usual desktop reads too. On a computer you already use, try it from
a second account first: `sudo useradd -m herald && sudo passwd herald`. Using MadX Agent OS as an app
inside your own desktop changes none of those files.

## Updating

`herald-os update` updates MadX Agent OS (a newer release for the tarball, checked against its
checksum), the system's packages, Flatpaks and Hermes. For the Arch package, run `git pull` and
`makepkg -si` again. See [Updates, channels and rollback](updates.md).

[docs/LINUX.md](../LINUX.md#arch-linux-and-omarchy) has the details of what goes where.
