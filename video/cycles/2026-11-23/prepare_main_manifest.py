#!/usr/bin/env python3
"""Build 2026-11-23 main_manifest.json with verified hashes and scene timings."""
import hashlib, json
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parents[2]
M = 'assets/motion/2026-11-23/main'
O = 'build/video/2026-11-23/overlays'
A = 'build/video/2026-11-23/audio'

# M1: 135s total (16s opening + 119s body) — 6 motion sources (7 motion scenes) + 5 stills = 12 scenes
# Every seek avoids black frames detected in task-139.
m1_scenes = [
    # Opening 0:00-0:16
    {'kind': 'motion', 'file': f'{M}/m1-v01-mercury-transit.webm', 'seek': 12.0, 'duration': 5.0, 'role': 'contextual', 'note': '0:00-0:05 hook: NASA SDO Mercury transit'},
    {'kind': 'motion', 'file': f'{M}/m1-v02-bepi-flyby6.webm', 'seek': 30.0, 'duration': 7.0, 'role': 'direct', 'note': '0:05-0:12 support: BepiColombo 6th Mercury flyby'},
    {'kind': 'motion', 'file': f'{M}/m2-v01-mammography-usda.webm', 'seek': 16.0, 'duration': 4.0, 'role': 'contextual', 'note': '0:12-0:16 M2 teaser: mammography suite'},
    # M1 body 0:16-2:15 (119s)
    {'kind': 'motion', 'file': f'{M}/m1-v03-bepi-flyby4.webm', 'seek': 22.0, 'duration': 15.0, 'role': 'direct', 'note': '4th flyby approach'},
    {'kind': 'motion', 'file': f'{M}/m1-v01-mercury-transit.webm', 'seek': 52.0, 'duration': 14.0, 'role': 'contextual', 'note': 'NASA SDO Mercury against Sun'},
    {'kind': 'still',  'file': f'{M}/m1-s01-bepi-hugs.png', 'crop': '8533:7100:0:820', 'duration': 10.0, 'role': 'direct', 'note': 'M-CAM Mercury close-up (cropped)'},
    {'kind': 'motion', 'file': f'{M}/m1-v05-bepi-flyby2.webm', 'seek': 14.0, 'duration': 14.0, 'role': 'direct', 'note': '2nd Mercury flyby'},
    {'kind': 'still',  'file': f'{M}/m1-s03-bepi-mtm-estec.jpg', 'duration': 10.0, 'role': 'direct', 'note': 'MTM hardware at ESTEC'},
    {'kind': 'motion', 'file': f'{M}/m1-v07-bepi-vibtest.webm', 'seek': 20.0, 'duration': 14.0, 'role': 'direct', 'note': 'Cleanroom vibration test of MPO + Mio stack'},
    {'kind': 'still',  'file': f'{M}/m1-s04-bepi-solarwing.jpg', 'duration': 10.0, 'role': 'direct', 'note': 'Solar wing deployment test at ESTEC'},
    {'kind': 'still',  'file': f'{M}/m1-s05-esoc-control.jpg', 'duration': 10.0, 'role': 'contextual', 'note': 'ESA ESOC Main Control Room archive'},
    {'kind': 'motion', 'file': f'{M}/m1-v06-bepi-flyby1.webm', 'seek': 35.0, 'duration': 11.0, 'role': 'direct', 'note': '1st Mercury flyby real M-CAM'},
    {'kind': 'still',  'file': f'{M}/m1-s02-bepi-goodbye4.jpg', 'crop': '8533:7100:0:820', 'duration': 11.0, 'role': 'direct', 'note': '4th flyby departure M-CAM (cropped)'},
]
assert sum(s['duration'] for s in m1_scenes) == 135.0

# M2: 112s total (2:15-4:07) — 6 motion scenes across 4 verified sources + 4 clean stills = 10 scenes
m2_scenes = [
    {'kind': 'still',  'file': f'{M}/m2-s05-addenbrookes-pd.jpg', 'duration': 10.0, 'role': 'direct', 'note': "Addenbrooke's Hospital campus, Cambridge"},
    {'kind': 'motion', 'file': f'{M}/m2-v01-mammography-usda.webm', 'seek': 2.0, 'duration': 12.0, 'role': 'contextual', 'note': 'Mammography clinic suite'},
    {'kind': 'still',  'file': f'{M}/m2-s02-addenbrookes-2.jpg', 'duration': 10.0, 'role': 'direct', 'note': "Addenbrooke's Hospital health research bus"},
    {'kind': 'motion', 'file': f'{M}/m2-v02-chelsea-nhs.webm', 'seek': 2.0, 'duration': 12.0, 'role': 'contextual', 'note': 'UK NHS hospital exterior'},
    {'kind': 'motion', 'file': f'{M}/m2-v07-pexels-7579841.mp4', 'seek': 1.0, 'duration': 12.0, 'role': 'contextual', 'note': 'Clinician reviewing scan'},
    {'kind': 'still',  'file': f'{M}/m2-s04-mammogram-mri.jpg', 'crop': '1340:940:680:350', 'duration': 10.0, 'role': 'contextual', 'note': 'Mammogram & MRI scan panels (text cropped out)'},
    {'kind': 'motion', 'file': f'{M}/m2-v01-mammography-usda.webm', 'seek': 26.0, 'duration': 12.0, 'role': 'contextual', 'note': 'Technician at mammography console'},
    {'kind': 'motion', 'file': f'{M}/m2-v03-guys-nhs.webm', 'seek': 2.0, 'duration': 12.0, 'role': 'contextual', 'note': "UK NHS hospital exterior (Guy's)"},
    {'kind': 'still',  'file': f'{M}/m2-s01-addenbrookes-1.jpg', 'duration': 10.0, 'role': 'direct', 'note': "Addenbrooke's Hospital building, Cambridge"},
    {'kind': 'motion', 'file': f'{M}/m2-v07-pexels-7579841.mp4', 'seek': 14.0, 'duration': 12.0, 'role': 'contextual', 'note': 'Clinician close-up scan review'},
]
assert sum(s['duration'] for s in m2_scenes) == 112.0

manifest = {
    'cycle': '2026-11-23',
    'width': 1920,
    'height': 1080,
    'fps': 60,
    'duration': 257.0,
    'openingSeconds': 16,
    'subscribeWindow': [30.0, 35.5],
    'subscribeOverlay': f'{O}/subscribe.png',
    'closing': f'{O}/closing-bg.png',
    'closingPanel': f'{O}/closing-panel.png',
    'closingBell': f'{O}/bell.png',
    'candidateOutput': 'build/video/2026-11-23/newhorizons.mp4',
    'output': 'build/video/newhorizons.mp4',
    'visualCounts': {
        'm1': {'motionScenes': 8, 'uniqueMotionFiles': 6, 'stills': 5},
        'm2': {'motionScenes': 6, 'uniqueMotionFiles': 4, 'stills': 4},
    },
    'sections': [
        {
            'id': 'm1',
            'title': f'{O}/title-bepicolombo.png',
            'duration': 135.0,
            'audio': f'{A}/main-lead-assembled.wav',
            'leadingSilence': 0.0,
            'scenes': m1_scenes,
        },
        {
            'id': 'm2',
            'title': f'{O}/title-edith.png',
            'duration': 112.0,
            'audio': f'{A}/main-second.mp3',
            'leadingSilence': 0.4,
            'scenes': m2_scenes,
        },
        {
            'id': 'closing',
            'closing': True,
            'duration': 10.0,
            'audio': f'{A}/main-closing.mp3',
            'leadingSilence': 1.0,
        },
    ],
    'hashes': {},
}

# Collect SHA-256 of every referenced input file
files = {
    manifest['subscribeOverlay'], manifest['closing'], manifest['closingPanel'], manifest['closingBell']
}
for sec in manifest['sections']:
    if sec.get('title'):
        files.add(sec['title'])
    if sec.get('audio'):
        files.add(sec['audio'])
    for s in sec.get('scenes', []):
        files.add(s['file'])

for rel in sorted(files):
    p = R / rel
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    manifest['hashes'][rel] = h.hexdigest()

out = C / 'main_manifest.json'
out.write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Wrote {out}: duration={manifest["duration"]}s, hashed_files={len(manifest["hashes"])}')
