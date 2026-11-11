#!/usr/bin/env bash
# Build-time only. Install the reviewed Hermes revision into the immutable OS;
# user profiles, credentials, memory and plugins continue to live in HERMES_HOME.
set -euo pipefail
lock="${1:?upstream lock required}"
runtime=/usr/lib/hermes-agent
repo="$(sed -n 's/^repo=//p' "$lock" | tr -d '[:space:]')"
sha="$(sed -n 's/^sha=//p' "$lock" | tr -d '[:space:]')"
[[ "$repo" == NousResearch/hermes-agent && "$sha" =~ ^[0-9a-f]{40}$ ]] || exit 1
[[ ! -e "$runtime" ]] || { echo 'Refusing to replace an existing runtime' >&2; exit 1; }

# Fedora's default Python is newer than this Hermes revision supports. The
# pinned wake extra's tflite-runtime wheel requires Python 3.11 on Linux.
dnf -y install --setopt=install_weak_deps=False python3.11 uv portaudio vulkan-loader libgomp
git init "$runtime"
git -C "$runtime" fetch --depth=1 "https://github.com/$repo.git" "$sha"
git -C "$runtime" checkout --detach FETCH_HEAD
[[ "$(git -C "$runtime" rev-parse HEAD)" == "$sha" ]]
printf '%s\n' "$sha" >"$runtime/.herald-os-upstream-sha"
rm -rf "$runtime/.git"
cd "$runtime"
# Use the upstream lock, including its integrity hashes. Never resolve a fresh
# main branch or silently fall back to an unlocked pip install.
export UV_PROJECT_ENVIRONMENT="$runtime/venv" UV_PYTHON_DOWNLOADS=never
# Keep the cache in the build staging tree that the Containerfile removes.
export UV_CACHE_DIR=/tmp/herald-os/uv-cache
sync_args=(--locked --no-dev --python /usr/bin/python3.11
  --extra all --extra anthropic --extra exa --extra firecrawl --extra parallel-web
  --extra edge-tts --extra voice --extra wake --extra messaging)
uv sync "${sync_args[@]}"
# Reconcile against the same lock without network, respecting upstream's explicit
# security overrides (plain pip check does not understand those overrides).
uv sync --offline "${sync_args[@]}"
uv pip freeze --python "$runtime/venv/bin/python" >"$runtime/dependencies.txt"
python3 - "$sha" <<'PY'
import hashlib, json, sys
from pathlib import Path
p = Path('/usr/lib/hermes-agent')
(p / 'madx-bundle.json').write_text(json.dumps({
    'repository': 'NousResearch/hermes-agent', 'revision': sys.argv[1],
    'lockSha256': hashlib.sha256((p / 'uv.lock').read_bytes()).hexdigest(),
    'python': '/usr/bin/python3.11',
    'extras': ['all', 'anthropic', 'exa', 'firecrawl', 'parallel-web', 'edge-tts', 'voice', 'wake', 'messaging'],
    'modelWeightsBundled': True, 'automaticDependencyDownloads': False,
}, indent=2) + '\n')
PY
install -m0755 /tmp/herald-os/linux/image/hermes-bundled /usr/bin/hermes
install -Dm0644 "$runtime/madx-bundle.json" /usr/share/herald-os/hermes-bundled.json
model=/usr/share/madx-model
install -Dm0644 /tmp/herald-os/linux/image/offline-model.json "$model/model.json"
install -m0644 /tmp/herald-os/linux/image/licenses/Apache-2.0.txt "$model/LICENSE"
python3 - "$model" <<'PY'
import hashlib, json, pathlib, shutil, sys, urllib.request
p = pathlib.Path(sys.argv[1])
m = json.loads((p / 'model.json').read_text())
base = f"https://huggingface.co/{m['repository']}/resolve/{m['revision']}/"
for name, url in ((m['file'], base + m['file']), ('README.md', m['modelCard'])):
    with urllib.request.urlopen(url, timeout=120) as src, (p / name).open('wb') as dest:
        shutil.copyfileobj(src, dest, 1024 * 1024)
weights = p / m['file']
with weights.open('rb') as f:
    if weights.stat().st_size != m['bytes'] or hashlib.file_digest(f, 'sha256').hexdigest() != m['sha256']:
        raise SystemExit('model size or digest does not match offline-model.json')
PY
install -m0755 /tmp/herald-os/linux/image/madx-local-model /usr/bin/madx-local-model
install -Dm0644 /tmp/herald-os/linux/image/madx-local-model.service /usr/lib/systemd/user/madx-local-model.service
/usr/libexec/madx-model/llama-server --version
chmod -R go-w "$runtime"
