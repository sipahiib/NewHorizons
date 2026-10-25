# Independent actual-output QA — 25 October 2026

TECHNICAL_AND_SAMPLED_VISUAL_GATE: PASS
FULL_AUDIOVISUAL_GATE: PASS_USER_CONFIRMED_COMPLETE_PLAYBACK
PROMOTION: PASSED_AFTER_USER_ACCEPTANCE
CLEANUP: NOT_PERFORMED

Independent qa_1025 agent checked the encoded candidate without rendering or changing implementation. Accepted review/research reused. Scope: approved single-story Sakana Aquarium main video; no Reels.

`verify_outputs.py` completed successfully against `build/video/2026-10-25/newhorizons.mp4`. Full-file audio/video decode passed with no errors. Actual profile: H.264/AAC, 1920×1080, 60 fps, square pixels, 11,970 frames, 199.500 seconds. This matches the manifest and stays below 310 seconds. Opening remains 0–16 seconds; closing is exactly 189.5–199.5 seconds. All 20 selected input hashes independently matched the manifest, including replacement sources.

Inspected 22 actual-output sample frames and contact sheet, including title present at 0/2/5.4 seconds and absent at 5.6; YouTube call absent at 29.9, present at 30.1/35.4, absent at 35.6; and closing entrance, settled panel and final frame. Full-size title, subscription and closing samples are readable with subjects retained. Replacement meeting footage at 75/105/189.4 and office footage at 180 seconds correspond to contextual workplace discussion. No rejected VOTE badges, financing chart, product demonstration, subtitle, lower source card, cover or other prominent editorial text appears in inspected samples. Sampled stills remain faithful office scenes. Glass panel, red Subscribe accent and yellow bell appear in closing samples; continuous animation quality awaits playback.

Actual-file audio analysis: −16.35 LUFS integrated, −1.42 dBTP, 2.90 LU range; no full-frame black interval detected. Detected sentence pauses are approximately one second. Opening pauses reach 2.148 seconds; body-to-closing pause is 3.842 seconds, including the scheduled two-second closing lead. Last detected speech ends at 196.391 seconds, leaving 3.109 seconds to end. These measurements show room for speech without end truncation; they do not verify spoken words. Approved narration text ends exactly: “That was our latest news. Stay with science, and stay tuned.” Descriptions correctly disclose contextual footage and separate upload Tags from hashtags.

Complete listening/viewing was unavailable. Pronunciation, every spoken word, final-sentence audibility, pacing and continuous motion remain unaccepted. Independent human complete audiovisual playback is required before promotion, final delivery or cleanup; do not change the human gate to passed from this report.

SHA-256: `394e114c49caf94efee7028c3f7b4a1c9110dda304cd4b70c6ae280c6e64d1dd`.

Evidence: `output_verification.json`; `build/video/2026-10-25/qa/{probe.json,decode.log,audio-analysis.log,black-analysis.log,contact.jpg,frames/}`.

## Controller acceptance record — 25 October 2026

User replied “onalıyorum” to the explicit complete viewing/listening checkpoint and linked review copy. Both human gates passed by user confirmation for the hash above; independent technical/sample report remains unchanged. Main promoted and hash-verified, previous main preserved. Historical references to unavailable full listening describe the automated QA stage; this user evidence supplies the final human gate.
