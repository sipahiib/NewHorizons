"""Fetch approved cycle-local source assets; no earlier media is copied."""
from pathlib import Path
import re,json,html,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent
assert 'approved by user selection' in (C/'APPROVAL.md').read_text()
A=ROOT/'assets/motion'/C.name/'main'; A.mkdir(parents=True,exist_ok=True)
assets=[]
def add(id,url,source,credit,role,rights):
 ext=url.split('?')[0].rsplit('.',1)[-1]; p=A/f'{id}.{ext}'
 assets.append(dict(id=id,file=str(p.relative_to(ROOT)),download=url,source=source,credit=credit,role=role,rights=rights))
nasa='https://www.nasa.gov/centers-and-facilities/langley/nasa-develops-batteries-to-power-humanitys-return-to-moon/'
for id,name in [('battery','lrc-2026-ocio-p-03142.jpg'),('removal','lrc-2026-ocio-p-03145.jpg'),('weighing','lrc-2026-ocio-p-03153.jpg'),('team','img-3541.jpg')]:
 add(id,'https://www.nasa.gov/wp-content/uploads/2026/10/'+name,nasa,'NASA/Ryan Hill' if id!='team' else 'NASA','actual SPEARS photograph','NASA media guidelines https://www.nasa.gov/nasa-brand-center/images-and-media/; credit; no endorsement; no third-party credit stated')
for id,name,url in [('storie1','storie','14874_060925_TVAC-Part1_1080_ProRes.webm'),('storie2','storie','14874_061025_TVAC-Part2_1080_ProRes.webm'),('chamber','tvac','SES_Chamber_Beauty_B-roll_59.97-h264.webm')]:
 s=(C/f'source_pages/{name}.html').read_text()
 match=next(html.unescape(x) for x in re.findall(r'href=["\']([^"\']+)["\']',s) if x.endswith('/'+url))
 add(id,'https://svs.gsfc.nasa.gov'+match,'https://svs.gsfc.nasa.gov/'+('14874/' if name=='storie' else '11807/'),'NASA/Lacey Young' if id=='storie1' else 'NASA/Beth Anthony' if id=='storie2' else 'NASA Goddard','contextual facility footage, not SPEARS experiment','NASA media guidelines; source sound excluded; source credited; no third-party credit stated')
s=(C/'source_pages/nature.html').read_text(); source='https://www.nature.com/articles/s44286-026-00454-4'
for video,mo,ext in [(1,5,'mp4'),(2,6,'mp4'),(3,7,'avi'),(4,8,'avi'),(6,10,'mp4')]:
 url=next(x for x in re.findall(r'href=["\']([^"\']+)["\']',s) if x.endswith(f'44286_2026_454_MOESM{mo}_ESM.{ext}'))
 add('rna-video'+str(video),html.unescape(url),source,'Verstraeten, Tran et al., Nature Chemical Engineering (2026)','actual experimental time-lapse microscopy; supplementary video '+str(video),'CC BY4.0 https://creativecommons.org/licenses/by/4.0/; attribution and changes disclosed; no per-asset exception stated')
(C/'main_media_sources.json').write_text(json.dumps(dict(cycle=C.name,status='approved-for-download',assets=assets),indent=2)+'\n')
for a in assets:
 p=ROOT/a['file']
 if not p.exists():subprocess.run(['curl','--fail','--location','--silent','--show-error','--connect-timeout','20','--max-time','300',a['download'],'-o',str(p)],check=True)
 a['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 a['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 v=next(x for x in a['probe']['streams'] if x['codec_type']=='video')
 print(a['id'],v['width'],v['height'],a['probe']['format'].get('duration'),flush=True)
(C/'main_media_sources.json').write_text(json.dumps(dict(cycle=C.name,status='downloaded-for-audit',assets=assets),indent=2)+'\n')
