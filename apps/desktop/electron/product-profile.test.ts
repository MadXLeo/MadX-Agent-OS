import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { PRODUCT } from '../shared/product.ts'
import { productProfilePath } from './product-profile.ts'

describe('product profile compatibility', () => {
  let root: string
  beforeEach(() => { root = fs.mkdtempSync(path.join(os.tmpdir(), 'madx-profile-')) })
  afterEach(() => { fs.rmSync(root, { recursive: true, force: true }) })

  it('uses a MadX path on a new installation without creating it during selection', () => {
    expect(productProfilePath(root)).toBe(path.join(root, PRODUCT.slug))
    expect(fs.readdirSync(root)).toEqual([])
  })

  it('preserves existing cookies and storage in place, even when a new profile exists', () => {
    const legacy = path.join(root, PRODUCT.compatibility.electronProfile)
    fs.mkdirSync(legacy)
    fs.mkdirSync(path.join(root, PRODUCT.slug))
    fs.writeFileSync(path.join(legacy, 'Cookies'), 'existing-database')
    expect(productProfilePath(root)).toBe(legacy)
    expect(productProfilePath(root)).toBe(legacy)
    expect(fs.readFileSync(path.join(legacy, 'Cookies'), 'utf8')).toBe('existing-database')
  })

  it('reuses an existing MadX profile when there is no legacy profile', () => {
    const current = path.join(root, PRODUCT.slug)
    fs.mkdirSync(current)
    expect(productProfilePath(root)).toBe(current)
  })

  it('refuses a file in place of the legacy profile instead of silently starting fresh', () => {
    fs.writeFileSync(path.join(root, PRODUCT.compatibility.electronProfile), 'not-a-directory')
    expect(() => productProfilePath(root)).toThrow('Refusing')
  })

  it('refuses profile links (junctions on Windows) rather than following them', () => {
    const target = path.join(root, 'external')
    fs.mkdirSync(target)
    fs.symlinkSync(target, path.join(root, PRODUCT.compatibility.electronProfile), process.platform === 'win32' ? 'junction' : 'dir')
    expect(() => productProfilePath(root)).toThrow('Refusing')
    expect(fs.existsSync(target)).toBe(true)
  })
})
