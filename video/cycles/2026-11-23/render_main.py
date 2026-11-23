#!/usr/bin/env python3
"""Cycle-isolated main render for 2026-11-23; enforces approval and independent review gates."""
import argparse, hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
C = Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument('--preview', action='store_true')
ap.add_argument('--resume', action='store_true')
args = ap.parse_args()

m = json.loads((C / 'main_manifest.json').read_text())
work = ROOT / f'build/video/{C.name}/work'
work.mkdir(parents=True, exist_ok=True)

if not args.preview:
    assert 'approved by the user' in (C / 'APPROVAL.md').read_text().lower()
    assert 'MAIN_RENDER_GATE: PASS' in (C / 'REVIEW.md').read_text(), 'Independent pre-render review PASS required'

for rel, digest in m['hashes'].items():
    h = hashlib.sha256()
    with (ROOT / rel).open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    assert h.hexdigest() == digest, f'Hash mismatch: {rel}'

assert m['duration'] <= 310 and m['openingSeconds'] == 16 and m['sections'][-1]['duration'] == 10

def run(cmd):
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-filter_complex_threads', '1', *cmd], check=True)

def encode(cmd, out_path, duration):
    run([
        *cmd, '-t', str(duration), '-an',
        '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast', '-crf', '18',
        '-pix_fmt', 'yuv420p', '-r', '60',
        '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
        str(out_path)
    ])

def render_scene(s, out_path, start, section_start, title):
    cmd = ['-loop', '1', '-framerate', '60'] if s['kind'] == 'still' else []
    if s['kind'] == 'motion' and s.get('seek', 0) > 0:
        cmd += ['-ss', str(s['seek'])]
    cmd += ['-i', str(ROOT / s['file'])]
    w, h = m['width'], m['height']
    pre = []
    if s['kind'] == 'motion':
        pre.append('setpts=PTS-STARTPTS')
    if s.get('crop'):
        pre.append('crop=' + s['crop'])
    pre.append('setsar=1')
    pref = ','.join(pre)
    fg = f'scale={w}:{h}:force_original_aspect_ratio=decrease'
    graph = (
        f'[0:v]{pref},split=2[f][b];'
        f'[b]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,'
        f'gblur=sigma=12,eq=brightness=-0.38:saturation=0.55,scale={w}:{h}[bg];'
        f'[f]{fg}[fg];'
        f'[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=60[base]'
    )
    overlays = []
    relative = start - section_start
    if title and relative < 5.5:
        overlays.append((title, f'lt(t,{5.5 - relative:.3f})'))
    lo, hi = m['subscribeWindow']
    if start < hi and start + s['duration'] > lo:
        overlays.append((m['subscribeOverlay'], f'gte(t,{max(0.0, lo - start):.3f})*lt(t,{hi - start:.3f})'))
    final = 'base'
    for i, (ov_file, en) in enumerate(overlays, 1):
        cmd += ['-loop', '1', '-framerate', '60', '-i', str(ROOT / ov_file)]
        graph += f";[{final}][{i}:v]overlay=0:0:shortest=1:enable='{en}'[o{i}]"
        final = f'o{i}'
    cmd += ['-filter_complex', graph, '-map', f'[{final}]']
    if args.preview:
        run([*cmd, '-frames:v', '1', str(out_path)])
    else:
        encode(cmd, out_path, s['duration'])

segments = []
start = 0.0
for sec in m['sections']:
    if sec.get('closing'):
        if args.preview:
            continue
        out_path = work / 'closing-segment.mp4'
        if not (args.resume and out_path.exists()):
            graph = (
                "[0:v]format=rgba[bg];"
                "[1:v]format=rgba,fade=t=in:st=0:d=0.8:alpha=1[panel];"
                "[bg][panel]overlay=x=0:y='30*max(0,1-t/0.8)'[glass];"
                "[glass]drawbox=x=575:y=389:w=180:h=85:color=0x63e1c9@0.22:t=fill:enable='between(t,1.2,1.8)',"
                "drawbox=x=688:y=628:w=544:h=88:color=white@0.55:t=3:enable='between(t,3,3.8)'[accent];"
                "[2:v]format=rgba,rotate='0.06*sin(8*t)':ow=rotw(iw):oh=roth(ih):c=none[bell];"
                "[accent][bell]overlay=x=1270:y=610:enable='gte(t,1.2)',fps=60[v]"
            )
            cmd = []
            for key in ('closing', 'closingPanel', 'closingBell'):
                cmd += ['-loop', '1', '-framerate', '60', '-i', str(ROOT / m[key])]
            encode([*cmd, '-filter_complex', graph, '-map', '[v]'], out_path, 10)
        segments.append(out_path)
        start += 10.0
    else:
        section_start = start
        assert abs(sum(s['duration'] for s in sec['scenes']) - sec['duration']) < 0.001
        for i, s in enumerate(sec['scenes']):
            out_path = work / (f'preview-{sec["id"]}-{i:02}.png' if args.preview else f'{sec["id"]}-{i:02}.mp4')
            if not (args.resume and out_path.exists() and not args.preview):
                render_scene(s, out_path, start, section_start, sec.get('title'))
            segments.append(out_path)
            start += s['duration']
            print(sec['id'], i + 1, '/', len(sec['scenes']), flush=True)

if args.preview:
    print('Preview frames rendered to', work)
    raise SystemExit(0)

assert abs(start - m['duration']) < 0.001

# Assemble master audio with loudness normalization
acmd, agraphs = [], []
for i, sec in enumerate(m['sections']):
    acmd += ['-i', str(ROOT / sec['audio'])]
    delay_ms = round(sec.get('leadingSilence', 0.0) * 1000)
    agraphs.append(f'[{i}:a]aresample=48000,adelay={delay_ms}:all=1,apad,atrim=duration={sec["duration"]}[a{i}]')
agraphs.append(''.join(f'[a{i}]' for i in range(len(m['sections']))) + f'concat=n={len(m["sections"])}:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]')
audio_out = work / 'main-audio.m4a'
run([*acmd, '-filter_complex', ';'.join(agraphs), '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', str(audio_out)])

concat_list = work / 'main-concat.txt'
concat_list.write_text(''.join(f"file '{p}'\n" for p in segments))
cand = ROOT / m['candidateOutput']
cand.parent.mkdir(parents=True, exist_ok=True)
run([
    '-f', 'concat', '-safe', '0', '-i', str(concat_list),
    '-i', str(audio_out),
    '-map', '0:v', '-map', '1:a', '-t', str(m['duration']),
    '-c', 'copy', '-bsf:v', 'h264_metadata=sample_aspect_ratio=1/1',
    '-aspect', f'{m["width"]}:{m["height"]}', '-movflags', '+faststart',
    str(cand)
])
print('Candidate rendered:', cand)
