"""Render cycle-isolated reviewed candidates or source-composed review previews."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('output',choices=['main','r1','r2']);parser.add_argument('--preview',action='store_true');a=parser.parse_args()
m=json.loads((C/f'{a.output}_manifest.json').read_text());work=ROOT/f'build/{"video" if a.output=="main" else "reels"}/{C.name}/work';work.mkdir(parents=True,exist_ok=True)
def run(args):subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1',*args],check=True)
def scene_render(s,out,i,n,preview=False):
 args=[]
 if s['kind']=='still':args+=['-loop','1','-framerate','60']
 else:
  if s.get('loop'):args+=['-stream_loop','-1']
  args+=['-ss',str(s.get('seek',0))]
 args+=['-i',str(ROOT/s['file'])]
 w,h=m['width'],m['height'];crop=f"crop={s['crop']}," if s.get('crop') else ''
 if a.output=='main':
  bw,bh=480,270;fg='scale=1700:700:force_original_aspect_ratio=decrease' if s['label']=='figure' else 'scale=1920:1080:force_original_aspect_ratio=decrease';xy='(W-w)/2:285' if s['label']=='figure' else '(W-w)/2:(H-h)/2'
 else:bw,bh=270,480;fg='scale=1080:760:force_original_aspect_ratio=decrease';xy='(W-w)/2:600+(760-h)/2'
 graph=f'[0:v]{crop}split=2[f][b];[b]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},gblur=sigma=12,eq=brightness=-0.38:saturation=0.55,scale={w}:{h}[bg];[f]{fg}[fg];[bg][fg]overlay={xy},setsar=1,fps=60[base]'
 final='base';idx=1
 overlays=[]
 if a.output=='main':
  if s.get('title'):overlays.append((s['title'],"lt(t,4)"))
 else:overlays.append((m['overlay'],'1'))
 overlays.append((s['overlay'],'1'))
 if a.output!='main' and i==n-1:overlays.append((m['ctaOverlay'],f"gte(t,{m['ctaStartInFinalScene']})"))
 for f,en in overlays:
  args+=['-loop','1','-framerate','60','-i',str(ROOT/f)];graph+=f";[{final}][{idx}:v]overlay=0:0:shortest=1:enable='{en}'[o{idx}]";final=f'o{idx}';idx+=1
 args+=['-filter_complex',graph,'-map',f'[{final}]']
 if preview:args+=['-frames:v','1']
 else:args+=['-t',str(s['duration']),'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709']
 run([*args,str(out)])
if a.preview:
 scenes=m['sections'][0]['scenes']+m['sections'][1]['scenes'] if a.output=='main' else m['scenes']
 for i,s in enumerate(scenes):scene_render(s,work/f'preview-{a.output}-{i:02}.png',i,len(scenes),True)
 print('Source-composed review previews complete');raise SystemExit
review=(C/'REVIEW.md').read_text()
if f'{a.output.upper()}_RENDER_GATE: PASS' not in review:raise SystemExit('Independent pre-render review must pass first')
if 'Status: **approved**' not in (C/'APPROVAL.md').read_text():raise SystemExit('Approval missing')
segments=[]
if a.output=='main':
 for sec in m['sections']:
  if sec.get('closing'):
   out=work/'closing-segment.mp4';graph="[0:v]fps=60,format=yuv420p,fade=t=in:st=0:d=0.8,drawbox=x=590:y=408:w=185:h=85:color=0x63e1c9@0.25:t=fill:enable='between(t,1,1.6)',drawbox=x=688:y=628:w=544:h=88:color=white@0.55:t=3:enable='between(t,3,3.8)'[bg];[1:v]format=rgba,rotate='0.06*sin(8*t)':ow=rotw(iw):oh=roth(ih):c=none[bell];[bg][bell]overlay=x=1270:y=610:enable='gte(t,1.2)'[v]"
   run(['-loop','1','-framerate','60','-i',str(ROOT/m['closing']),'-loop','1','-framerate','60','-i',str(ROOT/m['closingBell']),'-filter_complex',graph,'-map','[v]','-t',str(sec['duration']),'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60',str(out)]);segments.append(out)
  else:
   for i,s in enumerate(sec['scenes']):
    out=work/f'{sec["id"]}-{i:02}.mp4';scene_render(s,out,i,len(sec['scenes']));segments.append(out);print(f'{sec["id"]} scene {i+1}/{len(sec["scenes"])}',flush=True)
 audio_args=[];graphs=[]
 for i,sec in enumerate(m['sections']):
  audio_args+=['-i',str(ROOT/sec['audio'])];graphs.append(f'[{i}:a]aresample=48000,apad,atrim=duration={sec["duration"]}[a{i}]')
 graphs.append(''.join(f'[a{i}]' for i in range(len(m['sections'])))+f'concat=n={len(m["sections"])}:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]')
 audio=work/'main-audio.m4a';run([*audio_args,'-filter_complex',';'.join(graphs),'-map','[a]','-t',str(m['duration']),'-c:a','aac','-b:a','192k','-ar','48000',str(audio)])
else:
 for i,s in enumerate(m['scenes']):
  out=work/f'{a.output}-{i:02}.mp4';scene_render(s,out,i,len(m['scenes']));segments.append(out);print(f'{a.output} scene {i+1}/7',flush=True)
 audio=work/f'{a.output}-audio.m4a';run(['-i',str(ROOT/m['audio']),'-af',f'aresample=48000,loudnorm=I=-16:LRA=7:TP=-1.5,apad,atrim=duration={m["duration"]}','-t',str(m['duration']),'-c:a','aac','-b:a','192k','-ar','48000',str(audio)])
concat=work/f'{a.output}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in segments));output=ROOT/m.get('candidateOutput',m.get('output'));output.parent.mkdir(parents=True,exist_ok=True)
run(['-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-map','0:v','-map','1:a','-t',str(m['duration']),'-c','copy','-movflags','+faststart',str(output)])
print('Candidate rendered:',output,flush=True)
