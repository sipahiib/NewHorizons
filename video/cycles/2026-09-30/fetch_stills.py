"""Download candidate Commons stills with creator/licence provenance for review."""
import hashlib,json,urllib.parse,urllib.request,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CYCLE=Path(__file__).resolve().parent
queries={'m2':['Programmer writing code with Unit Tests','Programmers'], 'm3':['Hoover Dam Hydroelectric Pumps','ThreeGorgesDam-China2009'], 'm4':['BioFarma vaccine vials Bandung','Influenza virus research'], 'm5':['The-model-wind-turbine-and-the-active-grid-installed-in-a-wind-tunnel-of-the-University-of-Oldenburg','Farnborough Wind Tunnel Q121 Main Fan'], 'r1':['Computer user video call','Woman laptop video conference','Person typing on laptop'], 'r2':['Lake drought Spain','Mediterranean coast Greece','Irrigation vineyard Europe']}
records=[]
for story,terms in queries.items():
 for term in terms:
  params={'action':'query','generator':'search','gsrsearch':'filetype:bitmap '+term,'gsrnamespace':6,'gsrlimit':5,'prop':'imageinfo','iiprop':'url|size|extmetadata','format':'json'}
  url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
  data=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NewHorizons/1.0 editorial research'}),timeout=30))
  pages=list(data.get('query',{}).get('pages',{}).values())
  pages.sort(key=lambda x:0 if term.lower() in x['title'].lower() else 1)
  chosen=None
  for page in pages:
   info=page.get('imageinfo',[{}])[0];lic=info.get('extmetadata',{}).get('LicenseShortName',{}).get('value','')
   if info.get('width',0)>=1000 and info.get('height',0)>=700 and (lic.startswith('CC') or lic=='Public domain') and info.get('url','').lower().split('?')[0].endswith(('.jpg','.jpeg','.png')):
    chosen=(page,info,lic);break
  if not chosen:
   print('NO MATCH',story,term,flush=True);continue
  page,info,lic=chosen;meta=info.get('extmetadata',{})
  name=re.sub(r'[^a-z0-9]+','-',term.lower()).strip('-')[:55]+'.'+info['url'].split('?')[0].split('.')[-1].lower()
  rel=Path(f'assets/motion/2026-09-30/{"reels" if story.startswith("r") else "main"}/{story}/{name}')
  dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  try:
   req=urllib.request.Request(info['url'],headers={'User-Agent':'NewHorizons/1.0 editorial research'})
   with urllib.request.urlopen(req,timeout=50) as inp,dest.open('wb') as out:
    while chunk:=inp.read(1<<20):out.write(chunk)
   record={'story':story,'query':term,'title':page['title'],'file':str(rel),'source':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(page['title'].replace(' ','_')),'download':info['url'],'width':info['width'],'height':info['height'],'license':lic,'artist':meta.get('Artist',{}).get('value',''),'licenseUrl':meta.get('LicenseUrl',{}).get('value',''),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
   records.append(record);(CYCLE/'commons_stills.json').write_text(json.dumps(records,indent=2)+'\n');print(story,page['title'],lic,flush=True)
  except Exception as e:print('ERROR',story,term,e,flush=True)
