#!/usr/bin/env python3
"""Resolve primary source URLs and query media catalogs for 2026-11-23 cycle."""
import json, re, urllib.parse, urllib.request
from pathlib import Path

HEADERS = {'User-Agent': 'NewHorizonsEditorial/1.0 (science news research)'}

REDIRECTS = {
    'esa_arrival_1': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGnG0aLPaDiJG360iAhBYDwE4Hsw70bcElBFxPGxtjKJHmYMQjqtVI1EqtgCV-5gv56Gb1VB6o2S5oi4eWHCkBLNr8d8AO0qQuNhMoMcwDngFrhrNQ39Zcv7IrO3z8ZCiVg8-P-_E_WhUEz6Ya787ibfH99pa1cdgBLxeQ02rWe5EEvHB2kvtz5hkERpZdM5CaSxTp2BAlZ',
    'esa_arrival_2': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE_KAYLy8M7_WbanSLWfalE6D79kllbBuLUqXhBOEGnf9W7JsLeJxYXAVajFM1PM4PSUBLAezlscBZ19Ci87Igbo2gdST7cqvTY2Hv-_Jwip626sD7dlHLme9MucSelrx-DJPMVDApP1Z9-F-ottCWDqHxCavARHA==',
    'esa_arrival_3': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGwAZ5vjjC37GN4CkFX0APSq2FhnuuGiWftpP7hJN3ay5pwnLhfYhspWxhtrPUDBf7uxLy6iInxFTWen0OlWVbPJeFzwGrywAt17cAWyiBWs11HvXb3zw_nWMFHx2RLTqTV-BUP8xDzqKzH7w3F_KMZhOevuOe1GW-GU6kFW0d8RZ0kchUIuZ5F6AnTP2MH5zQ8fXtZ_63iBCBYcbO1eiff5YXeIE4sSspSijv',
    'warwick_edith': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrLRIDoVtjfeV40tnjGMCKGbhPOeiBLp0jqsfUN3vWbkbkWUOlvuEHkgqKpqVwwbEtA0G5D2uC9zd8B40VcPJ7EaAHEBG21RpEXvQctQQaKqz-lNro9pSFXKzAaX4Wztg434J7VLoIFTWw8sFNnBUVSpNa_oIr9FU53Ctb',
    'cuh_edith': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHoVbSqJj1hdTDOMtFZAhKHaidyRXXSdU3E4Im8Bf3I2-f7CGKj3EzWRWbj_A8bKuvEZrQfxExHaLSTqF9dESpyCEKXa-p83MIOAruYTTmr8HECxlx97H5g9Hmt5NrWXeKzplO--P8G6Qg0AKHaH56XwWqR8Aa6sfMuwVaZrdn0ShTXQkZTnhWEnqYhLet7bG4Tc-4XcLk=',
    'cam_edith': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFRfV8CgqI3-fjnAFUvMQpcESyu3V5YjjSKCDBUe54zrT35S04Nit9cOVp4gCO92HFsn-1ygkOC5Cca6irp0ezdGBHbu6duv75ScfbZ5Ler3ByiqixHoYBLanaB3XZ2-O8mdywvF22zTSMhs7PA519Ic1vpS0KmiALkb5oQNej_9H9DjTxaX9le7183Yen77YY0Z8LO9uVPHpMb4xQRlG67BZe4vkHNDl-KSyu3G7zgvxL1',
    'nihr_edith': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGbnfjf_-52da7PniaTsCInwsaNvSt-vG4ZnwbNOd3tB-JZobvnzATrv6OLE0pqGxmMdo_Rha9Gp-PVDETSPC_yHqbPuoN984xAdsaog_pP0rRdXsO3XZAlnpFVPilypLlHWSBtMU_9PRCB6sglonTeNcIulMvrxrdYNPBHeqii1ue4czoeJxjqfR6ruw==',
}

def fetch_info(url, timeout=20):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        final = r.geturl()
        body = r.read(250000).decode('utf-8', 'ignore')
        m = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
        title = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
        return final, title, body

out = {'resolved': {}, 'esa_news': [], 'wikimedia': {}}

for k, u in REDIRECTS.items():
    try:
        final, title, body = fetch_info(u)
        # extract brief text snippet
        text = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', body, flags=re.S | re.I)
        text = re.sub(r'\s+', ' ', text).strip()
        out['resolved'][k] = {'url': final, 'title': title, 'snippet': text[:1200]}
        print(f'OK {k}: {final} | {title}')
    except Exception as e:
        out['resolved'][k] = {'error': str(e)}
        print(f'ERR {k}: {e}')

# Query ESA BepiColombo main page for latest November 2026 articles and multimedia links
try:
    _, _, body = fetch_info('https://www.esa.int/Science_Exploration/Space_Science/BepiColombo')
    links = sorted(set(re.findall(r'href="(/(?:Science_Exploration/Space_Science/BepiColombo|ESA_Multimedia)/[^"]+)"', body)))
    out['esa_news'] = ['https://www.esa.int' + l for l in links[:40]]
    print(f'ESA BepiColombo page links: {len(links)}')
except Exception as e:
    print(f'ERR esa_news: {e}')

# Query Wikimedia Commons for BepiColombo, Mercury, Mammography, Addenbrooke's, Radiology videos and images
def wm_search(query, namespace=6, limit=15):
    params = {
        'action': 'query',
        'generator': 'search',
        'gsrsearch': query,
        'gsrnamespace': str(namespace),
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
            'artist': re.sub(r'<[^>]+>', '', (meta.get('Artist') or {}).get('value', ''))[:120],
        })
    return items

for label, q in [
    ('bepicolombo_all', 'BepiColombo Mercury'),
    ('bepicolombo_video', 'BepiColombo filetype:video'),
    ('mammogram_img', 'mammogram breast screening radiology'),
    ('mammography_video', 'mammography OR radiologist OR hospital filetype:video'),
    ('addenbrookes', "Addenbrooke's Hospital Cambridge"),
    ('radiologist_review', 'radiologist reading scan monitor'),
]:
    try:
        res = wm_search(q, limit=12)
        out['wikimedia'][label] = res
        print(f'WM {label}: {len(res)} items')
    except Exception as e:
        out['wikimedia'][label] = {'error': str(e)}
        print(f'ERR WM {label}: {e}')

dest = Path('video/cycles/2026-11-23/source_probe.json')
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print('Saved', dest)
