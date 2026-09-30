# Independent pre-render review — 2026-09-30

Correction-round re-review of the approved package, active manifests, narration, measured audio, selected media, rights notes, credits, and prior-use check.

**MAIN_RENDER_GATE: PASS** — no remaining pre-render blocker.  
**R1_RENDER_GATE: PASS** — no remaining pre-render blocker.  
**R2_RENDER_GATE: PASS** — no remaining pre-render blocker.

## Resolved findings and checks

- The opening now states Juice's Earth-flyby result before the approved question hook, followed by the four-story tease. Revised M1 speech measures 117.28 seconds in its 120-second section. All other sections fit without declared time stretching; Reel speech measures 42.456 and 42.84 seconds, leaving under three seconds to the 45-second endpoint. The closing retains the required final sentence.
- The main manifest totals 370 seconds: M1 120, four supports 60 each, and closing 10. M1 has four ESA stills and three distinct recorded satellite-dish clips relevant to tracking/communications, labelled context. The separate eight-second four-story teaser is documented as a derivative and is not counted as Juice footage. The final sunrise dish clip replaces the previously rejected shot. Each support has two stills and three motion clips. M5 now uses two independent photographs, and its overlay no longer claims tunnel imagery is shown.
- Both Reels have seven 45-second segments, mixing three original, source-attributed documentary still cards with four distinct recorded clips. The cards directly identify the Anthropic study and Rome declaration/initiative; the motion illustrates interviews or water use and is labelled as context rather than study participants or Rome meeting footage. R1's repeated final clip was replaced. Reel overlays include source and platform calls. Script inspection indicates frame-preserving Reel scaling and in-range overlays.
- Every selected manifest input exists and matches its SHA-256 entry. `MEDIA_AUDIT.md` lists source, usage basis, dimensions, hashes, and native video durations. `CREDITS.md` identifies the formerly unresolved creators. The selected ESA basis is CC BY-SA 3.0 IGO per still, with crop disclosure. The Reel cards use original typography rather than copying source-site artwork. `reel_prior_hash_check.json` reports no match against prior cycle manifests. No cover or thumbnail is selected.
- Narration's core claims and limits remain within the approved `RESEARCH_PACKET.md` framing. ESA supports the flyby date, 20° turn, 3.5 km/s increase, and pending science evaluation; Toshiba/TEPCO supports the 14-plant contract and supplier roles. Other stories distinguish supplier claims, preclinical or modeled results, and demonstrated outcomes.

Output QA remains required after render: inspect all scenes, disclosures and card readability, listen to complete narration, and verify technical format, sound and final timing. This review clears render only, not delivery.
