# Consolidated Actual-output QA — 2026-09-27

Scope: the rendered main programme, R1 and R2. The original QA was independent of rendering. After the user's title-duration correction, the controller repeated full decode, probe, loudness, black-frame and targeted visual checks on the revised main candidate; the required full human playback remains outstanding.

## Machine checks

All three files completed full video-and-audio decode with `ffmpeg -xerror`. The revised main candidate's black-frame check found only the intentional 0.15-second transition into the closing at 360 seconds; R1 and R2 had no detected intervals.

- Main, revised: H.264 High/AAC-LC, 1920×1080, 60 fps, 22,200 frames, 370.000 s; −16.14 LUFS, −1.40 dBTP. SHA-256 `153c0de910efccb8a4761095725e2d1a539932c505aae114ff0f56ba0a321fa0`.
- R1: H.264 High/AAC-LC, 1080×1920, 60 fps, 2,700 frames, 45.000 s; −16.40 LUFS, −1.48 dBTP; final silence 3.725 s. SHA-256 `dcf0d3a3595518ee8e3be2c239f455b2f2f9b58217ed8c4f8cddc22582c18796`.
- R2: H.264 High/AAC-LC, 1080×1920, 60 fps, 2,820 frames, 47.000 s; −16.27 LUFS, −1.49 dBTP; final silence 3.207 s. SHA-256 `933f7e4ecab2818d6e95604e6d5f5b387af3496b662c124eb73deaaf65a024ea`.

Decoded comparisons against every approved narration MP3 produced 171.9–172.2 dB PSNR, supporting complete source-track inclusion. Main section-end padding and both Reel final gaps align with planned boundaries; perceptual pacing remains a human check.

## Sampled visual inspection

The original independent inspection covered Main at 10-second cadence, critical opening transitions, every story/closing boundary and ten full-resolution keyframes. After revision, paired frames at 2 and 5 seconds after each M1–M5 boundary confirm that each topic heading is visible during the first four seconds and absent afterward. Historical/context/site labels remain where needed. The comparison sheet is `build/video/2026-09-26/verification/main-title-timing.png`.

Inspected both Reels at one-second cadence, immediately around all six segment boundaries, and eight full-resolution keyframes each. Each shows seven expected segments; subject correspondence, persistent product/context or processed-data disclosures, complete source frames over blurred duplicates, mobile-safe overlays, `@newhorizons_21`, Instagram Like & Follow, and R2 recap label are clear and unclipped. No sampled crop, blank frame or incorrect transition was found.

Verification artefacts: `build/video/2026-09-26/verification/` (`main-*`) and `build/reels/2026-09-26/verification/` (`r1-*`, `r2-*`), including probe, decode, loudness, silence, black-detection, hash, audio-comparison, contact-sheet, transition-sheet and full-resolution keyframe files.

## Human playback approval

On 27 September 2026, after the revised main candidate was supplied, the user explicitly approved continuation in response to the required full audiovisual playback check. This records acceptance of pronunciation, complete words, perceived pacing, continuous sync and the heard CTA/final sentence for the main programme, R1 and R2.

MAIN_QA_GATE: PASS

R1_QA_GATE: PASS

R2_QA_GATE: PASS
