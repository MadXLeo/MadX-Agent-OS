import { PRODUCT } from './product.ts'

/** Both identities can be present during an upgrade. Presentation privacy must not depend on it. */
export function isSlidesPresentation(window: { title: string; fullscreen?: boolean }): boolean {
  return [`${PRODUCT.apps.slides} Audience`, 'Herald Slides Audience'].includes(window.title) ||
    ([`${PRODUCT.name} · Slides`, 'Herald OS · Slides'].includes(window.title) && window.fullscreen === true)
}
