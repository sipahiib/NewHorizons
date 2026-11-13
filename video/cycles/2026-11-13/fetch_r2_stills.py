#!/usr/bin/env python3
"""Download candidate Flow Country stills and save Wikimedia source metadata."""
import hashlib, json, pathlib, urllib.parse, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'build/video/2026-11-13/media/r2'
OUT.mkdir(parents=True, exist_ok=True)
TITLES = [
 'File:Blanket bog in the Flow Country - geograph.org.uk - 7453418.jpg',
 'File:Blanket bog in the Flow Country - geograph.org.uk - 7453577.jpg',
 'File:Heading south across the Flow country bog - geograph.org.uk - 5737511.jpg',
 'File:Hills and bog of the Flow Country - geograph.org.uk - 7068579.jpg',
 'File:Wetland in the Flow Country, Scotland, UK - geograph.org.uk - 5668315.jpg',
 'File:The A838 through Flow Country - geograph.org.uk - 7453413.jpg',
 'File:Where once were trees in the Flow Country - geograph.org.uk - 7919865.jpg',
]
HEADERS = {'User-Agent': 'NewHorizonsEditorial/1.0 (science news research)'}
params = {'action':'query','titles':'|'.join(TITLES),'prop':'imageinfo','iiprop':'url|size|sha1|extmetadata','format':'json'}
req = urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params), headers=HEADERS)
data = json.load(urllib.request.urlopen(req,timeout=30)); entries=[]
pages={p['title']:p for p in data['query']['pages'].values()}
for n,title in enumerate(TITLES,1):
 p=pages[title]; info=p['imageinfo'][0]; meta=info['extmetadata']; url=info['url']; path=OUT / (f'verified-{n:02}.jpg' if n in (3,4) else f'flow-{n:02}.jpg')
 
 if not path.exists(): continue
 raw=path.read_bytes()
 if hashlib.sha1(raw).hexdigest()!=info['sha1']: raise ValueError(f'Source mismatch: {title}')
 entries.append({'file':str(path.relative_to(ROOT)),'title':title,'page':info['descriptionurl'],'url':url,'width':info['width'],'height':info['height'],'sha256':hashlib.sha256(raw).hexdigest(),'commons_sha1':info['sha1'],'local_sha1':hashlib.sha1(raw).hexdigest(),'license':meta.get('LicenseShortName',{}).get('value'),'license_url':meta.get('LicenseUrl',{}).get('value'),'artist_html':meta.get('Artist',{}).get('value'),'credit_html':meta.get('Credit',{}).get('value'),'description_html':meta.get('ImageDescription',{}).get('value')})
(ROOT/'video/cycles/2026-11-13/r2_source_metadata.json').write_text(json.dumps(entries,indent=2,ensure_ascii=False)+'\n')
print('Recorded metadata for',len(entries),'downloaded candidates')
