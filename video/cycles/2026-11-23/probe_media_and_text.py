#!/usr/bin/env python3
"""Fetch full primary article texts and search Wikimedia Commons for M1/M2 media."""
import json, re, urllib.parse, urllib.request
from pathlib import Path

HEADERS = {'User-Agent': 'NewHorizonsEditorial/1.0 (science news research)'}

URLS = {
    'esa_orbit': 'https://www.esa.int/media/about-us/directorates/science/bepicolombo-entering-orbit-around-mercury',
    'esa_timeline': 'https://www.esa.int/media/bepicolombo-arrival-at-mercury-timeline',
    'warwick': 'https://warwick.ac.uk/news/pressreleases/first-women-join-EDITH-trial/',
    'cuh': 'https://www.cuh.nhs.uk/news/cambridgeshire-women-first-join-world-leading-breast-screening-trial/',
    'esa_bepi_news_redirect': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEDvWrLmFs3V7vsXl4q-Pe0PImU48HHIsGMJzsO2R2wlk8RSnZyTUipN_y8dJFDV3imeO6GhpO6htMLqh7JJcml8me_Y5cMBwtOqp-vG5YJucCw-bXfwhHSnnS6rC7BMTz6DU6wyMOBLWVBxnYmqSyih3f7EPClsG4iNoej5X-Qgs40O2w3qyDgOhy2ej8jLgPrCTIZ78jre9dxDNBZJ7wiDI-MZEY=',
    'aa_bepi_redirect': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF05Tzlsn74DFMz2sqqJr4rJ7-VHd-INuTAD6ddO_VyI7c5yzpC5nCHmWBOLbqs_gAs-faMd7tffTSFN0JMUqPSmkdVnykv5p-aU39qUOzNKNw4qlVNbV66GCyhybZIUkThr8ixRnY3GbEKas9w7JdiON16C1fR9n7myWmhjPDeGqbj3N8nvAvV3a7H1Owkh2K_YJioFoxDpsZV_5YjoOM=',
}

def fetch_text(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        final = r.geturl()
        html = r.read(400000).decode('utf-8', 'ignore')
        # grab main/article if present
        m = re.search(r'<main[^>]*>(.*?)</main>', html, re.S | re.I) or re.search(r'<article[^>]*>(.*?)</article>', html, re.S | re.I)
        chunk = m.group(1) if m else html
        txt = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', chunk, flags=re.S | re.I)
        txt = re.sub(r'\s+', ' ', txt).strip()
        return final, txt[:4500]

def wm_search(query, limit=15):
    params = {
        'action': 'query',
        'generator': 'search',
        'gsrsearch': query,
        'gsrnamespace': '6',
        'gsrlimit': str(limit),
        'prop': 'imageinfo',
        'iiprop': 'url|size|mime|extmetadata',
        'format': 'json',
    }
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    data = json.load(urllib.request.urlopen(req, timeout=20))
    items = []
    for p in data.get('query', {}).get('pages', {}).values():
        ii = (p.get('imageinfo') or [{}])[0]
        meta = ii.get('extmetadata') or {}
        items.append({
            'title': p.get('title'),
            'mime': ii.get('mime'),
            'width': ii.get('width'),
            'height': ii.get('height'),
            'url': ii.get('url'),
            'page': ii.get('descriptionurl'),
            'license': (meta.get('LicenseShortName') or {}).get('value'),
            'license_url': (meta.get('LicenseUrl') or {}).get('value'),
            'artist': re.sub(r'<[^>]+>', '', (meta.get('Artist') or {}).get('value', ''))[:120],
            'desc': re.sub(r'<[^>]+>', '', (meta.get('ImageDescription') or {}).get('value', ''))[:200],
        })
    return items

out = {'articles': {}, 'wikimedia': {}}
for k, u in URLS.items():
    try:
        final, txt = fetch_text(u)
        out['articles'][k] = {'url': final, 'text': txt}
        print(f'OK {k}: {final} ({len(txt)} chars)')
    except Exception as e:
        out['articles'][k] = {'error': str(e)}
        print(f'ERR {k}: {e}')

for label, q in [
    ('bepi_launch_esoc_vid', 'BepiColombo Ariane OR ESOC OR ESTEC OR Mercury filetype:video'),
    ('bepi_esoc_img', 'BepiColombo ESOC OR Ariane OR ESTEC filetype:bitmap'),
    ('esoc_control_vid', 'ESOC Darmstadt control room ESA filetype:video'),
    ('mammogram_img', 'mammogram OR mammography filetype:bitmap'),
    ('radiologist_img', 'radiologist monitor OR breast cancer screening filetype:bitmap'),
    ('medical_vid', 'radiology OR hospital doctor OR medical imaging OR cancer screening filetype:video'),
    ('nhs_vid', 'NHS hospital England OR Cambridge filetype:video'),
]:
    try:
        res = wm_search(q, limit=15)
        out['wikimedia'][label] = res
        print(f'WM {label}: {len(res)} items')
    except Exception as e:
        out['wikimedia'][label] = {'error': str(e)}
        print(f'ERR WM {label}: {e}')

dest = Path('video/cycles/2026-11-23/media_text_probe.json')
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print('Saved', dest)
