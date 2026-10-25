# Production plan and commands — 25 October 2026

Approved spec: APPROVAL.md, RESEARCH_PACKET.md and ../../PRODUCTION_SPEC.md. Controller executes the existing Python/ffmpeg pipeline adapted into this cycle. No new product feature or shared renderer change. Preserve earlier cycles and accepted main. Main only; no Reels.

- [x] Final narration and independently attributable claims; English contextual disclosure.
- [x] Fresh licensed office/computer sources, cycle-local downloads, hashes and ffprobe; faithful still frames.
- [x] Specified Edge voice (-2%); measure speech before scene allocation; no stretching.
- [x] Cycle-local manifest and previews; independent review <=600 words, blockers resolved before render.
- [x] Render candidate to build/video/2026-10-25/newhorizons.mp4; independent output QA <=500 words, metadata reconciled.
- [x] Prepare review copy; full human viewing/listening approval remains a separate gate before promoting accepted main.

Primary review risks: context presented as actual product footage; unproven vendor benefits; wrong dates; stale assets; speech beyond fixed opening/closing slots; unwanted editorial overlays. Check source/claim mapping, manifests, source and output frames, speech measurements and full-file decode. No unit tests for content-only production scripts.

## Reproduction

Run from repository root with ffmpeg/ffprobe and .tools-edge-tts Python. Dependencies: installed edge-tts 7.3.1 copied to this cycle’s tts-runtime directory; no old media copied. Initial global 7.2.8 attempt received HTTP403; pinned runtime succeeded.

1. `python3 video/cycles/2026-10-25/resolve_media.py` (public network)
2. `python3 video/cycles/2026-10-25/fetch_media.py` (public network)
3. `.tools-edge-tts/bin/python video/cycles/2026-10-25/prepare_audio.py` (approved Microsoft voice service)
4. `.tools-edge-tts/bin/python video/cycles/2026-10-25/inspect_sources.py`
5. `.tools-edge-tts/bin/python video/cycles/2026-10-25/prepare_visuals.py`
6. `python3 video/cycles/2026-10-25/write_audit.py`
7. `.tools-edge-tts/bin/python video/cycles/2026-10-25/render.py main --preview`
8. Independent review and one bounded correction round; resolve blockers.
9. `.tools-edge-tts/bin/python video/cycles/2026-10-25/render.py main`
10. `python3 video/cycles/2026-10-25/verify_outputs.py`; independent output QA and human full viewing/listening before promotion.

Do not use --resume after changing inputs. Do not publish, push or clean up source assets. All metadata delivered locally.

Final full viewing/listening accepted by user on 25 October; accepted main promoted and hash-verified. Previous main preserved; no cleanup or publication. See DELIVERY_RECEIPT.json.
