import { PRODUCT } from '../shared/product.ts'

/** Prefer MadX settings; retain both earlier prefixes for existing launch scripts. */
export function osEnv(name: string, env: NodeJS.ProcessEnv = process.env): string | undefined {
  for (const prefix of PRODUCT.compatibility.environmentPrefixes) {
    const value = env[`${prefix}${name}`]
    if (value !== undefined) return value
  }
  return undefined
}
