# Reproduction — 2026-10-17

Run from repository root. Requires ffmpeg, ffprobe and .tools-edge-tts Python with Pillow. Network downloads/TTS are already authorised for this package. No publishing or push.

1. `python3 video/cycles/2026-10-17/write_narration.py`
2. `.tools-edge-tts/bin/python -m pip install --no-deps --target build/video/2026-10-17/tts-runtime edge-tts==7.3.1`
3. `.tools-edge-tts/bin/python video/cycles/2026-10-17/fetch_media.py`
4. `.tools-edge-tts/bin/python video/cycles/2026-10-17/prepare_audio.py`
5. `.tools-edge-tts/bin/python video/cycles/2026-10-17/prepare_visuals.py`
6. `python3 video/cycles/2026-10-17/write_audit.py`
7. `.tools-edge-tts/bin/python video/cycles/2026-10-17/render.py main --preview`
8. Independent pre-render review writes REVIEW.md; resolve blockers.
9. `.tools-edge-tts/bin/python video/cycles/2026-10-17/render.py main`
10. `python3 video/cycles/2026-10-17/verify_outputs.py`
11. Independent actual-output QA, full playback acceptance and output-specific DELIVERY_METADATA.md before final delivery.

Accepted cycle copy: build/video/2026-10-17/newhorizons.mp4. User full audiovisual acceptance received18October; hash-verified copy promoted to build/video/newhorizons.mp4. Previous accepted copy preserved as recorded in DELIVERY_RECEIPT.json. Never use --resume after changing sources/manifests. No Reels or thumbnails in this cycle.
