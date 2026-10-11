import json,subprocess,hashlib
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;A=ROOT/'assets/motion'/C.name/'main'
A.mkdir(parents=True,exist_ok=True)
items=[
 {'id':'capsule','file':'capsule.jpg','url':'https://www.nasa.gov/wp-content/uploads/2026/10/iss075e0185943.jpg','source':'https://www.nasa.gov/centers-and-facilities/ames/nasa-demonstrates-next-generation-heat-shield-technologies/','credit':'NASA','status':'direct KREPE-3 hardware; photographed 7 October 2026','rights':'NASA media guidelines; NASA credit'},
 {'id':'shield','file':'shield.jpg','url':'https://www.nasa.gov/wp-content/uploads/2026/10/acd25-0136-020.jpg','source':'https://www.nasa.gov/centers-and-facilities/ames/nasa-demonstrates-next-generation-heat-shield-technologies/','credit':'NASA/Brandon Torres-Navarrete','status':'direct KREPE thermal protection hardware','rights':'NASA media guidelines; photographer credit'},
 {'id':'watch','file':'watch.png','url':'https://www.tus.ac.jp/en/mediarelations/20261009_9677_01.png','source':'https://www.tus.ac.jp/en/mediarelations/archive/20261009_9677.html','credit':'Isao Shitanda / Tokyo University of Science','status':'direct study device/design figure','rights':'Institution image specifies original content; credit creator'}]
for a in items:
 p=A/a['file'];a['file']=str(p.relative_to(ROOT))
 if not p.exists():
  with urlopen(Request(a['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:p.write_bytes(r.read())
 a['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();a['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 print(a['id'],p.stat().st_size,flush=True)
(C/'main_media_sources.json').write_text(json.dumps(items,indent=2)+'\n')
