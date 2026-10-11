"""Create cycle-local graphics and manifests from approved real source media."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;D=C.name
A=f'assets/motion/{D}';W=f'build/video/{D}/work';R=f'build/reels/{D}/work'
for p in [W,R]:(ROOT/p).mkdir(parents=True,exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def text(d,xy,s,n=30,b=False,center=False,stroke=0):d.text(xy,s,font=ImageFont.truetype(bold if b else font,n),fill='white',anchor='mm' if center else None,stroke_width=stroke,stroke_fill='#061b23')
def png(file,w,h,fn):
 im=Image.new('RGBA',(w,h));fn(ImageDraw.Draw(im));im.save(ROOT/file);return file
registry=[a for a in json.loads((C/'main_media_sources.json').read_text()) if a['id'] in ['capsule','shield','watch']]
for id,file,url,source,credit,status,rights in [
 ('arcjet','arcjet-hd.mp4','https://nasaplus.akamaized.net/output/8895-7.m3u8','https://plus.nasa.gov/video/nasa-arc-jet-facility-history/','NASA Johnson Space Center','archive ground-test laboratory; released 28 August 2023; not KREPE-3','NASA media guidelines; only real B-roll selected; source sound removed'),
 ('arcjet-opening-repaired','arcjet-opening-repaired.mp4','https://nasaplus.akamaized.net/output/8895-7.m3u8','https://plus.nasa.gov/video/nasa-arc-jet-facility-history/','NASA Johnson Space Center','archive ground-test laboratory; clean first50seconds re-fetched from same official source','NASA media guidelines; real B-roll; source sound removed'),
 ('departure','departure.mp4','https://youtube.com/live/IoL51xLkMSY','https://plus.nasa.gov/scheduled-video/nasas-northrop-grumman-commercial-resupply-services-24-departure/','NASA','actual Cygnus XL departure coverage; 9 October 2026','NASA media guidelines; footage from official NASA recording; no simulation shots'),
 ('smartwatch','smartwatch.mp4','https://www.pexels.com/download/video/17770565/','https://www.pexels.com/video/a-person-wearing-a-watch-on-their-wrist-17770565/','Ali Alcántara / Pexels','ordinary smartwatch context; not research prototype or sweat sensor','Pexels License https://www.pexels.com/license/'),
 ('smartwatch-detail','smartwatch-detail.mp4','https://www.pexels.com/download/video/4211107/','https://www.pexels.com/video/close-up-shot-of-a-person-s-smart-watch-4211107/','Kaboompics / Pexels','ordinary smartwatch context; not research prototype or sweat sensor; native720p','Pexels License https://www.pexels.com/license/'),
 ('lab','lab.mp4','https://videos.pexels.com/video-files/8533377/8533377-uhd_2160_3840_30fps.mp4','https://www.pexels.com/video/scientists-working-at-a-laboratory-8533377/','Artem Podrez / Pexels','laboratory context; not TUS experiment','Pexels License https://www.pexels.com/license/'),
 ('chemistry','chemistry.mp4','https://www.pexels.com/download/video/8485643/','https://www.pexels.com/video/a-person-doing-experiment-in-the-laboratory-8485643/','Ivan S / Pexels','liquid handling context; not sweat sensing or TUS experiment','Pexels License https://www.pexels.com/license/')]:
 registry.append(dict(id=id,file=f'{A}/main/{file}',url=url,source=source,credit=credit,status=status,rights=rights))
def derivative(source,dest,operation,box=None,seek=None):
 file=f'{A}/main/{dest}';base=next(a for a in registry if a['file']==f'{A}/main/{source}')
 if box:
  im=Image.open(ROOT/base['file']).crop(box);im.save(ROOT/file)
 else:subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(seek),'-i',str(ROOT/base['file']),'-frames:v','1',str(ROOT/file)],check=True)
 registry.append({**base,'id':dest,'file':file,'derivation':{'sourceFile':base['file'],'operation':operation,'cropPixels':box,'seekSeconds':seek}})
 return file
capsuleDetail=derivative('capsule.jpg','capsule-detail.png','fixed static hardware detail crop',(1700,700,6500,4300))
shieldDetail=derivative('shield.jpg','shield-detail.png','fixed static hardware detail crop',(1400,700,6500,4700))
# Extract only genuine photographs from institutional composite, excluding its editorial labels.
device=derivative('watch.png','device-photo.png','fixed crop of actual assembled device photograph',(713,208,825,430))
electrode=derivative('watch.png','electrode-photo.png','fixed crop of actual electrode photograph',(418,202,492,459))
labstill=derivative('chemistry.mp4','chemistry-still.png','unanimated frame extraction',seek=12)
watchstill=derivative('smartwatch.mp4','smartwatch-still.png','unanimated frame extraction',seek=2)
def title(name,label):
 def draw(d):d.rounded_rectangle((65,45,1650,180),24,fill=(6,27,35,158));text(d,(100,88),label,48,True)
 return png(f'{W}/{name}.png',1920,1080,draw)
titles={'m1':title('m1-title','TWELVE CAPSULES, ONE FIERY TEST'),'m2':title('m2-title','CAN A WATCH READ SWEAT?')}
def sub(d):
 d.rounded_rectangle((1230,765,1855,1000),32,fill=(6,27,35,215),outline=(255,255,255,70),width=2)
 text(d,(1270,790),'YouTube',39,True);text(d,(1270,843),'@newhorizons_21',33)
 d.rounded_rectangle((1270,903,1815,970),25,fill='#e52430');text(d,(1542,937),'SUBSCRIBE',31,True,True)
subscribe=png(f'{W}/youtube-30s.png',1920,1080,sub)
def close(d):
 d.rectangle((0,0,1920,1080),fill='#082c38');d.rounded_rectangle((380,265,1540,815),48,fill=(31,65,76,255),outline=(74,102,111,255),width=2)
 text(d,(960,452),'LIKE • SUBSCRIBE',72,True,True)
 d.rounded_rectangle((690,630,1230,714),42,fill='#e52430');text(d,(960,671),'SUBSCRIBE',34,True,True)
closing=png(f'{W}/closing.png',1920,1080,close)
im=Image.open(ROOT/closing).convert('RGB');im.save(ROOT/closing)
def bell(d):
 d.ellipse((44,24,136,117),fill='#ffe36b');d.rectangle((44,74,136,120),fill='#ffe36b');d.polygon([(29,131),(44,109),(136,109),(151,131)],fill='#ffe36b');d.ellipse((75,130,105,160),fill='#ffe36b')
bellfile=png(f'{W}/closing-bell.png',180,180,bell)
def S(file,duration,**kw):return dict(kind='still',file=f'{A}/main/{file}',duration=duration,**kw)
def V(file,duration,seek=0,**kw):return dict(kind='motion',file=f'{A}/main/{file}',duration=duration,seek=seek,loop=False,**kw)
m1=[S('capsule.jpg',5.5),V('departure.mp4',6.5,600),V('smartwatch.mp4',4,0.5),S('shield.jpg',12),V('arcjet-hd.mp4',14,210),S('shield-detail.png',12),V('departure.mp4',14,1100),S('capsule-detail.png',12),V('arcjet-hd.mp4',14,220),V('arcjet-hd.mp4',14,210),S('shield.jpg',10),V('arcjet-hd.mp4',12,240),V('departure.mp4',14,605),V('arcjet-hd.mp4',16,270)]
# No looping or simulated sensor footage; low-native-resolution research photographs remain small.
m2=[S('device-photo.png',9,maxWidth=340,maxHeight=640),V('smartwatch-detail.mp4',13,0),S('electrode-photo.png',9,maxWidth=260,maxHeight=640),V('chemistry.mp4',16,1),S('chemistry-still.png',12),V('lab.mp4',7,0),V('smartwatch.mp4',5.5,0),S('device-photo.png',12,maxWidth=340,maxHeight=640),S('smartwatch-still.png',10),V('chemistry.mp4',16,2),V('lab.mp4',7,0.5),V('smartwatch-detail.mp4',13,0.3),S('electrode-photo.png',10.5,maxWidth=260,maxHeight=640)]
def counts(ss):return {'stills':sum(s['kind']=='still' for s in ss),'motion':sum(s['kind']=='motion' for s in ss)}
def hashes(ss):return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sorted({s['file'] for s in ss})}
assert sum(s['duration'] for s in m1)==160
assert sum(s['duration'] for s in m2)==140
main=dict(cycle=D,status='prepared-for-review',candidateOutput=f'build/video/{D}/newhorizons.mp4',finalOutput='build/video/newhorizons.mp4',duration=310,fps=60,width=1920,height=1080,sections=[dict(id='m1',duration=160,audio=f'build/video/{D}/audio/m1.wav',counts=counts(m1),scenes=m1,title=titles['m1']),dict(id='m2',duration=140,audio=f'build/video/{D}/audio/m2.mp3',counts=counts(m2),scenes=m2,title=titles['m2']),dict(id='closing',duration=10,audio=f'build/video/{D}/audio/closing.mp3',closing=True,leadingSilence=2)],closing=closing,closingBell=bellfile,titleDisplaySeconds=5.5,subscribeOverlay=subscribe,subscribeWindow=[30,35.5],hashes=hashes(m1+m2))
(C/'main_manifest.json').write_text(json.dumps(main,indent=2)+'\n')
rm=json.loads((C/'reel_media_sources.json').read_text())['assets']
for id,lines in [('r1',['COULD AI TRAINING','BE PAUSED IN HARDWARE?']),('r2',['CAN FISH REVEAL','HIDDEN POLLUTION?'])]:
 def draw(d):
  d.rounded_rectangle((50,155,1030,425),30,fill=(6,27,35,163));text(d,(90,230),lines[0],49,True);text(d,(90,310),lines[1],49,True)
 top=png(f'{R}/{id}-title.png',1080,1920,draw)
 def drawcta(d):text(d,(540,1585),'YouTube @newhorizons_21',37,True,True,3);text(d,(540,1645),'Instagram • Like & Follow',35,True,True,3)
 cta=png(f'{R}/{id}-cta.png',1080,1920,drawcta)
 assets=[a for a in rm if a['output']==id.upper()]
 if id=='r1':durations=[6,6,6,6,7,7,7]
 else:
  # Reorder contextual clips before final study photo; native short clips are never looped.
  assets=[assets[i] for i in [0,1,2,5,3,6,4]];durations=[6,6,6,7,7,6,7]
 scenes=[dict(kind='motion' if a['file'].endswith('.mp4') else 'still',file=a['file'],duration=du,seek=1 if id=='r1' else 0,loop=False) for a,du in zip(assets,durations)]
 m=dict(cycle=D,status='prepared-for-review',output=f'build/reels/{D}/{"01-ai-hardware-pause" if id=="r1" else "02-fish-hidden-stress"}.mp4',audio=f'build/video/{D}/audio/{id}.mp3',overlay=top,titleDisplaySeconds=5.5,ctaOverlay=cta,ctaWindow=[42,45],leadingSilence=0.8 if id=='r1' else 0.6,duration=45,fps=60,width=1080,height=1920,counts=counts(scenes),scenes=scenes,hashes=hashes(scenes))
 (C/f'{id}_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
for a in registry:
 p=ROOT/a['file'];a['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();a['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,avg_frame_rate','-of','json',str(p)]))
(C/'main_media_sources.json').write_text(json.dumps(registry,indent=2)+'\n')
print('Manifests prepared',counts(m1),counts(m2),flush=True)
