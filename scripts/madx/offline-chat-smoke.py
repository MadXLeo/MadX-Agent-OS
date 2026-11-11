#!/usr/bin/env python3
"""Exercise the installed Hermes CLI against the account's real bundled language model."""
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.request


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
        raise RuntimeError("bundled inference server did not become healthy")
    payload = json.dumps({"model": "madx-local", "messages": [{"role": "user", "content": "Hi"}]}).encode()
    req = urllib.request.Request(url + "/v1/chat/completions", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with opener.open(req, timeout=10):
            raise RuntimeError("local inference accepted an unauthenticated request")
    except urllib.error.HTTPError as exc:
        if exc.code != 401:
            raise
    start = time.monotonic()
    result = subprocess.run(["hermes", "chat", "--quiet", "--oneshot", "-q",
                             "Answer in one word, without tools. What is the capital city of France?"],
                            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=420)
    # The test profile and any credentials stay in the guest. Export an allowlisted
    # answer and timing only. No raw configuration, CLI stderr or conversation log.
    if result.returncode or not re.search(r"\bParis\b", result.stdout, re.I):
        raise RuntimeError(f"offline Hermes chat did not answer the probe (exit {result.returncode})")
    model = json.loads(Path("/usr/share/madx-model/model.json").read_text())
    print(json.dumps({"passed": True, "via": "installed Hermes CLI", "model": model["file"],
                      "modelRevision": model["revision"], "answerMatched": "Paris",
                      "anonymousRequestStatus": 401, "elapsedSeconds": round(time.monotonic() - start, 2)}))


if __name__ == "__main__":
    main()
