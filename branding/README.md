# Product identity

`product.json` is the source for names, version, appearance defaults and explicitly retained
compatibility identifiers. Run `npm run branding:sync` after editing it, then
`npm run branding:check`. Consumers use generated `apps/desktop/shared/product.ts`; translated
messages interpolate constants before user values, so user content is never rewritten.

The supplied `MadX Agent OS Metallic Logo.png` is preserved byte-for-byte as
`apps/desktop/src/assets/brand/madx-wordmark.png` and in the public brand folder. The desktop mark
and favicon use a viewport over its existing monogram; no substitute identity was invented.
The small favicon uses the exported monogram PNG. The compatible SVG asset embeds the original
PNG because image-mode SVG cannot load external subresources. PNG, ICO, ICNS and Plymouth exports
are checked against `assets.json`; native package rendering remains a release gate.

To regenerate artwork, run `node scripts/madx/export-icons.mjs` with Playwright and a Chromium
browser installed. Optional `MADX_PLAYWRIGHT_MODULE` and `MADX_BROWSER_CHANNEL` select an existing
authoring runtime. The exporter uses the source image and manifest viewport/clip, then writes the
asset checksums. Run `npm run branding:sync` and `npm run branding:check` afterward. The older
`scripts/make-icons.py` entry point delegates to this exporter.

`npm run branding:audit` produces a read-only triage report; `-- --json` lists every location.
`node scripts/madx/audit-branding.mjs --check` rejects unreviewed capitalized legacy product copy;
`legacy-allowlist.json` records file-specific compatibility and attribution exceptions.
Categories distinguish attribution, test fixtures, migration documentation, comments, candidate
visible copy, identifiers and assets. Identifiers are not automatically safe: some are displayed
in help/errors. This audit does not certify a complete rebrand or inspect an unbuilt native package.

Release artifacts and registry configuration now use MadX names. Legacy executable filenames,
application IDs, service units, API IDs and data paths remain compatibility contracts, with MadX
command/service aliases added by `linux/branding/install.py`. See `docs/madx/MIGRATIONS.md` for
preservation rules and `docs/madx/REMAINING_ISSUES.md` for required native/VM checks. Source copyright
in LICENSE/NOTICE is retained. New model-manager names in the manifest reserve identity only; no
unavailable feature is advertised as functioning.
