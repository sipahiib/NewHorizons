# Independent actual-output QA — 2026-10-07

Status: **technical/sample PASS; full audiovisual acceptance PASS by user confirmation**. QA agent did not prepare or render these outputs. Resolved `REVIEW.md` records all three pre-render gates as PASS.

## Tested candidates

| Output | Resolution | Duration / frames | Loudness / true peak | Final speech gap |
| --- | --- | --- | --- | --- |
| Main | 1920×1080 | 310 s / 18,600 | −16.2 LUFS / −1.4 dBTP | 2.27 s |
| R1 | 1080×1920 | 45 s / 2,700 | −16.3 LUFS / −1.5 dBTP | 1.46 s |
| R2 | 1080×1920 | 45 s / 2,700 | −16.2 LUFS / −1.5 dBTP | 3.90 s |

Independently rerun probes and complete video/audio decodes pass without errors for all three: H.264/AAC, progressive 60 fps, correct duration/frame count. Decoded audio has zero full-scale samples. Gap estimates use −40 dB RMS windows; both Reels satisfy the four-second limit. Approximately four-second main pauses precede the scheduled 160/300-second section boundaries; pacing was reserved for full listening.

Inspected every scene's start/middle/end plus opening, section and CTA boundaries: 91 main samples and 26 per Reel. Main opening follows 0–5 / 5–12 / 12–16 seconds, story change is at 160, closing at 300. Webb imagery/hardware, processed comparison labels and contextual drone disclosures match the accepted package. Corrected final drone excerpt contains performance footage in sampled frames. Closing glass/text are readable; sampled entrance/bell states appear; animation continuity was reserved for full playback.

Each Reel has seven visual segments. Source/actual-center comparisons support complete landscape preservation over blurred dark backgrounds. Contract/ocean/2021 Gorner labels, rubric/simulation captions and unboxed YouTube `@newhorizons_21` / Instagram calls at 42–45 seconds are readable, including independently inspected 360-pixel mobile reductions. No series labels or lower information cards appear.

Main approved audio envelope correlations at 0/160/300 seconds are 0.9965/0.9960/0.9982; R1/R2 are 0.9935/0.9967. This supports alignment, **not** pronunciation, exact spoken words, pacing or complete listening. The required final sentence is present in approved narration; its perceptual completion was reserved for full listening.

## Exact SHA-256 and evidence

- Main: `87baebb1f90fc1ac354c727f9d354e0cfa7d52eea8321f95c030ae220a664155`
- R1: `c777febea60551262aca34735633efe65b23c5d6a145bfd76dc1efb39504ef5c`
- R2: `ae2281b28ab6a2997195901bb1ab0041fc5197a28b5a22db17b8704a4a42d97b`

Evidence: `build/video/2026-10-07/verification/qa-main/` and `build/reels/2026-10-07/verification/qa-{r1,r2}/`: metrics, probes, decode/sound logs, sampled frames, comparison/mobile sheets and independent checks.

## Human acceptance — controller record

On 7 October 2026, after receiving all three exact candidates and an explicit request to watch/listen completely before final approval, the user replied “onay veriyorum.” This is recorded as user-confirmed full audiovisual acceptance, independently of rendering; no agent listening is claimed. Both human statuses are `passed` and the gate is `PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK`. Hashes were rechecked before delivery. Shared main promotion is verified in `DELIVERY_RECEIPT.json`; the previous dated output is preserved. No publication or cleanup occurred.
