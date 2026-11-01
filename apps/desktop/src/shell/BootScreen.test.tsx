// @vitest-environment happy-dom
import { act } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import { afterEach, expect, it, vi } from 'vitest'
import type { BackendState } from '../../shared/ipc.ts'
import { $backend, $prefs } from '../store/backend.ts'
import { BootScreen } from './BootScreen.tsx'

vi.mock('../features/status/StatusPanel.tsx', () => ({ StatusPanel: () => <div>Network controls</div> }))
vi.hoisted(() => { Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true }) })
let root: Root
let host: HTMLDivElement
afterEach(() => { act(() => root?.unmount()); host?.remove(); vi.restoreAllMocks() })

async function show(state: BackendState) {
  $prefs.set({ ...$prefs.get(), language: 'en' })
  $backend.set(state)
  host = document.createElement('div')
  document.body.append(host)
  root = createRoot(host)
  await act(async () => root.render(<><main>Local desktop</main><BootScreen state={state} /></>))
}

it.each(['waiting', 'failed'] as const)('allows local desktop access during %s without marking Hermes ready', async phase => {
  const state: BackendState = { phase, attempt: 0, error: 'Runtime unavailable', logTail: [] }
  await show(state)
  expect(host.textContent).toContain('Runtime unavailable')
  const proceed = [...host.querySelectorAll('button')].find(button => button.textContent === 'Continue to desktop')!
  expect(proceed).toBeDefined()
  await act(async () => proceed.click())
  expect(host.textContent).toBe('Local desktop')
  expect($backend.get()).toEqual(state)
})

it('retains failed-start retry and diagnostic controls before continuing', async () => {
  const restart = vi.fn().mockResolvedValue(undefined)
  Object.assign(window, { heraldOS: { backend: { restart } } })
  await show({ phase: 'failed', attempt: 1, error: 'Runtime unavailable', logTail: ['diagnostic line'] })
  const button = (name: string) => [...host.querySelectorAll('button')].find(item => item.textContent === name)!
  await act(async () => button('Show log').click())
  expect(host.querySelector('pre')?.textContent).toBe('diagnostic line')
  await act(async () => button('Try again').click())
  expect(restart).toHaveBeenCalledOnce()
  expect($backend.get().phase).toBe('failed')
})
