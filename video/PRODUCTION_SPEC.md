# NewHorizons Production Specification

This is the single source of truth for production constants.

## Main programme

- Duration: **6:10 / 370 seconds**.
- Main story: **0:00–2:00**, using **3–4 relevant sourced still images and 3–4 relevant motion clips**.
- Four supporting stories: **2:00–6:00**, exactly **60 seconds** each. Every support uses **2 relevant sourced still images and 3 relevant motion clips**.
- Closing CTA: **6:00–6:10**.
- Output: **1920×1080, 60 fps, H.264/AAC** at `build/video/newhorizons.mp4`.

The opening is part of the main story:

- 0:00–0:05: state its most surprising result.
- 0:05–0:12: show strong supporting real footage.
- 0:12–0:20: briefly tease the four other stories, including “And four other breakthroughs happened this week…”
- From 0:20: continue directly into the main story.

The opening narration and overlays must fit within the first 20 seconds of the main story.

Set individual scene durations according to the narration and the amount of useful visual information. The main-story scenes must total exactly 120 seconds; each support's five scenes must total exactly 60 seconds. Do not force equal scene lengths when a different allocation improves clarity, but avoid unnecessarily long static holds or rapid cuts that make a visual difficult to understand.

Never add a channel intro or static cover. Never shorten the main story below 90 seconds or a support below 60 seconds.

## Visual policy

Use relevant sourced still images and real recorded footage together for every main-programme story. The main story must contain 3–4 stills and 3–4 motion clips; every support must contain 2 stills and 3 motion clips. Prefer direct event, product, research or institutional material for both formats, followed by clearly labelled contextual material. Stills are an intentional part of the visual mix and are not merely a last resort.

Record provenance, usage conditions, native resolution and whether each visual is actual, contextual or illustrative in the active `MEDIA_AUDIT.md`. Never present stock or context as the reported experiment. Do not use generated, procedural or illustrative animation as main-programme story imagery. Do not use legacy `png/` assets or animate a still with pan/zoom to imply footage.

Keep each cycle's inputs and intermediates isolated. Never treat a file as current merely because it exists under `assets/` or `build/`; it must be selected by the active, non-superseded manifest and pass the current cycle audit.

Use restrained headings and occasional one-sentence takeaways. Preserve subject visibility and mobile readability.

## Narration and closing

Use Microsoft Edge TTS `en-GB-RyanNeural` at `-2%`; changing the voice requires user approval. Measure actual speech and check for clipped words, unnatural pacing and unexplained silence.

The main closing uses cinematic glass, English labels, subtle panel entrance, Like response, Subscribe accent and an animated bell. Do not show a channel name or handle. End narration exactly: “That was our latest news. Stay with science, and stay tuned.”

## Reels

- Duration: **45–50 seconds**.
- Output: **1080×1920, 9:16, 60 fps, H.264/AAC** under `build/reels/`.
- Use exactly seven visual segments, combining topic-relevant sourced still images and motion clips. Do not build a Reel entirely from only one format when suitable material in both formats is available.
- Every Reel visual must directly correspond to the Reel's subject or the specific point being narrated. Do not use generic or unrelated imagery merely to fill time.
- Never reuse a still image or motion clip that appeared in a previous NewHorizons video or Reel. Download and audit new, topic-specific media for every Reel cycle.
- Fit measured narration within 45 seconds; finish speech before the end and leave no more than four seconds afterward.
- Preserve the complete landscape frame over a darkened, blurred duplicate background.
- Include YouTube `@newhorizons_21` and Instagram like/follow calls.

Do not create or deliver cover images or thumbnails for the main video or Reels.

## Delivery metadata

After **every** completed main video and Reel, and before closing the delivery workflow, create current topic-specific Instagram hashtags, YouTube hashtags and a separate copy-ready YouTube Tags upload-field list for that individual output. This step is mandatory for every production cycle and must not be skipped even when the user does not ask for metadata separately.

Store the lists in the active cycle's `DELIVERY_METADATA.md`, link that file from the cycle `BRIEF.md`, keep YouTube Tags distinct from hashtags and verify current platform guidance at delivery time. Do not mark the cycle complete until this metadata file exists for every rendered deliverable. Do not publish metadata without separate authorisation.
