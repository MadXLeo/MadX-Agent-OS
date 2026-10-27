import { PRODUCT } from '../../../shared/product.ts'
import { useLayoutEffect, useRef } from 'react'
import type { ShellCommand, WmWindow } from '../../../shared/ipc.ts'
import type { FloatingAppId } from '../apps.ts'
import { onShellCommand } from '../../store/shell.ts'

/**
 * Subscribe to inbound `ShellCommand`s for the lifetime of a component. Registered in a layout
 * effect so commands queued before the (lazy) surface mounted are replayed before the first paint.
 */
export function useShellCommands(handler: (command: ShellCommand) => void): void {
  const latest = useRef(handler)
  latest.current = handler

  useLayoutEffect(() => onShellCommand(command => latest.current(command)), [])
}

/** Window titles main gives our own floating windows (see electron/shell/mode.ts); they double as identity. */
const OUR_FLOATING_TITLES: Record<string, FloatingAppId> = {
  [`${PRODUCT.name} · Terminal`]: 'terminal',
  [`${PRODUCT.name} · System`]: 'system',
  [`${PRODUCT.name} · Chat`]: 'chat-popout',
  [`${PRODUCT.name} · Studio`]: 'studio',
  [`${PRODUCT.name} · Canvas`]: 'canvas',
  [`${PRODUCT.name} · Docs`]: 'docs',
  [`${PRODUCT.name} · Sheets`]: 'sheets',
  [`${PRODUCT.name} · Slides`]: 'slides',
  [`${PRODUCT.name} · Pet Room`]: 'room',
  [`${PRODUCT.name} · Calc`]: 'calc'
}

export const OUR_MAIN_TITLE = PRODUCT.name

/** Which floating Hermes app one of our compositor windows hosts, when it is one. */
export function ourFloatingAppId(win: WmWindow): FloatingAppId | null {
  const title = win.title.startsWith(`${PRODUCT.compatibility.electronProfile} · `)
    ? PRODUCT.name + win.title.slice(PRODUCT.compatibility.electronProfile.length)
    : win.title
  return win.ours ? (OUR_FLOATING_TITLES[title] ?? null) : null
}

/** A short human label for a compositor window: its title, else its app id. */
export function windowLabel(win: WmWindow): string {
  return win.title.trim() || win.appId || 'Window'
}

/** The line prepended to a prompt when it was asked about a specific window. */
export function contextLine(context: WmWindow): string {
  return `Context: the focused window is "${windowLabel(context)}" (${context.appId || 'unknown app'}).`
}

/** The prompt text for a question asked about a window; its attachments travel with sendPrompt. */
export function composePrompt(text: string, context?: WmWindow | null): string {
  const parts: string[] = []

  if (context) {
    parts.push(contextLine(context))
  }

  const body = text.trim()

  if (body) {
    parts.push(body)
  }

  return parts.join('\n')
}
