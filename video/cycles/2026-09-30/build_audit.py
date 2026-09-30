import json,hashlib,subprocess
from pathlib import Path
C=Path(__file__).resolve().parent;R=C.parents[2]
stock={x['file']:x for x in json.loads((C/'stock_downloads.json').read_text())}
stills={x['file']:x for x in json.loads((C/'stock_stills.json').read_text())}
commons={x['file']:x for x in json.loads((C/'commons_stills.json').read_text())}
esa={x['file']:x for x in json.loads((C/'esa_stills.json').read_text())}
photos={x['file']:x for x in json.loads((C/'pexels_photos.json').read_text())}
cards={x['file']:x for x in json.loads((C/'editorial_cards.json').read_text())}
files=[]
for n in ['main','r1','r2']:
 m=json.loads((C/f'{n}_manifest.json').read_text());scenes=[s for sec in m['sections'] for s in sec.get('scenes',[])] if n=='main' else m['scenes']
 for s in scenes:
  f=s['file'];
  if f not in files and not f.startswith('build/'):files.append(f)
lines=['# Media Audit — 2026-09-30','','Status: prepared for independent pre-render review. All selected inputs are cycle-local and listed in active manifests. Generic imagery is labelled context. Original documentary cards are attributed to primary sources; the single M4 frame extract is disclosed as a sourced derivative.','','| Story | Format | File | Native dimensions | Duration | SHA-256 | Source / rights | Editorial classification |','| --- | --- | --- | --- | --- | --- | --- | --- |']
credits=['# Credits — 2026-09-30','','All sources below appear in prepared manifests. Layout cropping and fit to frame are visual modifications. Context labels distinguish unrelated locations, people and facilities.','','| File | Creator / institution | Source | Terms |','| --- | --- | --- | --- |']
for f in files:
 src=stock.get(f) or stills.get(f) or commons.get(f) or esa.get(f) or photos.get(f) or cards.get(f)
 if not src:raise ValueError(f)
 p=R/f
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(p)]))['streams'][0]
 dims=f"{probe['width']}×{probe['height']}";story=src.get('story','m1')
 if f in stock:source=src['page'];rights='Pexels Licence';creator=src['creator'];kind='recorded video • context'
 elif f in stills:source=src['sourcePage'];rights='Pexels Licence; frame extract';creator=src['creator'];kind='sourced still derivative • context'
 elif f in cards:source=src['source'];rights=src['license'];creator=src['creator'];kind='original source-attributed documentary still'
 elif f in photos:source=src['sourcePage'];rights='Pexels Licence';creator=src['creator'];kind='independent sourced photograph • context'
 elif f in commons:source=src['source'];rights=src['license']+(f" ({src['licenseUrl']})" if src['licenseUrl'] else '');creator=src.get('artist','Wikimedia Commons contributor').replace('|','/');kind='sourced still • context'
 else:source=src['page'];rights='CC BY-SA 3.0 IGO; cropped to fit frame';creator='ESA/Juice/JMC' if 'jmc' in f else ('ESA/Juice/NavCam' if 'navcam' in f else 'European Space Agency / ATG Europe');kind='actual 2026 flyby still / trajectory diagram'
 duration=src.get('probe',{}).get('format',{}).get('duration','still')
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 lines.append(f'| {story.upper()} | {kind} | `{f}` | {dims} | {duration} | `{sha}` | [source]({source}); {rights} | {"Actual flyby" if f in esa else ("Source-attributed factual card" if f in cards else "Context; not the reported site, participant or experiment")} |')
 credits.append(f'| `{f}` | {creator} | [page]({source}) | {rights} |')
(C/'MEDIA_AUDIT.md').write_text('\n'.join(lines)+'\n');(C/'CREDITS.md').write_text('\n'.join(credits)+'\n')

with (C/'MEDIA_AUDIT.md').open('a') as h:
 h.write('\n## Reuse and derived assets\n\nAll selected Reel media hashes were compared against video/cycles/2026-09-26 and 2026-09-23 manifests; see `reel_prior_hash_check.json`. The eight-second M1 teaser is a derivative of four current-cycle Pexels motion clips; its parent paths and hashes appear in `main_manifest.json`. It is a cross-story opening teaser and not counted toward the M1 motion minimum.\n')

teaser=R/'build/video/2026-09-30/work/opening-teaser.mp4'
with (C/'MEDIA_AUDIT.md').open('a') as h:
 h.write(f'\nOpening teaser derivative: `{teaser.relative_to(R)}`, 8.0 seconds, 1920×1080, SHA-256 `{hashlib.sha256(teaser.read_bytes()).hexdigest()}`. Four two-second extracts from current-cycle M2 `developers.mp4`, M3 `hydro-aerial.mp4`, M4 `vaccine-vial.mp4`, and M5 `wind-farm.mp4`; all Pexels footage and item rights appear above. It is a four-story tease, not Juice footage.\n')
