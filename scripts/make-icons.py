"""Compatibility entry point for the MadX artwork exporter (Node + Playwright)."""
import subprocess
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(subprocess.call(["node", str(root / "scripts/madx/export-icons.mjs")], cwd=root))
