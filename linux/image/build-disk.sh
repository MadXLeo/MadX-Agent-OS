#!/usr/bin/env bash
# Build a local image into a disposable artifact. Never selects a host disk or publishes an image.
set -euo pipefail
[[ "$(uname -s)" == Linux ]] || { echo 'image builds require a disposable Linux builder' >&2; exit 2; }
ref="${1:?image reference required}"
kind="${2:?anaconda-iso or qcow2 required}"
config="${3:?configuration file required}"
output="${4:?output directory required}"
[[ "$kind" == anaconda-iso || "$kind" == qcow2 ]] || { echo 'unsupported image type' >&2; exit 2; }
[[ "$ref" != -* && "$ref" != *[[:space:]]* && -f "$config" ]] || exit 2
[[ ! -e "$output" ]] || { echo 'output directory must be new' >&2; exit 2; }
[[ "$(realpath -m "$output")" == "$(pwd -P)/"* ]] || { echo 'output must stay below the working directory' >&2; exit 2; }
mkdir -p "$output"
config="$(realpath "$config")"
output="$(realpath "$output")"
builder=quay.io/centos-bootc/bootc-image-builder@sha256:2b52843ea2bfda73b0a08d97e76b734393b1d3a804681b9fabb26723bd3a2f0b
sudo podman image exists "$ref"
sudo podman run --rm --privileged --pull=newer --security-opt label=type:unconfined_t \
  -v "$output:/output" -v "$config:/config.toml:ro" \
  -v /var/lib/containers/storage:/var/lib/containers/storage \
  "$builder" --type "$kind" --rootfs btrfs --local "$ref"
