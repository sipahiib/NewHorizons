from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,math
ROOT=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent; D=C.name
A=f'assets/motion/{D}/main'; W=f'build/video/{D}/work'; (ROOT/W).mkdir(parents=True,exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def text(d,xy,s,n=40,b=False,center=False,fill='white'):d.text(xy,s,font=ImageFont.truetype(bold if b else font,n),fill=fill,anchor='mm' if center else None)
def png(name,w,h,fn):
 p=f'{W}/{name}.png';im=Image.new('RGBA',(w,h));fn(ImageDraw.Draw(im));im.save(ROOT/p);return p
def title(d):
 d.rounded_rectangle((65,45,1600,180),24,fill=(6,27,35,158));text(d,(100,87),'AI IS STEPPING INTO THE LAB',49,True)
t=png('ai-title',1920,1080,title)
def sub(d):
 d.rounded_rectangle((1250,770,1855,1000),30,fill=(6,27,35,210),outline=(255,255,255,65),width=2)
 text(d,(1290,795),'YouTube',40,True);text(d,(1290,850),'Like • Subscribe • Join in',29)
 d.rounded_rectangle((1290,910,1815,973),24,fill='#e62435');text(d,(1552,940),'SUBSCRIBE',30,True,True)
subscribe=png('youtube-30s',1920,1080,sub)
im=Image.new('RGB',(1920,1080));pix=im.load()
for y in range(1080):
 for x in range(1920):
  g=max(0,1-math.hypot((x-1250)/1450,(y-650)/950));pix[x,y]=(int(4+9*g),int(14+43*g),int(25+48*g))
im.save(ROOT/f'{W}/closing-bg.png')
def glass(d):
 d.rounded_rectangle((380,265,1540,815),48,fill=(70,102,120,80),outline=(190,220,235,95),width=2)
 d.line((430,285,1480,285),fill=(235,248,255,95),width=2);text(d,(960,435),'LIKE • SUBSCRIBE',72,True,True)
 d.rounded_rectangle((690,630,1230,714),42,fill='#e62435');text(d,(960,670),'SUBSCRIBE',34,True,True)
panel=png('closing-panel',1920,1080,glass)
def bell(d):
 d.ellipse((44,24,136,117),fill='#ffe36b');d.rectangle((44,74,136,120),fill='#ffe36b');d.polygon([(29,131),(44,109),(136,109),(151,131)],fill='#ffe36b');d.ellipse((75,130,105,160),fill='#ffe36b')
bellfile=png('closing-bell',180,180,bell)
# Stills are faithful source frames. They are held statically, never panned or animated.
stills=[('plate','31767906',14),('pipette','8381446',4),('samples','8381450',2),('liquid','8540609',5),('research','31767905',13)]
for name,id,seek in stills:
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(seek),'-i',str(ROOT/A/(id+'.mp4')),'-frames:v','1',str(ROOT/A/(name+'.png'))],check=True)
m={x['id']:x['seconds'] for x in json.loads((C/'audio_measurements.json').read_text())}
assert all(m[id]<=duration for id,duration in [('opening_hook',5),('opening_support',7),('opening_question',4),('closing',8)])
body_duration=math.ceil((m['body']+.6)*2)/2; main_duration=16+body_duration;total=main_duration+10
assert 220<=total<=250,total
# Fixed opening; remainder allocated in frame units without loops or slowed footage.
def V(id,du,seek=0):return dict(kind='motion',file=f'{A}/{id}.mp4',duration=du,seek=seek,loop=False,classification='contextual')
def S(id,du=6):return dict(kind='still',file=f'{A}/{id}.png',duration=du,classification='contextual')
opening=[V('31767906',5,0),V('11218535',7,0),V('31767903',4,0)]
body=[V('31767903',9,4),S('plate'),V('8381319',9,0),V('8381455',11,0),S('pipette'),V('8381446',8,0),V('11218535',10,8),S('samples'),V('31767906',10,6),V('31767903',10,14),V('8540609',9,0),S('liquid'),V('8381255',8,0),V('11218535',11,20),V('31767898',10,0),V('8863365',7,0.6),V('31767905',10,0),S('research'),V('31767905',10,16),V('8381455',8,2),V('31767906',10,17),V('31767905',9,27),V('8381319',8,1),V('31767903',5,25)]
# Make the gap equal the measured speech section. Distribute only to still holds (5–9 seconds).
gap=body_duration-sum(x['duration'] for x in body);ss=[s for s in body if s['kind']=='still'];frames=round(gap*60)
for i,s in enumerate(ss):
 n=round(frames/(len(ss)-i));s['duration']+=n/60;frames-=n
 assert 4<=s['duration']<=10,s
scenes=opening+body
verification=json.loads((C/'media_verification.json').read_text());lookup={a['file']:a for a in verification['assets']}
for s in scenes:
 if s['kind']=='motion':assert s['seek']+s['duration']<=float(lookup[s['file']]['probe']['format']['duration'])-.03,s
# Concatenate opening and body audio; no stretching.
args=[]
ids=['opening_hook','opening_support','opening_question','body']
for id in ids:args+=['-i',str(ROOT/f'build/video/{D}/audio/{id}.mp3')]
graph=';'.join(f'[{i}:a]aresample=48000,apad,atrim=duration={du}[a{i}]' for i,du in enumerate([5,7,4,body_duration]))+';[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]'
subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*args,'-filter_complex',graph,'-map','[a]','-c:a','pcm_s16le',str(ROOT/f'build/video/{D}/audio/ai.wav')],check=True)
counts=dict(stills=sum(s['kind']=='still' for s in scenes),motion=sum(s['kind']=='motion' for s in scenes))
manifest=dict(cycle=D,status='prepared-for-review',candidateOutput=f'build/video/{D}/newhorizons.mp4',finalOutput='build/video/newhorizons.mp4',duration=total,fps=60,width=1920,height=1080,openingSeconds=16,closingSeconds=10,sections=[dict(id='ai',duration=main_duration,audio=f'build/video/{D}/audio/ai.wav',counts=counts,scenes=scenes,title=t),dict(id='closing',duration=10,audio=f'build/video/{D}/audio/closing.mp3',closing=True,leadingSilence=2)],closing=f'{W}/closing-bg.png',closingPanel=panel,closingBell=bellfile,titleDisplaySeconds=5.5,subscribeOverlay=subscribe,subscribeWindow=[30,35.5])
files={s['file'] for s in scenes}|{t,subscribe,panel,bellfile,manifest['closing']}|{s['audio'] for s in manifest['sections']}
manifest['hashes']={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sorted(files)}
(C/'main_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(C/'timing.json').write_text(json.dumps(dict(opening=16,body=body_duration,closing=10,total=total,counts=counts),indent=2)+'\n')
print(total,counts,flush=True)
