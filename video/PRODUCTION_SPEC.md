# NewHorizons Production Specification

This is the single source of truth for production constants.

## Main programme

- Duration: **6:10 / 370 seconds**.
- Main story: **0:00–2:00**, exactly **8 × 15-second** visual segments.
- Four supporting stories: **2:00–6:00**, exactly **60 seconds** and **5 × 12-second** visual segments each.
- Closing CTA: **6:00–6:10**.
- Output: **1920×1080, 60 fps, H.264/AAC** at `build/video/newhorizons.mp4`.

The opening is part of the main story:

- 0:00–0:05: state its most surprising result.
- 0:05–0:12: show strong supporting real footage.
- 0:12–0:20: briefly tease the four other stories, including “And four other breakthroughs happened this week…”
- From 0:20: continue directly into the main story.

The opening narration and overlays must fit within the first two 15-second main-story segments.

Never add a channel intro or static cover. Never shorten the main story below 90 seconds or a support below 60 seconds.

## Visual policy

Use real recorded footage for every main-programme story. Prefer, in order: footage of the event/product/research; source-publisher or institution footage; clearly labelled contextual real footage. When suitable real video remains unavailable after documented availability and rights checks, use relevant sourced stills as a last resort.

Record provenance, usage conditions, native resolution and whether each visual is actual, contextual or illustrative in the active `MEDIA_AUDIT.md`. Never present stock or context as the reported experiment. Do not use generated, procedural or illustrative animation as main-programme story imagery. Do not use legacy `png/` assets or animate a still with pan/zoom to imply footage.

Keep each cycle's inputs and intermediates isolated. Never treat a file as current merely because it exists under `assets/` or `build/`; it must be selected by the active, non-superseded manifest and pass the current cycle audit.

Use restrained headings and occasional one-sentence takeaways. Preserve subject visibility and mobile readability.

## Narration and closing

Use Microsoft Edge TTS `en-GB-RyanNeural` at `-2%`; changing the voice requires user approval. Measure actual speech and check for clipped words, unnatural pacing and unexplained silence.

The main closing uses cinematic glass, English labels, subtle panel entrance, Like response, Subscribe accent and an animated bell. Do not show a channel name or handle. End narration exactly: “That was our latest news. Stay with science, and stay tuned.”

## Reels

- Duration: **45–50 seconds**.
- Output: **1080×1920, 9:16, 60 fps, H.264/AAC** under `build/reels/`.
- Use exactly seven motion clips.
- Fit measured narration within 45 seconds; finish speech before the end and leave no more than four seconds afterward.
- Preserve the complete landscape frame over a darkened, blurred duplicate background.
- Include YouTube `@newhorizons_21` and Instagram like/follow calls.

Do not create or deliver cover images or thumbnails for the main video or Reels.

## Delivery metadata

For every completed video, prepare current topic-specific Instagram and YouTube hashtag examples plus a separate copy-ready YouTube Tags upload-field list. Keep tags distinct from hashtags and verify current platform guidance at delivery time. Do not publish metadata without separate authorisation.
