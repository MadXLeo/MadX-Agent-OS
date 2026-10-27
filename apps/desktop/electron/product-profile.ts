import fs from 'node:fs'
import path from 'node:path'
import { PRODUCT } from '../shared/product.ts'

/**
 * Profile policy v1: upgrades reuse the existing profile; new installs get the MadX namespace.
 * No database copy/merge and no mutation of the previous profile. Permission errors are fatal,
 * because silently selecting a different profile would make user data appear lost.
 */
export function productProfilePath(appData: string): string {
  const legacy = path.join(appData, PRODUCT.compatibility.electronProfile)
  const current = path.join(appData, PRODUCT.slug)
  for (const candidate of [legacy, current]) {
    const stat = fs.lstatSync(candidate, { throwIfNoEntry: false })
    if (!stat) continue
    if (!stat.isDirectory() || stat.isSymbolicLink()) {
      throw new Error(`Refusing a non-directory or linked application profile: ${candidate}`)
    }
    return candidate
  }
  return current
}
