import { describe, expect, it } from 'vitest'
import { osEnv } from './env.ts'

describe('osEnv', () => {
  it('prefers MadX over both legacy prefixes', () => {
    expect(osEnv('SHELL_MODE', { MADX_OS_SHELL_MODE: 'panels', HERALD_OS_SHELL_MODE: 'desktop', HERMES_OS_SHELL_MODE: 'desktop' })).toBe('panels')
  })

  it('honours an explicit empty MadX value without reviving a legacy value', () => {
    expect(osEnv('DEV_SERVER', { MADX_OS_DEV_SERVER: '', HERALD_OS_DEV_SERVER: 'http://localhost:5180' })).toBe('')
  })

  it('reads the HERALD_OS_ name', () => {
    expect(osEnv('WINDOWED', { HERALD_OS_WINDOWED: '1' })).toBe('1')
  })

  it('falls back to the pre-rename HERMES_OS_ name', () => {
    expect(osEnv('ZOOM', { HERMES_OS_ZOOM: '1.5' })).toBe('1.5')
  })

  it('prefers the new name when both are set', () => {
    expect(osEnv('SHELL_MODE', { HERALD_OS_SHELL_MODE: 'panels', HERMES_OS_SHELL_MODE: 'desktop' })).toBe('panels')
  })

  it('is undefined when neither is set', () => {
    expect(osEnv('KIOSK', {})).toBeUndefined()
  })
})
