#!/usr/bin/env python3
"""Download and verify cycle-isolated media for 2026-11-23 main video."""
import hashlib, json, subprocess, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'assets/motion/2026-11-23/main'
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {'User-Agent': 'NewHorizonsEditorial/1.0 (https://github.com/newhorizons; editorial-research@newhorizons.local) curl/8.0'}

WM_FILES = [
    # M1 motion (7)
    ('m1-v01-mercury-transit.webm', 'M1', 'motion', 'contextual', 'File:Mercury Transit 2019 - 4K 2.webm'),
    ('m1-v02-bepi-flyby6.webm', 'M1', 'motion', 'direct', "File:BepiColombo's sixth Mercury flyby- the movie ESA505407.webm"),
    ('m1-v03-bepi-flyby4.webm', 'M1', 'motion', 'direct', "File:BepiColombo’s fourth Mercury flyby- the movie ESA501296.webm"),
    ('m1-v04-bepi-flyover.webm', 'M1', 'motion', 'direct', 'File:Fly over Mercury with BepiColombo ESA501304.webm'),
    ('m1-v05-bepi-flyby2.webm', 'M1', 'motion', 'direct', 'File:BepiColombo’s second Mercury flyby ESA468332.webm'),
    ('m1-v06-bepi-flyby1.webm', 'M1', 'motion', 'direct', 'File:Meeting Mercury ESA459665.webm'),
    ('m1-v07-bepi-vibtest.webm', 'M1', 'motion', 'direct', 'File:BepiColombo vibration test ESA380694.webm'),
    # M1 stills (5)
    ('m1-s01-bepi-hugs.png', 'M1', 'still', 'direct', 'File:BepiColombo hugs Mercury ESA24939504.png'),
    ('m1-s02-bepi-goodbye4.jpg', 'M1', 'still', 'direct', 'File:BepiColombo says goodbye to Mercury for the fourth time ESA501139 - BepiColombo says goodbye to Mercury for the fourth time.jpg'),
    ('m1-s03-bepi-mtm-estec.jpg', 'M1', 'still', 'direct', 'File:BepiColombo MTM ESTEC.jpg'),
    ('m1-s04-bepi-solarwing.jpg', 'M1', 'still', 'direct', 'File:Mercury Transfer Module solar wing deployment ESA380648.jpg'),
    ('m1-s05-esoc-control.jpg', 'M1', 'still', 'contextual', 'File:ESOC control room ESA253385.jpg'),
    # M2 motion (3 Wikimedia)
    ('m2-v01-mammography-usda.webm', 'M2', 'motion', 'contextual', 'File:20210609-RD-LSC-0070-Mammography Clips.webm'),
    ('m2-v02-chelsea-nhs.webm', 'M2', 'motion', 'contextual', 'File:Chelsea and Westminster Hospital Exterior, London.webm'),
    ('m2-v03-guys-nhs.webm', 'M2', 'motion', 'contextual', 'File:Guy’s Hospital Tower, London (2026).webm'),
    # M2 stills (5 Wikimedia, incl. backup)
    ('m2-s01-addenbrookes-1.jpg', 'M2', 'still', 'direct', "File:Addenbrooke's Hospital - geograph.org.uk - 3818932.jpg"),
    ('m2-s02-addenbrookes-2.jpg', 'M2', 'still', 'direct', "File:Addenbrooke's Hospital - geograph.org.uk - 3818935.jpg"),
    ('m2-s03-mammogram-calc.png', 'M2', 'still', 'contextual', 'File:Mammogram images of clustered calcifications at CC view and MLO view.png'),
    ('m2-s04-mammogram-mri.jpg', 'M2', 'still', 'contextual', 'File:Mammogram vs. MRI.jpg'),
    ('m2-s05-addenbrookes-pd.jpg', 'M2', 'still', 'direct', "File:Addenbrooke's hospital.JPG"),
]

PEXELS_FILES = [
    ('m2-v04-pexels-5207267.mp4', 'M2', 'motion', 'contextual', '5207267', 'https://www.pexels.com/video/doctor-reading-an-x-ray-scan-5207267/'),
    ('m2-v05-pexels-7089750.mp4', 'M2', 'motion', 'contextual', '7089750', 'https://www.pexels.com/video/doctor-reading-an-x-ray-scan-7089750/'),
    ('m2-v06-pexels-4225881.mp4', 'M2', 'motion', 'contextual', '4225881', 'https://www.pexels.com/video/doctors-examining-the-x-ray-result-4225881/'),
    ('m2-v07-pexels-7579841.mp4', 'M2', 'motion', 'contextual', '7579841', 'https://www.pexels.com/video/healthcare-professional-examining-a-chest-x-ray-while-wearing-protective-equipment-7579841/'),
    ('m2-v08-pexels-5843131.mp4', 'M2', 'motion', 'contextual', '5843131', 'https://www.pexels.com/video/a-doctor-and-a-sonographer-diagnosing-a-patient-mri-test-5843131/'),
    ('m2-v09-pexels-5843126.mp4', 'M2', 'motion', 'contextual', '5843126', 'https://www.pexels.com/video/a-doctor-and-patient-review-brain-scan-images-on-a-tablet-in-a-hospital-5843126/'),
    ('m2-v10-pexels-5842880.mp4', 'M2', 'motion', 'contextual', '5842880', 'https://www.pexels.com/video/a-sonographer-supervising-a-patient-mri-test-5842880/'),
]

def ffprobe_info(path: Path):
    res = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
        capture_output=True, text=True, check=True
    )
    meta = json.loads(res.stdout)
    v = next((s for s in meta.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not v:
        raise RuntimeError(f'No video stream in {path}')
    return {
        'width': v.get('width'),
        'height': v.get('height'),
        'codec': v.get('codec_name'),
        'fps': v.get('avg_frame_rate'),
        'duration': float(meta.get('format', {}).get('duration', 0) or 0),
        'bytes': path.stat().st_size,
    }

def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def sha1_file(path: Path):
    h = hashlib.sha1()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

# Fetch Wikimedia metadata in one API call
titles = [t for _, _, _, _, t in WM_FILES]
params = {
    'action': 'query',
    'titles': '|'.join(titles),
    'prop': 'imageinfo',
    'iiprop': 'url|size|sha1|mime|extmetadata',
    'format': 'json',
}
req = urllib.request.Request('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params), headers=HEADERS)
data = json.load(urllib.request.urlopen(req, timeout=30))
norm = {n['from']: n['to'] for n in data.get('query', {}).get('normalized', [])}
pages = {p['title']: p for p in data.get('query', {}).get('pages', {}).values()}

entries = []
for fname, story, kind, role, title in WM_FILES:
    ntitle = norm.get(title, title)
    page = pages.get(ntitle)
    if not page or 'imageinfo' not in page:
        print(f'MISSING WM: {title}')
        entries.append({'file': fname, 'story': story, 'kind': kind, 'role': role, 'title': title, 'error': 'missing_on_commons'})
        continue
    ii = page['imageinfo'][0]
    meta = ii.get('extmetadata') or {}
    url = ii['url']
    dest = OUT / fname
    if not dest.exists():
        print(f'GET WM {fname} ...', flush=True)
        ok = False
        for attempt in range(3):
            if attempt > 0:
                wait = 4 * attempt
                print(f'  retry {attempt} after {wait}s...', flush=True)
                time.sleep(wait)
            r = subprocess.run([
                'curl', '--fail', '--location', '--silent', '--show-error',
                '-A', HEADERS['User-Agent'], '--connect-timeout', '20', '--max-time', '240',
                '-o', str(dest), url
            ])
            if r.returncode == 0:
                ok = True
                break
            if dest.exists():
                dest.unlink()
        if not ok:
            print(f'SKIP WM {fname}: download failed', flush=True)
            entries.append({'file': fname, 'story': story, 'kind': kind, 'role': role, 'title': ntitle, 'error': 'download_failed'})
            continue
        time.sleep(2)
    local_sha1 = sha1_file(dest)
    if local_sha1 != ii['sha1']:
        raise ValueError(f'SHA1 mismatch for {fname}: {local_sha1} != {ii["sha1"]}')
    rec = {
        'file': str(dest.relative_to(ROOT)),
        'story': story,
        'kind': kind,
        'role': role,
        'source_kind': 'wikimedia',
        'title': ntitle,
        'page': ii['descriptionurl'],
        'url': url,
        'mime': ii['mime'],
        'width': ii['width'],
        'height': ii['height'],
        'sha1': local_sha1,
        'sha256': sha256_file(dest),
        'license': (meta.get('LicenseShortName') or {}).get('value'),
        'license_url': (meta.get('LicenseUrl') or {}).get('value'),
        'artist_html': (meta.get('Artist') or {}).get('value'),
        'credit_html': (meta.get('Credit') or {}).get('value'),
    }
    if kind == 'motion':
        rec['probe'] = ffprobe_info(dest)
        print(f"OK {fname}: {rec['probe']['width']}x{rec['probe']['height']} {rec['probe']['duration']:.1f}s ({rec['license']})", flush=True)
    else:
        print(f"OK {fname}: {rec['width']}x{rec['height']} ({rec['license']})", flush=True)
    entries.append(rec)

for fname, story, kind, role, pid, page_url in PEXELS_FILES:
    dest = OUT / fname
    route = f'https://www.pexels.com/download/video/{pid}/'
    try:
        if not dest.exists():
            print(f'GET Pexels {fname} ...', flush=True)
            r = subprocess.run([
                'curl', '--fail', '--location', '--silent', '--show-error',
                '--connect-timeout', '20', '--max-time', '180', '--max-filesize', '524288000',
                '-o', str(dest), '-w', '%{url_effective}', route
            ], capture_output=True, text=True, check=True)
            eff = r.stdout.strip()
        else:
            eff = route
        pinfo = ffprobe_info(dest)
        rec = {
            'file': str(dest.relative_to(ROOT)),
            'story': story,
            'kind': kind,
            'role': role,
            'source_kind': 'pexels',
            'asset_id': pid,
            'page': page_url,
            'url': route,
            'effective_url': eff,
            'width': pinfo['width'],
            'height': pinfo['height'],
            'sha256': sha256_file(dest),
            'license': 'Pexels License',
            'license_url': 'https://www.pexels.com/license/',
            'probe': pinfo,
        }
        print(f"OK {fname}: {pinfo['width']}x{pinfo['height']} {pinfo['duration']:.1f}s (Pexels)", flush=True)
        entries.append(rec)
    except Exception as e:
        if dest.exists():
            dest.unlink()
        print(f'ERR Pexels {fname}: {e}', flush=True)
        entries.append({'file': fname, 'story': story, 'kind': kind, 'role': role, 'asset_id': pid, 'error': str(e)})

# Cross-cycle hash check
prior_hashes = set()
motion_root = ROOT / 'assets/motion'
for p in motion_root.rglob('*'):
    if p.is_file() and '2026-11-23' not in p.parts:
        prior_hashes.add(sha256_file(p))
dupes = [e['file'] for e in entries if e.get('sha256') in prior_hashes]
out_meta = {
    'cycle': '2026-11-23',
    'status': 'downloaded-for-audit',
    'prior_cycle_hash_collisions': dupes,
    'assets': entries,
}
meta_path = ROOT / 'video/cycles/2026-11-23/main_media_metadata.json'
meta_path.write_text(json.dumps(out_meta, indent=2, ensure_ascii=False) + '\n')
print(f'Saved {meta_path}; assets={len(entries)}; prior_collisions={len(dupes)}')
