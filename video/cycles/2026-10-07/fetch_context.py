"""Acquire newly licensed recorded context, preserving source metadata."""
import json,subprocess,hashlib
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent
assert 'Status: **approved**' in (C/'APPROVAL.md').read_text()
selections=[
 ('main/m2/fpv.mp4',20492686,'Traveling on the Go'),
 ('reels/r1/signing.mp4',8091686,'Radek Černý'),
 ('reels/r1/agreement.mp4',8731254,'Mikhail Nilov'),
 ('reels/r2/ocean.mp4',19912847,'Yogi R'),
]
def pexels(item):
 file,i,credit=item;p=ROOT/f'assets/motion/{C.name}/{file}';p.parent.mkdir(parents=True,exist_ok=True)
 with urlopen(Request(f'https://www.pexels.com/download/video/{i}/',method='HEAD',headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:u=r.url
 native=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',u],timeout=60))
 if not p.exists():subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',u,'-t','40','-vf','scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2','-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','19',str(p)],check=True,timeout=240)
 return dict(file=str(p.relative_to(ROOT)),url=u,page=f'https://www.pexels.com/video/{i}/',credit=credit+' / Pexels',status='contextual recorded footage; not the reported experiment',rights='Pexels licence; editing/free editorial use; no endorsement',recordedDate='archive; date on source page',nativeProbe=native,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
results=[]
with ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(pexels,selections):results.append(r);print(r['file'],flush=True);(C/'context_sources.json').write_text(json.dumps(results,indent=2)+'\n')
p=ROOT/f'assets/motion/{C.name}/main/m2/magiclab.webm';p.parent.mkdir(parents=True,exist_ok=True)
u='https://upload.wikimedia.org/wikipedia/commons/0/0a/MagicLab_-_24_Drone_Flight.webm'
if not p.exists():
 with urlopen(Request(u,headers={'User-Agent':'NewHorizons editorial research'}),timeout=90) as r,p.open('wb') as f:
  while b:=r.read(1024*1024):f.write(b)
results.append(dict(file=str(p.relative_to(ROOT)),url=u,page='https://commons.wikimedia.org/wiki/File:MagicLab_-_24_Drone_Flight.webm',credit='Marco Tempest / CC BY 3.0; Daito Manabe, Motoi Ishibashi, Rhizomatiks Research',status='contextual autonomous-drone performance; not SANDO',rights='Reviewed CC BY 3.0; excerpts edited; original audio removed',recordedDate='2016-02-09',sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(C/'context_sources.json').write_text(json.dumps(results,indent=2)+'\n')
print('Context sources complete',flush=True)
