# NewHorizons — Coordination Record

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

1. Verify news and actual moving-media candidates. Distinguish proposed excerpts from visually confirmed footage.
2. Present topics, sources and candidates to the user. All five main topics, main H2, all three Reel topics and each Reel's H1 are explicitly approved. Actual motion excerpts and their rights remain to be verified and approved.
3. Resolve rights, availability and material substitutions before production. Do not infer blanket approval from the request to continue research.
4. After approval, enumerate previous-cycle audio/video paths before required cleanup; preserve non-media files and newly approved inputs.
5. Update scene mappings, narration and title timing together. Proposed main timeline: 110 seconds (ten 11-second clips), four 45-second supports, ten-second CTA = 300 seconds.
6. Render and verify under AGENTS.md: English Ryan narration, 1080p/60 main video, vertical 1080×1920/60 Reels, measured speech and closing, then cleanup. Ask before any GitHub push; never commit audio/video binaries.

## Read-only technical preflight

Update, 7 September: user approved ten original illustrative motion scenes in place of Isar/NSF footage. `render_main_motion.mjs` produces the main-story asset package; `main_motion_scenes.tsv` is a separate 110-second manifest. This does not overwrite the old full-programme manifest or claim a finished new programme. Prior-cycle 44 MP4 files were removed from the project by moving them to `/private/tmp/newhorizons-previous-cycle-sOmK5S`; the inventory and original relative paths are preserved there. Temporary storage is recoverable for now but is not a permanent backup. No MP3 files were found in the preflight inventory.

Main animation package completed and verified: ten silent H.264 clips, each 1920×1080, 60 fps, 11 seconds / 660 decoded frames. All one-second samples differ; full-rate decoded hashes and black-frame checks passed. Decoded frames at 2 and 8 seconds for every clip were visually reviewed. Full-frame mean-difference freeze detection initially flagged small foreground movement against static backgrounds; verification uses exact consecutive decoded-frame hashes instead, alongside visual review. See `main_motion_verification.json`. Temporary preview/contact sheets were removed after review. Source clips and reproducible scripts are preserved; no complete narrated programme or Reel is claimed by this asset milestone.

Reproduce into an empty target directory: `node video/render_main_motion.mjs 1 2 3 4 5 6 7 8 9 10`. Existing MP4s are not overwritten. Verify with `node video/verify_main_motion.mjs`; its newly generated contact sheet must be reviewed and cleaned up again.

- Existing `editorial_scenes.tsv` still refers to the previous cycle: five 24-second main clips, four 45-second supports and a ten-second closing (310 seconds). It has not been changed or executed for the new cycle.
- Existing English title timings also refer to the previous stories, with CTA at 300–310 seconds. New production must move the CTA to 290–300 seconds and remap all story boundaries.
- The English render wrapper selects English titles. Main renderer is configured for 1920×1080 at 60 fps.
- The Reels renderer fits the entire foreground over a blurred background at 1080×1920 and 60 fps. Updated both narration validation and renderer to accept only 26–30 seconds of audio without changing the fixed -2% voice rate. Closing media now uses the computed closing duration rather than a hard-coded three seconds. Shell syntax and boundary checks (25.9, 26, 27, 29.9, 30, 30.01, 32.5 seconds) passed; an actual new Reel render is still required for audiovisual QA.
- No prior output is evidence of successful verification for this new cycle.

## Latest media decision and access checks

The user rejected extending illustrative animation to Samsung and CENTURIA and asked for licensed real footage. After a detailed disclosure, the user explicitly approved generic real stock with English illustrative labels. The ordinary public Pexels Free Download route worked: thirty sources plus the longer M4 alternative were downloaded, probed and visually sampled. No access-control evasion, upgrade or purchase occurred. The old 2.92-second Panasonic close-up is excluded; the longer external-AC building shot is used. The prior browser/download blocker above is resolved.

Current production: English narration has been assembled at 300 seconds. The full-programme manifest and English titles now match the new 110/45/45/45/45/10-second timeline; main render and subsequent QA are in progress. Earlier preflight statements describing old manifests are historical. Main output is not yet verified.

R1 primary abstract and 4 September date are now confirmed through NCBI/PMC. The motion agent completed this bounded follow-up. Its next authorised task is five original R2 paper-helicopter animations, explicitly approved after discovering that the official NASA tutorial contains insufficient actual moving craft footage. Two other agents remain unavailable after usage-limit errors; do not describe three agents as simultaneously active.

Reels final English texts were drafted. The safety reviewer rejected the network TTS request because final-text approval was not explicit; the full three texts were presented for user approval, without attempting a workaround. Reels render remains pending this gate and R2 asset verification. “Continue” has not been treated as GitHub push approval.

## Delivery follow-up

The user approved labelled real stock for Samsung/CENTURIA, five original R2 animations, and all three final Reels texts with meaning-preserving duration shortening. These gates are resolved. Main video rendered at exactly 300 seconds / 18,000 frames; sampled visual review and signal checks passed. Reels rendered at 30.0, 30.0 and 30.45 seconds; final verification and disposable-build cleanup follow the report scripts. Reels use fixed Ryan -2% without time stretching. Their closing is measured from the last detected spoken audio, not file duration. R1 has a brief 0.224-second opening offset to satisfy the minimum video duration without an overlong closing.

All three sub-agent roles remain documented, but they are not continuously active. The motion agent completed R1 primary verification and R2 animation production, then hit a usage limit on a requested diagram correction; the coordinator applied that correction locally. Do not report usage-limited agents as working.

Preserve the four final local MP4s and approved source assets. Cleanup removes only inventoried temporary narration, decoded QA frames and disposable render intermediates. No GitHub action is authorised yet.

Completed: all four final outputs passed technical checks and sampled visual review. Frame totals are 18,000 main and 1,800 / 1,800 / 1,827 Reels. Measured last-word-to-end gaps are 3.883 / 3.743 / 2.930 seconds. Cleanup removed 181 inventoried disposable build files (887,745,344 bytes); see `cleanup_manifest.json`. The recreated paper preview and obsolete corrected cut-scene temporary backup were also removed. These disposable intermediates are not recoverable through the project, but can be regenerated from preserved scripts and text. Approved source assets and the four final videos remain. The earlier prior-cycle recovery directory is untouched. GitHub push approval remains outstanding.
