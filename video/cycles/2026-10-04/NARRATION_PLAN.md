# Narration Plan — 2026-10-04

Approved main runtime: 310 seconds. Exact approved hooks are retained in `narration.json`; voice/rate follow [PRODUCTION_SPEC.md](../../PRODUCTION_SPEC.md). Actual measurements are in `audio_measurements.json`. No speech stretching was used.

| Timeline | Narration source | Measured speech | Padding |
| --- | --- | --- | --- |
| 0–5 | m1_hook | 3.408s | 1.592s |
| 5–12 | m1_footage | 6.816s | 0.184s |
| 12–16 | m1_teaser | 3.888s | 0.112s |
| 16–160 | m1_body | 143.664s | 0.336s |
| 160–300 | m2 | 136.008s | 3.992s |
| 300–310 | closing | 8.640s | 1.360s |
| R1 0–45 | r1 | 42.480s | 2.520s |
| R2 0–45 | r2 | 42.120s including pause | 2.880s |

Opening hook uses the actual current spoofed-phone photograph; 5–12s uses recorded ESA field footage with an archival label; 12–16s shows contextual wearable footage while teasing M2. There is no channel intro or cover. Main first story audio is assembled from four measured files with padding to the stated boundaries. The body has no extra silent insertions. Source clip audio is removed; only narration enters the mix. Final loudness normalisation does not change time.

The ending sentence is exactly the prescribed sentence. Reel CTA begins at 42s and remains to 45s; speech already fits 45s, and the actual output gap must also be measured in QA. Main figures appear while the method/results/limitations are discussed; contextual footage is disclosed persistently.

The final main-video claim about clinical benefit remains a possibility requiring prospective validation. R1 reports clinician preference, not a patient-outcome improvement. R2 reports collected measurements and research goals, not a completed warning system. Full-text methods were verified in `SOURCE_VERIFICATION.md`.

Independent pre-render review precedes final renders. Complete listening and output QA follow rendering; the above file durations do not establish audio quality or pronunciation.

Output QA found the original R2 final silence was4.272s despite the MP3 container duration. A0.6s sentence pause was inserted at23.85s, inside the independently identified silent interval23.344–24.347s. Approved text, voice, rate and45s runtime are retained. The original source is preserved as `audio/r2.source.mp3`; `correct_r2_audio.py` reproduces the correction. Independent QA remeasures the actual final gap after remux.
