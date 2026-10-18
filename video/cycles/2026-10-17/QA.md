# Independent actual-output QA — 18 October 2026

TECHNICAL_SAMPLE_GATE: **PASS_TECHNICAL_AND_SAMPLED_VISUALS**
DELIVERY_GATE: **PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK**

Inspected candidate: `build/video/2026-10-17/newhorizons.mp4`. QA was independent of render. No technical/sample blocker found; this is a review-copy gate, not full audiovisual acceptance or publication authorisation.

Full-file decode completed without errors. Output is H.264/AAC, 1920×1080, 60 fps, 14,010 frames, 233.500 seconds, square pixels and 16:9 display. Runtime is below 310 seconds. Accepted plan retains the 16-second single-story opening and final 10-second closing (223.5–233.5).

Visually inspected 27 scene-midpoint frames plus 22 opening, boundary and closing samples. Laboratory equipment, pipetting and sample handling correspond to the approved contextual selection, with five static scenes and 22 motion segments. Corrected source8863365 scene shows laboratory footage. No prominent additional editorial captions, distorted aspect ratios or unreadable cards were found in samples. Full-file black detection found no interval ≥0.1 seconds at pixel threshold0.02.

Title is present at5.4 and absent5.6; subscription is absent29.9, present30.1/35.4 and absent35.6. Closing samples223.7–233.4 show glass entrance and readable Like/Subscribe/bell elements. Exact approved windows0–5.5,30–35.5 and223.5–233.5 are supported by resolved pre-render review; sampled output does not prove every individual boundary frame or complete animation quality.

Audio analysis: −16.33 LUFS integrated, −1.41 dBTP, LRA3.30 LU; no clipping indicated. At−45dB/≥0.35s detection, opening pauses are3.291,3.031 and2.769 seconds; most body sentence pauses are approximately one second. Transition silence is221.552–225.660 (4.108 seconds). Final detected speech ends230.391, leaving3.109 seconds, exceeding the container-based estimate2.264 seconds. Opening/closing pauses are documented intentions; their perceived pacing remains for listening acceptance.

**At independent QA handoff, pending:** continuous viewing and complete narration listening, including pronunciation, missing/clipped words, context disclosure, exact final sentence, pacing and closing animation. No complete listening or human full-playback pass is claimed. Final delivery and cleanup remain blocked until that evidence is recorded; human-approval fields must remain pending.

SHA-256: `91b1ed683bc0d0f4cc57503fa43c5a2c154f82a9418fffa4692b611a18d544b4`.

Evidence: `output_verification.json`; `build/video/2026-10-17/qa/` contains probe, empty decode-error log, full audio/black diagnostics, scene timestamps, actual frames and contact sheets. Contact-sheet unused cells are padding, not black output frames.

## User playback acceptance

On 18 October 2026 the user replied “onayladım.” to the linked review copy and explicit full viewing/listening checkpoint. This records complete continuous viewing and narration-listening acceptance for the SHA-256 above. Both human fields now pass; the accepted copy was promoted and hash-verified. This is human evidence, not a claim of automated listening. See DELIVERY_RECEIPT.json. Cleanup and publication were not performed.
