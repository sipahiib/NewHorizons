"""Render the reviewed 2026-09-26 main candidate without replacing prior delivery."""
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
CYCLE=Path(__file__).resolve().parent
manifest=json.loads((CYCLE/'main_manifest.json').read_text())
review=(CYCLE/'REVIEW.md').read_text()
if 'MAIN_RENDER_GATE: PASS' not in review:
    raise SystemExit('Independent main pre-render review must pass first')
work=ROOT/'build/video/2026-09-26/work'
work.mkdir(parents=True,exist_ok=True)

def run(args):
    subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1',*args],check=True)

section_files=[]
audio_files=[]
for section in manifest['sections']:
    sid=section['id']
    audio_files.append(ROOT/section['audio'])
    if section.get('closing'):
        output=work/'section-closing.mp4'
        graph="[0:v]fps=60,format=yuv420p,fade=t=in:st=0:d=0.8[bg];[1:v]format=rgba,rotate='0.06*sin(8*t)':ow=rotw(iw):oh=roth(ih):c=none[bell];[bg][bell]overlay=x=1270:y=610:enable='gte(t,1.2)'[v]"
        run(['-loop','1','-framerate','60','-i',str(ROOT/manifest['closing']),'-loop','1','-framerate','60','-i',str(ROOT/manifest['closingBell']),'-filter_complex',graph,'-map','[v]','-t','10','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60',str(output)])
        section_files.append(output)
        print('Rendered main closing',flush=True)
        continue
    scene_files=[]
    for i,scene in enumerate(section['scenes']):
        output=work/f'{sid}-scene-{i+1:02}.mp4'
        args=[]
        if scene['kind']=='still': args += ['-loop','1','-framerate','60']
        else:
            if scene.get('loop'): args += ['-stream_loop','-1']
            args += ['-ss',str(scene.get('seek',0))]
        primary_overlay = manifest['teaserOverlay'] if scene.get('teaser') else manifest['overlays'][sid]
        args += ['-i',str(ROOT/scene['file']),'-loop','1','-framerate','60','-i',str(ROOT/primary_overlay)]
        if scene.get('teaser'):
            primary_enable = '1'
        elif i == 0:
            primary_enable = f"lt(t,{manifest.get('titleDisplaySeconds',4)})"
        else:
            primary_enable = '0'
        graph=f"[0:v]split=2[f][b];[b]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,gblur=sigma=15,eq=brightness=-0.35:saturation=0.62,scale=1920:1080[bg];[f]scale=1920:1080:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=60[base];[base][1:v]overlay=0:0:shortest=1:enable='{primary_enable}'[o1]"
        label='o1'
        extra_overlay = None
        if scene.get('context'): extra_overlay = manifest['contextOverlay']
        elif scene.get('label') == 'historical': extra_overlay = manifest['historicalOverlay']
        elif scene.get('label') == 'site': extra_overlay = manifest['siteContextOverlay']
        if extra_overlay:
            args += ['-loop','1','-framerate','60','-i',str(ROOT/extra_overlay)]
            graph += ';[o1][2:v]overlay=0:0:shortest=1[final]'
            label='final'
        args += ['-filter_complex',graph,'-map',f'[{label}]','-t',str(scene['duration']),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(output)]
        run(args)
        scene_files.append(output)
        print(f'Rendered {sid} scene {i+1}/{len(section["scenes"])}',flush=True)
    concat=work/f'{sid}-concat.txt'
    concat.write_text(''.join(f"file '{p}'\n" for p in scene_files))
    output=work/f'section-{sid}.mp4'
    run(['-f','concat','-safe','0','-i',str(concat),'-c','copy',str(output)])
    section_files.append(output)

video_concat=work/'main-video-concat.txt'
video_concat.write_text(''.join(f"file '{p}'\n" for p in section_files))
audio_args=[]
for p in audio_files: audio_args += ['-i',str(p)]
audio_graph=[]
for i,section in enumerate(manifest['sections']):
    audio_graph.append(f'[{i}:a]aresample=48000,apad,atrim=duration={section["duration"]}[a{i}]')
audio_graph.append(''.join(f'[a{i}]' for i in range(len(audio_files)))+f'concat=n={len(audio_files)}:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]')
audio_file=work/'main-audio.m4a'
run([*audio_args,'-filter_complex',';'.join(audio_graph),'-map','[a]','-t','370','-c:a','aac','-b:a','192k','-ar','48000',str(audio_file)])
run(['-f','concat','-safe','0','-i',str(video_concat),'-i',str(audio_file),'-map','0:v','-map','1:a','-t','370','-c:v','copy','-c:a','copy','-movflags','+faststart',str(ROOT/manifest['candidateOutput'])])
print('Rendered 370-second main candidate; independent actual-output QA required',flush=True)
