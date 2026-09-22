# NewHorizons Repository Guide

## Scope and authority

Work only in `/Users/is9565/Downloads/NewHorizons`. Explicit user instructions override repository guidance. Use `newhorizons-start` only when the user sends the exact command `/start`; that command always opens a new dated editorial cycle and does not silently resume an older pending cycle.

Never publish, purchase, request external permission or push unless the user separately authorises that action. Ask before every GitHub push and confirm an unclear target. Keep media local: never commit or push `.mp3`, `.mp4`, `.m4a`, `.mov`, `.wav`, `.webm` or `build/video/editorial-en/`. Version only reproducible scripts, text, manifests and metadata.

## Read only what the task needs

Do not load all project Markdown by default. Use this routing table:

| Task | Required context |
| --- | --- |
| Start a new cycle or research stories | `RESEARCH.md`, `video/EDITORIAL_POLICY.md`; read an older `BRIEF.md` only to prevent repetition |
| Write narration or select media | active `RESEARCH_PACKET.md`, `APPROVAL.md`, `video/PRODUCTION_SPEC.md` |
| Review before render | active `RESEARCH_PACKET.md`, `APPROVAL.md`, relevant manifests and `video/PRODUCTION_SPEC.md`; write `REVIEW.md` |
| Render | active `APPROVAL.md`, resolved `REVIEW.md`, `video/PRODUCTION_SPEC.md` |
| Verify output | active `APPROVAL.md`, resolved `REVIEW.md`, `video/QA_CHECKLIST.md`, actual outputs and verification manifests; write `QA.md` |
| Small code or metadata edit | this file and the directly affected files only |

`video/SOURCES.md` and `video/WORKFLOW.md` are short pointers, not complete task packets. The active cycle is declared in both. Historical material under `video/archive/` is read only when investigating history.

## Workflow boundaries

Store every editorial cycle under `video/cycles/YYYY-MM-DD/`. Preserve prior cycles; never replace history by clearing a shared file. A topic change after approval requires new user approval. Routine corrections that preserve the approved editorial package do not.

Use sub-agents only for substantial parallel research or required independence. Do not create nested agents. A normal cycle uses at most four sub-agent sessions, no full-history forks and at most one correction round per agent. Reviewer must be independent of the work reviewed; output QA must be independent of the render. The controller performs small edits, integration and routine commands.

Later agents consume accepted handoffs instead of repeating research. Reviewer reopens only unsupported, contradictory or materially incomplete claims; QA evaluates the rendered outputs rather than redoing editorial research.

Each agent receives one bounded deliverable, exact readable/writable files and acceptance criteria. Target limits: 1,500 words per task packet; 1,200 words for research handoff; 600 for review; 500 for QA; 3,000 total handoff words per cycle.

At cycle completion, record sub-agent sessions, full-history forks, nested agents, follow-up rounds and handoff word counts in the cycle `BRIEF.md`.

Keep narration, manifests and render scripts in `video/`, motion assets in `assets/motion/`, branding in `assets/branding/`, the main output at `build/video/newhorizons.mp4`, and approved Reels in `build/reels/`. Files below `video/` also follow `video/AGENTS.md`.
