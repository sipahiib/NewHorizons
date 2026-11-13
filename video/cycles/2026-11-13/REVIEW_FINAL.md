# Independent R2 pre-render review — 13 November 2026

R2_RENDER_GATE: PASS

This pass covers the local R2 render only. Publication and distribution are not authorised or cleared by this review.

## Correction review

I recomputed SHA-1 for all six selected Commons files: each matches the source SHA-1 recorded from Wikimedia's API in `r2_source_metadata.json`. Their source titles, creators, dimensions, license URLs and local SHA-256 values are recorded in the metadata and credits. The NASA still visually corresponds to the Flow Country satellite image and the audit records its NASA/USGS credit, local hash and resized dimensions. The earlier incorrect files remain excluded.

The updated audit documents a no-hit search of prior cycle and archive text for the source IDs and names, and a 699-file exact-byte scan of prior local media. The text-result file is empty. This is reasonable available evidence, but neither test can exclude unrecorded or transformed earlier use. The audit identifies that limitation.

The Commons images are identified as CC BY-SA 2.0; attribution, source and license links and resizing are recorded. The audit explicitly reserves the adaptation, share-alike and compatibility decision for before distribution. That unresolved downstream decision does not prevent the local render; it must be resolved with required notices and any necessary user decision before distribution. NASA usage conditions also apply. The audit's earlier progress notes are historical and its further-verification section is current; label the historical status clearly when integrating this review.

## Other checks

R2-A, shortened narration and TTS are approved; R1 is excluded. Approval records the user's complete listening and acceptance. Audio measures 44.256 s; silence detection at -40 dB estimates speech end around 43.36 s, leaving about 2.64 s in the planned 46 s output. Seven distinct stills total 46 s and match manifest hashes. Inspected images are consistent with the subject; no cover is selected.

The title preview is readable and the CTA PNG is unboxed. The script schedules the title for 0–5.5 s and CTA for 43–46 s, and uses a blurred background and full foreground frame. Its gate reads `REVIEW.md`; integrate this accepted review there before rendering. Independent full audiovisual output QA must verify actual timing, speech, framing and mobile legibility before delivery.
