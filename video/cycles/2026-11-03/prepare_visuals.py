from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,subprocess,math
R=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent; D=C.name
W=R/'build/video'/D/'work'; W.mkdir(parents=True,exist_ok=True); A=R/'build/video'/D/'audio'; M=R/'build/video'/D/'media'
def rel(p):return str(p.relative_to(R))
def png(name,draw):
 p=W/(name+'.png'); im=Image.new('RGBA',(1920,1080));draw(ImageDraw.Draw(im)); im.save(p);return rel(p)
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def write(d,xy,s,n,anchor=None): d.text(xy,s,font=ImageFont.truetype(font,n),fill='white',anchor=anchor)
def title(s):
 return lambda d:(d.rounded_rectangle((65,45,1500,180),24,fill=(6,27,35,158)),write(d,(100,88),s,48))
t1=png('title-swift',title('SWIFT’S FINAL CHAPTER'));t2=png('title-hospital',title('AI AND HOSPITAL HANDOVERS'))
def sub(d):
 d.rounded_rectangle((1250,770,1855,1000),30,fill=(6,27,35,190));write(d,(1290,795),'YouTube',40);write(d,(1290,850),'Like • Subscribe • Join in',29);d.rounded_rectangle((1290,910,1815,973),24,fill='#e62435');write(d,(1552,941),'SUBSCRIBE',30,'mm')
subscribe=png('subscribe',sub)
im=Image.new('RGB',(1920,1080),(8,30,42));im.save(W/'closing-bg.png')
def panel(d):
 d.rounded_rectangle((380,265,1540,815),48,fill=(70,102,120,80),outline=(190,220,235,95),width=2);d.line((430,285,1480,285),fill=(235,248,255,95),width=2);write(d,(960,435),'LIKE • SUBSCRIBE',72,'mm');d.rounded_rectangle((690,630,1230,714),42,fill='#e62435');write(d,(960,670),'SUBSCRIBE',34,'mm')
cp=png('closing-panel',panel);bell=Image.new('RGBA',(180,180));d=ImageDraw.Draw(bell);d.ellipse((44,24,136,117),fill='#ffe36b');d.rectangle((44,74,136,120),fill='#ffe36b');d.polygon([(29,131),(44,109),(136,109),(151,131)],fill='#ffe36b');d.ellipse((75,130,105,160),fill='#ffe36b');bell.save(W/'bell.png')
for i,id in enumerate(['6997946','5030431','8460080','5453578']):
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss','3','-i',str(M/f'pexels-{id}.mp4'),'-frames:v','1',str(M/f'hospital-still-{i}.png')],check=True)
def length(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))
# Remove leading MP3 silence without altering the -2% voice speed.
subprocess.run(['ffmpeg','-y','-v','error','-ss','0.20','-i',str(A/'hook.mp3'),'-t','4.8','-c:a','pcm_s16le',str(A/'hook-trim.wav')],check=True)
def combine(ids,durations,out):
 args=[]
 for id in ids:args += ['-i',str(A/id)]
 filt=';'.join(f'[{i}:a]aresample=48000,apad,atrim=duration={v}[a{i}]' for i,v in enumerate(durations))+';'+''.join(f'[a{i}]' for i in range(len(ids)))+f'concat=n={len(ids)}:v=0:a=1[a]'
 subprocess.run(['ffmpeg','-y','-v','error',*args,'-filter_complex',filt,'-map','[a]','-c:a','pcm_s16le',str(A/out)],check=True)
swift=math.ceil(length(A/'swift.mp3'))+1; hospital=math.ceil(length(A/'hospital.mp3'))+1
combine(['hook-trim.wav','support.mp3','teaser.mp3','swift.mp3'],[5,7,4,swift],'swift.wav')
# Real Swift launch, stills and actual telescope/rescue footage; Roman is contextual.
def motion(f,d,seek=0,classification='direct'):return {'kind':'motion','file':rel(M/f),'duration':d,'seek':seek,'classification':classification}
def still(f,d,classification='direct'):return {'kind':'still','file':rel(M/f),'duration':d,'classification':classification}
lead=[motion('nasa-swift-history.webm',5,11),motion('nasa-swift-history.webm',7,16),still('swift-assembly.jpg',4),still('swift-assembly.jpg',6),motion('nasa-swift-history.webm',7,11),still('swift-andromeda.jpg',7),motion('nasa-roman-context.webm',8,0,'contextual'),still('swift-andromeda.jpg',7),still('swift-assembly.jpg',6),motion('nasa-roman-context.webm',8,10,'contextual'),still('nasa-link-test.jpg',7),motion('nasa-link-excerpt.mp4',9,8),still('nasa-link-pegasus.jpg',7),still('swift-assembly.jpg',6),still('swift-andromeda.jpg',7),motion('nasa-swift-history.webm',6,11)]
# Crop the right side of the Roman cleanroom footage to remove prominent embedded signage.
for scene in lead:
 if scene['file'].endswith('nasa-roman-context.webm'):scene['crop']='iw*0.68:ih:0:0'
 if scene['file'].endswith('nasa-link-excerpt.mp4'):scene['crop']='iw*0.56:ih:iw*0.34:0'
# Fit measured narration by varying the final scene duration; avoid truncation.
lead[-1]['duration'] += 16+swift-sum(x['duration'] for x in lead)
assert 3<=lead[-1]['duration']<=12
clinical=[motion('pexels-6997946.mp4',8,0,'contextual'),still('hospital-still-0.png',6,'contextual'),motion('pexels-5030431.mp4',8,0,'contextual'),motion('pexels-5453578.mp4',9,0,'contextual'),still('hospital-still-3.png',6,'contextual'),motion('pexels-8460080.mp4',9,0,'contextual'),motion('pexels-6997946.mp4',9,9,'contextual'),still('hospital-still-1.png',6,'contextual'),motion('pexels-5030431.mp4',8,2,'contextual'),motion('pexels-5453578.mp4',9,5,'contextual'),still('hospital-still-2.png',6,'contextual'),motion('pexels-8460080.mp4',8,4,'contextual')]
clinical[1]['duration']+=hospital-sum(x['duration'] for x in clinical)
assert 3<=clinical[1]['duration']<=12
for s in lead+clinical:
 if s['kind']=='motion':assert s['seek']+s['duration']<length(R/s['file'])-.02, s
m={'cycle':D,'status':'prepared-for-review','candidateOutput':f'build/video/{D}/newhorizons.mp4','finalOutput':'build/video/newhorizons.mp4','duration':16+swift+hospital+10,'fps':60,'width':1920,'height':1080,'openingSeconds':16,'closingSeconds':10,'sections':[{'id':'swift','duration':16+swift,'audio':rel(A/'swift.wav'),'scenes':lead,'title':t1},{'id':'hospital','duration':hospital,'audio':rel(A/'hospital.mp3'),'scenes':clinical,'title':t2},{'id':'closing','duration':10,'audio':rel(A/'closing.mp3'),'closing':True,'leadingSilence':2}], 'closing':rel(W/'closing-bg.png'),'closingPanel':cp,'closingBell':rel(W/'bell.png'),'titleDisplaySeconds':5.5,'subscribeOverlay':subscribe,'subscribeWindow':[30,35.5]}
assert m['duration']<=310
files={s['file'] for sec in m['sections'] for s in sec.get('scenes',[])}|{t1,t2,subscribe,cp,m['closing'],m['closingBell']}|{s['audio'] for s in m['sections']}
for sec in m['sections']:
 if 'scenes' in sec:sec['counts']={'motion':sum(x['kind']=='motion' for x in sec['scenes']),'stills':sum(x['kind']=='still' for x in sec['scenes'])}
m['hashes']={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(files)}
(C/'main_manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Duration:',m['duration'],'Swift:',16+swift,'hospital:',hospital)
