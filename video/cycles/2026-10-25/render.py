"""Cycle-isolated render: independent gates required, originals never overwritten."""
from pathlib import Path
import argparse,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('output',choices=['main','r1','r2']);p.add_argument('--preview',action='store_true');p.add_argument('--resume',action='store_true');a=p.parse_args()
m=json.loads((C/f'{a.output}_manifest.json').read_text());work=ROOT/f'build/{"video" if a.output=="main" else "reels"}/{C.name}/work';work.mkdir(parents=True,exist_ok=True)
if not a.preview:
 assert 'approved by user selection' in (C/'APPROVAL.md').read_text()
 assert f'{a.output.upper()}_RENDER_GATE: PASS' in (C/'REVIEW.md').read_text(),'Independent review missing'
for file,digest in m['hashes'].items():assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,file
if a.output=='main':assert m['duration']<=310 and m['openingSeconds']==16 and m['sections'][-1]['duration']==10
else:assert len(m['scenes'])==7 and m['duration']==45

def run(args):subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1',*args],check=True)
def encode(args,out,duration):run([*args,'-t',str(duration),'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(out)])
def scene(s,out,start,section_start,title):
 args=['-loop','1','-framerate','60'] if s['kind']=='still' else ['-ss',str(s.get('seek',0))]
 args+=['-i',str(ROOT/s['file'])];w,h=m['width'],m['height'];pre=[]
 if s.get('crop'):pre.append('crop='+s['crop'])
 if s.get('speed',1)!=1:pre.append('setpts=(PTS-STARTPTS)/'+str(s['speed']))
 pre.append('setsar=1');pref=','.join(pre)
 bw,bh=(480,270) if a.output=='main' else (270,480)
 fg=f"scale={s.get('maxWidth',w)}:{s.get('maxHeight',h if a.output=='main' else 760)}:force_original_aspect_ratio=decrease"
 xy='(W-w)/2:(H-h)/2' if a.output=='main' else '(W-w)/2:600+(760-h)/2'
 graph=f'[0:v]{pref},split=2[f][b];[b]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},gblur=sigma=12,eq=brightness=-0.38:saturation=0.55,scale={w}:{h}[bg];[f]{fg}[fg];[bg][fg]overlay={xy},fps=60[base]'
 overlays=[]
 if a.output=='main':
  relative=start-section_start
  if title and relative<5.5:overlays.append((title,f'lt(t,{5.5-relative})'))
  lo,hi=m['subscribeWindow']
  if start<hi and start+s['duration']>lo:overlays.append((m['subscribeOverlay'],f'gte(t,{max(0,lo-start)})*lt(t,{hi-start})'))
 else:
  if start<5.5:overlays.append((m['overlay'],f'lt(t,{5.5-start})'))
  lo,hi=m['ctaWindow']
  if start+s['duration']>lo:overlays.append((m['ctaOverlay'],f'gte(t,{max(0,lo-start)})*lt(t,{hi-start})'))
 final='base'
 for i,(file,en) in enumerate(overlays,1):
  args+=['-loop','1','-framerate','60','-i',str(ROOT/file)];graph+=f";[{final}][{i}:v]overlay=0:0:shortest=1:enable='{en}'[o{i}]";final=f'o{i}'
 args+=['-filter_complex',graph,'-map',f'[{final}]']
 if a.preview:run([*args,'-frames:v','1',str(out)])
 else:encode(args,out,s['duration'])
segments=[];start=0;sections=m['sections'] if a.output=='main' else [dict(id=a.output,duration=m['duration'],scenes=m['scenes'])]
for sec in sections:
 if sec.get('closing'):
  if a.preview:continue
  out=work/'closing-segment.mp4'
  if not(a.resume and out.exists()):
   graph="[0:v]format=rgba[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.8:alpha=1[panel];[bg][panel]overlay=x=0:y='30*max(0,1-t/0.8)'[glass];[glass]drawbox=x=575:y=389:w=180:h=85:color=0x63e1c9@0.22:t=fill:enable='between(t,1.2,1.8)',drawbox=x=688:y=628:w=544:h=88:color=white@0.55:t=3:enable='between(t,3,3.8)'[accent];[2:v]format=rgba,rotate='0.06*sin(8*t)':ow=rotw(iw):oh=roth(ih):c=none[bell];[accent][bell]overlay=x=1270:y=610:enable='gte(t,1.2)',fps=60[v]"
   args=[]
   for file in ['closing','closingPanel','closingBell']:args+=['-loop','1','-framerate','60','-i',str(ROOT/m[file])]
   encode([*args,'-filter_complex',graph,'-map','[v]'],out,10)
  segments.append(out);start+=10
 else:
  section_start=start
  assert abs(sum(s['duration'] for s in sec['scenes'])-sec['duration'])<.001
  for i,s in enumerate(sec['scenes']):
   out=work/(f'preview-{sec["id"]}-{i:02}.png' if a.preview else f'{sec["id"]}-{i:02}.mp4')
   if not(a.resume and out.exists() and not a.preview):scene(s,out,start,section_start,sec.get('title'))
   segments.append(out);start+=s['duration'];print(sec['id'],i+1,len(sec['scenes']),flush=True)
if a.preview:raise SystemExit
assert abs(start-m['duration'])<.001
args=[];graphs=[]
for i,sec in enumerate(sections):
 audio=sec['audio'] if a.output=='main' else m['audio'];delay=sec.get('leadingSilence',0) if a.output=='main' else m.get('leadingSilence',0)
 args+=['-i',str(ROOT/audio)];graphs.append(f'[{i}:a]aresample=48000,adelay={round(delay*1000)}:all=1,apad,atrim=duration={sec["duration"]}[a{i}]')
graphs.append(''.join(f'[a{i}]' for i in range(len(sections)))+f'concat=n={len(sections)}:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]')
audio=work/f'{a.output}-audio.m4a';run([*args,'-filter_complex',';'.join(graphs),'-map','[a]','-c:a','aac','-b:a','192k','-ar','48000',str(audio)])
concat=work/f'{a.output}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in segments));output=ROOT/m.get('candidateOutput',m.get('output'));output.parent.mkdir(parents=True,exist_ok=True)
run(['-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-map','0:v','-map','1:a','-t',str(m['duration']),'-c','copy','-bsf:v','h264_metadata=sample_aspect_ratio=1/1','-aspect',f'{m["width"]}:{m["height"]}','-movflags','+faststart',str(output)])
print('Candidate rendered:',output,flush=True)
