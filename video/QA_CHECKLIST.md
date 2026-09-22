# NewHorizons Verification Checklist

## Before render

Confirm and record in the active `REVIEW.md`:

- `APPROVAL.md` covers every selected topic, Reel and hook;
- claims, dates and limitations match `RESEARCH_PACKET.md`;
- every asset appears in `MEDIA_AUDIT.md` with provenance, rights condition, resolution and direct/contextual/fallback status;
- main and Reel clip counts and durations match `PRODUCTION_SPEC.md`;
- narration fits measured time without stretching, clipping or unexplained silence;
- overlays are ordered, nonoverlapping, in range and readable;
- source-to-visual correspondence and persistent limitation labels are accurate;
- no stale media, cover or thumbnail enters the render;
- all blocking review findings are resolved.

The reviewer must be independent of the package they approve.

## After render

Confirm and record in the active `QA.md`:

- full-file decode succeeds;
- codecs, resolution, frame rate, frame count and actual duration are correct;
- opening, story boundaries and closing match the production specification;
- actual footage is relevant and disclosures are readable;
- complete narration has been listened to for pronunciation, missing/clipped words and pacing;
- sound level, silence and final speech-to-end gap are acceptable;
- overlays and mobile layouts are visually inspected in rendered output;
- main final sentence and Reel calls to action are complete;
- SHA-256 hashes and verification artifact paths are recorded.

Metadata and contact sheets do not replace watching the footage and listening to the complete narration. QA must be independent of the render. Blocking findings prevent delivery.

Only after independent full audiovisual playback passes, record the evidence in the cycle `QA.md`, set both human-approval `status` fields in `current_delivery_review.json` to `passed`, and set its machine gate to `PASS_FULL_HUMAN_AUDIOVISUAL_PLAYBACK`. Cleanup must remain blocked for every other value.

After verified delivery, remove only inventoried disposable intermediates. Preserve approved sources, scripts, manifests, branding and current deliverables.
