/** Public appearance preference; absence in an older profile means Automatic. */
export type VisualQuality = 'auto' | 'full' | 'balanced' | 'performance'
export type RenderCapability = 'accelerated' | 'software' | 'unknown'

export function normalizeVisualQuality(value: unknown): VisualQuality {
  return value === 'full' || value === 'balanced' || value === 'performance' ? value : 'auto'
}

/** Chromium feature status, never a GPU vendor/name guess. Unknown is not evidence of acceleration. */
export function renderingCapability(status: { gpu_compositing?: string; webgl?: string }): RenderCapability {
  const features = [status.gpu_compositing, status.webgl]
  if (features.some(value => value && /disabled|unavailable|software/.test(value))) return 'software'
  if (features.every(value => value === 'enabled' || value === 'enabled_on')) return 'accelerated'
  return 'unknown'
}

export function effectiveVisualQuality(preference: unknown, capability: RenderCapability = 'unknown'): Exclude<VisualQuality, 'auto'> {
  const setting = normalizeVisualQuality(preference)
  if (setting !== 'auto') return setting
  // Acceleration alone is not a performance benchmark. Full Glass is an explicit choice.
  return capability === 'software' ? 'performance' : 'balanced'
}
