# Reel media handoff — 15 October 2026

Status: source preparation complete; independent review and actual-output QA remain required. `APPROVAL.md` authorises both Reels. No rendering or TTS performed.

## Files and reproduction

`reel_media_sources.json` selects exactly seven segments per Reel and records URLs obtained from saved current source pages, credits, rights evidence, native dimensions, static crops, hashes and suggested timing. All sources freshly downloaded under `assets/motion/2026-10-15/reels/`; no previous-cycle media copied. Run `.tools-edge-tts/bin/python video/cycles/2026-10-15/fetch_reel_media.py` with network access to reproduce downloads, crops and manifest.

## R1

Seven faithful map-only crops: Figure 10 precipitation/wind/pressure, Figure 11 hurricane wind/pressure/precipitation, Figure 5c generated HiROv2 Prediction 0 Bora wind. Paper HTML explicitly records CC BY 4.0 and no selected figure caption names a third-party exception. Credit Anna Kwa et al., paper title, arXiv identifier and licence link; disclose crops. Creative Commons webpage direct download returned HTTP 403, but the paper's licence statement and link are saved.

These are scientific simulation outputs. Figure 5c is a conditional HiROv2 downscaling sample, whereas Figures 10–11 are free-running HiRO-ACEv2 examples. Narration must identify simulated fields. Crops retain plotted interiors, coastlines, grid, topography and vectors while removing titles, ticks and colourbars; do not claim quantitative colour values without a scale. Figure 10 crops are about 555×378 native; Figures 11 and 5c provide roughly 1,100-pixel panels. No reconstructed or AI-upscaled data.

## R2

Two distinct clean Aqua MODIS photographs: acquired 21 September (MODIS gallery published 23 September), and acquired 23 September (Earth Observatory). Native sizes: 5960×4555 and 2160×1740. Credit MODIS Land Rapid Response Team/NASA GSFC and NASA Earth Observatory/Michala Garrison respectively, plus listed data credits.

Five non-overlapping excerpts from the freshly downloaded 1920×1080, 30fps, 103.367-second SVS5681 date-free version: 22–26, 26–30, 30–35, 35–39 and 40–46 seconds. Four static storm/ocean crops remove country labels; final excerpt retains the whole frame during the 3D introduction before prominent rulers. Start/mid/end samples are in `svs_selected_inspection.jpg`. First crop is only 500×500 native: use restrained foreground sizing and inspect final mobile clarity. Other crops range from 800×600 to 1200×780. Suggested 0.8× playback is optional, providing useful pacing; disclose any slowdown and crops in credits/descriptions. Scene durations remain flexible within seven total segments and 45 seconds.

Credit: “NASA's Scientific Visualization Studio. Data provided by the joint NASA/JAXA GPM mission.” NASA/SVS informational-use conditions saved; no asset-specific third-party restriction found. Narration distinguishes satellite photography from satellite-derived rainfall visualization and must not imply quantified climate rainfall attribution.

The originally proposed third still is an SST anomaly map with labels, not a third natural-colour image. Controller accepted two photographs plus five visualization excerpts within the same approved route. Downloaded `r2_eo_sst.jpg` is explicitly excluded.

## Freshness and remaining gates

Checked 60 prior-cycle JSON files containing 535 distinct recorded SHA-256 values: no selected source or crop hash match and no source URL match. This verifies recorded provenance; undocumented transformed duplicates cannot be excluded by hashes alone. Reviewer should assess crop meaning, low-resolution panel clarity and the selected transition intervals. Do not render from excluded or inspection assets.
