import { expect, it } from 'vitest'
import { effectiveVisualQuality, normalizeVisualQuality, renderingCapability } from './visual-quality.ts'

it.each([undefined, null, 'ultra', {}, 2])('keeps missing or invalid appearance preferences safe: %j', value => {
  expect(normalizeVisualQuality(value)).toBe('auto')
  expect(effectiveVisualQuality(value)).toBe('balanced')
})
it('chooses performance for software rendering and a conservative mode for accelerated or unknown rendering', () => {
  expect(renderingCapability({ gpu_compositing: 'enabled', webgl: 'enabled' })).toBe('accelerated')
  expect(effectiveVisualQuality('auto', 'accelerated')).toBe('balanced')
  for (const status of ['disabled_software', 'unavailable_software', 'disabled_off', 'unavailable_off']) {
    const capability = renderingCapability({ gpu_compositing: status, webgl: 'enabled' })
    expect(capability).toBe('software')
    expect(effectiveVisualQuality('auto', capability)).toBe('performance')
  }
  expect(renderingCapability({})).toBe('unknown')
  expect(renderingCapability({ gpu_compositing: 'future-value', webgl: 'enabled' })).toBe('unknown')
})
it.each(['full', 'balanced', 'performance'] as const)('preserves a deliberate manual choice: %s', setting => {
  expect(effectiveVisualQuality(setting, 'software')).toBe(setting)
  expect(effectiveVisualQuality(setting, 'accelerated')).toBe(setting)
})
