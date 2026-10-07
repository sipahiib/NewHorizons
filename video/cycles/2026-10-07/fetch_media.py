"""Download only this cycle's explicitly selected, approved source registry."""
import json,hashlib,subprocess
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
C=Path(__file__).resolve().parent;ROOT=C.parents[2]
assert 'Status: **approved**' in (C/'APPROVAL.md').read_text()
items=[a for a in json.loads((C/'media_sources.json').read_text()) if not a.get('derivation') and any(a['url'].startswith(h) for h in ('https://assets.science.nasa.gov/','https://svs.gsfc.nasa.gov/','https://dlmultimedia.esa.int/'))]
def get(a):
 p=ROOT/a['file'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists() or p.stat().st_size<1024:
  partial=p.with_suffix(p.suffix+'.part')
  with urlopen(Request(a['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as r,partial.open('wb') as f:
   while b:=r.read(1024*1024):f.write(b)
  partial.replace(p)
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 return {'file':a['file'],'bytes':p.stat().st_size,'sha256':sha,'probe':probe}
with ThreadPoolExecutor(max_workers=4) as ex:
 results=[]
 for r in ex.map(get,items):
  results.append(r);(C/'native_source_probes.json').write_text(json.dumps(results,indent=2)+'\n');print(r['file'],r['bytes'],flush=True)
