# Repository Guidelines

## Project Scope

Work only in `/Users/is9565/Downloads/NewHorizons`. Use `NewHorizons` for the project and `newhorizons-start` for its startup skill. Read `RESEARCH.md` for the research brief and `video/SOURCES.md` for the current editorial package. Explicit user instructions override this guide.

Keep sources in `video/SOURCES.md`, narration/manifests/render scripts in `video/`, motion assets in `assets/motion/`, and branding in `assets/branding/`. Deliver the main video to `build/video/newhorizons.mp4` and approved Reels to `build/reels/`.

## Rules

- Select one visually compelling main story with broad audience relevance and four supporting stories. Verify claims with reliable primary sources; distinguish publication dates from event dates and findings from speculation.
- Every story must answer: **What happened? Who did it/source? Why does it matter? How could it affect the viewer?** Explain practical relevance without promising unproven benefits.
- Use the approved **6:10** schedule: main story **0:00–2:00**, four supports **60 seconds each**, closing **6:00–6:10**. The first 20 seconds belong to the main story, not an additional intro. Never shorten the main below 90 seconds or a support below 60 seconds.
- Open immediately with relevant motion footage, never a channel intro or static cover:
  - **0:00–0:05:** a striking, factually accurate announcement, e.g. “This week, researchers revealed…”
  - **0:05–0:12:** a visual hook showing the main development.
  - **0:12–0:20:** frame the programme, e.g. “Four more important developments are coming. Let's begin with the biggest.”
- Use natural English for narration, headings and calls to action. Avoid the fixed introduction “First of our news is.” Limit each topic to one important financial figure or point.

## Agent Workflow & Approval

The main controller assigns tasks, integrates accepted outputs and owns production and delivery approval. Use these roles in stages within available agent slots:

- **Researcher:** verified stories, source links, dates and claim limitations.
- **Scriptwriter:** timed English narration, hook options and screen text.
- **Visual Designer:** five motion candidates per topic, storyboard and usage conditions.
- **Reviewer:** independent factual, editorial and rule checks before production.
- **Video Producer:** narration and render from the approved package.
- **QA:** independent inspection of the actual video and recorded verification results.

Agents work on separate assigned artifacts; the controller integrates shared-file changes. Reviewer must not approve their own authored work; QA must not approve their own render. Completion claims require evidence, not merely a “done” report.

Present topics, sources, motion candidates and several main-story English hooks together for user approval. Record the selected package and hook; prior-cycle approval does not cover new content. Obtain approval before media downloads, final narration or rendering. After editorial approval, resolve routine corrections autonomously; ask again only for a material change to the approved package. The controller authorizes rendering after Reviewer findings are resolved, then authorizes delivery after QA.

## Visuals & Audio

- Main video: **1920×1080, 60 fps, H.264/AAC**.
- For the main programme, use real recorded video footage for every story; do not use generated, procedural or illustrative animation as story visuals. Prefer footage of the reported event, product, research or institution, then clearly labelled contextual real footage. If no suitable real video can be found after checking availability and usage rights, relevant sourced still images are an allowed fallback. Record the fallback and its reason in `video/SOURCES.md`, and never present a contextual still as direct documentation of the reported event.
- Each news topic normally uses exactly **five distinct visual segments**: main **5 × 24 seconds**, each support **5 × 12 seconds**. The opening's 5/7/8 narration and overlays fit within the first main segment. A sourced still-image segment is permitted only under the real-video fallback rule above; do not use legacy `png/` assets or turn a still into purported news footage with pan/zoom.
- Prefer source-publisher footage. Record provenance, usage conditions, native resolution and whether footage is actual, contextual or illustrative. Do not pass stock or generated visuals off as the reported experiment.
- Use restrained animated headings and exceptional one-sentence takeaways; preserve subject visibility and mobile readability.
- Use Microsoft Edge TTS **`en-GB-RyanNeural` at `-2%`**. Changing the voice requires user approval. Measure actual speech duration and check timing adjustments for clipped words, unnatural pacing or unexplained silence.
- Main closing: the final ten seconds use the cinematic-glass CTA with English labels, subtle panel entrance, Like response, Subscribe accent and animated bell. No channel name or handle.
- End the main narration exactly: **“That was our latest news. Stay with science, and stay tuned.”**

## Reels

For each new main-video cycle, propose two independent Reels: **Future of AI** and **The Planet Earth**. Prioritize reliable, useful, engaging material and avoid repeated topics. Append candidates below the main stories in `video/SOURCES.md`, preserving those stories. Apply the same editorial approval process; produce one Reel per approved topic.

Reels: **45-50 seconds, 1080×1920, 9:16, 60 fps, H.264/AAC**, with seven motion clips each. Fit measured narration within 45 seconds; finish speech before the video ends and leave at most four seconds afterward. Preserve complete landscape frames over a darkened, blurred duplicate background. Closing calls include YouTube **`@newhorizons_21`** and Instagram like/follow.

Do not create or deliver cover images or thumbnails for the main video or Reels. Existing historical cover files may be preserved, but they must not be treated as current deliverables or reused as video intros, closing backgrounds or production inputs.

## Verification & Delivery

Before render, verify approved inputs, per-story clip counts/durations, narration timing, source-to-visual correspondence, and ordered, nonoverlapping, in-range overlays. After render, verify full-file decoding, codecs, resolution, frame rate, actual duration, speech completeness, sound levels, readable overlays, opening and closing. Inspect the actual footage and listen to narration; metadata alone is insufficient. Resolve blocking findings before delivery.

Isolate each cycle's inputs and intermediates to prevent stale media reuse. After verified delivery, remove only identified disposable intermediates and obsolete outputs. Preserve approved source assets, scripts, manifests, branding and current main/Reels deliverables.

Ask before GitHub push; confirm the target if unclear. Never commit or push `.mp3`, `.mp4`, or `build/video/editorial-en/`. Keep media local and version only reproducible scripts, text, manifests and metadata.
