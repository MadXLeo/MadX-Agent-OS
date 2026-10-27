import { describe, expect, it } from 'vitest'
import { translate, type Language } from './i18n.ts'
import { PRODUCT } from './product.ts'
import { surfaceTitle, FLOATING_APPS } from '../electron/shell/mode.ts'
import { DOCK_MENU_TITLE, DOCK_TITLE } from '../src/shell/surfaces/dock-menu.ts'

describe('MadX identity across integration boundaries', () => {
  it('keeps menu window identity identical in main and renderer', () => {
    expect(surfaceTitle('dock')).toBe(DOCK_TITLE)
    expect(surfaceTitle('dock')).toBe(`${PRODUCT.name} · Dock`)
    expect(DOCK_MENU_TITLE).toBe(`${PRODUCT.name} · Dock Menu`)
    expect(surfaceTitle('main')).toBe(PRODUCT.name)
    for (const id of Object.keys(FLOATING_APPS)) {
      expect(surfaceTitle(`window:${id}`)).toMatch(/^MadX Agent OS · /)
    }
  })

  it.each<Language>(['en', 'pt-BR', 'zh-CN'])('brands setup/app labels in %s without touching user content', language => {
    expect(translate(language, 'app.canvas')).toBe(PRODUCT.apps.canvas)
    expect(translate(language, 'app.docs')).toBe(PRODUCT.apps.docs)
    expect(translate(language, 'permission.screen.title')).toContain(PRODUCT.name)
    expect(translate(language, 'commandBar.ask', { text: 'Open Herald OS notes' })).toContain('Open Herald OS notes')
  })
})
