# Media Audit — 2026-09-26

Status: R2 rendered and machine/sampled-visual QA passed, with full human audiovisual playback still required. R1 and main selections are prepared for independent pre-render review; render remains gated.

## R2 — NISAR volcano

Source: https://svs.gsfc.nasa.gov/5675 ; direct movie URL and SHA-256 hashes are in `r2_manifest.json`. Downloaded 26 September 2026 into the cycle's isolated directory. Native H.264, 3840×2160, 30 fps, 16.700 seconds. NASA SVS publishes the movie as an observed-radar-data visualisation. It includes a geographic introduction and rendered terrain, not optical footage. Approved Reel explicitly uses processed radar time-lapse; this does not change the main programme's prohibition on illustrative animation.

Usage basis: NASA-produced media under https://www.nasa.gov/nasa-brand-center/images-and-media/ ; source credit NASA Scientific Visualization Studio. No item-specific third-party copyright restriction found. Preserve labels and attribution; no endorsement implied.

Three PNGs extracted without visual alteration at 5.00, 9.00 and 16.66 seconds are sourced observation stills, not generated imagery. Four motion segments use distinct portions and a final explicitly labelled full-sequence recap. Recap freezes the last source frame for 0.3 seconds to fill its 17-second slot; no speech or source motion is sped up/slowed down. All 7 scene durations total 47 seconds. This is one source sequence, not seven independent observations. Original landscape frame remains intact above a darkened blurred duplicate.

Visual inspection: controller viewed a contact sheet and full-resolution late frame; dates, volcano terrain and source scale labels are present. Independent reviewer must inspect input progression and overlays. Source is new to the active cycle; no old-cycle media copied. Hash comparison against recorded prior manifests is logged separately.

Narration: Ryan at -2%, 44.640 seconds file length; measured final speech end 43.70225 seconds, giving 3.29775 seconds to planned end. Mandatory YouTube handle and Instagram like/follow are in overlays and spoken CTA.

## R1 — Gemini Live Avatar

Selected direct stills: three Google Cloud product images from the approved announcement, 1920×1080 or about 2000×1118. They are brief, attributed editorial excerpts used to show the actual product and its interface; Google does not grant an express general reuse licence. Selected motion: three new Pexels-licensed recordings of people in video calls (3840×2160, 2160×3840 and 1080×1920), used only for the narration's point about face-mediated interaction. A persistent overlay says “Context: human video call • not Gemini output.” The final seven-scene plan contains three stills and four motion excerpts, totals 45 seconds, preserves complete source frames over blur and leaves 3.835 seconds after measured speech end. Exact URLs and hashes are in `r1_manifest.json`. This treatment keeps direct product evidence while preventing contextual people from being presented as Google output.

## Main programme

### M1 — McGetchin crater

Three direct stills: the UCLA/NASA LRO crater image (1152×768) and two unaltered frames from the published Diviner thermal blink. Four motion clips use the published 592×824 Diviner data GIF, an eight-second real-footage teaser of the four support stories, recorded NASA LRO assembly footage (640×360) and recorded launch footage (320×240). The teaser occupies exactly 0:12–0:20 and labels each support; contextual lab/tunnel excerpts are marked as context. The low-resolution launch source is the compact NASA download and will be contained rather than enlarged by cropping. NASA footage is used under NASA media guidance; UCLA/JHU APL-partnered research images are attributed editorial excerpts. Persistent copy states that thermal measurements are not impact footage. The downloaded location map is excluded from the active manifest.

### M2 — Meta Muse and AI glasses

Two direct Meta announcement stills (1080×1400 and 1920×1672) and three distinct excerpts from Meta's own “Bringing Muse to AI Glasses” demonstration movie. All are company announcement material, attributed in-frame and presented as a demo rather than proof of reliability or current worldwide availability. No unrelated VR-headset footage is selected. Express general reuse permission remains unresolved; use is limited to short editorial excerpts that directly support the approved report.

### M3 — antiferroelectric hafnia

Two direct UNL research diagrams (1332×585 and 754×859) show the atom-resolved order and field response. Direct motion is UNL's 1280×624 atomic-resolution scan. Two new Pexels-licensed contextual recordings show microscope work (4096×2160) and electrical testing (1280×720), each persistently labelled `CONTEXT FOOTAGE`; neither is presented as the reported experiment. The institution article does not publish an express reuse licence for its figures/video, so those items are attributed editorial excerpts.

### M4 — human skeletal gene regulation

Two direct paper figures (1200×1107 and 1200×1378) come from the open-access Nature article. The article and figures are CC BY 4.0; the selected captions contain no third-party exclusion. Three new Pexels-licensed laboratory recordings (two 2160×3840, one 4096×2160) are persistently labelled as context. Credits will name the paper authors, Nature, DOI and CC BY 4.0, with resizing/compositing disclosed.

### M5 — Bedretto FEAR 3

Two actual Bedretto tunnel stills from Wikimedia Commons: entrance, 3000×4000, Markusp74, CC BY-SA 3.0; interior, 4000×3000, Pierre Granite, CC BY-SA 4.0. Three new Pexels-licensed underground-tunnel motion sources are persistently labelled as context and are not presented as FEAR 3 footage. The Bedretto virtual tour and site news images were excluded because the site's copying terms require written consent; no permission request was sent.

`main_manifest.json` records exact files, hashes, scene order and duration. Every support has two stills and three motion clips; M1 has three stills and four motion clips. Context labels remain visible throughout every fallback clip.
