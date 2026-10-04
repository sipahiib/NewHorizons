from pathlib import Path
import json,subprocess,fitz,hashlib,io
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
C=Path(__file__).resolve().parent
r=json.loads((C/'media_sources.json').read_text())
for iid,sec in [(6997946,14),(5998403,9),(5453568,12)]:
 src=ROOT/f'assets/motion/2026-10-04/reels/r1/pexels-{iid}.mp4';d=src.with_name(f'pexels-{iid}-still.png')
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(sec),'-i',str(src),'-frames:v','1',str(d)],check=True)
 original=next(a for a in r if a['file']==str(src.relative_to(ROOT)));new={**original,'file':str(d.relative_to(ROOT)),'derivation':f'Unanimated source-video frame at {sec}s','sha256':hashlib.sha256(d.read_bytes()).hexdigest()}
 with Image.open(d) as im:new['probe']={'width':im.width,'height':im.height}
 r.append(new)
doc=fitz.open(ROOT/'build/video/2026-10-04/research/ecg.pdf')
figs=[('fig1-roc',1,(54,240,547,451)),('fig2-aggregation',2,(53,49,282,226)),('fig5-monitoring',5,(54,49,547,225)),('fig6-processing',5,(90,297,511,535))]
for name,pg,rect in figs:
 d=ROOT/f'assets/motion/2026-10-04/main/m2/{name}.png';doc[pg].get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(rect)).save(d)
 with Image.open(d) as im:w,h=im.size
 r.append(dict(file=str(d.relative_to(ROOT)),story='m2',source='https://www.nature.com/articles/s44325-026-00153-2',download='https://www.nature.com/articles/s44325-026-00153-2_reference.pdf',credit='van der Valk et al. (2026), npj Cardiovascular Health',rights='CC BY 4.0; original figure crop and scaling, no data modifications',status='actual-study-figure',sha256=hashlib.sha256(d.read_bytes()).hexdigest(),probe=dict(width=w,height=h),derivation=f'Figure extracted from PDF page {pg+1}; crop {rect} at 3x'))
# Idempotently retain one record per local file.
r=list({a['file']:a for a in r}.values());native=json.loads((C/'native_source_probes.json').read_text());
for a in r:
 if a['file'] in native:a['nativeProbe']=native[a['file']]
(C/'media_sources.json').write_text(json.dumps(r,indent=2)+'\n')
items=[]
for a in r:
 if a['file'].endswith('.mp4'):continue
 im=Image.open(ROOT/a['file']).convert('RGB');im.thumbnail((330,230));cell=Image.new('RGB',(360,275),'#162127');cell.paste(im,((360-im.width)//2,12));ImageDraw.Draw(cell).text((10,245),Path(a['file']).name,fill='white');items.append(cell)
out=Image.new('RGB',(1440,275*((len(items)+3)//4)),'#162127')
for i,im in enumerate(items):out.paste(im,((i%4)*360,(i//4)*275))
out.save(ROOT/'build/video/2026-10-04/verification/stills-contact.jpg')
items=[]
for t in range(32,204,2):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(ROOT/'assets/motion/2026-10-04/main/m1/jammertest-2025.mp4'),'-frames:v','1','-vf','scale=320:-1','-f','image2pipe','-vcodec','png','-'])
 im=Image.open(io.BytesIO(raw));cell=Image.new('RGB',(330,210),'#162127');cell.paste(im,(5,0));ImageDraw.Draw(cell).text((8,187),str(t),fill='white');items.append(cell)
out=Image.new('RGB',(1980,210*((len(items)+5)//6)),'#162127')
for i,im in enumerate(items):out.paste(im,((i%6)*330,(i//6)*210))
out.save(ROOT/'build/video/2026-10-04/verification/esa-shots.jpg')
