# Independent Pre-render Review — Correction Round — 2026-09-23

Status: **PASS**

No blocking or important pre-render findings remain. This was the single permitted correction round.

## Resolved findings

1. **Media state and integrity — resolved.** `current_media_manifest.json` is now `final-selection` and partitions all 43 assets into exactly 28 selected and 15 rejected IDs. `current_media_verification.json` contains the same 28 accepted and 15 rejected IDs, no pending reviews, and `downloaded: true` for all 43 assets. Every accepted asset has a 64-character SHA-256 value; rejected assets do not. I recomputed all 28 selected-file hashes locally: 28/28 match. The 28 unique paths consumed by the main and Reel render manifests exactly equal the accepted path set.

2. **Unsupported claim detail — resolved.** The four cited claims were narrowed in the production narration: “more than 185” is now “many”; the battery's unsupported “within two weeks” onset is removed; the Claude line now attributes coding results to Anthropic's own evaluations and retains the provider-benchmark caveat; the amoeba's five-minute/70°C recovery claim is removed. Approved hooks, topics and material limitations remain intact.

3. **Reel overlay root — resolved.** `generate_reel_overlays.mjs` now derives the repository root from `import.meta.dirname`, so output consistently lands in the same absolute `build/reels/overlays` directory consumed by `make_reels.sh`, regardless of caller working directory.

## Revalidated gates

- `ffprobe` reports the assembled main narration at exactly 370.000 seconds and its six padded sections at 120/60/60/60/60/10 seconds. Updated measured speech lengths are 116.616, 58.392, 58.032, 57.312, 59.640 and 9.864 seconds, all within their slots.
- The main scene manifest remains exactly 29 scenes and 370.000 seconds, uses only `2026-09-23` paths, and preserves the required 8 × 15-second main structure, four 5 × 12-second supports and 10-second closing.
- Reel audio is 43.896 seconds (R1) and 43.272 seconds (R2). The render logic produces 46.896- and 46.272-second outputs respectively, with exactly 3.000 seconds after speech and seven equal clips (6.699429 and 6.610286 seconds). All fourteen source/seek ranges remain long enough.
- Contextual disclosure labels, rights/source records, approved voice/rate, exact closing sentence, output formats and current-cycle isolation remain compliant.
- Updated shell/JavaScript syntax and JSON parsing checks pass.
