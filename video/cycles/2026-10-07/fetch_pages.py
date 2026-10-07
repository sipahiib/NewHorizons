"""Retain primary source/media page snapshots for this cycle's audit."""
from urllib.request import urlopen, Request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
C = Path(__file__).resolve().parent
assert 'Status: **approved**' in (C/'APPROVAL.md').read_text()
P = C/'source_pages'; P.mkdir(exist_ok=True)
URLS = {
 'webb':'https://science.nasa.gov/asset/webb/ngc-7129-nircam-image/',
 'webb_compare':'https://science.nasa.gov/missions/webb/nasas-webb-captures-commotion-from-nebulas-stellar-jets/',
 'webb_broll':'https://svs.gsfc.nasa.gov/12461/',
 'webb_cleanroom':'https://svs.gsfc.nasa.gov/12896/',
 'climate':'https://climate.esa.int/en/news-events/2026-climate-science-headlines-outlined-in-new-report/',
 'glacier':'https://www.esa.int/ESA_Multimedia/Videos/2021/09/Glaciers_and_climate_change2',
 'sando':'https://news.mit.edu/2026/planning-system-ensures-robots-flight-path-will-remain-collision-free-1007',
 'ironclad':'https://openai.com/index/advancing-computer-use-with-ironclad/',
}
def get(item):
 k,u=item
 try:
  with urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:data=r.read()
  (P/f'{k}.html').write_bytes(data);return k,len(data)
 except Exception as e:return k,str(e)
with ThreadPoolExecutor(max_workers=6) as ex:
 for row in ex.map(get,URLS.items()):print(row,flush=True)
