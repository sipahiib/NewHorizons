# Pre-render review — 23 November 2026 (Main video)

MAIN_RENDER_GATE: PASS

Scope: independent pre-render review of the main programme only (no Reels approved). Checked against `PRODUCTION_SPEC.md`, `QA_CHECKLIST.md`, `APPROVAL.md`, `RESEARCH_PACKET.md`, `MEDIA_AUDIT.md`, `CREDITS.md`, `NARRATION_PLAN.md`, `main_audio_measurements.json`, `main_manifest.json`, `render_main.py`, `make_main_overlays.swift`, and rendered preview/overlay PNGs.

## Blocking checks — all PASS

1. **Approval & scope**
   - `APPROVAL.md` records user approval for M1 BepiColombo (lead), M2 EDITH (second), both verbatim hooks, no Reels, and Edge TTS synthesis (`en-GB-RyanNeural` at `-2%`).
   - `main_manifest.json` and `render_main.py` enforce cycle isolation, approval/review gates, and SHA-256 verification of all inputs and overlays.

2. **Factual framing & limitations**
   - **M1:** Uses ESA's wording for the shorter-than-planned braking burn caused by a software issue, keeps the initial orbit and downstream schedule explicitly uncertain pending assessment, omits the unverified cost figure, and frames the 590 × 11,640 km figure as the *planned* initial polar orbit (pinned to `esa.int` in `MEDIA_AUDIT.md`).
   - **M2:** Clearly states this is a trial launch with no results yet, keeps £10 m NIHR funding as the single financial figure, states that NHS clinicians retain all clinical decisions, and omits the unverified ministerial visit.

3. **Timing & audio**
   - Total planned runtime is **257.0 s (4:17)** (<= 310 s ceiling): opening **16.0 s** (0–5, 5–12, 12–16 s), M1 total **135.0 s**, M2 **112.0 s** (combined **247.0 s** <= 300 s), closing **10.0 s**.
   - Measured TTS (`en-GB-RyanNeural`, `-2%`) fits every window without clipping: hook 4.464 s, support 6.072 s, trimmed teaser 4.3 s (4.19 s speech at 11.70–15.95 s), M1 body 117.912 s in 119 s, M2 110.184 s (+0.4 s lead) in 112 s, closing 5.736 s (+1.0 s lead) in 10 s.
   - Closing sentence matches verbatim: *"That was our latest news. Stay with science, and stay tuned."*

4. **Visuals & overlays**
   - Real footage and stills only (M1: 6 unique motion files / 8 scenes + 5 stills; M2: 4 unique motion files / 6 scenes + 4 stills; counts recorded in `main_manifest.json`), with zero cross-cycle hash collisions (`prior_cycle_hash_collisions: []`) and no generated/CGI animation.
   - Contextual and archive sources (NASA SDO, ESOC, mammography clinic, London NHS exteriors, scan-review clips) are disclosed in narration and `CREDITS.md`.
   - Title cards (`title-bepicolombo.png`, `title-edith.png`) use 62% opacity (`alpha: 0.62`), omit `"NEW HORIZONS • M1/M2"`, and display for 5.5 s at each story start only. No lower info card or other editorial text appears.
   - YouTube card (`subscribe.png`) runs at 00:30–00:35.5 (5.5 s) with no paid-membership claim. Closing uses glass panel, Like/Subscribe accents, and animated bell with no channel name or handle.
   - Inspected preview frames (`preview-m1-00/01/02/05/10/12.png`, `preview-m2-00/02/03/04/05/08.png`) confirm clean crops without embedded captions or labels.

## Non-blocking observations

- `MEDIA_AUDIT.md` describes `m2-s04-mammogram-mri.jpg` as cropping the left mammogram panel only, whereas `main_manifest.json` (`1340:940:680:350`, `preview-m2-05.png`) shows both the mammogram and MRI panels cleanly with all text removed.
- At 5.0–5.5 s (`preview-m1-01.png`), the M1 title bar briefly overlaps the top-left ESA corner watermark for 0.5 s; title text remains readable.
- `preview-m2-08.png` shows real exterior signage reading "Addenbrooke's Dialysis Centre" and `preview-m2-02.png` shows a "University of Birmingham" health research bus parked at Addenbrooke's; neither is an embedded graphic label, though worth noting during output QA.
- In `render_main.py`, the closing Like highlight box (`x=575:y=389:w=180:h=85`) sits slightly left/above `"LIKE • SUBSCRIBE"` (`x=670` in `closing-panel.png`); verify visual balance in rendered QA.
