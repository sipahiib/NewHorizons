# Output QA — 23 November 2026 (Main video)

MAIN_OUTPUT_QA: PASS

> Technical and visual output QA passes. **Full human audiovisual playback and listening acceptance by the user is still required** before final delivery, promotion to `build/video/newhorizons.mp4`, or marking `current_delivery_review.json` passed (`QA_CHECKLIST.md`).

## Target & integrity

- **File:** `build/video/2026-11-23/newhorizons.mp4` (121,531,921 bytes / 115.9 MiB)
- **SHA-256:** `e5965897168cb8affd1c45db53349ab430450b817fa5c69d4385049faf2fa7b9`
- **Decode integrity (`ffmpeg -v error -i ... -f null -`):** PASS (0 errors)
- **Video stream:** H.264 High (`avc1`), 1920×1080 (16:9), `yuv420p`, `bt709` (space/transfer/primaries), progressive, 60 fps (`60/1`), 15,420 frames, `257.000000 s` (4:17; <= 310 s ceiling), 3.61 Mbps.
- **Audio stream:** AAC LC (`mp4a`), 48,000 Hz, mono, 164.5 kbps, `257.000000 s`.
- **Delivery metadata:** `DELIVERY_METADATA.md` present with Instagram hashtags, 3 YouTube hashtags, and separate YouTube Tags upload list.

## Audio measurements

- **Loudness (`ebur128`):** Integrated `-16.2 LUFS`, LRA `3.0 LU`, True peak `-1.4 dBFS` (no clipping).
- **Boundary `silencedetect` (`-40 dB`, `0.3 s`):**
  - **Opening (0–16 s):** hook speech starts at 0.00 s; pauses at 3.60–5.23 s (1.64 s) and 10.25–11.77 s (1.51 s); teaser transitions cleanly into M1 body at 16 s.
  - **M1→M2 (135 s):** M1 ends at 133.03 s; 2.61 s transition pause (`133.03–135.64 s`); M2 starts cleanly at 135.64 s.
  - **Closing (247–257 s):** M2 ends at 244.68 s; 3.48 s transition pause into closing narration at 248.16 s (1.00 s mid-sentence pause at 249.65–250.65 s); final speech ends at 252.88 s with 4.12 s tail silence to 257.00 s. No clipped words or unexpected dead air detected.

## Rendered frame inspection (`tmp/2026-11-23-qa/`)

- **0:02 (`frame-00-00-02.png`):** SDO Mercury transit; translucent upper title card `"BEPICOLOMBO ENTERS MERCURY ORBIT"` legible, no series prefix or lower info card.
- **0:06 (`frame-00-00-06.png`):** BepiColombo 6th flyby; title card cleanly removed after 5.5 s.
- **0:13 (`frame-00-00-13.png`):** Mammography clinic contextual clip in M2 teaser window; no overlays.
- **0:32 (`frame-00-00-32.png`):** SDO transit with bottom-right YouTube card (`YouTube / Like • Subscribe • Join in / SUBSCRIBE`), legible, no paid-membership claim.
- **0:37 (`frame-00-00-37.png`):** SDO solar disk; YouTube card cleanly removed.
- **2:16 (`frame-00-02-16.png`):** Addenbrooke's Hospital exterior (blurred pillarbox); translucent upper title card `"UK AI BREAST SCREENING TRIAL"` legible, no prefix or lower card.
- **2:22 (`frame-00-02-22.png`):** Addenbrooke's exterior; title card cleanly removed.
- **3:15 (`frame-00-03-15.png`):** Cropped mammogram + MRI still; clean crop, all source text/labels removed.
- **4:09 & 4:14 (`frame-00-04-09.png`, `frame-00-04-14.png`):** Closing glass panel with `"LIKE • SUBSCRIBE"`, `"SUBSCRIBE"`, and animated yellow bell (visible tilt change); no channel name/handle. Non-blocking note: `"SUBSCRIBE"` sits slightly left of center; overall layout is clean and legible.
