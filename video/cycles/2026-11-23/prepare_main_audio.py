#!/usr/bin/env python3
"""Synthesize approved 2026-11-23 main narration with Edge TTS and measure durations."""
import json, os, subprocess
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parents[2]
OUT = R / 'build/video/2026-11-23/audio'
OUT.mkdir(parents=True, exist_ok=True)

PARTS = {
    'hook': 'The hardest place to park in the Solar System is right next to the Sun.',
    'support': 'After an eight-year journey, BepiColombo has finally been captured into orbit around Mercury.',
    'teaser': "And later, seven hundred thousand women join the world's largest trial of AI in breast screening.",
    'lead': (
        "On the twenty-first of November, the joint European Space Agency and Japan Aerospace Exploration Agency "
        "mission BepiColombo fired four thrusters on Mercury's night side and slowed down enough to be captured "
        "by the planet's gravity.\n\n"
        "Reaching Mercury is one of orbital mechanics' toughest puzzles. Because the planet orbits so close to the Sun, "
        "a spacecraft falling inward accelerates rapidly. To enter orbit instead of whipping past, BepiColombo had to "
        "shed huge amounts of orbital energy across an eight-year cruise that began in October twenty-eighteen, using "
        "nine planetary flybys—including six past Mercury itself. The archive solar-transit footage here from NASA "
        "shows how small Mercury sits beside the Sun, while the close-up black-and-white views come from "
        "BepiColombo's own monitoring cameras during those earlier flybys, alongside pre-launch cleanroom tests and "
        "an archive view of Europe's operations centre in Darmstadt.\n\n"
        "BepiColombo is only the second mission ever to orbit Mercury, and the first carrying two separate science "
        "orbiters: Europe's Mercury Planetary Orbiter and Japan's Mio, sheltered inside a sunshield. Together, they "
        "are designed to study the planet's magnetic field, its dense iron-rich interior, its cratered surface, and "
        "ice hidden in permanently shadowed polar craters.\n\n"
        "Capture day also brought a real-world engineering reminder. ESA reported that a software issue cut the "
        "braking burn shorter than planned. Mission controllers confirmed the spacecraft is safe, and teams are still "
        "assessing the exact initial orbit—planned as an elliptical path five hundred and ninety by eleven thousand "
        "six hundred and forty kilometres around the poles. Under ESA's arrival plan, the two orbiters are due to "
        "separate on the ninth and tenth of December, with Mio's sunshield released around the sixteenth of December "
        "and routine science targeted for April twenty twenty-seven. Whether that timetable shifts will become clearer "
        "as ESA completes its orbit assessment."
    ),
    'second': (
        "Seven hundred thousand women, and one question: can AI help spot cancer earlier? On the twenty-third of "
        "November, Addenbrooke's Hospital in Cambridge became the first of about thirty NHS sites across the UK to "
        "begin recruiting women for EDITH—the world's largest clinical trial of artificial intelligence in breast "
        "screening.\n\n"
        "Backed by ten million pounds from the National Institute for Health and Care Research, the three-year study "
        "is co-led by Professor Sian Taylor-Phillips at the University of Warwick and Professor Fiona Gilbert at the "
        "University of Cambridge and Addenbrooke's Hospital, working with NHS England.\n\n"
        "Breast cancer is the most common cancer in women, with around fifty-five thousand cases diagnosed in the UK "
        "each year. Across the country, more than two million women aged fifty to seventy-one attend routine NHS "
        "breast screening annually. Today, every mammogram is independently read by two specialist radiologists, even "
        "though fewer than one percent of screening scans show signs of cancer. While the Cambridge photographs show "
        "Addenbrooke's Hospital, the mammography clinic, London NHS hospital exteriors and scan-review clips here are "
        "contextual archive footage rather than scenes from the trial itself.\n\n"
        "EDITH is testing whether AI-assisted tools can help flag subtle warning signs and safely allow many routine "
        "negative scans to be reviewed by one specialist alongside the AI—potentially easing pressure on radiologists "
        "so clinicians can spend more time with patients who need care.\n\n"
        "Crucially, this is a trial launch, not a finished result. There are no outcome data yet, and it has not yet "
        "been proven whether AI improves detection in routine NHS screening. For women invited to take part, the "
        "screening appointment itself does not change, and human NHS clinicians remain responsible for every clinical "
        "decision."
    ),
    'closing': 'That was our latest news. Stay with science, and stay tuned.',
}

env = os.environ.copy()
tts_rt = R / 'build/video/2026-11-03/tts-runtime'
if tts_rt.exists():
    env['PYTHONPATH'] = str(tts_rt)

results = {}
for k, text in PARTS.items():
    txt_path = OUT / f'{k}.txt'
    mp3_path = OUT / f'main-{k}.mp3'
    txt_path.write_text(text + '\n')
    subprocess.run([
        str(R / '.tools-edge-tts/bin/python'), '-m', 'edge_tts',
        '--voice', 'en-GB-RyanNeural', '--rate=-2%',
        '--file', str(txt_path), '--write-media', str(mp3_path)
    ], env=env, check=True)
    dur = float(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'csv=p=0', str(mp3_path)
    ]).decode().strip())
    results[k] = round(dur, 3)
    print(f'{k}: {dur:.3f}s', flush=True)

(C / 'main_audio_measurements.json').write_text(json.dumps(results, indent=2) + '\n')
print('Total raw speech:', round(sum(results.values()), 3), 's')
