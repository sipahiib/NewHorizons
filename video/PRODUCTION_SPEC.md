# NewHorizons Production Specification

This is the single source of truth for production constants.

## Main programme

- Duration: **5:00–5:30 / 300–330 seconds**. Default planning target: **5:10 / 310 seconds**; fix the exact runtime in the active cycle's approval and narration plan.
- Lead story at the default target: **0:00–2:40 / 160 seconds**.
- Second story at the default target: **2:40–5:00 / 140 seconds**.
- Closing CTA at the default target: **5:00–5:10 / 10 seconds**. Adjust story durations when an approved cycle chooses another total within the range.
- Output: **1920×1080, 60 fps, H.264/AAC** at `build/video/newhorizons.mp4`.

The opening is part of the main story:

- 0:00–0:05: state its most surprising result.
- 0:05–0:12: show strong supporting real footage.
- 0:12–0:16: briefly tease the second story.
- From 0:16: continue directly into the lead story.

The opening narration and overlays must fit within the first 16 seconds of the lead story.

Set individual scene durations according to the narration and the amount of useful visual information. At the default target, the lead-story scenes must total 160 seconds and the second-story scenes 140 seconds; their sum plus the closing must match the cycle's approved runtime. Do not force equal scene lengths when a different allocation improves clarity, but avoid unnecessarily long static holds or rapid cuts that make a visual difficult to understand.

Never add a channel intro or static cover. Keep enough time for both approved stories to explain the evidence, limits and viewer relevance; do not cut either story merely to meet an arbitrary equal split.

## Visual policy

Use relevant sourced still images and real recorded footage together for both main-programme stories. At the default runtime, use **5 stills and 7 motion clips for the lead story, and 4 stills and 6 motion clips for the second story** as adaptable planning targets, not fixed quotas. Adjust the counts to the approved narration and available relevant media while avoiding long static holds; record the selected counts in the cycle's media manifest. Prefer direct event, product, research or institutional material for both formats, followed by clearly labelled contextual material. Stills are an intentional part of the visual mix and are not merely a last resort.

Record provenance, usage conditions, native resolution and whether each visual is actual, contextual or illustrative in the active `MEDIA_AUDIT.md`. Never present stock or context as the reported experiment. Do not use generated, procedural or illustrative animation as main-programme story imagery. Do not use legacy `png/` assets or animate a still with pan/zoom to imply footage.

Keep each cycle's inputs and intermediates isolated. Never treat a file as current merely because it exists under `assets/` or `build/`; it must be selected by the active, non-superseded manifest and pass the current cycle audit.

Use restrained headings and occasional one-sentence takeaways. Preserve subject visibility and mobile readability.

For main-programme story overlays:

- Omit the “NEW HORIZONS • M1/M2” line above story titles. Show only the story title in the upper title card.
- Remove the lower source-and-note information card entirely. Keep full source credits in the active cycle's `CREDITS.md`; show any essential context disclosure separately on screen.
- Make remaining information-card backgrounds 30 percentage points more transparent than the current design (for example, 92% opacity becomes 62%, and 93% becomes 63%). Keep the text readable. This does not change the main closing CTA.

## Narration and closing

Use Microsoft Edge TTS `en-GB-RyanNeural` at `-2%`; changing the voice requires user approval. Measure actual speech and check for clipped words, unnatural pacing and unexplained silence.

The main closing uses cinematic glass, English labels, subtle panel entrance, Like response, Subscribe accent and an animated bell. Do not show a channel name or handle. End narration exactly: “That was our latest news. Stay with science, and stay tuned.”

## Reels

- Duration: **45–50 seconds**.
- Output: **1080×1920, 9:16, 60 fps, H.264/AAC** under `build/reels/`.
- Use exactly seven visual segments in total. Each segment may use a topic-relevant sourced still image or motion clip; any mix is allowed, such as four clips plus three stills or five clips plus two stills.
- Every Reel visual must directly correspond to the Reel's subject or the specific point being narrated. Do not use generic or unrelated imagery merely to fill time.
- Never reuse a still image or motion clip that appeared in a previous NewHorizons video or Reel. Download and audit new, topic-specific media for every Reel cycle.
- Fit measured narration within 45 seconds; finish speech before the end and leave no more than four seconds afterward.
- Preserve the complete landscape frame over a darkened, blurred duplicate background.
- Include YouTube `@newhorizons_21` and Instagram like/follow calls.
- Do not show series labels such as “THE FUTURE OF AI” or “THE PLANET EARTH” in the top title card. Do not use a lower information card; show the required YouTube and Instagram calls as unboxed text in the final seconds.
- Set the top title card background to **64% opacity** (30 percentage points more transparent than the former 94% background) and keep the title readable.

Do not create or deliver cover images or thumbnails for the main video or Reels.

## Delivery metadata

After **every** completed main video and Reel, and before closing the delivery workflow, create current topic-specific Instagram hashtags, YouTube hashtags and a separate copy-ready YouTube Tags upload-field list for that individual output. This step is mandatory for every production cycle and must not be skipped even when the user does not ask for metadata separately.

Store the lists in the active cycle's `DELIVERY_METADATA.md`, link that file from the cycle `BRIEF.md`, keep YouTube Tags distinct from hashtags and verify current platform guidance at delivery time. Do not mark the cycle complete until this metadata file exists for every rendered deliverable. Do not publish metadata without separate authorisation.
