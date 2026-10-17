# Independent output QA — 2026-10-15

TECHNICAL_GATE: PASS
SAMPLED_VISUAL_GATE: PASS
DELIVERY_GATE: PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK
PROMOTION_GATE: PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK
CLEANUP_GATE: PLAYBACK_REQUIREMENT_PASSED; NO_CLEANUP_PERFORMED

Independent QA agent did not prepare or render production outputs. Scope: completed candidate files, accepted approval/review/manifests and narration plan, selected source hashes, decoded frames and encoded audio measurements. Automated full audiovisual acceptance is **not** claimed; subsequent user acceptance is recorded below.

All three complete files decode without errors. Main: 263.000 seconds, 15,780 frames, 1920×1080. Both Reels: 45.000 seconds, 2,700 frames, 1080×1920, exactly seven visual segments. All are 60 fps H.264/AAC, square pixels. Main remains below 310 seconds; opening is 0–16 within NASA 0–128, RNA 128–253, closing exactly 253–263. Opening image transitions occur at 5 and 12 seconds.

Inspected every scene at start/middle/end: 75 main and 21 frames per Reel, plus exact boundary samples and a ten-frame closing sequence. NASA photography/contextual facility footage, RNA microscopy, AI simulation panels and Polo satellite/rainfall imagery match their accepted source roles and narration framing. Selected source hashes all match manifests. No prominent embedded source captions, lower information cards, subtitles, series labels or cover found in samples. Titles disappear at 5.5 seconds; main subscription appears 30–35.5; unboxed Reel calls appear 42–45. Reel foregrounds remain complete over blurred backgrounds. Revised closing has glass entrance, Like response, Subscribe accent and bell; the extra tagline is absent.

Encoded audio mean/maximum levels: main −16.7/−1.4 dB; R1 −16.8/−1.4; R2 −16.9/−1.4. No measured clipping. Final silence at −40 dB: main 3.122 seconds, corrected R1 3.762, R2 3.614; both Reel gaps satisfy ≤4 seconds. Longer main pauses align with approved opening/transition/closing slots. Source/output PCM correlations are 0.997–0.999, supporting encoded waveform correspondence, including closing audio at 255 seconds. Narration text retains the required final sentence; waveform correspondence cannot certify its pronunciation or intelligibility.

One QA correction round resolved excessive R1 ending silence; square-pixel corrections and the controller's closing correction were independently rechecked. No technical/sample blockers remain.

**At independent tool QA:** audio input was unsupported, so complete listening and continuous viewing remained pending. That limitation is unchanged; subsequent human confirmation resolves the acceptance gate without claiming automated listening.

Evidence and full SHA-256 values: [qa_independent.json](qa_independent.json); decoded metadata, logs, source checks and sampled frames: `build/video/2026-10-15/qa-independent/`. Final hash prefixes: main `ed784a8bb64005ed`, R1 `70f9d192f68fe1db`, R2 `52706896344ef164`.

## Human acceptance — 15 October 2026

The user replied “onay veriyorum” to all three review-copy links and the explicit full viewing/listening checkpoint. Confirmation applies to the unchanged final hashes below. Both human approval fields are passed; machine gate PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK. Main was promoted to build/video/newhorizons.mp4 and hash-verified; previous shared main remains preserved. Reels accepted in their dated directory. Evidence and UTC timestamp: delivery_review.json and DELIVERY_RECEIPT.json. No publication or cleanup occurred.
