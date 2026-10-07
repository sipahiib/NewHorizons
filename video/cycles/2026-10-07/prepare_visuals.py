"""Compose audited stills, transparent overlays and cycle-local manifests."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;D=C.name
A=f'assets/motion/{D}';W=f'build/video/{D}/work';R=f'build/reels/{D}/work'
for p in [W,R]: (ROOT/p).mkdir(parents=True,exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def fnt(n,b=False):return ImageFont.truetype(bold if b else font,n)
def text(d,xy,s,n=30,b=False,center=False,stroke=0):
 d.text(xy,s,font=fnt(n,b),fill='white',anchor='mm' if center else None,stroke_width=stroke,stroke_fill='#061b23')
def png(file,w,h,fn):
 im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im);fn(d)
 if file.endswith('/closing.png'):im=Image.alpha_composite(Image.new('RGBA',(w,h),'#082c38'),im).convert('RGB')
 im.save(ROOT/file);return file
def top(name,s):
 def draw(d):
  d.rounded_rectangle((65,45,1635,180),24,fill=(6,27,35,158));text(d,(100,88),s,48,True)
 return png(f'{W}/{name}.png',1920,1080,draw)
titles={'m1':top('m1-title','WEBB REVEALS A STELLAR NURSERY'),'m2':top('m2-title','HOW DRONES PLAN FOR MOVING OBSTACLES'),'teaser':top('teaser','NEXT: PLANNING AROUND MOVING OBSTACLES')}
def tag(name,label,credit):
 def draw(d):
  d.rounded_rectangle((70,205,1620,265),14,fill=(6,27,35,161));text(d,(95,220),label,27)
  text(d,(70,1030),credit,23,stroke=2)
 return png(f'{W}/{name}.png',1920,1080,draw)
webbcredit='NASA, ESA, CSA, STScI; Image Processing: Alyssa Pagan (STScI)'
magiccredit='Marco Tempest / CC BY 3.0 • edited excerpts'
tags={
 'science':tag('science','INFRARED DATA • OBSERVED DEC 2025 • RELEASED OCT 2026',webbcredit),
 'comparison':tag('comparison','SPITZER / WEBB COMPARISON • PROCESSED SCIENTIFIC IMAGES',webbcredit),
 'webb2016':tag('webb2016','ARCHIVE • WEBB HARDWARE • 2016 • NOT NEBULA FOOTAGE','NASA Goddard Space Flight Center'),
 'webb2018':tag('webb2018','ARCHIVE • WEBB HARDWARE • 2018 • NOT NEBULA FOOTAGE','NASA Goddard Space Flight Center'),
 'magic':tag('magic','ARCHIVE CONTEXT • AUTONOMOUS DRONE PERFORMANCE • NOT SANDO',magiccredit),
 'fpv':tag('fpv','CONTEXT • FPV FLIGHT • NOT SANDO OR A DISASTER DEPLOYMENT','Traveling on the Go / Pexels'),
 'limits':tag('limits','CONTEXT, NOT SANDO • SAFETY GUARANTEES REQUIRE STATED ASSUMPTIONS',magiccredit),
}
def close(d):
 d.rectangle((0,0,1920,1080),fill='#082c38');d.rounded_rectangle((380,265,1540,815),48,fill=(255,255,255,25),outline=(255,255,255,50),width=2)
 text(d,(960,452),'LIKE • SUBSCRIBE',72,True,True);text(d,(960,550),'Stay with science.',42,center=True)
 d.rounded_rectangle((690,630,1230,714),42,fill='#ff5968');text(d,(960,671),'SUBSCRIBE',34,True,True)
closing=png(f'{W}/closing.png',1920,1080,close)
def bell(d):
 d.ellipse((44,24,136,117),fill='#ffe36b');d.rectangle((44,74,136,120),fill='#ffe36b');d.polygon([(29,131),(44,109),(136,109),(151,131)],fill='#ffe36b');d.ellipse((75,130,105,160),fill='#ffe36b')
bellfile=png(f'{W}/closing-bell.png',180,180,bell)
originals={a['file']:a for a in json.loads((C/'media_sources.json').read_text()) if not a.get('derivation') and not a['file'].endswith('/review.mp4')}
originals.update({a['file']:a for a in json.loads((C/'context_sources.json').read_text()) if not a['file'].endswith('/review.mp4')})
registry=list(originals.values())
# Static detail crops retain direct scientific provenance; no pan/zoom is applied.
source=f'{A}/main/m1/ngc7129.jpg';im=Image.open(ROOT/source)
for name,box in {'gold':(0,3300,7300,10100),'red':(7300,1800,11800,8500),'grey':(1000,0,9500,3000),'gas':(2500,2300,11500,10400)}.items():
 file=f'{A}/main/m1/{name}.png';detail=im.crop(box);detail.thumbnail((1920,1920));detail.save(ROOT/file)
 base=next(a for a in registry if a['file']==source)
 registry.append({**base,'file':file,'derivation':{'sourceFile':source,'cropPixels':box,'operation':'fixed unanimated crop'},'status':'direct scientific still crop'})
file=f'{A}/main/m1/ngc-display.png';display=im.copy();display.thumbnail((1920,1920));display.save(ROOT/file)
base=next(a for a in registry if a['file']==source)
registry.append({**base,'file':file,'derivation':{'sourceFile':source,'operation':'aspect-preserving resize for static display'},'status':'direct scientific still resized'})
def frame(file,seek,dest):
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(seek),'-i',str(ROOT/file),'-frames:v','1',str(ROOT/dest)],check=True)
 base=next(a for a in registry if a['file']==file)
 registry.append({**base,'file':dest,'derivation':{'sourceFile':file,'seekSeconds':seek,'operation':'unanimated frame extraction'},'status':base['status']+'; extracted still'})
for seek in [55,110,170]:frame(f'{A}/main/m2/magiclab.webm',seek,f'{A}/main/m2/magic-{seek}.png')
frame(f'{A}/main/m2/fpv.mp4',8,f'{A}/main/m2/fpv-still.png')
for name,file,seek in [('signing-still','signing.mp4',24),('signing-late-still','signing.mp4',32),('agreement-still','agreement.mp4',2)]:frame(f'{A}/reels/r1/{file}',seek,f'{A}/reels/r1/{name}.png')
for name,file,seek in [('ocean-still','ocean.mp4',12),('ice-still','gorner.mp4',5),('melt-still','gorner.mp4',165)]:frame(f'{A}/reels/r2/{file}',seek,f'{A}/reels/r2/{name}.png')
def S(file,duration,label,**extra):return dict(kind='still',file=f'{A}/{file}',duration=duration,label=label,overlay=tags[label],**extra)
def V(file,duration,seek,label,**extra):return dict(kind='motion',file=f'{A}/{file}',duration=duration,seek=seek,loop=False,label=label,overlay=tags[label],**extra)
# Science-led chapter needs static gas details; hardware archive supports instrument explanation.
m1=[S('main/m1/ngc-display.png',5,'science',title=titles['m1']),V('main/m1/webb-broll-1.webm',7,38,'webb2016'),V('main/m2/magiclab.webm',4,107,'magic',title=titles['teaser']),S('main/m1/ngc-display.png',12,'science'),S('main/m1/gold.png',14,'science'),S('main/m1/red.png',14,'science'),S('main/m1/grey.png',12,'science'),V('main/m1/webb-broll-2.webm',12,96,'webb2016'),S('main/m1/gas.png',14,'science'),S('main/m1/comparison.png',16,'comparison'),V('main/m1/webb-broll-1.webm',14,136,'webb2016'),V('main/m1/webb-cleanroom.mp4',14,145,'webb2018'),V('main/m1/webb-broll-2.webm',14,134,'webb2016'),S('main/m1/ngc-display.png',8,'science')]
m2=[V('main/m2/magiclab.webm',12,52,'magic',title=titles['m2']),V('main/m2/fpv.mp4',14,2,'fpv'),S('main/m2/magic-55.png',14,'magic'),V('main/m2/magiclab.webm',14,75,'magic'),S('main/m2/magic-110.png',14,'magic'),V('main/m2/magiclab.webm',14,130,'magic'),S('main/m2/magic-170.png',14,'limits'),V('main/m2/magiclab.webm',14,190,'limits'),S('main/m2/fpv-still.png',14,'fpv'),V('main/m2/magiclab.webm',16,150,'limits')]
def counts(ss):return {'stills':sum(s['kind']=='still' for s in ss),'motion':sum(s['kind']=='motion' for s in ss)}
def hashes(ss):return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sorted({s['file'] for s in ss})}
main=dict(cycle=D,status='prepared-for-review',candidateOutput=f'build/video/{D}/newhorizons.mp4',finalOutput='build/video/newhorizons.mp4',duration=310,fps=60,width=1920,height=1080,sections=[dict(id='m1',duration=160,audio=f'build/video/{D}/audio/m1.wav',counts=counts(m1),scenes=m1),dict(id='m2',duration=140,audio=f'build/video/{D}/audio/m2.mp3',counts=counts(m2),scenes=m2),dict(id='closing',duration=10,audio=f'build/video/{D}/audio/closing.mp3',closing=True)],closing=closing,closingBell=bellfile,titleDisplaySeconds=4,hashes=hashes(m1+m2))
(C/'main_manifest.json').write_text(json.dumps(main,indent=2)+'\n')
reels={
'r1':(['CAN AN AI AGENT','FOLLOW THE RULES?'],[('motion','agreement.mp4',0),('still','signing-late-still.png',0),('motion','signing.mp4',14),('still','signing-still.png',0),('motion','signing.mp4',20),('still','agreement-still.png',0),('motion','signing.mp4',26)],'01-ai-business-rules.mp4'),
'r2':(['OCEAN HEAT CAN LAST','FOR GENERATIONS'],[('motion','ocean.mp4',0),('still','ocean-still.png',0),('motion','ocean.mp4',15),('still','ice-still.png',0),('motion','gorner.mp4',16),('still','melt-still.png',0),('motion','ocean.mp4',22)],'02-ocean-heat.mp4')}
for id,(lines,files,out) in reels.items():
 def drawtitle(d):
  d.rounded_rectangle((50,155,1030,425),30,fill=(6,27,35,163));text(d,(90,230),lines[0],49,True);text(d,(90,310),lines[1],49,True)
 title=png(f'{R}/{id}-title.png',1080,1920,drawtitle)
 def drawcta(d):
  text(d,(540,1585),'YouTube @newhorizons_21',37,True,True,3);text(d,(540,1645),'Instagram • Like & Follow',35,True,True,3)
 cta=png(f'{R}/{id}-cta.png',1080,1920,drawcta)
 scenes=[]
 for i,(kind,name,seek) in enumerate(files):
  file=f'{A}/reels/{id}/{name}';a=next(a for a in registry if a['file']==file)
  label='CONTRACT CONTEXT • NOT THE EVALUATED AI' if id=='r1' else 'ARCHIVE CONTEXT • GORNER GLACIER • 2021' if 'ice' in name or 'gorner' in name or 'melt' in name else 'OCEAN CONTEXT • NOT HEAT MEASUREMENTS'
  def detail(d,label=label,credit=a['credit'],i=i,id=id):
   d.rounded_rectangle((60,480,1020,545),16,fill=(6,27,35,163));text(d,(540,512),label,24,center=True)
   text(d,(540,1408),credit,25,center=True,stroke=2)
   if id=='r1' and i in [1,2]:text(d,(540,1490),'Rubric score: 55.0% vs 41.6%',32,True,True,2)
   if id=='r1' and i in [3,4]:text(d,(540,1490),'Time estimates are simulated',30,True,True,2)
  overlay=png(f'{R}/{id}-detail-{i}.png',1080,1920,detail)
  scenes.append(dict(kind=kind,file=file,duration=9 if i==6 else 6,seek=seek,loop=False,label=label,overlay=overlay))
 m=dict(cycle=D,status='prepared-for-review',output=f'build/reels/{D}/{out}',audio=f'build/video/{D}/audio/{id}.mp3',overlay=title,ctaOverlay=cta,ctaStartInFinalScene=6,duration=45,fps=60,width=1080,height=1920,counts=counts(scenes),scenes=scenes,hashes=hashes(scenes))
 (C/f'{id}_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
# Registry covers originals and every selected derivative.
for a in registry:
 p=ROOT/a['file'];a['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();a['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,r_frame_rate','-of','json',str(p)]))
(C/'media_sources.json').write_text(json.dumps(registry,indent=2)+'\n')
print('Overlays and manifests prepared',counts(m1),counts(m2),flush=True)
