import { PRODUCT } from '../../shared/product.ts'
import type { ShellMode, ShellSurface } from '../../shared/ipc.ts'
import { osEnv } from '../env.ts'

/** `panels` only when the session asks for it (niri); everything else is the single-window desktop. */
export function shellMode(): ShellMode {
  return osEnv('SHELL_MODE') === 'panels' ? 'panels' : 'desktop'
}

/** Window titles double as the identity niri window rules match on; keep them stable. */
export const SURFACE_TITLE: Record<Exclude<ShellSurface, `window:${string}`>, string> = {
  desktop: PRODUCT.name,
  main: PRODUCT.name,
  menubar: `${PRODUCT.name} · Menu Bar`,
  dock: `${PRODUCT.name} · Dock`,
  command: `${PRODUCT.name} · Command`,
  panel: `${PRODUCT.name} · Panel`,
  screensaver: `${PRODUCT.name} · Screensaver`,
  wallpaper: `${PRODUCT.name} · Wallpaper`,
  emoji: `${PRODUCT.name} · Emoji`,
  pet: `${PRODUCT.name} · Pet`
}

/** The Dock's menu for a running app: a window the Dock opens and draws into (electron/shell/dock-menu.ts). */
export const DOCK_MENU_TITLE = `${PRODUCT.name} · Dock Menu`

/** Floating Hermes apps that may open as their own window in panels mode. */
export const FLOATING_APPS: Record<string, { title: string; width: number; height: number }> = {
  terminal: { title: `${PRODUCT.name} · Terminal`, width: 900, height: 560 },
  system: { title: `${PRODUCT.name} · System`, width: 980, height: 640 },
  'chat-popout': { title: `${PRODUCT.name} · Chat`, width: 520, height: 720 },
  studio: { title: `${PRODUCT.name} · Studio`, width: 1280, height: 800 },
  'capture-editor': { title: `${PRODUCT.name} · Markup`, width: 960, height: 680 },
  camera: { title: `${PRODUCT.name} · Camera`, width: 240, height: 240 },
  widget: { title: `${PRODUCT.name} · Widget`, width: 360, height: 280 },
  canvas: { title: `${PRODUCT.name} · Canvas`, width: 1320, height: 840 },
  docs: { title: `${PRODUCT.name} · Docs`, width: 1120, height: 840 },
  sheets: { title: `${PRODUCT.name} · Sheets`, width: 1280, height: 820 },
  slides: { title: `${PRODUCT.name} · Slides`, width: 1280, height: 820 },
  room: { title: `${PRODUCT.name} · Pet Room`, width: 1100, height: 720 },
  calc: { title: `${PRODUCT.name} · Calc`, width: 780, height: 560 }
}

export function surfaceTitle(surface: ShellSurface): string {
  if (surface.startsWith('window:')) {
    return FLOATING_APPS[surface.slice('window:'.length)]?.title ?? PRODUCT.name
  }

  return SURFACE_TITLE[surface as keyof typeof SURFACE_TITLE]
}

export function parseSurface(value: string | null | undefined): ShellSurface {
  if (!value) {
    return 'desktop'
  }

  if (value.startsWith('window:') || value in SURFACE_TITLE) {
    return value as ShellSurface
  }

  return 'desktop'
}
