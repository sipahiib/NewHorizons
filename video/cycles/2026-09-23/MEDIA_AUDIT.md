# Media Audit — 2026-09-23

Status: **final selection reviewed; ready for independent pre-render review**.

The active manifest contains 43 locally downloaded assets. Technical verification completed 43/43 with valid video streams. The final scene manifest uses only current-cycle paths; no prior-cycle file is an input. Selected assets were visually inspected for subject correspondence, duration and misleading framing. SHA-256 hashes were computed for every selected main-programme source after download.

## Final selection

- **M1 — Mars:** NASA/JPL-Caltech “Meet the Mars Samples: Lefroy Bay” MP4, direct Margin Unit/sample footage. The 59.526-second source is reused at distinct timecodes across the eight scenes; the final two excerpts loop where the cleared direct source is shorter than the 120-second section. On-screen label: “NASA/JPL Margin Unit sample footage.”
- **M2 — cybersecurity AI:** five Pexels clips of real computer/security work. They do not show the Korean model or measured performance. Persistent label: “Contextual cybersecurity footage — not the announced model.”
- **M3 — factory AI:** three Pexels sources showing factory workers and machinery, with the longest source reused at separated timecodes. Earlier candidates containing visible Chinese signage were rejected. Persistent label: “Contextual factory footage — not the Korean hackathon.”
- **M4 — bioresorbable battery:** four real laboratory sources; two are reused/looped to fill the five scenes. They do not depict the battery or pig experiment. Direct paper figures were not selected because editable reuse rights were not established. Persistent label: “Contextual laboratory footage — not the reported battery.”
- **M5 — Arctic melt season:** five Pexels sea-ice/frozen-sea sources. Glacier/land-ice candidates were rejected so the imagery is not mislabelled as sea ice. Persistent label: “Contextual sea-ice footage — not the study measurements.”
- **R1 — Claude Opus 5.5:** seven contextual computer/workflow clips. Persistent label: “Contextual workflow footage — not a Claude product demo.”
- **R2 — fire amoeba:** geothermal and laboratory footage drawn from three sufficiently long Pexels sources at separated timecodes. The short hot-spring candidate was rejected. Publisher-hosted microscopy was excluded because its CC BY-NC-ND licence does not permit the intended edit. Persistent label: “Contextual geothermal/lab footage — not the reported amoeba.”

## Rights and provenance

- NASA source page: <https://science.nasa.gov/resource/meet-the-mars-samples-lefroy-bay-sample-23/>; credit NASA/JPL-Caltech. Use remains subject to NASA media guidelines and the source-page credit.
- Pexels assets retain their individual source pages and creator credits in `../../current_media_manifest.json`; use is governed by the Pexels licence linked there.
- `../../current_media_verification.json` records download time, resolution, codec, duration and local path for all 43 files.
- `../../editorial_scenes.tsv` is the authoritative final selection and timecode manifest.

## Known limitations accepted for review

No direct reusable event footage was found for M2–M5 or either Reel. Those sections therefore use clearly labelled contextual real footage. M1 has direct footage but only one cleared motion source, producing deliberate time-separated reuse. These limitations must remain visible and must not be obscured by titles.
