#!/usr/bin/env bash
# Build stage only. Ship the executable and notices, not a compiler or download client.
set -euo pipefail
cd /tmp
dnf -y install --setopt=install_weak_deps=False python3 git cmake ninja-build gcc-c++ /usr/bin/glslc vulkan-loader-devel vulkan-headers
pin="$(python3 -c 'import json; print(json.load(open("offline-model.json"))["engineRevision"])')"
[[ "$pin" =~ ^[0-9a-f]{40}$ ]]
git init llama
git -C llama fetch --depth=1 https://github.com/ggml-org/llama.cpp.git "$pin"
git -C llama checkout --detach FETCH_HEAD
[[ "$(git -C llama rev-parse HEAD)" == "$pin" ]]
cmake -S llama -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF \
  -DGGML_NATIVE=OFF -DGGML_VULKAN=ON -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF \
  -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_SERVER=ON
cmake --build build --target llama-server --parallel 2
install -Dm0755 build/bin/llama-server /out/llama-server
install -m0644 llama/LICENSE /out/llama.cpp-LICENSE
dnf clean all
rm -rf /tmp/build /tmp/llama
