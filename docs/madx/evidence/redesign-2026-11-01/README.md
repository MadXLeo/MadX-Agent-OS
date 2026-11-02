# Renderer evidence — 2026-11-01

Before source: `2e844ca74b87b04395bb6232b368edc5b8bea451`.
After source: `517d72fce3f4c066187030038084e6a3db72e841` (includes identity commit `93fdc9c`).
Screenshots were captured before committing the identical application changes.

The preview imports actual Desktop/MainWindow components. Its ignored local adapter supplies
empty/offline results and stores appearance choices only for the preview session. No native
Electron IPC, Hermes runtime, VM, system metrics or real user data is connected. Baseline's
misleading Starting/idle labels are retained in the before pictures as observed; the redesign
shows unavailable states. These are renderer screenshots, not OS installation evidence.

| Files | Target layout | Observed CSS viewport | Evidence |
| --- | --- | --- | --- |
| home-before-1920.jpg / home-after-1920.jpg | 1920x1080 | 1920x1080 | Original and redesigned Home |
| home-before-1366.jpg / home-after-1366.jpg | 1366x768 | 1366x767 | Original and redesigned Home |
| home-before-1024.jpg / home-after-1024.jpg | 1024x768 | 1023x767 | Representative small layout; not actual VirtualBox resolution |
| settings-performance-1024.jpg | 1024x768 | 1023x767 | Performance selected; computed top-bar backdrop-filter was none |
| launcher-640.jpg | 640x768 | approximately 640x768 | Five rendered columns; ArrowDown selected Hermes, next ArrowDown selected MadX Canvas, directly below |

The browser's Windows scaling rounds some CSS sizes and full-page captures can include outer
dark padding. Image pixel dimensions therefore differ from the tested application viewport;
the JSON manifest records actual encoded dimensions and checksums. Images are not rescaled or
composited. A stale capture was replaced after reconnecting the browser; only verified pictures
are retained. The final 1024 Home also shows the repaired non-wrapping command trigger.

Additional interactions inspected: Home navigation, Hermes history/output toggles, compact Add
space focus/cancel, and graphics-mode changes. The tests separately prove hidden output preserves
editor state. There are no native frame pacing or interaction latency measurements here, no
proof of compositor-level animations, and no measured VirtualBox resolution. Those remain
required acceptance evidence after an authorized native image build.

`manifest.json` records checksums and dimensions of these eight images, local test-report hashes
and production entry-point hashes. Full local logs remain ignored because they include host paths.
The portable/full test counts, skips and one baseline Windows failure are documented in REDESIGN.md.
