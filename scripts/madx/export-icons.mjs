// Deterministic raster exports of the existing SVG viewport; never redraws the supplied artwork.
// Optional authoring tool: set MADX_PLAYWRIGHT_MODULE to an installed Playwright module directory.
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'

const require = createRequire(import.meta.url)
const { chromium } = require(process.env.MADX_PLAYWRIGHT_MODULE || 'playwright')
const root = fileURLToPath(new URL('../../', import.meta.url))
const product = JSON.parse(fs.readFileSync(path.join(root, 'branding/product.json'), 'utf8'))
const source = fs.readFileSync(path.join(root, 'apps/desktop/src/assets/brand/madx-wordmark.png'))
const image = `data:image/png;base64,${source.toString('base64')}`
const outputs = new Map()
const pngs = new Map()
const browser = await chromium.launch({ headless: true, ...(process.env.MADX_BROWSER_CHANNEL ? { channel: process.env.MADX_BROWSER_CHANNEL } : {}) })
try {
  const page = await browser.newPage({ deviceScaleFactor: 1 })
  for (const size of [16, 32, 64, 128, 256, 512, 1024]) {
    await page.setViewportSize({ width: size, height: size })
    await page.setContent(`<style>html,body{margin:0;background:transparent}</style><svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="${product.assets.monogramViewBox}"><defs><clipPath id="mark"><path d="${product.assets.monogramClip}"/></clipPath></defs><image clip-path="url(#mark)" href="${image}" width="2172" height="724"/></svg>`)
    await page.locator('svg').waitFor()
    pngs.set(size, await page.screenshot({ omitBackground: true }))
  }
  await page.setViewportSize({ width: 600, height: 200 })
  await page.setContent(`<style>html,body{margin:0;background:transparent}img{width:600px;height:200px}</style><img src="${image}">`)
  await page.locator('img').evaluate(img => img.decode())
  const splash = await page.screenshot({ omitBackground: true })
  outputs.set('linux/plymouth/herald-os/logo.png', splash)
} finally { await browser.close() }

outputs.set('apps/desktop/build/icon.png', pngs.get(1024))
outputs.set('apps/desktop/public/brand/herald-icon.png', pngs.get(256))
outputs.set('apps/desktop/public/brand/madx-icon.png', pngs.get(256))
outputs.set('apps/desktop/src/assets/brand/herald-mark.png', pngs.get(256))
// ICNS uses PNG payloads for these icon types, including retina-size icon representations.
const chunks = [...new Map([[16,'icp4'],[32,'icp5'],[64,'icp6'],[128,'ic07'],[256,'ic08'],[512,'ic09'],[1024,'ic10']])].map(([size, type]) => {
  const data = pngs.get(size), header = Buffer.alloc(8)
  header.write(type, 0, 'ascii'); header.writeUInt32BE(data.length + 8, 4)
  return Buffer.concat([header, data])
})
const icnsHeader = Buffer.alloc(8); icnsHeader.write('icns', 0, 'ascii'); icnsHeader.writeUInt32BE(8 + chunks.reduce((sum, chunk) => sum + chunk.length, 0), 4)
outputs.set('apps/desktop/build/icon.icns', Buffer.concat([icnsHeader, ...chunks]))
const sizes = [16, 32, 64, 128, 256]
const icoHeader = Buffer.alloc(6 + sizes.length * 16); icoHeader.writeUInt16LE(1, 2); icoHeader.writeUInt16LE(sizes.length, 4)
let offset = icoHeader.length
sizes.forEach((size, index) => {
  const entry = 6 + index * 16, data = pngs.get(size)
  icoHeader[entry] = icoHeader[entry + 1] = size === 256 ? 0 : size
  icoHeader.writeUInt16LE(1, entry + 4); icoHeader.writeUInt16LE(32, entry + 6)
  icoHeader.writeUInt32LE(data.length, entry + 8); icoHeader.writeUInt32LE(offset, entry + 12); offset += data.length
})
outputs.set('apps/desktop/build/icon.ico', Buffer.concat([icoHeader, ...sizes.map(size => pngs.get(size))]))
const manifest = { sourceSha256: crypto.createHash('sha256').update(source).digest('hex'), viewport: product.assets.monogramViewBox, clip: product.assets.monogramClip, files: {} }
for (const [relative, data] of outputs) {
  fs.writeFileSync(path.join(root, relative), data)
  manifest.files[relative] = crypto.createHash('sha256').update(data).digest('hex')
}
fs.writeFileSync(path.join(root, 'branding/assets.json'), JSON.stringify(manifest, null, 2) + '\n')
console.log(`Exported ${outputs.size} icon/splash resources from the supplied artwork.`)
