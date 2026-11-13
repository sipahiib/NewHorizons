from pathlib import Path
import json, subprocess
C=Path(__file__).resolve().parent; ROOT=C.parents[2]; m=json.loads((C/'r2_manifest.json').read_text())
if 'R2_RENDER_GATE: PASS' not in (C/'REVIEW.md').read_text(): raise SystemExit('Independent review required')
w=ROOT/'build/reels/2026-11-13/work'; w.mkdir(parents=True,exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def run(args): subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*args],check=True)
segments=[]
for i,s in enumerate(m['scenes']):
 out=w/f'scene-{i:02}.mp4'; segments.append(out)
 f="[0:v]split=2[a][b];[a]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=12,eq=brightness=-0.38,scale=1080:1920[bg];[b]scale=1080:760:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=60"
 f+='[base]'
 args=['-loop','1','-framerate','60','-i',str(ROOT/s['file'])]
 if i in (0,6):
  args+=['-loop','1','-framerate','60','-i',str(w/('title.png' if i==0 else 'cta.png'))]
  f+=";[base][1:v]overlay=0:0:enable='"+("lt(t,5.5)" if i==0 else "gte(t,4)")+"'[out]"
 else: f+=';[base]null[out]'
 run([*args,'-filter_complex',f,'-map','[out]','-t',str(s['duration']),'-an','-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-r','60',str(out)])
concat=w/'concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in segments));output=ROOT/m['output'];output.parent.mkdir(parents=True,exist_ok=True)
run(['-f','concat','-safe','0','-i',str(concat),'-i',str(ROOT/m['audio']),'-af','aresample=48000,loudnorm=I=-16:LRA=7:TP=-1.5,apad','-t','46','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)])
