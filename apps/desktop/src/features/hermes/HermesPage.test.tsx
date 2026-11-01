// @vitest-environment happy-dom
import { act } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import { afterEach, expect, it, vi } from 'vitest'
import { $prefs } from '../../store/backend.ts'
import { $connection } from '../../store/gateway.ts'
import { HermesPage } from './HermesPage.tsx'

vi.hoisted(() => { Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true }) })
// Child editors have their own coverage. Here an uncontrolled input detects a destructive remount.
vi.mock('./Conversation.tsx', () => ({ Conversation: () => <textarea aria-label="Conversation draft" defaultValue="Draft to keep" /> }))
vi.mock('./ArtifactPane.tsx', () => ({ ArtifactPane: () => <textarea aria-label="Artifact draft" defaultValue="Unsaved output" /> }))
vi.mock('./BotPicker.tsx', () => ({ NewConversationButton: ({ disabled }: { disabled: boolean }) => <button disabled={disabled}>New conversation</button> }))
vi.mock('../chat/SessionList.tsx', () => ({ SessionList: () => <aside>Saved conversations</aside> }))
let root: Root
let host: HTMLDivElement
afterEach(() => { act(() => root?.unmount()); host?.remove() })

async function show() {
  $prefs.set({ ...$prefs.get(), language: 'en' })
  $connection.set('closed')
  host = document.createElement('div')
  document.body.append(host)
  root = createRoot(host)
  await act(async () => root.render(<HermesPage />))
}
const button = (name: string) => [...host.querySelectorAll('button')].find(item => item.textContent === name)!

it('keeps conversation and unsaved artifact editors mounted across output toggles', async () => {
  await show()
  const conversation = host.querySelector('textarea[aria-label="Conversation draft"]')!
  const artifact = host.querySelector('textarea[aria-label="Artifact draft"]')!
  const output = host.querySelector<HTMLElement>('#madx-hermes-output')!
  expect(output.hidden).toBe(true)
  await act(async () => button('Show output').click())
  expect(output.hidden).toBe(false)
  expect(button('Hide output').getAttribute('aria-expanded')).toBe('true')
  await act(async () => button('Hide output').click())
  expect(output.hidden).toBe(true)
  expect(host.querySelector('textarea[aria-label="Conversation draft"]')).toBe(conversation)
  expect(host.querySelector('textarea[aria-label="Artifact draft"]')).toBe(artifact)
})

it('keeps history available and reports the real offline state', async () => {
  await show()
  expect(host.querySelector('[role="status"]')?.textContent).toBe('Hermes Agent is unavailable')
  expect(button('New conversation').disabled).toBe(true)
  await act(async () => button('History').click())
  expect(host.querySelector('[role="dialog"]')?.textContent).toContain('Saved conversations')
  await act(async () => host.querySelector<HTMLButtonElement>('[aria-label="Close sessions"]')!.click())
  expect(host.querySelector('[role="dialog"]')).toBeNull()
})
