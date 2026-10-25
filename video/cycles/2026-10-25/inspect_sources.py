from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;O=R/'build/video'/C.name/'source-inspection';O.mkdir(parents=True,exist_ok=True)
m=json.loads((C/'media_verification.json').read_text());sheet=Image.new('RGB',(960,len(m['assets'])*200),'#121820');d=ImageDraw.Draw(sheet)
for row,a in enumerate(m['assets']):
 du=float(a['probe']['format']['duration'])
 for col,t in enumerate([.5,du/2,max(.5,du-1)]):
  p=O/f'{a["id"]}-{col}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(R/a['file']),'-frames:v','1','-vf','scale=320:180',str(p)],check=True)
  sheet.paste(Image.open(p),(col*320,row*200));d.text((col*320+5,row*200+182),a['id']+' @ '+str(round(t,1)),fill='white')
sheet.save(O/'contact.jpg');print(O/'contact.jpg')
