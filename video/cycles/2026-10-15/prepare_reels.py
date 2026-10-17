"""Compose seven approved media segments per Reel, without generic imagery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;D=C.name;W=f'build/reels/{D}/work';(ROOT/W).mkdir(parents=True,exist_ok=True)
assets=json.loads((C/'reel_media_sources.json').read_text())['assets']
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def text(d,xy,s,n=40,b=False):d.text(xy,s,font=ImageFont.truetype(bold if b else font,n),fill='white',anchor='mm',stroke_width=2,stroke_fill='#061b23')
for id,lines,stem in [('r1',['AI MAKES STORM','SIMULATION CHEAPER'],'01-ai-storm-simulations'),('r2',['WHAT STRENGTHENED','HURRICANE POLO?'],'02-hurricane-polo-attribution')]:
 im=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(im);d.rounded_rectangle((50,155,1030,425),30,fill=(6,27,35,163));text(d,(540,240),lines[0],49,True);text(d,(540,320),lines[1],49,True);title=f'{W}/{id}-title.png';im.save(ROOT/title)
 im=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(im);text(d,(540,1585),'YouTube @newhorizons_21',37,True);text(d,(540,1645),'Instagram • Like & Follow',35,True);cta=f'{W}/{id}-cta.png';im.save(ROOT/cta)
 selected=sorted([a for a in assets if a['output']==id.upper()],key=lambda a:a['segment']);assert len(selected)==7
 durations=[6,6,6,6,7,6,8];scenes=[]
 for a,dur in zip(selected,durations):
  motion=a['file'].endswith(('.mp4','.mov','.webm'));s=dict(kind='motion' if motion else 'still',file=a['file'],duration=dur,loop=False,maxWidth=900,maxHeight=760)
  if motion:
   s['seek']=a['suggested_in_seconds'];s['speed']=(a['suggested_out_seconds']-s['seek'])/dur
   if a.get('crop_xyxy'):
    x,y,x2,y2=a['crop_xyxy'];s['crop']=f'{x2-x}:{y2-y}:{x}:{y}'
   # native first crop remains a restrained 650-pixel foreground
   if a.get('native_crop_dimensions',[1920])[0]<700:s['maxWidth']=650;s['maxHeight']=650
  scenes.append(s)
 m=dict(cycle=D,status='prepared-for-review',output=f'build/reels/{D}/{stem}.mp4',audio=f'build/video/{D}/audio/{id}.mp3',overlay=title,titleDisplaySeconds=5.5,ctaOverlay=cta,ctaWindow=[42,45],leadingSilence=0.5 if id=='r1' else 0,duration=45,fps=60,width=1080,height=1920,counts=dict(stills=sum(s['kind']=='still' for s in scenes),motion=sum(s['kind']=='motion' for s in scenes)),scenes=scenes,hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sorted({s['file'] for s in scenes})})
 (C/f'{id}_manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(id,m['counts'])
