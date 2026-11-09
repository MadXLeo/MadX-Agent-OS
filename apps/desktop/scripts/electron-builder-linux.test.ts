import { createHash } from 'node:crypto'
import fs from 'node:fs/promises'
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import os from 'node:os'
import path from 'node:path'
import { runInNewContext } from 'node:vm'
import { afterEach, describe, expect, it, vi } from 'vitest'

const require = createRequire(import.meta.url)
const config = require('./electron-builder-linux.cjs')
const desktop = require('../package.json')
const electron = require('electron/package.json')
const bundled = require('electron/checksums.json')
const builderRequire = createRequire(require.resolve('app-builder-lib/package.json'))
const get = builderRequire('@electron/get')
const realDownload = get.downloadArtifact
const { downloadElectronArtifactZip } = builderRequire('./out/util/electronGet.js')
const roots: string[] = []

async function cache() {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'madx-electron-checksums-'))
  roots.push(root)
  return root
}

afterEach(async () => {
  vi.restoreAllMocks()
  for (const root of roots.splice(0)) {
    // Only remove directories created by this test beneath the OS temp directory.
    expect(path.dirname(path.resolve(root))).toBe(path.resolve(os.tmpdir()))
    expect(path.basename(root)).toMatch(/^madx-electron-checksums-/)
    await fs.rm(root, { recursive: true, force: true })
  }
})

describe('Linux Electron packaging checksums', () => {
  it('loads with the real builder schema and preserves existing packaging and security settings', async () => {
    const { validateConfiguration } = builderRequire('./out/util/config/config.js')
    const { DebugLogger } = builderRequire('builder-util')
    await validateConfiguration(config, new DebugLogger())
    const { electronDownload, electronVersion, ...packaging } = config
    expect(packaging).toEqual(desktop.build)
    expect(electronVersion).toBe(desktop.devDependencies.electron)
    expect(electronDownload.mirrorOptions).toEqual({})
    expect(electronDownload.unsafelyDisableChecksums).toBeUndefined()
    expect(desktop.scripts['dist:linux']).toContain('--config scripts/electron-builder-linux.cjs --linux --publish never')
    for (const arch of ['x64', 'arm64']) {
      const name = `electron-v${electronVersion}-linux-${arch}.zip`
      expect(electronDownload.checksums[name]).toBe(bundled[name])
    }
  })

  it('reproduces the extra checksum request and HTTP failure without inline checksums', async () => {
    const requested: string[] = []
    const downloader = { download: async (url: string, destination: string) => {
      requested.push(url)
      if (url.endsWith('/SHASUMS256.txt')) throw new Error('HTTP 504 at checksum endpoint')
      await fs.writeFile(destination, 'fixture Electron bytes')
    } }
    await expect(realDownload({ version: electron.version, artifactName: 'electron', platform: 'linux', arch: 'x64', cacheRoot: await cache(), downloader })).rejects.toThrow('HTTP 504 at checksum endpoint')
    expect(requested.map(url => new URL(url).pathname)).toEqual([
      `/electron/electron/releases/download/v${electron.version}/electron-v${electron.version}-linux-x64.zip`,
      `/electron/electron/releases/download/v${electron.version}/SHASUMS256.txt`
    ])
  })

  it.each(['x64', 'arm64'])('the real builder forwards %s checksums and needs no checksum network request', async arch => {
    const bytes = Buffer.from(`fixture Electron ${arch}`)
    const filename = `electron-v${electron.version}-linux-${arch}.zip`
    const requested: string[] = []
    vi.spyOn(get, 'downloadArtifact').mockImplementation((options: object) => realDownload({
      ...options,
      downloader: { download: async (url: string, destination: string) => {
        requested.push(url)
        if (!url.endsWith('/' + filename)) throw new Error('Unexpected network request: ' + new URL(url).pathname)
        await fs.writeFile(destination, bytes)
      } }
    }))
    const downloaded = await downloadElectronArtifactZip({
      version: electron.version, artifactName: 'electron', platformName: 'linux', arch, cacheDir: await cache(),
      electronDownload: { ...config.electronDownload, checksums: { [filename]: createHash('sha256').update(bytes).digest('hex') } }
    })
    expect(await fs.readFile(downloaded)).toEqual(bytes)
    expect(requested).toHaveLength(1)
  })

  it('the real builder rejects corrupted bytes rather than bypassing verification or falling back online', async () => {
    const filename = `electron-v${electron.version}-linux-x64.zip`
    const requested: string[] = []
    vi.spyOn(get, 'downloadArtifact').mockImplementation((options: object) => realDownload({
      ...options,
      downloader: { download: async (url: string, destination: string) => {
        requested.push(url)
        await fs.writeFile(destination, 'corrupted bytes')
      } }
    }))
    await expect(downloadElectronArtifactZip({
      version: electron.version, artifactName: 'electron', platformName: 'linux', arch: 'x64', cacheDir: await cache(),
      electronDownload: config.electronDownload
    })).rejects.toThrow(/checksum/i)
    expect(requested).toHaveLength(1)
    expect(requested[0]).toMatch(new RegExp(filename.replaceAll('.', '\\.') + '$'))
  })

  it.each(['version', 'x64', 'arm64'])('rejects a mismatched version or missing %s checksum', invalid => {
    const source = readFileSync(new URL('./electron-builder-linux.cjs', import.meta.url), 'utf8')
    const checksums = { ...bundled }
    if (invalid !== 'version') delete checksums[`electron-v${electron.version}-linux-${invalid}.zip`]
    const modules: Record<string, unknown> = {
      '../package.json': desktop,
      'electron/package.json': invalid === 'version' ? { version: '0.0.0' } : electron,
      'electron/checksums.json': checksums
    }
    expect(() => runInNewContext(source, { module: { exports: {} }, require: (name: string) => modules[name] })).toThrow(/pinned Electron|checksum/)
  })
})
