from pathlib import Path
import json,urllib.request,concurrent.futures
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent

def resolve(row):
 id,slug,credit,fps=row
 # Public Pexels CDN variants; select only a URL which responds successfully.
 for res in ['hd_1920_1080','uhd_3840_2160','uhd_4096_2160','uhd_2560_1440','hd_1280_720']:
  for f in dict.fromkeys([fps,25,24,30]):
   url=f'https://videos.pexels.com/video-files/{id}/{id}-{res}_{f}fps.mp4'
   try:
    req=urllib.request.Request(url,method='HEAD',headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=15) as r:
     if r.status==200:
      print(id,res,f,flush=True)
      return dict(id=id,page=f'https://www.pexels.com/video/{slug}-{id}/',url=url,file=f'assets/motion/{C.name}/main/{id}.mp4',classification='contextual',rights='Pexels License',credit=credit)
   except Exception:pass
 print('UNRESOLVED',id,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: assets=list(pool.map(resolve,json.loads((C/'media_candidates.json').read_text())))
(C/'media_sources.json').write_text(json.dumps(dict(cycle=C.name,status='approved-for-download',assets=[a for a in assets if a]),indent=2)+'\n')
