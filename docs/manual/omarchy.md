# Running inside Omarchy

On [Omarchy](https://omarchy.org), MadX Agent OS runs as an app inside Omarchy's own desktop: Omarchy
keeps its bar, keys and window rules, and MadX Agent OS follows its theme.

## Setting it up

Install the Arch package, then let MadX Agent OS fit itself into Omarchy:

```bash
git clone https://github.com/MadXLeo/MadX-Agent-OS.git
cd MadX-Agent-OS/packaging/arch/herald-os-bin && makepkg -si
herald-os setup              # once: Hermes Agent and MadX's system tools
herald-os omarchy install
```

`herald-os omarchy status` shows what is in place, and `herald-os omarchy remove` takes it all out
again. It works with Omarchy 4 and Omarchy 3, and never overwrites a file of yours: when one is in
the way, it prints the line to add instead.

## What you get

- **The theme:** when you change Omarchy's theme, MadX Agent OS takes its colours and background.
- **The menu:** on Omarchy 4, a MadX Agent OS row on the Omarchy menu. On Omarchy 3, MadX Agent OS is in
  Applications.
- **Keys**, none of them taken by Omarchy:

| Action | Omarchy 4 | Omarchy 3 |
| --- | --- | --- |
| Open MadX Agent OS | `Super+Alt+H` | `Super+Alt+H`, then Return |
| Ask Hermes about this window | `Super+Alt+A` | `Super+Alt+H`, then A |
| The command bar | `Super+Alt+C` | `Super+Alt+H`, then C |
| Talk to Hermes | `Super+Alt+V` | `Super+Alt+H`, then V |
| Dictate into the focused app | `Super+Alt+X` | `Super+Alt+H`, then X |
| Emoji | `Super+Alt+E` | `Super+Alt+H`, then E |
| Missions | `Super+Alt+M` | `Super+Alt+H`, then M |

- **Updates:** `herald-os update` updates MadX Agent OS and Hermes, and leaves the system to
  `omarchy-update`. Apps from Settings > Software install through Omarchy's own package tools.
- **Fingerprint and security keys:** `herald-os setup fingerprint` and `herald-os setup fido2` run
  Omarchy's own setup for them.

## Sharing Hermes with Hermes Desktop

Omarchy's Hermes Desktop and MadX Agent OS can share one Hermes home (`~/.hermes`): the same memories,
conversations, sign-in and connections. Running both is safe; Settings > Network says when another
app's messaging gateway is running. To have MadX Agent OS use the Hermes that Hermes Desktop started
instead of starting its own, see [docs/LINUX.md](../LINUX.md#inside-hyprland-and-omarchy-app-mode).

## How it differs from Hermes on Omarchy

On its own, Omarchy offers Hermes as one of its coding agents, started in a terminal in a mode that
does not stop to ask. MadX Agent OS is a whole desktop around Hermes that asks before it changes
anything; see the [FAQ](faq.md).

## Status

This has been tested against Omarchy 4's own configuration, theme scripts and menu, including real
key presses under Hyprland, but not yet on an Omarchy machine.
[Reports](https://github.com/MadXLeo/MadX-Agent-OS/issues) are welcome.
