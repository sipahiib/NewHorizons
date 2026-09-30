"""Render reviewed R2 into its cycle folder, preserving earlier deliveries."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CYCLE = Path(__file__).resolve().parent
manifest = json.loads((CYCLE/'r2_manifest.json').read_text())
review = (CYCLE/'REVIEW.md').read_text()
if 'R2_RENDER_GATE: PASS' not in review:
    raise SystemExit('Independent R2 pre-render review must pass first')
overlay_review = (CYCLE/'REEL_OVERLAY_REVIEW.md').read_text()
if 'R2_OVERLAY_RENDER_GATE: PASS' not in overlay_review:
    raise SystemExit('Independent revised-overlay review must pass first')
work = ROOT/'build/reels/2026-09-30/work'

def run(args):
    subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1',*args], check=True)

segments=[]
for i, scene in enumerate(manifest['scenes']):
    output=work/f'r2-segment-{i+1:02}.mp4'
    args=[]
    if scene['kind']=='still':
        args += ['-loop','1','-framerate','60']
    else:
        if scene.get('loop'):
            args += ['-stream_loop','-1']
        args += ['-ss',str(scene.get('seek',0))]
    args += ['-i',str(ROOT/scene['file']),'-loop','1','-framerate','60','-i',str(ROOT/manifest['overlay'])]
    graph='[0:v]split=2[f][b];[b]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=12,eq=brightness=-0.38:saturation=0.55,scale=1080:1920[bg];[f]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=60[base];[base][1:v]overlay=0:0:shortest=1[o1]'
    final='o1'
    if scene['kind']=='motion':
        args += ['-loop','1','-framerate','60','-i',str(ROOT/manifest['contextOverlay'])]
        graph += ';[o1][2:v]overlay=0:0:shortest=1[final]'
        final='final'
    if i == len(manifest['scenes']) - 1:
        args += ['-loop','1','-framerate','60','-i',str(ROOT/manifest['ctaOverlay'])]
        graph += f";[{final}][3:v]overlay=0:0:shortest=1:enable='gte(t,{manifest['ctaStartInFinalScene']})'[cta]"
        final='cta'
    args += ['-filter_complex',graph,'-map',f'[{final}]','-t',str(scene['duration']),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(output)]
    run(args)
    segments.append(output)
    print(f'Rendered R2 segment {i+1}/7', flush=True)
concat=work/'r2-concat.txt'
concat.write_text(''.join(f"file '{p}'\n" for p in segments))
run(['-f','concat','-safe','0','-i',str(concat),'-i',str(ROOT/manifest['audio']),
     '-filter_complex',f"[1:a]aresample=48000,loudnorm=I=-16:LRA=7:TP=-1.5,apad,atrim=duration={manifest['duration']}[a]",
     '-map','0:v','-map','[a]','-t',str(manifest['duration']),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(ROOT/manifest['output'])])
print('Rendered R2 candidate; independent actual-output QA required', flush=True)
