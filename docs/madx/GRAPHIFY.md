# Local Graphify code navigation

This project uses [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify),
the official **`graphifyy`** Python package, pinned to **0.9.101**. It is development
tooling, not part of the desktop dependency tree or Linux image. The project wrapper
installs only into `.venv/graphify`; it does not install host system software, change
global AI configuration, register MCP servers, install Git hooks, or contact a model.

## Use from the repository root

Python 3.10+ and Git are required. Use an existing Python; do not install a new host
runtime without authorization. On Windows, `py -3` can replace `python` if available.

```text
python scripts/madx/graphify.py setup
python scripts/madx/graphify.py build
python scripts/madx/graphify.py status
python scripts/madx/graphify.py query "HermesPage"
python scripts/madx/graphify.py query "finalize-root-mount"
python scripts/madx/graphify.py explain "a node ID or exact label returned by query"
python scripts/madx/graphify.py path "first exact node ID" "second exact node ID"
```

Setup downloads the pinned package and its dependencies from PyPI. Dependency
ranges are upstream-defined; only Graphify itself is pinned. `pip check` must pass.
Build uses at most four AST workers with `--code-only`, `GRAPHIFY_BACKEND=none` and
`--no-label`; query logging is disabled. No API key or subscription is required.
No cloud or semantic documentation extraction is enabled.

Results are in ignored `graphify-out/`: `graph.json`, `GRAPH_REPORT.md`, `graph.html`
and `madx-index.json`. The HTML is a convenience view; queries work without opening
it. On large repositories the visualization groups nodes into communities. Graphify's
HTML may reference browser libraries; no source upload is part of this workflow.
Generated graphs/caches are not committed or shipped as OS assets.

`status` checks the current working-file fingerprint, including uncommitted changes
and new nonignored files. A missing/stale index returns a nonzero status; queries warn
on stale data. Rebuild after edits or switching branches. Every result must be checked
against source before editing; Graphify can infer relationships and omit unsupported
inputs (for example extensionless shell commands). Use PROJECT_MAP/`rg` as fallback.

`.graphifyignore` excludes dependencies, upstream runtime checkout, build/VM output,
evidence artifacts, environment files and common credential files. The wrapper
does not follow other worktrees or index the user's Hermes home. Do not remove those
exclusions merely to increase the node count.

## Other AI assistants

Give the assistant this repository/worktree and ask it to read `AGENTS.md`.
`CLAUDE.md` and `GEMINI.md` point to the same handoff. The instructions and Python
commands also work for other coding assistants; no special global integration is
required. No `/graphify` or `$graphify` skill has been registered by this setup.

Use Graphify for **where code lives and how symbols connect**. Use
[PROJECT_STATUS.md](PROJECT_STATUS.md) and [WORK_ITEMS.json](WORK_ITEMS.json) for
**what passed, what remains, and what to do next**. Code-only extraction intentionally
does not turn prose status claims into verified results. Keep both sources current.

## Validation

```text
python -m unittest discover -s scripts/madx/tests -p test_graphify_tooling.py
python scripts/madx/graphify.py status
```

This does not rerun OS acceptance. Native CI/image/installer evidence remains tied
to the exact source revision recorded in PROJECT_STATUS.

## Initial local run — 2026-11-03

Graphify 0.9.101 installed successfully and `pip check` passed. The initial extraction
processed **1,663 code files**, writing **20,998 nodes / 72,211 relationship records**;
the HTML grouped these into 354 communities. Those are index counts, not test counts.
HermesPage and finalize-root-mount queries returned the correct repository files;
all repository-like source paths in the graph existed, and no excluded/private or
absolute host paths appeared in source_file fields. The initial freshness check passed.

Limitations retained from that run:

- 127 non-code files (113 docs, 14 images) were intentionally skipped with no LLM extraction.
- 52 files were unclassified; 96 code files produced no symbols (including some test files).
- `apps/desktop/src/features/canvas/edit-dialogs.tsx` produced a partial-parse warning
  (eight symbols extracted). This is an index coverage warning, not proof of a TypeScript
  defect; the complete workspace TypeScript check passed on 2026-11-03. Use the
  source/compiler for that file; do not rewrite valid app code to silence the warning.
- Query results can be truncated by Graphify's token budget; prefer an exact symbol/file
  or follow up with explain rather than treating absent results as absent functionality.

Logs and query samples are local under `.venv/graphify-*.log`. A subsequent rebuild may
change counts as tooling changes. No source was uploaded to Graphify Cloud or an LLM.

The six focused wrapper/handoff checks, source-map/link checks, `npm run typecheck`,
`npm run branding:check`, `pip check` and `git diff --check` passed for this change.
The OS suites/builds were not unnecessarily repeated for documentation/developer
tooling; their exact native release results remain linked from PROJECT_STATUS.
