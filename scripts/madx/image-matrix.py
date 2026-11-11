#!/usr/bin/env python3
"""Select explicit image scope; omitted architectures are deferred, never passed."""
import argparse
import json


def select(nvidia_only=False, publish=False, variant="standard"):
    if nvidia_only and (publish or variant != "nvidia"):
        raise ValueError("NVIDIA-only scope requires publish=false and validation_variant=nvidia")
    matrix = [
        dict(arch="amd64", label="amd64", variant="standard", image="madx-agent-os",
             suffix="-amd64", shell="x64", runner="ubuntu-24.04"),
        dict(arch="arm64", label="arm64", variant="standard", image="madx-agent-os",
             suffix="-arm64", shell="arm64", runner="ubuntu-24.04-arm"),
        dict(arch="amd64", label="amd64, NVIDIA", variant="nvidia", image="madx-agent-os-nvidia",
             suffix="", shell="x64", runner="ubuntu-24.04"),
    ]
    return {"include": [entry for entry in matrix if not nvidia_only or entry["variant"] == "nvidia"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nvidia-only", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--variant", choices=["standard", "nvidia"], default="standard")
    args = parser.parse_args()
    print(json.dumps(select(args.nvidia_only, args.publish, args.variant), separators=(",", ":")))
