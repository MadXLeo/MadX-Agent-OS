# Fedora NVIDIA offline candidate

The requested target is Fedora 44 x86_64 with the NVIDIA driver, Hermes Agent, a local inference server and a model on the installation media. A fresh account gets local chat automatically. Dependencies and model weights are fetched when building the image. Installation, first boot and the first chat must succeed with the guest disconnected from the internet.

The Hermes source is pinned by `upstream/UPSTREAM.lock` at `f97608f178d1ffeca59860195ab7da295f7c8e5f`. The image builds the runtime with its locked dependencies and desktop, voice, wake, messaging and listed provider extras. The settings and bridge belong to the session user. Existing accounts keep their provider settings. Runtime package installation is disabled for the image-owned launcher.

The default local model is Qwen2.5-1.5B-Instruct Q4_K_M (1,117,320,736 bytes). Its revision, SHA-256 and llama.cpp source revision are in `linux/image/offline-model.json`. The build verifies the weights and includes the model license, model card and engine license. The inference server binds to loopback, uses a unique credential generated per account, and supports CPU and Vulkan. RTX 4070 acceleration, external displays and hardware performance require direct observation. Online services such as web search still need connectivity. Offline acceptance covers the installed desktop runtime and text chat. Speech model assets and optional third-party integrations have separate requirements.

## Run sequence

1. Verify the redesign branch's new source SHA. Its push starts Linux desktop, bridge/CLI, pinned Hermes, scripts, signing and secret checks. Review reports and skips. macOS coverage is deferred for this milestone.
2. Dispatch the registered `image.yml` on that exact branch revision with `publish=false`, `disks=true`, `validation_variant=nvidia` and `nvidia_only=true`. Only the NVIDIA amd64 job belongs to this image run. The default matrix on other builds still includes the standard variants.
3. Before constructing the ISO, run the actual image read-only as a non-root user with external networking disabled. Require provider setup, a real answer from Hermes using the bundled model, rejection of an unauthenticated inference request, and the existing server/auth/bridge/memory/restart smoke. Inspect `hermes-bundle-evidence/offline-chat.json`, `runtime.json`, the dependency inventory and both manifests.
4. Verify the complete image run, artifact and ISO hashes. Dispatch `installer-test.yml` for that same revision and image run with `account=madx-test`, `validation_variant=nvidia` and an empty release tag. The installer receives its test kickstart on the disposable ISO and boots with no NIC. On reboot QEMU restricts networking and forwards test SSH to loopback. The guest must discover the pinned bundled Hermes, preserve the bridge, show the graphical desktop and answer through its configured local model.

The earlier NVIDIA ISO from source `42bcc70` predates bundling. A new ISO, disconnected installed-guest chat and the physical Alienware result remain unverified until the corresponding runs produce evidence.
