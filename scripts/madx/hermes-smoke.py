#!/usr/bin/env python3
"""Run the real pinned Hermes server in a temporary profile, without a model provider.

This checks process/API/bridge discovery and persistence, not LLM chat or desktop tool execution.
Run with a Python environment containing the pinned Hermes project's dependencies.
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]


def clean_environment(home: Path, token: str, ready: Path) -> dict:
    keep = {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "COMSPEC", "PATHEXT", "LANG"}
    env = {key: value for key, value in os.environ.items() if key.upper() in keep}
    env.update(HOME=str(home), USERPROFILE=str(home), HERMES_HOME=str(home),
               HERMES_DESKTOP="1", HERALD_OS="1", HERMES_PARENT_PID=str(os.getpid()),
               HERMES_DASHBOARD_SESSION_TOKEN=token, HERMES_DESKTOP_READY_FILE=str(ready),
               PYTHONUNBUFFERED="1", PYTHONUTF8="1", NO_COLOR="1", TERMINAL_CWD=str(home),
               HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9",
               NO_PROXY="127.0.0.1,localhost")
    return env


def request(port, path, token=None, body=None):
    headers = {"X-Hermes-Session-Token": token} if token else {}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, headers=headers)
    # Do not inherit the caller's proxy settings for the test's loopback requests.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=30) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as exc:
        return exc.code, None


def stop(child):
    import psutil
    # Hermes may re-exec into a supervised child. Retain only descendants of our live handle.
    try:
        descendants = psutil.Process(child.pid).children(recursive=True)
    except psutil.NoSuchProcess:
        descendants = []
    for process in reversed(descendants):
        try:
            process.terminate()
        except psutil.NoSuchProcess:
            pass
    if child.poll() is None:
        child.terminate()
        try:
            child.wait(timeout=15)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(timeout=10)
    _, alive = psutil.wait_procs(descendants, timeout=10)
    for process in alive:
        process.kill()
    psutil.wait_procs(alive, timeout=10)


def run(runtime: Path, scratch: Path) -> dict:
    pinned = next(line.split("=", 1)[1] for line in (ROOT / "upstream/UPSTREAM.lock").read_text().splitlines() if line.startswith("sha="))
    # sync-upstream.sh uses an archive in CI; do not accidentally read the parent MadX Git HEAD.
    actual = (subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD"], text=True).strip()
              if (runtime / ".git").exists() else (runtime / ".herald-os-upstream-sha").read_text().strip())
    if actual != pinned:
        raise ValueError("Hermes checkout differs from UPSTREAM.lock")
    result = {"runtimeRevision": actual, "platform": sys.platform, "checks": [], "passed": False,
              "notTested": ["model-backed chat", "model tool selection", "interactive approvals/denials",
                            "Linux host adapter execution", "native desktop recovery", "systemd service startup"]}
    scratch.mkdir(parents=True, exist_ok=True)
    # Hermes deliberately excludes any skill path containing '.venv'. Keep the throwaway profile
    # in the repository's ignored VM-build directory, while logs/reports can stay under .venv.
    profiles = ROOT / "linux/vm/build"
    profiles.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hermes-smoke-", dir=profiles, ignore_cleanup_errors=True) as temporary:
        home = Path(temporary)
        token = secrets.token_urlsafe(32)
        ready = home / "ready.json"
        env = clean_environment(home, token, ready)
        (home / "config.yaml").write_text("plugins:\n  enabled: [herald-os-bridge]\nplatform_toolsets:\n  cli: [herald_os]\nmemory:\n  provider: builtin\n", encoding="utf-8")
        shutil.copytree(ROOT / "plugins/herald-os-bridge", home / "plugins/herald-os-bridge",
                        ignore=shutil.ignore_patterns("__pycache__", "tests", ".pytest_cache"))
        seed = "from tools.memory_tool_store import MemoryStore; s=MemoryStore(); s.load_from_disk(); r=s.add('memory','MadX runtime persistence probe'); assert r.get('success'), r"
        subprocess.run([sys.executable, "-c", seed], cwd=runtime, env=env, check=True, timeout=60, capture_output=True)
        memory_file = home / "memories/MEMORY.md"
        before = memory_file.read_bytes()
        result["checks"].append("real MemoryStore write")
        for attempt in range(2):
            ready.unlink(missing_ok=True)
            log_path = scratch / f"hermes-smoke-{attempt}.log"
            with log_path.open("w", encoding="utf-8") as log:
                child = subprocess.Popen([sys.executable, "-m", "hermes_cli.main", "serve", "--host", "127.0.0.1", "--port", "0"],
                                         cwd=runtime, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
                try:
                    deadline = time.monotonic() + 180
                    port = None
                    while time.monotonic() < deadline and child.poll() is None:
                        try:
                            port = json.loads(ready.read_text())["port"]
                            if request(port, "/api/status", token)[0] == 200:
                                break
                        except (OSError, ValueError, KeyError):
                            pass
                        time.sleep(1)
                    else:
                        raise RuntimeError(f"Hermes did not become healthy; inspect {log_path.name}")
                    assert request(port, "/api/memory")[0] == 401, "protected API accepted no token"
                    assert request(port, "/api/memory", "invalid-token")[0] == 401, "protected API accepted wrong token"
                    status, memory = request(port, "/api/memory", token)
                    assert status == 200 and memory["builtin_files"]["memory"] == len(before), f"memory API: HTTP {status}; expected {len(before)} bytes, got {memory}"
                    assert memory_file.read_bytes() == before, "restart changed stored memory"
                    status, toolsets = request(port, "/api/tools/toolsets", token)
                    assert status == 200 and any(row["name"] == "herald_os" and "system_info" in row["tools"] for row in toolsets), "bridge tools not registered"
                    if attempt == 0:
                        status, _ = request(port, "/api/skills", token, {"name": "madx-runtime-probe", "content": "---\nname: madx-runtime-probe\ndescription: Isolated runtime probe\n---\nRead-only test skill.\n"})
                        assert status == 200, "skill creation failed"
                    status, skills = request(port, "/api/skills", token)
                    assert status == 200 and any(row["name"] == "madx-runtime-probe" for row in skills), f"test skill absent after launch {attempt + 1}: HTTP {status}"
                    assert request(port, "/api/madx-nonexistent-probe", token)[0] == 404, "unknown API path did not return 404"
                    result["checks"].append(f"launch {attempt + 1}: status, auth rejection, bridge discovery, memory, skills, 404")
                finally:
                    stop(child)
                    log.flush()
                    log.close()
                    # The profile token must not persist in the diagnostic log.
                    log_path.write_text(log_path.read_text(encoding="utf-8").replace(token, "<ephemeral-token>"), encoding="utf-8")
        result["checks"].append("owned server stopped and restarted with preserved profile")
    result["passed"] = True
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, default=ROOT / "upstream/hermes-agent")
    parser.add_argument("--scratch", type=Path, default=ROOT / ".venv/astra-runtime")
    parser.add_argument("--report", type=Path, default=ROOT / ".venv/astra-hermes-runtime.json")
    args = parser.parse_args()
    try:
        result = run(args.runtime.resolve(), args.scratch.resolve())
    except Exception as exc:
        result = {"passed": False, "platform": sys.platform, "error": f"{type(exc).__name__}: {exc}", "scope": "real provider-free runtime smoke"}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
