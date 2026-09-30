# Narration preparation — 2026-09-30

Approved topics and hooks are in `APPROVAL.md`. The draft script is in `narration.json`; cycle-isolated generated audio is under `build/video/2026-09-30/audio/`. Voice: Microsoft Edge TTS `en-GB-RyanNeural` at `-2%`, with no time stretching. One second of intentional opening alignment silence is inserted in M1. No earlier audio was reused.

Measured file durations in `audio_measurements.json`: M1 117.280/120 seconds; M2 58.656/60; M3 58.680/60; M4 58.488/60; M5 58.632/60; closing 8.856/10; R1 42.456/45; R2 42.840/45. These are file durations, not verified final speech-end times. Both Reels are planned at 45 seconds. Independent pre-render review passed; full audiovisual output QA remains open.

The first TTS pass found M2 too long and M3/M5/R1 too short for their targets. The text was revised and remeasured; the figures above reflect the second/final sizing pass. The production spec's exact closing sentence is preserved.

The first M1 line was revised after review to state the gravity-assist result within five seconds, followed by approved question hook 2. Its TTS file was regenerated and remeasured.

After sampled output QA found an extended quiet handoff, M5 gained the source-consistent sentence “Now it needs field testing.” Its independent correction review is in `AUDIO_REVISION_REVIEW.md`; the main audio stream was remuxed without changing video frames.
