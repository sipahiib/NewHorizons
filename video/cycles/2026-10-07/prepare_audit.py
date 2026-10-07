"""Verify selected sources, timing, provenance and prior-use checks."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
rows=json.loads((C/'media_sources.json').read_text());by={a['file']:a for a in rows}
prior=[]
for p in (ROOT/'video/cycles').glob('*/media_sources.json'):
 if p.parent==C:continue
 try:
  r=json.loads(p.read_text());prior.extend((p.parent.name,x) for x in r if isinstance(x,dict))
 except (ValueError,TypeError):pass
priorhash={x.get('sha256') for _,x in prior if x.get('sha256')}
priorurls={x.get(k) for _,x in prior for k in ['page','source','url','download'] if x.get(k)}
selected=set();checks=[]
for id in ['main','r1','r2']:
 m=json.loads((C/f'{id}_manifest.json').read_text());ss=[s for section in m['sections'] for s in section.get('scenes',[])] if id=='main' else m['scenes']
 assert sum(s['duration'] for s in ss)==(300 if id=='main' else 45)
 if id=='main':assert [sum(s['duration'] for s in section.get('scenes',[])) for section in m['sections'][:2]]==[160,140]
 else:assert len(ss)==7
 for s in ss:
  a=by[s['file']];selected.add(a['file']);h=hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest();assert h==m['hashes'][a['file']]==a['sha256']
  orig=by.get(a.get('derivation',{}).get('sourceFile'),a)
  if id!='main':
   hits=[]
   if h in priorhash or orig['sha256'] in priorhash:hits.append('hash')
   if any(orig.get(k) in priorurls for k in ['page','url'] if orig.get(k)):hits.append('source URL')
   checks.append({'output':id,'file':a['file'],'sourceFile':orig['file'],'priorUseHits':hits});assert not hits
  if s['kind']=='motion':
   duration=float(a['probe']['format']['duration']);assert s.get('seek',0)+s['duration']<=duration+0.05,(s,duration)
(C/'prior_reuse_audit.json').write_text(json.dumps({'method':'selected Reel derivative and originating source hash/URL compared with every prior-cycle source registry','priorCycles':sorted({d for d,_ in prior}),'checks':checks,'status':'PASS'},indent=2)+'\n')
lines=['# Media Audit — 2026-10-07','', 'Selected files pass source hash, provenance, timing and prior-use checks. Primary registry: [media_sources.json](media_sources.json); original probes: [native_source_probes.json](native_source_probes.json); prior use: [prior_reuse_audit.json](prior_reuse_audit.json).','', 'Main counts: M1 eight still segments and six motion segments (including the second-story teaser); M2 four stills and six motion clips. The science-image chapter uses extra static detail views to explain infrared gas structure; main counts are adaptable. Each Reel has exactly four motion clips and three stills, all newly acquired sources. Stills extracted from newly licensed clips remain unanimated.','', 'MIT NC photos and both unlicensed SANDO videos are excluded. OpenAI demos/screenshots are excluded. M2 uses the approved contextual fallback: CC BY 3.0 autonomous-drone performance and Pexels FPV interiors, persistently labelled not SANDO. R1 uses specific contract-review/signing context, persistently labelled not the evaluated AI. R2 ocean waves are context, not heat measurements; Gorner is 2021 archive. All original source audio is removed.','', 'NASA material is used factually with full attribution, without endorsement; no third-party copyrighted asset identified on the selected pages. ESA Gorner is ESA Standard Licence editorial/informational footage; reviewed samples and selected intervals avoid interview captions, end branding and unrelated sections. Pexels licence supports editing and factual context. MagicLab CC BY 3.0 supports edited excerpts with attribution and licence notice. Direct-photo crop coordinates and video frame origins are in the registry.','', 'Excluded after visual inspection: Pexels8960646 shows a job description, so neither that video nor extracted still enters any active render. MagicLab credits/BTS interval255–271s is excluded; final M2 uses verified clean flight150–166s.', '', '## Selected assets','', '| File | Native/derived dimensions | Status | Credit / terms |','|---|---|---|---|']
credits=['# Credits — 2026-10-07','','Sources and claim boundaries: [RESEARCH_PACKET.md](RESEARCH_PACKET.md). Exact assets and transformations: [media_sources.json](media_sources.json).','']
for file in sorted(selected):
 a=by[file];v=next(x for x in a['probe']['streams'] if 'width' in x);orig=by.get(a.get('derivation',{}).get('sourceFile'),a)
 lines.append(f"| `{file}` | {v['width']}×{v['height']} | {a['status']} | {a['credit']}; {a['rights']} |")
seen=set()
for file in sorted(selected):
 a=by[file];orig=by.get(a.get('derivation',{}).get('sourceFile'),a)
 if orig['file'] in seen:continue
 seen.add(orig['file']);credits += [f"- [{orig['file']}]({orig['page']}): {orig['credit']}. {orig['rights']}. Date: {orig['recordedDate']}."]
credits += ['','MagicLab full attribution: Marco Tempest, “MagicLab — 24 Drone Flight”; Daito Manabe, Motoi Ishibashi and Rhizomatiks Research. [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Excerpts edited, original audio removed, some frames extracted as stills. No association with or endorsement of SANDO is implied.']
(C/'MEDIA_AUDIT.md').write_text('\n'.join(lines)+'\n');(C/'CREDITS.md').write_text('\n'.join(credits)+'\n')
print('Audit PASS',len(selected),'selected files')
