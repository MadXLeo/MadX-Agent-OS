import { describe, expect, it } from 'vitest'
import { isSlidesPresentation } from './product-windows.ts'

describe('presentation privacy across the identity migration', () => {
  it.each(['MadX Slides Audience', 'Herald Slides Audience'])('recognizes %s', title => {
    expect(isSlidesPresentation({ title })).toBe(true)
  })
  it.each(['MadX Agent OS · Slides', 'Herald OS · Slides'])('requires fullscreen for %s', title => {
    expect(isSlidesPresentation({ title, fullscreen: true })).toBe(true)
    expect(isSlidesPresentation({ title, fullscreen: false })).toBe(false)
  })
  it('does not confuse unrelated fullscreen windows with a presentation', () => {
    expect(isSlidesPresentation({ title: 'Browser', fullscreen: true })).toBe(false)
  })
})
