"""Fetch cycle-isolated Pexels excerpts. Run only for an approved cycle."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[3]
CYCLE = Path(__file__).resolve().parent
ITEMS = json.loads((CYCLE / 'stock_candidates.json').read_text())
record_file = CYCLE / 'stock_downloads.json'
records = {r['id']: r for r in json.loads(record_file.read_text())} if record_file.exists() else {}

for item in ITEMS:
    if len(sys.argv) > 1 and item['story'] not in sys.argv[1:]:
        continue
    iid = item['id']
    subdir = 'reels' if item['story'].startswith('r') else 'main'
    rel = Path(f'assets/motion/2026-09-30/{subdir}/{item["story"]}/{item["slug"]}.mp4')
    dest = ROOT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if iid in records and dest.exists() and dest.stat().st_size > 1024:
        print(f'skip {iid}', flush=True)
        continue
    page = f'https://www.pexels.com/video/{iid}/'
    endpoint = f'https://www.pexels.com/download/video/{iid}/'
    req = Request(endpoint, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=25) as response:
            source = response.url
        subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',source,'-t',str(item['seconds']),
                        '-vf','scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2',
                        '-an','-c:v','libx264','-preset','veryfast','-crf','20',str(dest)],check=True,timeout=120)
        probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
            'format=duration,size:stream=width,height,r_frame_rate','-of','json',str(dest)]))
        records[iid] = {**item,'page':page,'download':source,'file':str(rel),
            'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'probe':probe}
        record_file.write_text(json.dumps(list(records.values()),indent=2)+'\n')
        print(f'ok {item["story"]} {iid}: {probe["format"]["duration"]}s',flush=True)
    except Exception as exc:
        print(f'ERROR {item["story"]} {iid}: {exc}',flush=True)
