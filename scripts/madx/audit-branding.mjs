// Read-only triage: a finding is never automatically declared safe just because it is lowercase.
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import ts from 'typescript'

const root = fileURLToPath(new URL('../../', import.meta.url))
const files = [...new Set(execFileSync('git', ['ls-files', '-z', '--cached', '--others', '--exclude-standard'], { cwd: root, encoding: 'utf8' }).split('\0').filter(Boolean))].sort()
const findings = []
function category(file, text, comment = false) {
  if (/^(LICENSE|NOTICE)$|build\/licenses\//.test(file)) return 'required-attribution'
  if (/\.test\.[cm]?[jt]sx?$|(?:^|\/)tests\//.test(file)) return 'test-fixture'
  if (/^docs\/madx\//.test(file)) return 'migration-documentation'
  if (comment) return 'source-comment'
  if (/\bHerald\b/.test(text)) return 'product-copy-review'
  return 'identifier-review'
}
for (const file of files) {
  const full = path.join(root, file)
  if (!fs.existsSync(full) || !fs.lstatSync(full).isFile()) continue
  if (/\.(png|icns|ico|jpe?g|webp|gif)$/i.test(file)) {
    if (/herald/i.test(file) || /build\/icon\./.test(file)) findings.push({ file, line: 0, category: 'asset-review' })
    continue
  }
  if (!/\.(tsx?|jsx?|mjs|cjs|json|md|py|sh|kdl|toml|yml|yaml|conf|desktop|service|timer|xml|svg)$/.test(file) && !/^(LICENSE|NOTICE)$|(?:^|\/)(Containerfile[^/]*|herald-[^/.]+)$/.test(file)) continue
  if (file === 'package-lock.json' || /madx-icon\.svg$/.test(file)) continue
  const source = fs.readFileSync(full, 'utf8')
  if (!/herald/i.test(source)) continue
  if (/\.[cm]?[jt]sx?$/.test(file)) {
    const ast = ts.createSourceFile(file, source, ts.ScriptTarget.Latest, true, file.endsWith('tsx') ? ts.ScriptKind.TSX : ts.ScriptKind.TS)
    const recorded = new Set()
    const visit = node => {
      if ((ts.isStringLiteralLike(node) || ts.isJsxText(node) || ts.isTemplateHead(node) || ts.isTemplateMiddle(node) || ts.isTemplateTail(node)) && /herald/i.test(node.text)) {
        const line = ast.getLineAndCharacterOfPosition(node.getStart(ast)).line + 1
        findings.push({ file, line, category: category(file, node.text) })
        recorded.add(line)
      }
      ts.forEachChild(node, visit)
    }
    visit(ast)
    source.split('\n').forEach((line, index) => {
      if (/herald/i.test(line) && !recorded.has(index + 1)) findings.push({ file, line: index + 1, category: category(file, line, /^\s*(\/\/|\/\*|\*)/.test(line)) })
    })
  } else {
    source.split('\n').forEach((line, index) => {
      if (/herald/i.test(line)) findings.push({ file, line: index + 1, category: category(file, line, /^\s*(#|\/\/)/.test(line) && !file.endsWith('.md')) })
    })
  }
}
const counts = {}
for (const finding of findings) counts[finding.category] = (counts[finding.category] ?? 0) + 1
const report = { schemaVersion: 1, scope: 'Repository source; native packages not built or inspected', status: 'review-required', counts, findings }
if (process.argv.includes('--json')) console.log(JSON.stringify(report, null, 2))
else {
  console.log('Legacy branding triage (candidates, not automatic exemptions):')
  for (const [kind, count] of Object.entries(counts).sort()) console.log(`  ${kind}: ${count}`)
  const visible = findings.filter(item => item.category === 'product-copy-review')
  console.log('\nFirst remaining product-copy locations:')
  for (const finding of visible.slice(0, 20)) console.log(`  ${finding.file}:${finding.line}`)
  console.log('\nUse --json for all locations. Compatibility and legal text require human review. Native icon/packaging and Linux branding migration remain incomplete.')
}
