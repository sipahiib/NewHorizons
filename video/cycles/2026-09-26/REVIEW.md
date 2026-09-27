# Consolidated Independent Pre-render Review — 2026-09-26

Scope: final independent review of R1 and the main programme, with the prior independent R2 gate and its essential evidence preserved. I reviewed the approved research, narration, audits, rights notes, credits, current manifests and hash record, preparation/render scripts, every referenced source file, derived still, overlay and audio path. I decoded all motion/audio inputs, inspected representative frames and final overlay compositions, and did not render deliverables.

## Editorial, provenance and rights

`APPROVAL.md` covers M1–M5, R1, R2, their hooks, limitations and direct/contextual approach. Narration claims match the research packet: vendor announcements remain vendor evidence; the lunar result is thermal inference rather than impact footage; hafnia applications remain prospective; the cartilage work is not a treatment study; FEAR 3 is preliminary and not earthquake prediction. Every selected asset is recorded in the audit with source, dimensions, correspondence and rights condition. Google, Meta and UNL material is accurately described as attributed editorial excerpts without an express general reuse licence; Nature figures, Commons stills, Pexels footage and NASA material carry their documented conditions. Credits are complete for the prepared package.

## R2 preserved result

The prior reviewer verified NASA SVS item 5675, all current hashes, three sourced stills plus four motion segments, seven scenes totaling 47 seconds, full-frame landscape treatment, processed/non-live labels and CTA. Ryan narration is 44.640 seconds; measured speech ends about 43.704 seconds, leaving about 3.296 seconds. No prior-manifest hash match was found.

R2_RENDER_GATE: PASS

## R1 result

R1 has exactly seven scenes totaling 45 seconds: three direct Google stills and four contextual recorded-motion excerpts. All six assets match manifest hashes and the prior-hash record reports no reuse. Product stills now say `AI-generated avatar • Google demonstration`; recorded human calls remain persistently identified as context and not Gemini output. The portrait renderer preserves complete frames over blurred duplicates; headings, source, platform CTAs and labels are readable and nonoverlapping. Ryan at -2% is recorded in the generation data; the 42.120-second audio matches approved text, decodes cleanly, shows no digital clipping, and leaves about 3.82 seconds after detected final speech. The renderer targets 1080×1920, 60 fps, H.264/AAC and is review-gated.

R1_RENDER_GATE: PASS

## Main result

The manifest totals 370 seconds: M1 is 120 seconds with three stills/four motion segments; every support is 60 seconds with two stills/three motion clips; closing is 10 seconds. Hashes match. Context, historical LRO and dated Bedretto labels are readable; the dedicated 0:12–0:20 teaser overlay no longer overlaps its four support labels. Measured M1 speech places the result by 4.395 seconds and the required teaser sentence at about 12.003–19.771 seconds. All section audio decodes, fits without stretching, and peaks below clipping. Closing copy and bell behavior match the specification. No cover, thumbnail, legacy asset or excluded location map enters either render path.

Resolution verification: the sole blocking opening shot has been replaced. Both `prepare_main.mjs` and `main_manifest.json` now assign 0:05–0:12 to real recorded `lro-launch.mp4` footage at seek 145 for seven seconds, labelled `historical`. The source decodes through the full interval and sampled frames show the LRO launch vehicle on its pad. Scene boundaries remain exactly 0:05 and 0:12; M1 remains 120 seconds with three stills and four motion segments.

MAIN_RENDER_GATE: PASS
