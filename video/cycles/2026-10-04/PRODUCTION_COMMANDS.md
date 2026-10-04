# Reproduction — 2026-10-04

Run from the repository root after current approval. Networking requires the normal environment's network access. Retained accepted paper PDFs and original ESA page snapshots support provenance and figure derivation.

```sh
.tools-edge-tts/bin/python video/cycles/2026-10-04/fetch_media.py
.tools-edge-tts/bin/python video/cycles/2026-10-04/prepare_figures.py
.tools-edge-tts/bin/python video/cycles/2026-10-04/prepare_audio.py
node video/cycles/2026-10-04/prepare_visuals.mjs
python3 video/cycles/2026-10-04/prepare_audit.py
```

The source registry retains native source probes and explicit video-derived still origins. Original PDF downloads: `https://www.nature.com/articles/s44325-026-00153-2_reference.pdf` and `https://www.nature.com/articles/s41746-026-03320-y_reference.pdf`. Use the approved corpus; refresh review if its factual contents change.

Assemble M1 from four voice files in order, padding respectively to 5, 7, 4 and 144 seconds, resampling to 48kHz PCM WAV. The active measured assembly is `build/video/2026-10-04/audio/m1.wav`. No time stretching.

Independent review must issue each output's render gate before its command:

```sh
python3 video/cycles/2026-10-04/render.py main
python3 video/cycles/2026-10-04/render.py r1
python3 video/cycles/2026-10-04/render.py r2
```

These commands produce cycle-local candidates. The shared main delivery path is updated only after independent complete audiovisual playback passes, with evidence in `QA.md` and `current_delivery_review.json`. Metadata is in `DELIVERY_METADATA.md`; publishing requires separate authorisation. No cleanup while playback remains pending.
