# NewHorizons context checkpoint

Updated: 2026-09-27 after completion of the September 26 production cycle.

This is a repository-local continuity note, not a replacement for AGENTS.md or the specialised policies. It summarises accessible project records; it does not claim access to all past conversations or a new independent factual/audiovisual audit.

## Latest cycle transition

The user invoked newhorizons-start with `/start` on 2026-09-26 and approved the editorial package. The cycle in `video/cycles/2026-09-26/` is complete: main topics are McGetchin lunar crater, Meta Muse glasses, hafnia, cartilage evolution and FEAR 3; Reels cover Gemini Live Avatar and NISAR volcano monitoring. Independent pre-render review passed, technical and sampled-visual QA passed, and the user approved full audiovisual playback on 2026-09-27. After user feedback, every M1–M5 topic heading appears only for the first four seconds of its section. The revised main is `build/video/newhorizons.mp4`; dated Reels are under `build/reels/2026-09-26/`. Publication remains unauthorised.

## September 23 checkpoint

- Active cycle: `video/cycles/2026-09-23/`. Its BRIEF and QA record completion, technical QA PASS and user-confirmed full audiovisual playback on 23 September. `video/current_delivery_review.json` records both human approvals as passed and gate `PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK`.
- Main topics: Mars water history; Korean cybersecurity AI; Korean factory AI; bioresorbable battery research in pigs; Arctic melt-season stabilization. Independent Reels: Claude Opus 5.5 provider claims and Incendiamoeba cascadensis. Treat factual details as recorded editorial content, not newly verified facts from this checkpoint.
- Local outputs exist: `build/video/newhorizons.mp4`, `build/reels/01-future-of-ai.mp4`, `build/reels/02-planet-earth.mp4`. Hashes and technical evidence are in QA and the delivery-review JSON; hashes were not recomputed during this context review.
- Topic-specific delivery metadata is prepared in `video/cycles/2026-09-23/DELIVERY_METADATA.md`; publication is not authorised.
- The 2026-09-18 cycle separately records pending complete human audiovisual playback. Do not transfer the newer cycle's approval to it.
- No new cycle, production, cleanup, commit or push was requested by this memory update.

## Continuing work

- Only the exact `/start` command invokes the startup skill and opens a new dated editorial cycle. Preserve older cycles, including their unfinished work.
- Read root/video AGENTS and route to the relevant task documents. Use APPROVAL for editorial authorisation, current production manifests for selected inputs, REVIEW for pre-render findings and QA plus delivery-review JSON for delivery status.
- Current production rules: main 370 seconds, 1920×1080/60 fps; Reels 45–50 seconds, 1080×1920/60 fps; narration en-GB-RyanNeural at -2%. Consult `video/PRODUCTION_SPEC.md` for full requirements.
- Current visual rules require sourced stills mixed with real footage, relevant audited sources, no reused prior-output Reel media and no thumbnails. Mandatory per-output hashtags and separate YouTube Tags belong in the cycle's delivery metadata.
- Preserve explicit authorisation boundaries: separate authorisation for publishing, purchasing and external permission requests; ask before every GitHub push. Keep media local and out of commits/pushes.
- Use agents only for substantial parallel research or required independent review/QA; no nested agents or full-history forks. Routine integration remains with the controller.

## Record discrepancies to remember

- WORKFLOW's stale production-preparation status was corrected to match the completed cycle records in this update.
- The research packet still says proposed/awaiting approval; the later APPROVAL, BRIEF and QA establish actual approval/completion. Preserve the research packet as historical proposal context.
- The completed September 23 records describe all-motion visuals, equal scene lengths and historical narration measurements. Current PRODUCTION_SPEC requires mixed still/motion visuals and allows narration-led variable scene lengths. Do not reuse the completed package as a specification template or retroactively claim it meets every current rule.
- NARRATION_PLAN retains an older “185+ targets” detail; REVIEW records its removal from production narration. REVIEW's predicted Reel durations also differ from QA's measured final outputs. Prefer the final corrected narration and actual-output QA for those facts.
