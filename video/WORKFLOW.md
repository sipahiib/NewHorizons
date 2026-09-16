# NewHorizons — Coordination Record

## Current governing main-video schedule — updated 16 September 2026

The required main-programme duration is **6:10 (370 seconds)**:

- Main story: **0:00–2:00** — 120 seconds, exactly eight 15-second visual segments.
- Support 1: **2:00–3:00** — 60 seconds, normally five 12-second visual segments.
- Support 2: **3:00–4:00** — 60 seconds, normally five 12-second visual segments.
- Support 3: **4:00–5:00** — 60 seconds, normally five 12-second visual segments.
- Support 4: **5:00–6:00** — 60 seconds, normally five 12-second visual segments.
- Closing CTA: **6:00–6:10** — 10 seconds.

The opening 20 seconds are part of the main story, not additional runtime. This schedule governs all new main-video planning, narration, manifests, overlays, rendering and QA. The 300- and 310-second entries later in this file document an already completed historical cycle and must not be reused as production instructions.

## 6 September 2026 research cycle

The user authorised three sub-agents and selected main-story hook H2:
“This launch from Norway could change how Europe's satellites get to space.”

The earlier role definitions were not found in the inspected project files or agent configuration. The following is the current working allocation, not a claim to have recovered those definitions. AGENTS.md remains the governing project workflow.

| Role | Current task | Handoff |
| --- | --- | --- |
| news_verification | Independently check the five main stories, primary sources, dates and claim boundaries | Evidence and corrections to coordinator |
| main_motion | Resolve the actual Spectrum replay and ten substantiated motion candidates | Source availability, clip evidence and unresolved rights/timecodes |
| reels_research | Check the three independent categories and seek strictly current alternatives to date exceptions | Topic proposals, sources, motion candidates and caveats |
| Coordinator | Integrate findings, maintain approval record and inspect technical readiness | User-facing proposal and approval gate |

Research agents do not edit shared production files, download media, finalise narration, delete previous media or render. Only the coordinator integrates their findings. Agent names here document assignments; they do not imply the agents are permanently running.

## Approval and production gates

Current-cycle approval, 16 September 2026: the user approved the package in `video/SOURCES.md` with M2 changed from FLEX/Sentinel-3C to NASA Roman primary-instrument activation. The approved set is M1 UCSF neuroprosthesis, M2 Roman, M3 CoRe-VLN, M4 atomically thin transistor injector, M5 retinal AF signal, R1 Future of AI education and R2 Planet Earth sea-ice collisions. Approved hooks are M1-H1, R1-H1 and R2-H1. This authorises in-repository media acquisition, final narration and rendering for that exact package. Material topic substitutions still require approval; routine failed-media replacement within the documented real-footage policy does not. Publication, purchase, external permission requests, commits and GitHub pushes remain unauthorised.

Delivery note requested by the user: when the main video and Reels are complete, provide a separate example set of current, topic-specific Instagram and YouTube hashtags for each finished video. Verify contemporary platform guidance at delivery time; avoid irrelevant bulk tags and do not publish anything externally.

Cover policy amended by the user: do not create or deliver cover images or thumbnails for the main video or Reels. Existing historical cover assets are retained only as archive material and are not current deliverables or production inputs.

The previous Hands-on Science visual substitution is historical and no longer belongs to the current production set.

1. Verify news and real recorded-video candidates for every main-programme story. Generated, procedural and illustrative animation is not permitted in the main programme. Distinguish proposed excerpts from visually confirmed footage. If suitable real video is unavailable after availability and rights checks, document the search outcome and propose relevant sourced still images as the fallback.
2. Present topics, sources and candidates to the user. All five main topics, main H1, both current Reel topics and each Reel's H1 are explicitly approved. Actual motion excerpts and their rights remain to be verified before production.
3. Resolve rights, availability and material substitutions before production. Do not infer blanket approval from the request to continue research.
4. After approval, enumerate previous-cycle audio/video paths before required cleanup; preserve non-media files and newly approved inputs.
5. Update scene mappings, narration and title timing together. Required main timeline: 120-second main story, four 60-second supports and a 10-second CTA = 370 seconds. Use boundaries 0/120/180/240/300/360/370 seconds, eight 15-second M1 segments and five 12-second segments per support.
6. Render and verify under AGENTS.md: English Ryan narration, 1080p/60 main video, vertical 1080×1920/60 Reels, measured speech and closing, then cleanup. Ask before any GitHub push; never commit audio/video binaries.

## Historical read-only technical preflight — 7 September 2026

Update, 7 September: user approved ten original illustrative motion scenes in place of Isar/NSF footage. `render_main_motion.mjs` produces the main-story asset package; `main_motion_scenes.tsv` is a separate 110-second manifest. This does not overwrite the old full-programme manifest or claim a finished new programme. Prior-cycle 44 MP4 files were removed from the project by moving them to `/private/tmp/newhorizons-previous-cycle-sOmK5S`; the inventory and original relative paths are preserved there. Temporary storage is recoverable for now but is not a permanent backup. No MP3 files were found in the preflight inventory.

Main animation package completed and verified: ten silent H.264 clips, each 1920×1080, 60 fps, 11 seconds / 660 decoded frames. All one-second samples differ; full-rate decoded hashes and black-frame checks passed. Decoded frames at 2 and 8 seconds for every clip were visually reviewed. Full-frame mean-difference freeze detection initially flagged small foreground movement against static backgrounds; verification uses exact consecutive decoded-frame hashes instead, alongside visual review. See `main_motion_verification.json`. Temporary preview/contact sheets were removed after review. Source clips and reproducible scripts are preserved; no complete narrated programme or Reel is claimed by this asset milestone.

Reproduce into an empty target directory: `node video/render_main_motion.mjs 1 2 3 4 5 6 7 8 9 10`. Existing MP4s are not overwritten. Verify with `node video/verify_main_motion.mjs`; its newly generated contact sheet must be reviewed and cleaned up again.

- At that time, `editorial_scenes.tsv` referred to an earlier configuration: five 24-second main clips, four 45-second supports and a ten-second closing (310 seconds). This is retained only as historical context and is not a valid schedule for future production.
- At that time, English title timings placed the CTA at 300–310 seconds. Those timings are obsolete; future production must use the governing 0/120/180/240/300/360/370-second boundaries above.
- The English render wrapper selects English titles. Main renderer is configured for 1920×1080 at 60 fps.
- The Reels renderer fits the entire foreground over a blurred background at 1080×1920 and 60 fps. Updated both narration validation and renderer to accept only 26–30 seconds of audio without changing the fixed -2% voice rate. Closing media now uses the computed closing duration rather than a hard-coded three seconds. Shell syntax and boundary checks (25.9, 26, 27, 29.9, 30, 30.01, 32.5 seconds) passed; an actual new Reel render is still required for audiovisual QA.
- No prior output is evidence of successful verification for this new cycle.

## Historical media decision and access checks — 7 September 2026

The user rejected extending illustrative animation to Samsung and CENTURIA and asked for licensed real footage. After a detailed disclosure, the user explicitly approved generic real stock with English illustrative labels. The ordinary public Pexels Free Download route worked: thirty sources plus the longer M4 alternative were downloaded, probed and visually sampled. No access-control evasion, upgrade or purchase occurred. The old 2.92-second Panasonic close-up is excluded; the longer external-AC building shot is used. The prior browser/download blocker above is resolved.

For that completed cycle, English narration was assembled at 300 seconds. The full-programme manifest and English titles used the then-approved 110/45/45/45/45/10-second timeline. This paragraph is a historical production record, not the schedule for a future render.

R1 primary abstract and 4 September date are now confirmed through NCBI/PMC. The motion agent completed this bounded follow-up. Its next authorised task is five original R2 paper-helicopter animations, explicitly approved after discovering that the official NASA tutorial contains insufficient actual moving craft footage. Two other agents remain unavailable after usage-limit errors; do not describe three agents as simultaneously active.

Reels final English texts were drafted. The safety reviewer rejected the network TTS request because final-text approval was not explicit; the full three texts were presented for user approval, without attempting a workaround. Reels render remains pending this gate and R2 asset verification. “Continue” has not been treated as GitHub push approval.

## Historical delivery follow-up — 7 September 2026

The user approved labelled real stock for Samsung/CENTURIA, five original R2 animations, and all three final Reels texts with meaning-preserving duration shortening. These gates are resolved. Main video rendered at exactly 300 seconds / 18,000 frames; sampled visual review and signal checks passed. Reels rendered at 30.0, 30.0 and 30.45 seconds; final verification and disposable-build cleanup follow the report scripts. Reels use fixed Ryan -2% without time stretching. Their closing is measured from the last detected spoken audio, not file duration. R1 has a brief 0.224-second opening offset to satisfy the minimum video duration without an overlong closing.

All three sub-agent roles remain documented, but they are not continuously active. The motion agent completed R1 primary verification and R2 animation production, then hit a usage limit on a requested diagram correction; the coordinator applied that correction locally. Do not report usage-limited agents as working.

Preserve the four final local MP4s and approved source assets. Cleanup removes only inventoried temporary narration, decoded QA frames and disposable render intermediates. No GitHub action is authorised yet.

Completed: all four final outputs passed technical checks and sampled visual review. Frame totals are 18,000 main and 1,800 / 1,800 / 1,827 Reels. Measured last-word-to-end gaps are 3.883 / 3.743 / 2.930 seconds. Cleanup removed 181 inventoried disposable build files (887,745,344 bytes); see `cleanup_manifest.json`. The recreated paper preview and obsolete corrected cut-scene temporary backup were also removed. These disposable intermediates are not recoverable through the project, but can be regenerated from preserved scripts and text. Approved source assets and the four final videos remain. The earlier prior-cycle recovery directory is untouched. GitHub push approval remains outstanding.
