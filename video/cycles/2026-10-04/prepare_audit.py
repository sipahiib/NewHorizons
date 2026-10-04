"""Produce the selected-input audit from the current manifests and source registry."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
registry={a['file']:a for a in json.loads((C/'media_sources.json').read_text())}
ms={k:json.loads((C/f'{k}_manifest.json').read_text()) for k in ['main','r1','r2']}
selected=[]
for k,m in ms.items():
 scenes=[s for sec in m['sections'] for s in sec.get('scenes',[])] if k=='main' else m['scenes']
 assert sum(s['duration'] for s in scenes)==(300 if k=='main' else 45)
 if k!='main':assert len(scenes)==7
 for s in scenes:
  a=registry[s['file']];assert hashlib.sha256((ROOT/s['file']).read_bytes()).hexdigest()==m['hashes'][s['file']]
  if s['kind']=='motion':assert s.get('seek',0)+s['duration']<=float(a['probe']['format']['duration'])+0.02
  selected.append(s['file'])
old=[]
for p in (ROOT/'video').rglob('*.json'):
 if C in p.parents:continue
 try:old.append(p.read_text())
 except (OSError,UnicodeError):pass
previous='\n'.join(old);checks=[]
for k in ['r1','r2']:
 for file in sorted(set(s['file'] for s in ms[k]['scenes'])):
  a=registry[file];idmatch=re.search(r'pexels-(\d+)',file);id=idmatch.group(1) if idmatch else Path(file).name
  assert id not in previous,f'Prior media ID match: {id}'
  assert a['sha256'] not in previous,f'Prior content hash match: {id}'
  checks.append({'file':file,'sourceId':id,'priorSourceMatch':False,'priorHashMatch':False})
(C/'prior_reuse_audit.json').write_text(json.dumps({'scope':'All pre-existing video JSON manifests/registries, excluding the active cycle; source-ID and SHA-256 comparison. Current Reel stills are derived from current new footage, not older media.','checks':checks},indent=2)+'\n')
lines=['# Media Audit — 2026-10-04','','Status: selected inputs verified for independent pre-render review. Exact segment times, selected counts and file hashes are authoritative in `main_manifest.json`, `r1_manifest.json`, `r2_manifest.json`. Full source URLs, native/local probes and derivations are in `media_sources.json`.','','## Selected layout and correspondence','','M1: five current photographs, eight real archival cuts, plus a four-second M2 teaser. The extra cut preserves the required seven-second opening and avoids loops or long holds. Photographs show September 2026. Motion shows September 2025, persistently labelled archive. The original 1080p ESA documentary is cropped to its upper 1920×800 to remove burned-in documentary subtitles; no synthetic imagery is used. All selected ranges contain recorded people/equipment/fieldwork, not its opening/ending animations. Sources retain on-screen ESA attribution.','','M2: four original research figures, six contextual healthcare/wearable clips. Watch stock does not show the studied Withings capture or model. The scan-review shot illustrates clinical imaging generally, not a filmed echocardiogram. Persistent context labels exclude study-participant/device claims; figure labels identify retrospective single-centre research. Figures are unanimated; only plot regions are cropped/scaled, without changing data.','','R1: four new contextual clips plus three unanimated frames from those same newly downloaded licensed clips. Three public photo downloads returned HTTP 403 and were abandoned; no access restriction was bypassed. Within-Reel source repetition is disclosed and permitted; prior-cycle footage is not reused. All scenes concern medical note preparation/chart review/team handoff.','','R2: five campaign/source stills plus two disjoint cuts (0–6s and 7–16s) from the NASA cabin recording. First frame is expressly labelled a scientific diagram; other scenes show the actual summer 2026 campaign, not a photographed fire-cloud event. The low-resolution hangar image (767×431) is retained for direct aircraft correspondence; its complete frame is only modestly enlarged in the central Reel area. NASA motion is 720×480. All complete Reel source frames fit within the central 1080×760 area without cropping.','','## Per-item source and resolution','','| Selected local file | Native resolution | Local resolution | Status / credit |','| --- | --- | --- | --- |']
credits=['# Credits — 2026-10-04','','Selected source records, exact downloads, SHA-256 and adaptations: [media_sources.json](media_sources.json). This local editorial package implies no endorsement. Required copyright notices are also shown on screen.','','## Usage basis','','- ESA: [media terms](https://www.esa.int/ESA_Multimedia/Terms_and_conditions_of_use_of_images_and_videos_available_on_the_esa_website), editorial/informational reuse with credit. Current ESA/jensenmedia photos carry ESA Standard Licence. Testnor group photo without an ESA licence was excluded. [Documentary](https://www.esa.int/esatv/Videos/2026/02/Jammertest_strengthening_satellite_navigation), September 2025 footage, cropped to omit existing subtitles; audio removed.','','- Study figures: [van der Valk et al., npj Cardiovascular Health](https://www.nature.com/articles/s44325-026-00153-2), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Original Figures 1, 2, 5 and 6 cropped/scaled; no data edits. Source authors: Viktor van der Valk, Douwe Atsma, Roderick Scherptong and Marius Staring.','','- Healthcare stock: [Pexels licence](https://www.pexels.com/license/). Context only, no endorsement and no identification as study participants. Video excerpts are silent; R1 stills are unanimated frames from the same new recordings. The AI-summary paper is CC BY-NC-ND; no publisher artwork is reproduced.','','- NASA: [media guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/), factual editorial use of NASA-credited assets. [INSPYRE report](https://science.nasa.gov/earth/natural-disasters/wildfires/nasa-campaign-explores-clouds-spawned-by-wildfires/). Third-party fire photographs were excluded. The schematic is illustrative; aircraft/lab/ground images are actual campaign documentation.','','## Item credits','']
def dims(a):
 if 'streams' in a:
  v=next(s for s in a['streams'] if 'width' in s);return f"{v['width']}×{v['height']}"
 return f"{a['width']}×{a['height']}"
for f in sorted(set(selected)):
 a=registry[f];native=a.get('nativeProbe',a['probe']);name=Path(f).name
 lines.append(f"| `{name}` | {dims(native)} | {dims(a['probe'])} | {a['status']} / {a['credit']} |")
 credits.append(f"- [{name}]({a['source']}): {a['credit']}." )
lines+=['','## Reuse and technical checks','','Source IDs and SHA-256 for all selected Reel inputs have no matches in older project JSON manifests/registries; see `prior_reuse_audit.json`. The source pages/IDs were also compared during selection. This is a recorded provenance audit, not a claim of perceptual duplicate detection across unrelated source IDs. Each manifest hash matches the selected local file. All motion ranges fit their measured files without looping. Local Pexels excerpts are downscaled from the native dimensions, never reported as native. Figures retain embedded native raster dimensions in the registry. Low-resolution fallbacks are explicitly identified above.','','No prior-cycle generated assets, covers or thumbnails are active inputs. Main and Reel title backgrounds use specification opacity; there is no lower information card. Unboxed copyright credits remain to satisfy source terms.']
(C/'MEDIA_AUDIT.md').write_text('\n'.join(lines)+'\n');(C/'CREDITS.md').write_text('\n'.join(credits)+'\n');print('Selected media, prior reuse, durations and hashes verified.')
