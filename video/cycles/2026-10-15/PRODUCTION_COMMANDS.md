# Reproduction — 2026-10-15

Run from the repository root. All media and outputs are cycle-isolated. Do not select prior-cycle media or run legacy entry points. Network access is required for original downloads and explicitly authorised Microsoft Edge TTS. Packages for the TTS client remain in the cycle work directory; the shared environment is unchanged.

```bash
.tools-edge-tts/bin/python video/cycles/2026-10-15/fetch_main.py
.tools-edge-tts/bin/python video/cycles/2026-10-15/fetch_reel_media.py
.tools-edge-tts/bin/python video/cycles/2026-10-15/write_narration.py
.tools-edge-tts/bin/python -m pip install --no-deps --target build/video/2026-10-15/tts-runtime edge-tts==7.3.1
.tools-edge-tts/bin/python video/cycles/2026-10-15/prepare_audio.py
.tools-edge-tts/bin/python video/cycles/2026-10-15/prepare_visuals.py
.tools-edge-tts/bin/python video/cycles/2026-10-15/prepare_reels.py
```

Source listing pages are preserved under source_pages (main) and the Reel media directory (Reels). Inspect media audit and manifests. Generate composition-only previews with render.py OUTPUT --preview. Independent REVIEW.md must pass the relevant gate before each render:

```bash
.tools-edge-tts/bin/python video/cycles/2026-10-15/render.py main
.tools-edge-tts/bin/python video/cycles/2026-10-15/render.py r1
.tools-edge-tts/bin/python video/cycles/2026-10-15/render.py r2
.tools-edge-tts/bin/python video/cycles/2026-10-15/verify_outputs.py
```

Do not use --resume after changing a manifest or source; it assumes unchanged previously rendered segments. Final candidates require independent QA of actual outputs. Technical/sample verification alone cannot establish complete viewing/listening acceptance. Never automatically promote an unaccepted candidate over build/video/newhorizons.mp4. Do not publish, push or clean up sources as part of reproduction.

Recorded QA corrections: repair_r1_audio.py shifted the original R1 narration by0.5seconds (no stretching or text change); prepare_reels.py now includes that delay for fresh reproduction. normalize_sar.py corrected initial candidate H264/container pixel aspect metadata; render.py now writes square-pixel metadata directly. Closing's extra tagline was removed and only that10-second segment was rerendered with the independent revised gate. Original candidates were preserved with descriptive pre-correction suffixes and are excluded from the current package.
