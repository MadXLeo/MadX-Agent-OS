// Reuse the checksums shipped in the lockfile-pinned Electron npm package, as
// Electron's own installer does. Keep binary verification without a second
// SHASUMS256.txt network request during image packaging.
const desktop = require('../package.json')
const electron = require('electron/package.json')
const bundledChecksums = require('electron/checksums.json')

if (!/^\d+\.\d+\.\d+$/.test(electron.version) || desktop.devDependencies.electron !== electron.version) {
  throw new Error('Linux packaging requires the exact pinned Electron version')
}

const checksums = Object.fromEntries(['x64', 'arm64'].map(arch => {
  const filename = `electron-v${electron.version}-linux-${arch}.zip`
  const checksum = bundledChecksums[filename]
  if (typeof checksum !== 'string' || !/^[0-9a-f]{64}$/.test(checksum)) {
    throw new Error(`Missing or invalid bundled Electron checksum: ${filename}`)
  }
  return [filename, checksum]
}))

module.exports = {
  ...desktop.build,
  electronVersion: electron.version,
  electronDownload: {
    // v26 uses this key to select ElectronGetOptions and forward checksums.
    mirrorOptions: {},
    checksums
  }
}
