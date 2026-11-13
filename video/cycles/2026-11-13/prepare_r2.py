from pathlib import Path
import json,hashlib
C=Path(__file__).resolve().parent; root=C.parents[2]
files=['flow-01.jpg','nasa-flow.jpg','flow-02.jpg','verified-03.jpg','verified-04.jpg','flow-05.jpg','flow-06.jpg']
base='build/video/2026-11-13/media/r2/'
scenes=[{'file':base+f,'kind':'still','duration':d,'classification':'direct'} for f,d in zip(files,[6,7,7,6,7,6,7])]
paths=[x['file'] for x in scenes]+['build/video/2026-11-13/audio/r2-short.mp3']
m={'cycle':'2026-11-13','status':'prepared-for-review','output':'build/reels/2026-11-13/planet-earth-flow-country.mp4','audio':paths[-1],'duration':46,'width':1080,'height':1920,'fps':60,'title':'SCOTLAND’S FLOW COUNTRY','title_seconds':5.5,'cta_seconds':3,'scenes':scenes,'hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}}
(C/'r2_manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
