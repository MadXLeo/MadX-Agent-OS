"""Parse Linux sources without executing installers; verify packaging inputs agree."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--bash", default=shutil.which("bash"))
args = parser.parse_args()
if not args.bash:
    parser.error("bash is required for syntax checks; no scripts will be executed")

files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
counts = {"python": 0, "bash": 0, "toml": 0}
for name in sorted(set(files)):
    path = ROOT / name
    if not name or not path.is_file() or not name.startswith(("linux/", "packaging/", "scripts/", "plugins/")):
        continue
    if path.suffix in (".png", ".jpg", ".webp", ".ico", ".icns"):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError:
        continue
    if path.suffix == ".py" or text.startswith("#!/usr/bin/env python"):
        ast.parse(text, filename=name)
        counts["python"] += 1
    elif path.suffix in (".sh", ".install") or path.name == "PKGBUILD" or text.startswith("#!/usr/bin/env bash"):
        subprocess.run([args.bash, "-n"], input=text, text=True, encoding="utf-8", check=True)
        counts["bash"] += 1
    elif path.suffix == ".toml":
        tomllib.loads(text)
        counts["toml"] += 1

product = json.loads((ROOT / "branding/product.json").read_text(encoding="utf-8"))
helper = (ROOT / "packaging/arch/herald-os-bin/herald-os-package.sh").read_bytes()
assert helper == (ROOT / "packaging/arch/herald-os-git/herald-os-package.sh").read_bytes()
digest = hashlib.sha256(helper).hexdigest()
for kind in ("bin", "git"):
    recipe = (ROOT / f"packaging/arch/herald-os-{kind}/PKGBUILD").read_text(encoding="utf-8")
    assert digest in recipe, f"{kind} helper checksum is stale"
    assert f"pkgname={product['slug']}-{kind}" in recipe
    assert "'herald-os'" in recipe, "legacy package capability must remain provided"
for filename in ("linux/image/packages.sh", "linux/bin/herald-os-gpu-check"):
    assert product["distribution"]["nvidiaImage"] in (ROOT / filename).read_text(encoding="utf-8")
assert product["repository"] in (ROOT / "linux/image/Containerfile").read_text(encoding="utf-8")
print(f"Native source checks passed: {counts}; package names, helper checksums and registry references agree.")
