# The `madx` command line

On MadX Agent OS Linux, everything the hotkeys and menus do is a `madx` command, so you, Hermes and
your scripts drive the system the same way. Any of them can be a key of your own (see
[Make it yours](make-it-yours.md#keyboard-shortcuts)). `madx commands` lists every command,
`madx --help` shows them grouped, and `madx debug` prints what a bug report needs.

`madx-agent-os` and the legacy `herald-os` remain compatible entry points to the same implementation.
Existing scripts, configuration folders and service identifiers continue to work. On an older
installation without `madx`, use its existing command until the updated package is installed.

## Hermes and the desktop

| Command | What it does |
| --- | --- |
| `madx ask [text]` | Ask Hermes about the focused window, or about the text |
| `madx command` | Open the command bar |
| `madx voice` | Start or end a voice conversation |
| `madx applications` | Open Applications |
| `madx page missions` | Show a page: `overview`, `hermes`, `missions`, `memory`, `files`, `automations`, `connections`, `settings` |
| `madx open terminal` | Open the Terminal, or `system` for the System monitor |
| `madx launch firefox` | Start an installed app |
| `madx menu` | Open the MadX Agent OS menu |
| `madx panel wifi` | Open a quick panel: `wifi`, `bluetooth`, `audio`, `display`, `power`, `clock` |
| `madx os <command.id> [json]` | Run any MadX Agent OS command, the same ones Hermes uses |

## Software and updates

| Command | What it does |
| --- | --- |
| `madx install <id>` | Install from the catalog; `madx catalog list` shows it |
| `madx install app <name>` | Install any Flatpak app |
| `madx install webapp <name> <url>` | Make a web app |
| `madx remove …` | The same, the other way |
| `madx windows status` | The Windows VM: `start`, `stop`, `connect`, `remove` |
| `madx update` | Update everything (`--check` only reports) |
| `madx channel [stable\|edge]` | Show or change the update channel |
| `madx rollback` | Go back to the previous version |
| `madx firmware [check\|update]` | Firmware updates |
| `madx omakase install` | Put back the apps every install starts with |

## The look

| Command | What it does |
| --- | --- |
| `madx theme set <name>` | Change the theme (`theme list` shows them) |
| `madx font set <family>` | The interface font (`--mono` for the code font) |
| `madx wallpaper <image>` | Set the wallpaper |
| `madx bar` | Show, hide and move menu-bar items, and set the clock |
| `madx branding set` | Your logo and name in About, your picture on the lock screen |
| `madx plugin list` | Widgets: `add`, `enable`, `disable`, `update`, `remove` |
| `madx keymap omarchy` | Omarchy's copy and paste keys (`keymap herald` switches back) |

## Everyday

| Command | What it does |
| --- | --- |
| `madx capture screenshot` | Screenshots, recording, colours, QR codes and text ([Screenshots, recording, text and QR codes](capture.md)) |
| `madx clipboard` | Clipboard history |
| `madx dictate`, `madx emoji` | Dictation and the emoji picker |
| `madx reminder 20m stretch` | A reminder (`reminder list`, `reminder clear`) |
| `madx notify <title> [body]` | Show a notification |
| `madx weather` | The weather (`weather location --set <city>`) |
| `madx toggle dnd` | Switch `nightlight`, `dnd`, `idle` (stay awake) or `screensaver` |
| `madx restart wifi` | Restart `wifi`, `bluetooth`, `sound` or the `touchpad` when it stopped working; the touchpad asks for your password |
| `madx idle show` | The idle timings, in seconds (`idle set lock=10` takes minutes) |
| `madx crash list` | Recent crashes (`crash diagnose`, `crash mute`) |
| `madx hook list` | Scripts that run when something happens |
| `madx event <name>` | Report an event, so hooks and event automations run |

## The system

| Command | What it does |
| --- | --- |
| `madx lock` | Lock the screen |
| `madx password` | Set your password |
| `madx password --disk` | Change the disk password asked for at start-up (it asks for the current one first; `--new-owner` also removes every other key) |
| `madx suspend`, `madx power` | Sleep now, or open the power menu |
| `madx setup` | Once per account on Arch or the tarball: Hermes Agent and MadX's tools (`madx setup --undo` takes them back) |
| `madx setup fingerprint` | Fingerprint sign-in (`setup fido2` for a security key) |
| `madx setup ssh --key '<public key>'` | Turn SSH on for keys only, rate-limited per address (`--github <user>` for your GitHub keys; `--off [--end-sessions]`, `--status`); see [Security](security.md#ssh) |
| `madx reset` | Erase this computer's account and start setup again |
| `madx omarchy install` | Run MadX Agent OS inside Omarchy |
| `madx wm <action>` | A window-manager action, such as `wm toggle-overview` |
| `madx state`, `madx debug` | Diagnostics |

## In scripts

Commands that act on the desktop talk to the running MadX Agent OS over its control socket, so they need
a session to be running; system chores (install, update, reminders) work without one. The
`madx os` command takes the ids Hermes uses, for example
`madx os page.open '{"name": "missions"}'`.
