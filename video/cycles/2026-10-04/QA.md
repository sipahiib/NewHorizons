# Independent Actual-output QA — 2026-10-04

Status: **passed; technical checks and user audiovisual acceptance complete**. QA was independent of preparation/render. No technical or sampled visual blocker remains after one R2 correction. The user completed the final acceptance gate under [QA_CHECKLIST.md](../../QA_CHECKLIST.md).

| Output | Actual video | Frames | Sound | Final silence |
| --- | --- | --- | --- | --- |
| Main | 310.000s, 1920×1080, 60fps | 18,600 | −16.3 LUFS; −1.4dBFS true peak | 2.224s |
| R1 | 45.000s, 1080×1920, 60fps | 2,700 | −16.2 LUFS; −1.5dBFS true peak | 3.355s |
| R2 corrected | 45.000s, 1080×1920, 60fps | 2,700 | −16.3 LUFS; −1.5dBFS true peak | 3.672s |

All three actual files passed full video/audio decode with error escalation, H.264/AAC probing and decoded frame counting. Decoded PCM had zero full-scale samples. Silence uses −40dB/minimum0.4s; independent10ms RMS final gaps were2.27/3.40/3.76s. Internal pauses follow narration/source padding. Human pacing attention: main295.129–300.227s contains5.098s planned story-boundary silence including source tail.

Inspected actual start/middle/end frames of all25main scenes and each Reel’s seven segments, plus opening/boundary/closing/CTA frames. Main opening follows0–5s current spoofed-phone still,5–12s real archival field footage,12–16s wearable teaser; story/closing boundaries are160/300s. Current2026, archive2025, healthcare-context and retrospective-study labels are visible. Samples contain relevant recorded footage/stills/figures, readable titles, no channel intro/cover, prohibited series label or lower information card, and no residual ESA documentary captions. Closing samples show English glass panel, Subscribe accent and changing bell positions without channel handle. Reel full-source/actual-center comparisons confirm preserved source edges over darkened blurred backgrounds; unboxed YouTube@newhorizons_21 and Instagram Like & Follow appear exactly42–45s.

Main closing waveform correlates0.998 with approved closing audio starting300s. Its source text ends exactly: “That was our latest news. Stay with science, and stay tuned.” This confirms waveform alignment, not semantic listening. Reel audio correlations exceed0.994.

R2 initially had4.272s final silence. Controller inserted0.6s at verified silent23.85s. Independent correction decode/sound/hash checks pass; encoded video packet hash and all26sampled frames are unchanged. Corrected sentence pause is1.569s.

SHA-256:

- Main: `94a668f49e8f80392835b0c97b85e1c411a8826b6f8b5585c8a67e5b7d9db578`
- R1: `052010cd6b070ab8ef40414f2e8077f484658a15610ecbe5672649c2e1180197`
- R2: `913018dee749bbddbacd3f8b8a6dc6f023c48851a7a99ecba26d7569061d4c49`

Evidence: `build/video/2026-10-04/verification/qa-main/` and `build/reels/2026-10-04/verification/qa-r1/`, `qa-r2/`, `qa-r2-initial/`: probes, decode logs, sound logs, decoded local audio, waveforms, full-resolution frames, contacts and source comparisons. [delivery_review.json](delivery_review.json) records paths/gates; [qa_outputs.py](qa_outputs.py) reproduces checks.

## Human acceptance and delivery

On 2026-10-04T14:44:52+03:00, the user replied “onay veriyorum” to the request for complete viewing/listening approval of all three linked outputs. Both human approval fields are passed on that explicit acceptance; this is user evidence, not automated perceptual listening. Gate: `PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK`. Main promoted to `build/video/newhorizons.mp4`; hash unchanged. Reels remain at their approved dated paths.
