# Production commands — 11 October 2026

Run from repository root. Network commands require environment network access. User approval is in APPROVAL.md. No publication command is included.

```sh
python3 video/cycles/2026-10-11/fetch_main.py
python3 video/cycles/2026-10-11/prepare_audio.py
/Users/is9565/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 video/cycles/2026-10-11/prepare_visuals.py
python3 video/cycles/2026-10-11/prepare_audit.py
python3 video/cycles/2026-10-11/render.py main --preview
python3 video/cycles/2026-10-11/render.py r1 --preview
python3 video/cycles/2026-10-11/render.py r2 --preview
```

Original additional media URLs and rights are in main_media_sources.json/reel_media_sources.json. NASA archive source is the1080p variant8895-7.m3u8; download only real recorded footage. Source correction artifact records clean first50seconds for first lab excerpt. Reel media handoff records all14selected downloads; no historical source is an active input.

After independent REVIEW.md pass:

```sh
python3 video/cycles/2026-10-11/render.py main
python3 video/cycles/2026-10-11/render.py r1
python3 video/cycles/2026-10-11/render.py r2
```

The renderer now includes the Reel leading delays, so fresh renders need no retime command. retime_reel_audio.py records the bounded initial-output correction only; do not apply twice. repair_main_segment.py repaired the original in-progress segment; fresh renders already select the repaired source through the manifest.

After completed render, independent QA runs qa_outputs.py with the bundled Pillow Python for each main/r1/r2 output. These tools provide technical/sample evidence only. Full audiovisual acceptance must be recorded separately before final promotion or cleanup. No cover generation, shared-final replacement or cleanup has been performed.
