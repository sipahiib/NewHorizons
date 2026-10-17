"""Build graphics and current manifests, with flexible measured story timing."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,math,io
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;D=C.name;A=f'assets/motion/{D}/main';W=f'build/video/{D}/work';R=f'build/reels/{D}/work'
for x in [W,R]:(ROOT/x).mkdir(parents=True,exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def text(d,xy,s,n=40,b=False,center=False,fill='white',stroke=0):d.text(xy,s,font=ImageFont.truetype(bold if b else font,n),fill=fill,anchor='mm' if center else None,stroke_width=stroke,stroke_fill='#041820')
def png(p,w,h,fn):
 im=Image.new('RGBA',(w,h));fn(ImageDraw.Draw(im));im.save(ROOT/p);return p
for name,source,t,crop in [('rna-control','rna-video1.mp4',30,'1280:1120:0:80'),('rna-vacuoles','rna-video2.mp4',30,'1280:1120:0:80'),('rna-fusion','rna-video3.avi',8,'2048:1840:0:100'),('rna-compartments','rna-video4.avi',10,'2048:1840:0:100')]:
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(t),'-i',str(ROOT/A/source),'-vf','crop='+crop,'-frames:v','1',str(ROOT/A/(name+'.png'))],check=True)
def title(id,label):
 def draw(d):
  d.rounded_rectangle((65,45,1690,180),24,fill=(6,27,35,158));text(d,(100,87),label,49,True)
 return png(f'{W}/{id}-title.png',1920,1080,draw)
titles={'nasa':title('nasa','BATTERIES BUILT FOR EXTREME COLD'),'rna':title('rna','MUTATIONS MAKE RNA DROPLETS MOVE')}
def sub(d):
 d.rounded_rectangle((1250,770,1855,1000),30,fill=(6,27,35,210),outline=(255,255,255,65),width=2)
 text(d,(1290,795),'YouTube',40,True);text(d,(1290,850),'Like • Subscribe • Join in',29)
 d.rounded_rectangle((1290,910,1815,973),24,fill='#e62435');text(d,(1552,940),'SUBSCRIBE',30,True,True)
subscribe=png(f'{W}/youtube-30s.png',1920,1080,sub)
# Closing-only graphics; no generated scientific imagery.
im=Image.new('RGB',(1920,1080));pix=im.load()
for y in range(1080):
 for x in range(1920):
  glow=max(0,1-math.hypot((x-1250)/1450,(y-650)/950));pix[x,y]=(int(4+9*glow),int(14+43*glow),int(25+48*glow))
im.save(ROOT/f'{W}/closing-bg.png')
def glass(d):
 d.rounded_rectangle((380,265,1540,815),48,fill=(70,102,120,80),outline=(190,220,235,95),width=2)
 d.line((430,285,1480,285),fill=(235,248,255,95),width=2)
 text(d,(960,435),'LIKE • SUBSCRIBE',72,True,True)
 d.rounded_rectangle((690,630,1230,714),42,fill='#e62435');text(d,(960,670),'SUBSCRIBE',34,True,True)
panel=png(f'{W}/closing-panel.png',1920,1080,glass)
def bell(d):
 d.ellipse((44,24,136,117),fill='#ffe36b');d.rectangle((44,74,136,120),fill='#ffe36b');d.polygon([(29,131),(44,109),(136,109),(151,131)],fill='#ffe36b');d.ellipse((75,130,105,160),fill='#ffe36b')
bellfile=png(f'{W}/closing-bell.png',180,180,bell)
def counts(ss):return dict(stills=sum(s['kind']=='still' for s in ss),motion=sum(s['kind']=='motion' for s in ss))
def hashes(ss):return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sorted({s['file'] for s in ss})}
def S(file,duration=1,**kw):return dict(kind='still',file=f'{A}/{file}',duration=duration,**kw)
def V(file,duration=1,seek=0,**kw):return dict(kind='motion',file=f'{A}/{file}',duration=duration,seek=seek,loop=False,**kw)
def weighted(scenes,duration,weights):
 frames=round(duration*60);allocated=0
 for i,(s,w) in enumerate(zip(scenes,weights)):
  n=frames-allocated if i==len(scenes)-1 else round(frames*w/sum(weights));s['duration']=n/60;allocated+=n
 return scenes
mic='1280:1120:0:80';bright='2048:1840:0:100'
measure_path=C/'audio_measurements.json'
if not measure_path.exists():print('Graphics and microscopy stills prepared; audio measurements needed for manifests.');raise SystemExit
m={x['id']:x['seconds'] for x in json.loads(measure_path.read_text())}
required=['opening_hook','opening_support','opening_teaser','nasa_body','rna','closing','r1','r2']
if any(x not in m for x in required):print('Graphics prepared; remaining TTS measurements pending.');raise SystemExit
assert all(m[x]<=t for x,t in [('opening_hook',5),('opening_support',7),('opening_teaser',4),('closing',8),('r1',45),('r2',45)])
nasa_duration=16+math.ceil((m['nasa_body']+.6)*2)/2;rna_duration=math.ceil((m['rna']+.6)*2)/2;total=nasa_duration+rna_duration+10
assert total<=310,total
body=weighted([S('removal.jpg'),V('chamber.webm',seek=48),S('weighing.jpg'),V('storie1.webm',seek=170),S('battery.jpg'),V('storie2.webm',seek=104),V('storie1.webm',seek=230),S('team.jpg'),V('chamber.webm',seek=75),V('storie2.webm',seek=220)],nasa_duration-16,[11,11,10,12,11,10,10,11,10,10])
nasa=[S('battery.jpg',5),V('chamber.webm',7,3),V('rna-video2.mp4',4,21,crop=mic)]+body
rna=weighted([V('rna-video2.mp4',seek=27,crop=mic),S('rna-control.png'),V('rna-video1.mp4',seek=15,crop=mic),S('rna-vacuoles.png'),V('rna-video2.mp4',seek=43,crop=mic),V('rna-video3.avi',seek=0,crop=bright),S('rna-fusion.png'),V('rna-video4.avi',seek=0,crop=bright),V('rna-video2.mp4',seek=65,crop=mic),S('rna-compartments.png'),V('rna-video1.mp4',seek=62,crop=mic)],rna_duration,[12,9,12,9,13,12,9,12,13,9,12])
# Opening source audio segments stay fixed at 5, 7 and 4 seconds; speech is never stretched.
args=[]
for id in ['opening_hook','opening_support','opening_teaser','nasa_body']:args+=['-i',str(ROOT/f'build/video/{D}/audio/{id}.mp3')]
graph=';'.join(f'[{i}:a]aresample=48000,apad,atrim=duration={du}[a{i}]' for i,du in enumerate([5,7,4,nasa_duration-16]))+';[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]'
subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*args,'-filter_complex',graph,'-map','[a]','-c:a','pcm_s16le',str(ROOT/f'build/video/{D}/audio/nasa.wav')],check=True)
main=dict(cycle=D,status='prepared-for-review',candidateOutput=f'build/video/{D}/newhorizons.mp4',finalOutput='build/video/newhorizons.mp4',duration=total,fps=60,width=1920,height=1080,openingSeconds=16,closingSeconds=10,sections=[dict(id='nasa',proposalId='M2',duration=nasa_duration,audio=f'build/video/{D}/audio/nasa.wav',counts=counts(nasa),scenes=nasa,title=titles['nasa']),dict(id='rna',proposalId='M1',duration=rna_duration,audio=f'build/video/{D}/audio/rna.mp3',counts=counts(rna),scenes=rna,title=titles['rna']),dict(id='closing',duration=10,audio=f'build/video/{D}/audio/closing.mp3',closing=True,leadingSilence=2)],closing=f'{W}/closing-bg.png',closingPanel=panel,closingBell=bellfile,titleDisplaySeconds=5.5,subscribeOverlay=subscribe,subscribeWindow=[30,35.5],hashes=hashes(nasa+rna))
(C/'main_manifest.json').write_text(json.dumps(main,indent=2)+'\n')
(C/'timing.json').write_text(json.dumps(dict(nasa=nasa_duration,rna=rna_duration,closing=10,total=total,openingIncludedInNasa=16),indent=2)+'\n')
print('Main timings',total,nasa_duration,rna_duration,flush=True)
