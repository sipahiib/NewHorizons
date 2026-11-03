# Cycle production commands

Approved package: APPROVAL.md, RESEARCH_PACKET.md, NARRATION_PLAN.md. Local assets and source conditions: MEDIA_AUDIT.md; cycle-isolated media under build/video/2026-11-03/media/. No Reels.

- Generate voice with `video/cycles/2026-11-03/prepare_audio.py` using cycle-local edge-tts 7.3.1 and the specified voice; Swift body was regenerated after the contextual disclosure moved earlier. Audio source text files are in cycle-local build audio.
- `.tools-edge-tts/bin/python video/cycles/2026-11-03/prepare_visuals.py` creates cycle-local stills, titles, audio concatenation, timing and manifest. Retain sources and output.
- `.tools-edge-tts/bin/python video/cycles/2026-11-03/render.py main --preview`; independent REVIEW.md must pass.
- `.tools-edge-tts/bin/python video/cycles/2026-11-03/render.py main` renders the isolated candidate; it does not promote the prior main.
- `python3 video/cycles/2026-11-03/verify_outputs.py` verifies the candidate; independent actual-output QA and complete human audiovisual playback remain separate gates before delivery/promotion.
