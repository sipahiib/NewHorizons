# Independent pre-render review — R2, 13 November 2026

R2_RENDER_GATE: BLOCKED

## Correction-round findings

The two incorrectly attributed Galaxy-marked files are no longer selected. I checked the six selected Commons files: their actual pixel dimensions now match the metadata and their SHA-256 values match that record. The replacement files are visibly different landscapes without the prior Galaxy marks. Matching dimensions and locally recorded hashes are not independent proof of correspondence to the named originals or their licenses; the source pages could not be opened in this review. Establish and record source-to-file correspondence and applicable rights for all seven selected files, including NASA, and the CC BY-SA distribution treatment.

The 699-file exact-byte prior-use scan is useful but predates the two replacements and cannot detect altered copies. Scan the corrected set and document a comparison with available previous outputs and source records; do not present the existing result as verification of the replacements. The audit still labels itself in progress and contains obsolete claims that no files were downloaded or checked; update its current status and per-file evidence after the checks.

The audit says the complete narration has not been listened to. Listen to the actual shortened audio against the approved text for completeness, clipping, pronunciation, pacing and silence, and measure the actual final speech-to-end gap. The 44.256-second file duration does not establish speech end. I did not listen to the audio.

The current render script uses FFmpeg `drawtext`; the controller reports the installed FFmpeg lacks that filter. Replace or repair and test the title and CTA rendering before render. Verify title readability and exact window, final unboxed calls and landscape framing in independent output QA.

## Other checks

Approval records R2-A and the shortened narration and excludes R1. The written narration follows the packet's broad framing, including the 2024 Landsat capture. Seven still scenes total 46 seconds, within the specified 45–50 seconds. The six selected Commons images' dimensions and local SHA-256 hashes agree with source metadata; this does not verify origin. The planned timing is a 5.5-second topic title and calls during the final three seconds. The selected road image depicts the landscape under the supplied source record. No cover is selected. The script intends 1080 × 1920, 60 fps H.264/AAC and the required blurred background.

Resolve the blockers and obtain an independent review before rendering. Actual output still requires independent full audiovisual QA.
# Independent R2 pre-render review — 13 November 2026

R2_RENDER_GATE: PASS

This pass covers the local R2 render only. Publication and distribution are not authorised or cleared by this review.

## Correction review

I recomputed SHA-1 for all six selected Commons files: each matches the source SHA-1 recorded from Wikimedia's API in `r2_source_metadata.json`. Their source titles, creators, dimensions, license URLs and local SHA-256 values are recorded in the metadata and credits. The NASA still visually corresponds to the Flow Country satellite image and the audit records its NASA/USGS credit, local hash and resized dimensions. The earlier incorrect files remain excluded.

The updated audit documents a no-hit search of prior cycle and archive text for the source IDs and names, and a 699-file exact-byte scan of prior local media. The text-result file is empty. This is reasonable available evidence, but neither test can exclude unrecorded or transformed earlier use. The audit identifies that limitation.

The Commons images are identified as CC BY-SA 2.0; attribution, source and license links and resizing are recorded. The audit explicitly reserves the adaptation, share-alike and compatibility decision for before distribution. That unresolved downstream decision does not prevent the local render; it must be resolved with required notices and any necessary user decision before distribution. NASA usage conditions also apply. The audit's earlier progress notes are historical and its further-verification section is current; label the historical status clearly when integrating this review.

## Other checks

R2-A, shortened narration and TTS are approved; R1 is excluded. Approval records the user's complete listening and acceptance. Audio measures 44.256 s; silence detection at -40 dB estimates speech end around 43.36 s, leaving about 2.64 s in the planned 46 s output. Seven distinct stills total 46 s and match manifest hashes. Inspected images are consistent with the subject; no cover is selected.

The title preview is readable and the CTA PNG is unboxed. The script schedules the title for 0–5.5 s and CTA for 43–46 s, and uses a blurred background and full foreground frame. Its gate reads `REVIEW.md`; integrate this accepted review there before rendering. Independent full audiovisual output QA must verify actual timing, speech, framing and mobile legibility before delivery.
# Independent final main pre-render review — 13 November 2026

**MAIN_RENDER_GATE: PASS** — local render only.

The prior blocker is resolved: `NARRATION_PLAN.md` no longer presents generation and measurement as pending, identifies the superseded opening as historical, and records the final approved and listened-to hook and assembly. The renderer checks `REVIEW.md` for its gate; integrate this independent decision there before rendering, and do not use `--resume` with unverified old segments. This pass does not authorise distribution and does not replace independent full audiovisual output QA.

## Evidence reviewed

- The user confirmed listening to the final assembled 16-second opening and its transitions. Its recorded SHA-256 matches the file; decoded first 16 seconds of `main-lead-assembled.wav` match the opening file exactly. Earlier complete-preview listening covers the unchanged remainder. I did not independently listen to the audio.
- All 23 distinct selected source, audio and overlay input hashes match `main_manifest.json`. Lead scenes total 99 seconds (13 motion segments, two still segments); the second story totals 61 seconds (three motion, six still); the final ten-second closing gives 170 seconds. This is the plan, not output verification.
- The revised Washington clip 03 audit records its source, CC BY 4.0, 1232×1028, 5 fps, contextual status, source slowdown and crop. Sampled actual selected turbine frames show a different underwater turbine; the approved narration identifies it as different. The separate FloWave photo is scheduled during its disclosure. Sampled selected NASA launch, arrival and Hubble servicing frames are consistent with their contextual descriptions. Generic ocean remains a substantial fallback and cannot depict the experiment. I inspected representative frames, not complete moving shots; the earlier review records one-second sampling of selected spans.
- Hubble gallery credit and NASA's guidance are documented. The specific third-party rights position remains unresolved: the release does not establish whether credited external contributions carry additional rights. This uncertainty need not block a private local review render; it **does block distribution clearance**, which remains unauthorised and requires an image-specific rights assessment. No permission request was made. Credits and earlier inventory entries retain provisional wording; finalise and reconcile them before distribution.
- Narration preserves model-scale testing and simulated comparison, and distinguishes Hubble observations from prospective Roman follow-up. Title and subscription windows are scheduled in the renderer; output readability, actual timing, full imagery and audio require independent post-render audiovisual QA.
