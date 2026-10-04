# Media Audit — 2026-10-04

Status: selected inputs verified for independent pre-render review. Exact segment times, selected counts and file hashes are authoritative in `main_manifest.json`, `r1_manifest.json`, `r2_manifest.json`. Full source URLs, native/local probes and derivations are in `media_sources.json`.

## Selected layout and correspondence

M1: five current photographs, eight real archival cuts, plus a four-second M2 teaser. The extra cut preserves the required seven-second opening and avoids loops or long holds. Photographs show September 2026. Motion shows September 2025, persistently labelled archive. The original 1080p ESA documentary is cropped to its upper 1920×800 to remove burned-in documentary subtitles; no synthetic imagery is used. All selected ranges contain recorded people/equipment/fieldwork, not its opening/ending animations. Sources retain on-screen ESA attribution.

M2: four original research figures, six contextual healthcare/wearable clips. Watch stock does not show the studied Withings capture or model. The scan-review shot illustrates clinical imaging generally, not a filmed echocardiogram. Persistent context labels exclude study-participant/device claims; figure labels identify retrospective single-centre research. Figures are unanimated; only plot regions are cropped/scaled, without changing data.

R1: four new contextual clips plus three unanimated frames from those same newly downloaded licensed clips. Three public photo downloads returned HTTP 403 and were abandoned; no access restriction was bypassed. Within-Reel source repetition is disclosed and permitted; prior-cycle footage is not reused. All scenes concern medical note preparation/chart review/team handoff.

R2: five campaign/source stills plus two disjoint cuts (0–6s and 7–16s) from the NASA cabin recording. First frame is expressly labelled a scientific diagram; other scenes show the actual summer 2026 campaign, not a photographed fire-cloud event. The low-resolution hangar image (767×431) is retained for direct aircraft correspondence; its complete frame is only modestly enlarged in the central Reel area. NASA motion is 720×480. All complete Reel source frames fit within the central 1080×760 area without cropping.

## Per-item source and resolution

| Selected local file | Native resolution | Local resolution | Status / credit |
| --- | --- | --- | --- |
| `esa-0.jpg` | 3000×2000 | 3000×2000 | actual-September-2026 / ©ESA/jensenmedia |
| `esa-1.jpg` | 3840×2160 | 3840×2160 | actual-September-2026 / ©ESA/jensenmedia |
| `esa-2.png` | 3000×2000 | 3000×2000 | actual-September-2026 / ©ESA/jensenmedia |
| `esa-3.jpg` | 3000×2000 | 3000×2000 | actual-September-2026 / ©ESA/jensenmedia |
| `esa-4.jpg` | 3000×2000 | 3000×2000 | actual-September-2026 / ©ESA/jensenmedia |
| `jammertest-2025-source.mp4` | 1920×1080 | 1920×1080 | archive-September-2025 / ©European Space Agency — ESA |
| `fig1-roc.png` | 2050×866 | 1479×633 | actual-study-figure / van der Valk, Atsma, Scherptong & Staring (2026), npj Cardiovascular Health |
| `fig2-aggregation.png` | 950×730 | 687×531 | actual-study-figure / van der Valk, Atsma, Scherptong & Staring (2026), npj Cardiovascular Health |
| `fig5-monitoring.png` | 2050×726 | 1479×528 | actual-study-figure / van der Valk, Atsma, Scherptong & Staring (2026), npj Cardiovascular Health |
| `fig6-processing.png` | 1750×984 | 1263×714 | actual-study-figure / van der Valk, Atsma, Scherptong & Staring (2026), npj Cardiovascular Health |
| `pexels-7088462.mp4` | 2160×3840 | 608×1080 | context / MART PRODUCTION / Pexels |
| `pexels-7195664.mp4` | 4096×2160 | 1920×1012 | context / kaboompics / Pexels |
| `pexels-8026528.mp4` | 4096×2160 | 1920×1012 | context / MART PRODUCTION / Pexels |
| `pexels-8311312.mp4` | 1920×1080 | 1920×1080 | context / Ammad Rasool / Pexels |
| `pexels-8413638.mp4` | 2160×3840 | 608×1080 | context / SHVETS production / Pexels |
| `pexels-8460066.mp4` | 1920×1080 | 1920×1080 | context / Los Muertos Crew / Pexels |
| `pexels-36656061.mp4` | 1080×1920 | 608×1080 | context / GIUSEPPE DE BERGOLIS / Pexels |
| `pexels-5453568-still.png` | 3840×2160 | 1920×1080 | context / Tima Miroshnichenko / Pexels |
| `pexels-5453568.mp4` | 3840×2160 | 1920×1080 | context / Tima Miroshnichenko / Pexels |
| `pexels-5998403-still.png` | 1080×1920 | 608×1080 | context / Pavel Danilyuk / Pexels |
| `pexels-5998403.mp4` | 1080×1920 | 608×1080 | context / Pavel Danilyuk / Pexels |
| `pexels-6997946-still.png` | 1920×1080 | 1920×1080 | context / Pavel Danilyuk / Pexels |
| `pexels-6997946.mp4` | 1920×1080 | 1920×1080 | context / Pavel Danilyuk / Pexels |
| `afrc2026-0144-226orig-er2-inst.jpg` | 4128×2752 | 4128×2752 | actual-campaign-2026 / NASA/Carla Escamilla |
| `inspyre-light-walk.mp4` | 720×480 | 720×480 | actual-campaign-2026 / NASA/Katie Jepson |
| `inspyre-news-image-7-28-26-4.jpeg` | 767×431 | 767×431 | actual-campaign-2026 / NASA/Bill Ingalls, NASA/JSC/Mark Sowa |
| `inspyre-preview-loiacono-0172.jpg` | 6000×4000 | 6000×4000 | actual-campaign-2026 / NASA/Milan Loiacono |
| `inspyre-preview-loiacono-9318.jpg` | 6000×4000 | 6000×4000 | actual-campaign-2026 / NASA/Milan Loiacono |
| `inspyre-pyrocb-diagram.png` | 1355×1339 | 1355×1339 | illustrative-scientific-diagram / NASA/Bill Ingalls, NASA/JSC/Mark Sowa |

## Reuse and technical checks

Source IDs and SHA-256 for all selected Reel inputs have no matches in older project JSON manifests/registries; see `prior_reuse_audit.json`. The source pages/IDs were also compared during selection. This is a recorded provenance audit, not a claim of perceptual duplicate detection across unrelated source IDs. Each manifest hash matches the selected local file. All motion ranges fit their measured files without looping. Local Pexels excerpts are downscaled from the native dimensions, never reported as native. Figures retain embedded native raster dimensions in the registry. Low-resolution fallbacks are explicitly identified above.

No prior-cycle generated assets, covers or thumbnails are active inputs. Main and Reel title backgrounds use specification opacity; there is no lower information card. Unboxed copyright credits remain to satisfy source terms.
