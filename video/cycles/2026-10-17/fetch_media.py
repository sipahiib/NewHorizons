from pathlib import Path
import json,urllib.request,concurrent.futures,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent
m=json.loads((C/'media_sources.json').read_text());assert m['status']=='approved-for-download'
def fetch(a):
 p=ROOT/a['file'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  req=urllib.request.Request(a['url'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=90) as r,p.open('wb') as f:
   while b:=r.read(1024*1024):f.write(b)
 a['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 a['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate:format=duration','-of','json',str(p)]))
 print(a['id'],a['probe']['format']['duration'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,m['assets']))
(C/'media_verification.json').write_text(json.dumps(m,indent=2)+'\n')
