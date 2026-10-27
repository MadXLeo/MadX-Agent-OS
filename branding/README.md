# Product identity

`product.json` is the source for names, version, appearance defaults and explicitly retained
compatibility identifiers. Run `npm run branding:sync` after editing it, then
`npm run branding:check`. Consumers use generated `apps/desktop/shared/product.ts`; translated
messages interpolate constants before user values, so user content is never rewritten.

The supplied `MadX Agent OS Metallic Logo.png` is preserved byte-for-byte as
`apps/desktop/src/assets/brand/madx-wordmark.png` and in the public brand folder. The desktop mark
and favicon use a viewport over its existing monogram; no substitute identity was invented.
The SVG favicon embeds the original PNG because image-mode SVG cannot load external subresources.
This is intentionally an initial integration, not a small hand-optimized vector icon. Native PNG,
ICO/ICNS and Plymouth assets still require production exports and package verification.

`npm run branding:audit` produces a read-only triage report; `-- --json` lists every location.
Categories distinguish attribution, test fixtures, migration documentation, comments, candidate
visible copy, identifiers and assets. Identifiers are not automatically safe: some are displayed
in help/errors. This audit does not certify a complete rebrand or inspect an unbuilt native package.

Executable filenames, application IDs, release artifact filenames, registries and system services
remain compatibility identifiers for this increment. The source copyright in LICENSE/NOTICE is
retained. New model-manager names in the manifest reserve identity only; no unavailable feature is
advertised as functioning.
