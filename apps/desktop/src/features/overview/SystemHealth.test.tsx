// @vitest-environment happy-dom
import { act } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import { afterEach, expect, it, vi } from 'vitest'
import type { SystemStats } from '../../../shared/ipc.ts'
import { SystemHealth } from './SystemHealth.tsx'

vi.hoisted(() => { Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true }) })
const sample = vi.hoisted(() => ({ value: null as SystemStats | null }))
vi.mock('../../store/system.ts', () => ({ useSystemStats: () => sample.value }))
let root: Root
let host: HTMLDivElement
afterEach(() => { act(() => root?.unmount()); host?.remove(); vi.useRealTimers(); sample.value = null })
async function show() {
  host = document.createElement('div')
  root = createRoot(host)
  await act(async () => root.render(<dl><SystemHealth /></dl>))
}
it('does not invent metrics when native readings are unavailable', async () => {
  await show()
  expect(host.textContent).toContain('CPU Unavailable · Memory Unavailable')
  expect(host.textContent).not.toContain('0%')
})
it('uses actual samples and expires readings if the sampler stops', async () => {
  vi.useFakeTimers()
  sample.value = { sampledAt: Date.now(), cpuPercent: 23, memoryTotal: 1000, memoryUsed: 460 } as SystemStats
  await show()
  expect(host.textContent).toContain('CPU 23% · Memory 46%')
  await act(async () => vi.advanceTimersByTime(20_000))
  expect(host.textContent).toContain('CPU Unavailable · Memory Unavailable')
})
it('rejects malformed readings', async () => {
  sample.value = { sampledAt: Date.now(), cpuPercent: NaN, memoryTotal: 0, memoryUsed: 0 } as SystemStats
  await show()
  expect(host.textContent).toContain('CPU Unavailable · Memory Unavailable')
})
