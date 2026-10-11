"""Render cycle-isolated reviewed candidates; source-composed previews do not bypass gates."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('output',choices=['main','r1','r2']);p.add_argument('--preview',action='store_true');p.add_argument('--reuse-unchanged',action='store_true');p.add_argument('--visuals-only',action='store_true');p.add_argument('--assemble-only',action='store_true');a=p.parse_args()
m=json.loads((C/f'{a.output}_manifest.json').read_text());work=ROOT/f'build/{"video" if a.output=="main" else "reels"}/{C.name}/work';work.mkdir(parents=True,exist_ok=True)
def run(args):subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1',*args],check=True)
def scene_render(s,out,global_start,section_start=0,title=None,preview=False):
 args=[]
 if s['kind']=='still':args+=['-loop','1','-framerate','60']
 else:args+=['-ss',str(s.get('seek',0))]
 args+=['-i',str(ROOT/s['file'])]
 w,h=m['width'],m['height']
 if a.output=='main':bw,bh=480,270;fg=f"scale={s.get('maxWidth',1920)}:{s.get('maxHeight',1080)}:force_original_aspect_ratio=decrease";xy='(W-w)/2:(H-h)/2'
 else:bw,bh=270,480;fg='scale=1080:760:force_original_aspect_ratio=decrease';xy='(W-w)/2:600+(760-h)/2'
 graph=f'[0:v]split=2[f][b];[b]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},gblur=sigma=12,eq=brightness=-0.38:saturation=0.55,scale={w}:{h}[bg];[f]{fg}[fg];[bg][fg]overlay={xy},setsar=1,fps=60[base]'
 overlays=[]
 if a.output=='main':
  relative=global_start-section_start
  if title and relative<5.5:overlays.append((title,f'lt(t,{5.5-relative})'))
  lo,hi=m['subscribeWindow']
  if global_start<hi and global_start+s['duration']>lo:overlays.append((m['subscribeOverlay'],f'gte(t,{max(0,lo-global_start)})*lt(t,{hi-global_start})'))
 else:
  if global_start<5.5:overlays.append((m['overlay'],f'lt(t,{5.5-global_start})'))
  lo,hi=m['ctaWindow']
  if global_start+s['duration']>lo:overlays.append((m['ctaOverlay'],f'gte(t,{max(0,lo-global_start)})*lt(t,{hi-global_start})'))
 final='base'
 for idx,(file,en) in enumerate(overlays,1):
  args+=['-loop','1','-framerate','60','-i',str(ROOT/file)];graph+=f";[{final}][{idx}:v]overlay=0:0:shortest=1:enable='{en}'[o{idx}]";final=f'o{idx}'
 args+=['-filter_complex',graph,'-map',f'[{final}]']
 if preview:args+=['-frames:v','1']
 else:args+=['-t',str(s['duration']),'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709']
 run([*args,str(out)])
if not a.preview:
 review=(C/'REVIEW.md').read_text()
 if f'{a.output.upper()}_RENDER_GATE: PASS' not in review:raise SystemExit('Independent pre-render review must pass')
 if 'Status: **editorial package approved by user selection**' not in (C/'APPROVAL.md').read_text():raise SystemExit('Approval missing')
 if a.output=='main' and 'REVISED_MAIN_VISUAL_GATE' in review:
  gate='REVISED_MAIN_VISUAL_GATE: PASS' if a.visuals_only else 'REVISED_MAIN_RENDER_GATE: PASS'
  if gate not in review:raise SystemExit('Revised main review gate is pending')
segments=[];global_start=0
sections=m['sections'] if a.output=='main' else [dict(id=a.output,duration=m['duration'],scenes=m['scenes'])]
for sec in sections:
 if sec.get('closing'):
  if a.preview:continue
  out=work/'closing-segment.mp4';graph="[0:v]fps=60,format=yuv420p,fade=t=in:st=0:d=0.8,drawbox=x=590:y=408:w=185:h=85:color=0x63e1c9@0.25:t=fill:enable='between(t,1,1.6)',drawbox=x=688:y=628:w=544:h=88:color=white@0.55:t=3:enable='between(t,3,3.8)'[bg];[1:v]format=rgba,rotate='0.06*sin(8*t)':ow=rotw(iw):oh=roth(ih):c=none[bell];[bg][bell]overlay=x=1270:y=610:enable='gte(t,1.2)'[v]"
  if not (a.assemble_only and out.exists()):run(['-loop','1','-framerate','60','-i',str(ROOT/m['closing']),'-loop','1','-framerate','60','-i',str(ROOT/m['closingBell']),'-filter_complex',graph,'-map','[v]','-t',str(sec['duration']),'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60',str(out)])
  segments.append(out)
 else:
  section_start=global_start
  for i,s in enumerate(sec['scenes']):
   out=work/(f'preview-{sec["id"]}-{i:02}.png' if a.preview else f'{sec["id"]}-{i:02}.mp4')
   reusable=out.exists() and (a.assemble_only or (a.reuse_unchanged and a.output=='main' and sec['id']=='m1' and i not in [2,4,8]))
   if not reusable:scene_render(s,out,global_start,section_start,sec.get('title'),a.preview)
   segments.append(out);global_start+=s['duration'];print(f'{sec["id"]} scene {i+1}/{len(sec["scenes"])}',flush=True)
if a.preview or a.visuals_only:raise SystemExit
if a.output=='main':
 args=[];graphs=[]
 for i,sec in enumerate(m['sections']):
  args+=['-i',str(ROOT/sec['audio'])];delay=f',adelay={int(sec.get("leadingSilence",0)*1000)}:all=1' if sec.get('leadingSilence') else ''
  graphs.append(f'[{i}:a]aresample=48000{delay},apad,atrim=duration={sec["duration"]}[a{i}]')
 graphs.append(''.join(f'[a{i}]' for i in range(len(m['sections'])))+f'concat=n={len(m["sections"])}:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]')
 audio=work/'main-audio.m4a';run([*args,'-filter_complex',';'.join(graphs),'-map','[a]','-t',str(m['duration']),'-c:a','aac','-b:a','192k','-ar','48000',str(audio)])
else:
 audio=work/f'{a.output}-audio.m4a';run(['-i',str(ROOT/m['audio']),'-af',f'aresample=48000,adelay={int(m.get("leadingSilence",0)*1000)}:all=1,loudnorm=I=-16:LRA=7:TP=-1.5,apad,atrim=duration={m["duration"]}','-t',str(m['duration']),'-c:a','aac','-b:a','192k','-ar','48000',str(audio)])
concat=work/f'{a.output}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in segments));output=ROOT/m.get('candidateOutput',m.get('output'));output.parent.mkdir(parents=True,exist_ok=True)
run(['-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-map','0:v','-map','1:a','-t',str(m['duration']),'-c','copy','-movflags','+faststart',str(output)])
print('Candidate rendered:',output,flush=True)
