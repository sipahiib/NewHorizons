# NewHorizons — Active Coordination Record

This file contains only the current production state and active gates. Completed and superseded records are preserved in `video/archive/WORKFLOW_HISTORY.md` and must not be treated as current instructions.

## Governing main-video schedule — updated 18 September 2026

The required main-programme duration is **6:10 (370 seconds)**:

- Main story: **0:00–2:00** — 120 seconds, exactly eight 15-second visual segments.
- Support 1: **2:00–3:00** — 60 seconds, exactly five 12-second visual segments.
- Support 2: **3:00–4:00** — 60 seconds, exactly five 12-second visual segments.
- Support 3: **4:00–5:00** — 60 seconds, exactly five 12-second visual segments.
- Support 4: **5:00–6:00** — 60 seconds, exactly five 12-second visual segments.
- Closing CTA: **6:00–6:10** — 10 seconds.

The opening 20 seconds are part of the main story, not additional runtime. All current planning, narration, manifests, overlays, rendering and QA use boundaries 0/120/180/240/300/360/370 seconds. Historical 300- and 310-second schedules are obsolete.

## Current approval — 18 September 2026

The user approved the package in `video/SOURCES.md`:

- M1 polar ice-sheet loss — main hook M1-H1
- M2 xvr surgical-navigation AI
- M3 NTU artificial leaf
- M4 TRPM2 pain pathway
- M5 Ryugu M-S-H
- R1 ChatGPT for Word — Reel hook R1-H1
- R2 squid/ocean acidification — Reel hook R2-H1

This authorises in-repository media acquisition, final narration and rendering for that exact package. Material topic substitutions require new approval. Routine failed-media replacement within the documented real-footage policy does not. Publication, purchase, external permission requests, commits and GitHub pushes remain unauthorised.

The selected contextual motion files passed the recorded technical and visual preflight. Current files use Pexels contextual real footage under recorded source terms; persistent disclosures must prevent it from being presented as direct documentation of the reported event.

Delivery metadata requested by the user: provide current, topic-specific Instagram and YouTube hashtag examples and a separate copy-ready **YouTube Tags** upload-field list for every completed video. Keep tags distinct from hashtags and verify current platform guidance at delivery time. The current-cycle tag lists are in `video/YOUTUBE_TAGS.md`.

Do not create or deliver cover images or thumbnails. Historical cover assets are archive material and are not current production inputs.

## Active production gates

1. Verify news claims and real recorded-video candidates for every story. Distinguish actual event footage from contextual footage and document rights, availability and any still-image fallback.
2. Confirm that the approved topics, sources, motion candidates and hooks still match `video/SOURCES.md`. A material substitution returns to user approval.
3. Before required cleanup, enumerate previous-cycle audio/video paths and preserve non-media files and newly approved inputs.
4. Prepare final narration, overlays and manifests together on the governing 370-second timeline. Use Microsoft Edge TTS `en-GB-RyanNeural` at `-2%`.
5. Run an independent Reviewer check on the approved production package. Resolve blocking findings before render.
6. Render the main video and approved Reels to their required formats.
7. Run independent QA on the actual outputs: decode, inspect footage, listen to narration, verify codecs, resolution, frame rate, duration, sound, overlays, opening and closing.
8. Resolve blocking findings, deliver verified outputs and clean only inventoried disposable intermediates. Preserve approved sources, scripts, manifests, branding and current deliverables.

## Lean agent allocation

Use at most four sub-agent sessions for a normal cycle and never create nested agents.

| Stage | Default owner | Bounded handoff |
| --- | --- | --- |
| Research + motion candidates | One combined Researcher/Visual Designer agent | `RESEARCH_PACKET.md`, maximum 1,200 words |
| Integration + script | Controller | Approved scripts and manifests |
| Pre-render review | Independent Reviewer | `REVIEW.md`, maximum 600 words |
| Render | Controller or one Video Producer agent when delegation is materially useful | Render log and exact output paths |
| Output verification | Independent QA | `QA.md`, maximum 500 words |

Sub-agents receive a concise task packet, not the full conversation history. Later agents consume accepted handoffs instead of repeating research. Each agent normally receives at most one correction round. Short inspections, routine commands, small edits and integration remain with the controller.

## Per-cycle record

Create `video/cycles/YYYY-MM-DD/` only when a new editorial cycle begins. Use the following files as needed:

- `BRIEF.md` — scope, current rules and exact assignment boundaries
- `RESEARCH_PACKET.md` — selected stories, primary sources, claim limits and visual candidates
- `APPROVAL.md` — user-approved topics and hooks
- `REVIEW.md` — independent pre-render findings and resolution status
- `QA.md` — actual-output verification evidence

At cycle completion, record:

| Metric | Target |
| --- | --- |
| Sub-agent sessions | 4 or fewer |
| Full-history forks | 0 |
| Nested agents | 0 |
| Follow-up rounds | At most 1 per agent |
| Task-packet size | 1,500 words or fewer per agent |
| Total handoff size | 3,000 words or fewer |

Agent names document assignments; they do not imply continuously running processes. Stop each agent after its accepted handoff.
