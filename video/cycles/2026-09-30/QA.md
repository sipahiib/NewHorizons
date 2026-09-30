# Independent output QA — 2026-09-30

**MAIN_QA_GATE: FAIL — full audiovisual playback unresolved.**  
**R1_QA_GATE: FAIL — full audiovisual playback unresolved.**  
**R2_QA_GATE: FAIL — full audiovisual playback unresolved.**

I did not render these outputs. I decoded each complete file with `ffmpeg -xerror`, probed its streams, checked representative rendered frames, and measured audio silence and level. I could not listen to the complete narration or watch the footage continuously with the available perception tools. Therefore pronunciation, missing or clipped words, exact spoken closing sentence, continuous visual accuracy, and perceived pacing remain unverified. These are blocking checklist items; no delivery or cleanup is cleared.

| Output | Actual technical result | SHA-256 |
| --- | --- | --- |
| `build/video/2026-09-30/newhorizons.mp4` | H.264/AAC; 1920×1080; 60 fps; 22,200 frames; 370.000 s; full decode succeeds after audio revision | `a702ffa414da79e1b59e5cef4c22f33a4d4fe80f7356137ff891b56a2d82be01` |
| `build/reels/2026-09-30/01-future-of-ai.mp4` | H.264/AAC; 1080×1920; 60 fps; 2,700 frames; 45.000 s; revised file fully decodes | `3c621b6513164593badf8107a062d560b0f1ea2c001ec4aecbd9324ba6575445` |
| `build/reels/2026-09-30/02-the-planet-earth.mp4` | H.264/AAC; 1080×1920; 60 fps; 2,700 frames; 45.000 s; revised file fully decodes | `86c688f6d69f29b2cb7f0a01d8b04978388abac021f900861e26bdc44059e58a` |

Rendered-frame evidence for the revised Reels is at `build/reels/2026-09-30/verification/revised-overlay/`: `contact.png` and individual `r1-02.png` through `r1-43.png` / `r2-02.png` through `r2-43.png`, sampled at 2, 9, 21, 39 and 43 seconds. In these samples, both titles remain legible on the revised translucent upper panel; the series text and entire lower information card are absent. Context labels remain visible on sampled motion, and the unboxed YouTube/Instagram CTA appears at 43 seconds but not 39 seconds, consistent with its final-three-second timing. The sampled footage and source cards correspond to their topics. All 14 Reel source hashes match their manifests. This is sampled inspection, not continuous viewing. Earlier Reel sheets under `build/video/2026-09-30/verification/` predate this overlay revision. The main rendered-frame sheet remains at `build/video/2026-09-30/verification/main-sheet.jpg`; the main closing panel is visible there. The active production inputs are `main_manifest.json`, `r1_manifest.json`, `r2_manifest.json`, `narration.json`, and `audio_measurements.json` beside this file.

`silencedetect` at −35 dB found Reel end gaps of 3.46 s (R1) and 3.04 s (R2), within the four-second limit. After the reviewed M5 audio revision (`AUDIO_REVISION_REVIEW.md`, `audio_revision_manifest.json`), the main quiet gap before the 6:00 CTA is 2.49 s, down from 4.96 s. Main final quiet gap is 2.03 s. Mean/max levels: main −16.4/−1.4 dB; R1 and R2 −16.9/−1.4 to −1.5 dB. No black interval of at least 0.5 s was detected in the earlier main video; the video stream is byte-identical after remux (`ffmpeg` stream-copy MD5 `8a6898e644fad752f333d641e019da47` for both candidates). Full playback is still required before any gate can pass.
