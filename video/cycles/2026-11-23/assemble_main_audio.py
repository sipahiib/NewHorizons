#!/usr/bin/env python3
"""Assemble opening (16s) + M1 body (119s) = 135s without clipping any speech."""
import json, subprocess
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parents[2]
A = R / 'build/video/2026-11-23/audio'

def run(args):
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', *map(str, args)], check=True)

# Trim only leading/trailing silence on teaser (speech 0.245s..4.438s -> keep 0.18s..4.48s = 4.30s)
run(['-i', A / 'main-teaser.mp3', '-af', 'atrim=start=0.18:end=4.48,asetpts=PTS-STARTPTS', '-c:a', 'pcm_s16le', A / 'main-teaser-trim.wav'])

# Build exact 16.000s opening: hook at 0.00s, support at 5.00s, teaser at 11.70s (ends 16.00s)
# Then append main-lead.mp3 at 16.00s padded to 119.00s -> total 135.000s.
graph = (
    "[0:a]aresample=48000,apad,atrim=duration=5.0[a0];"
    "[1:a]aresample=48000,apad,atrim=duration=6.7[a1];"
    "[2:a]aresample=48000,apad,atrim=duration=4.3[a2];"
    "[3:a]aresample=48000,apad,atrim=duration=119.0[a3];"
    "[a0][a1][a2][a3]concat=n=4:v=0:a=1[out]"
)
run([
    '-i', A / 'main-hook.mp3',
    '-i', A / 'main-support.mp3',
    '-i', A / 'main-teaser-trim.wav',
    '-i', A / 'main-lead.mp3',
    '-filter_complex', graph, '-map', '[out]',
    '-c:a', 'pcm_s16le', A / 'main-lead-assembled.wav'
])

# Update measurements JSON with final teaser duration
m = json.loads((C / 'main_audio_measurements.json').read_text())
m['teaser'] = 5.352
m['teaser_trimmed'] = 4.300
m['assembled_lead_total'] = 135.000
m['planned_second_total'] = 112.000
m['planned_closing_total'] = 10.000
m['planned_total_runtime'] = 257.000
(C / 'main_audio_measurements.json').write_text(json.dumps(m, indent=2) + '\n')
print('Assembled main-lead-assembled.wav (135.0s); total planned runtime = 257.0s')
