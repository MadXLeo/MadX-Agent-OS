#!/usr/bin/env python3
"""Exercise the installed Hermes CLI against the account's real bundled language model."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request


def cli_failure(result):
    # Strip terminal styling and wrapping before matching the pinned CLI's errors.
    # Never include the raw output in artifacts. It can contain profile credentials.
    output = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout + "\n" + result.stderr)
    message = " ".join(output.lower().split())
    if "below the minimum" in message and "context" in message:
        return "configured context is below the Hermes minimum"
    if "401" in message or "unauthorized" in message:
        return "provider authentication failed"
    if "connection refused" in message or "connection error" in message:
        return "could not connect to the local provider"
    if "out of memory" in message or "cannot allocate memory" in message:
        return "out of memory"
    if "timed out" in message:
        return "provider timed out"
    if result.returncode:
        return "Hermes CLI exited without completing the probe"
    return "reply did not contain the expected answer"


def fail(stage, reason, **details):
    print(json.dumps({"passed": False, "stage": stage, "reason": reason, **details}), flush=True)
    sys.exit(f"Offline chat failed in {stage}: {reason}")


def main():
    port = 18000 + os.getuid() % 30000
    url = f"http://127.0.0.1:{port}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        try:
            with opener.open(url + "/health", timeout=3) as response:
                if json.load(response).get("status") == "ok":
                    break
        except (OSError, ValueError):
            pass
        time.sleep(1)
    else:
        fail("server readiness", "bundled inference server did not become healthy")
    payload = json.dumps({"model": "madx-local", "messages": [{"role": "user", "content": "Hi"}]}).encode()
    req = urllib.request.Request(url + "/v1/chat/completions", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with opener.open(req, timeout=10):
            fail("access control", "local inference accepted an unauthenticated request")
    except urllib.error.HTTPError as exc:
        if exc.code != 401:
            fail("access control", "unexpected HTTP status", httpStatus=exc.code)
    except OSError:
        fail("access control", "local inference endpoint unavailable")
    start = time.monotonic()
    try:
        result = subprocess.run(["hermes", "chat", "--quiet", "--oneshot", "-q",
                                 "Answer in one word, without tools. What is the capital city of France?"],
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=420)
    except subprocess.TimeoutExpired:
        fail("Hermes chat", "CLI timed out", timeoutSeconds=420, anonymousRequestStatus=401)
    except OSError:
        fail("Hermes chat", "could not launch the installed CLI", anonymousRequestStatus=401)
    # The test profile and any credentials stay in the guest. Export an allowlisted
    # answer and timing only. No raw configuration, CLI stderr or conversation log.
    if result.returncode or not re.search(r"\bParis\b", result.stdout, re.I):
        fail("Hermes chat", cli_failure(result), exitCode=result.returncode, anonymousRequestStatus=401)
    model = json.loads(Path("/usr/share/madx-model/model.json").read_text())
    print(json.dumps({"passed": True, "via": "installed Hermes CLI", "model": model["file"],
                      "modelRevision": model["revision"], "answerMatched": "Paris",
                      "anonymousRequestStatus": 401, "elapsedSeconds": round(time.monotonic() - start, 2)}))


if __name__ == "__main__":
    main()
