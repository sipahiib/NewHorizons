# Video Workspace Rules

This file applies to work below `video/`. Read the specialised policy named by the root routing table instead of loading every policy file.

- `EDITORIAL_POLICY.md` governs research, sources, claims, hooks and approval.
- `PRODUCTION_SPEC.md` is the single source of truth for timing, visuals, narration, formats and delivery paths.
- `QA_CHECKLIST.md` governs pre-render review and actual-output QA.
- `cycles/YYYY-MM-DD/` contains cycle-specific facts, decisions and evidence.

Do not put current-cycle approval or audit history into permanent policy files. Do not copy permanent technical specifications into cycle files; link to `PRODUCTION_SPEC.md` instead.

Use real recorded story footage under the hierarchy in `PRODUCTION_SPEC.md`. Any fallback must be recorded in the active cycle's `MEDIA_AUDIT.md`. Keep source attribution in `CREDITS.md` and factual research in the cycle's `RESEARCH_PACKET.md`.

Before media download, final narration, TTS or rendering, confirm that `APPROVAL.md` records user approval. A material topic, hook or factual-framing substitution returns to approval. Resolve blocking `REVIEW.md` findings before render and blocking `QA.md` findings before delivery.

Do not create or deliver thumbnails or cover images. Historical cover assets and cover-generation scripts are not current production inputs.

Preserve approved source assets, scripts, manifests, branding and current deliverables. Remove only specifically identified disposable intermediates after verified delivery. Never treat metadata-only checks as audiovisual QA.

Isolate every cycle's source assets, manifests and disposable intermediates. Do not copy media from another cycle into an active package unless provenance, rights, subject correspondence and file hashes are reverified and recorded. A manifest marked superseded, historical or legacy is never an active production input.

Historical entry points are listed in `LEGACY_SCRIPTS.md` and fail closed without an explicit cycle flag. `download_current_media.mjs` accepts only an explicit repository-local manifest whose status is `approved-for-download`.
