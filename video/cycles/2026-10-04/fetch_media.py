"""Download approved, cycle-isolated sources and retain per-item provenance."""
import hashlib,json,subprocess
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
CYCLE=Path(__file__).resolve().parent
DATE=CYCLE.name
assert 'Status: **approved**' in (CYCLE/'APPROVAL.md').read_text()
RESEARCH=ROOT/f'build/video/{DATE}/research'
creators={8460066:'Los Muertos Crew',8311312:'Ammad Rasool',8026528:'MART PRODUCTION',8413638:'SHVETS production',7088462:'MART PRODUCTION',7195664:'kaboompics',6997946:'Pavel Danilyuk',5998403:'Pavel Danilyuk',36656061:'GIUSEPPE DE BERGOLIS',5453568:'Tima Miroshnichenko'}
records=json.loads((CYCLE/'media_sources.json').read_text()) if (CYCLE/'media_sources.json').exists() else []
def fetch(url,dest):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r,dest.open('wb') as out:
            while b:=r.read(1024*1024):out.write(b)
    return dest
def record(dest,story,source,download,credit,rights,status='context'):
    if dest.suffix=='.mp4':
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,r_frame_rate','-of','json',str(dest)]))
    else:
        with Image.open(dest) as im:probe={'width':im.width,'height':im.height}
    previous=next((a for a in records if a['file']==str(dest.relative_to(ROOT))),{})
    records[:]=[a for a in records if a['file']!=str(dest.relative_to(ROOT))]
    records.append(dict(**{k:v for k,v in previous.items() if k in ('nativeProbe','derivation')},file=str(dest.relative_to(ROOT)),story=story,source=source,download=download,credit=credit,rights=rights,status=status,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),probe=probe))
    (CYCLE/'media_sources.json').write_text(json.dumps(records,indent=2)+'\n')
    print('OK',str(dest.relative_to(ROOT)),flush=True)

# The group photograph is deliberately excluded: its Testnor credit has no ESA licence.
for i in range(5):
    s=BeautifulSoup((RESEARCH/f'esa-{i}.html').read_text(),'html.parser')
    link=next(a for a in s.select('a[href]') if 'HI-RES' in a.get_text())
    u=urljoin('https://www.esa.int',link['href']);dest=ROOT/f'assets/motion/{DATE}/main/m1/esa-{i}{Path(u).suffix}'
    fetch(u,dest)
    source=next((a.get('href') for a in s.select('link[rel="canonical"]')),None) or ['ESA_team_at_Jammertest_2026','Spoofed_smartphone','Galileo_Signal_Authentication_Service_test_in_Norway','Navigation_laboratory_van_in_Norway','ESA_engineers_test_a_drone_Jammertest_2026'][i]
    if not str(source).startswith('http'):source='https://www.esa.int/ESA_Multimedia/Images/2026/09/'+source
    record(dest,'m1',source,u,'©ESA/jensenmedia','ESA Standard Licence; editorial/informational use with credit','actual-September-2026')
s=BeautifulSoup((RESEARCH/'esa-6.html').read_text(),'html.parser')
u=next(a['href'] for a in s.select('a[href]') if a.get_text(strip=True).startswith('Source MP4'))
dest=fetch(u,ROOT/f'assets/motion/{DATE}/main/m1/jammertest-2025-source.mp4')
record(dest,'m1','https://www.esa.int/esatv/Videos/2026/02/Jammertest_strengthening_satellite_navigation',u,'©European Space Agency — ESA','ESA Standard Licence; editorial/informational use with on-screen credit','archive-September-2025')

videos={'m2':[8460066,8311312,8026528,8413638,7088462,7195664],'r1':[6997946,5998403,36656061,5453568]}
for story,ids in videos.items():
    for iid in ids:
        u=f'https://www.pexels.com/download/video/{iid}/'
        try:
            with urlopen(Request(u,method='HEAD',headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:direct=r.url
            dest=ROOT/f'assets/motion/{DATE}/{"reels" if story.startswith("r") else "main"}/{story}/pexels-{iid}.mp4'
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():
                subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',direct,'-t','24','-vf','scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2','-an','-c:v','libx264','-preset','veryfast','-crf','20',str(dest)],check=True,timeout=150)
            record(dest,story,f'https://www.pexels.com/video/{iid}/',direct,creators[iid]+' / Pexels','Pexels licence; contextual healthcare footage')
        except Exception as e:print('ERROR',iid,str(e),flush=True)
# Public still downloads were denied. R1 uses unanimated frames from newly licensed videos; see prepare_figures.py.

# Only NASA-credited material is selected, not the two INSPYRE/third-party fire photos.
nasa='https://science.nasa.gov/earth/natural-disasters/wildfires/nasa-campaign-explores-clouds-spawned-by-wildfires/'
items=[('inspyre-pyrocb-diagram.png','NASA/Bill Ingalls, NASA/JSC/Mark Sowa'),('inspyre-news-image-7-28-26-4.jpeg','NASA/Bill Ingalls, NASA/JSC/Mark Sowa'),('inspyre-preview-loiacono-9318.jpg','NASA/Milan Loiacono'),('afrc2026-0144-226orig-er2-inst.jpg','NASA/Carla Escamilla'),('inspyre-preview-loiacono-0172.jpg','NASA/Milan Loiacono'),('inspyre-light-walk.mp4','NASA/Katie Jepson')]
for name,credit in items:
    u='https://science.nasa.gov/wp-content/uploads/2026/10/'+name
    dest=fetch(u,ROOT/f'assets/motion/{DATE}/reels/r2/{name}')
    record(dest,'r2',nasa,u,credit,'NASA media usage guidelines; factual editorial use, credit, no endorsement','illustrative-scientific-diagram' if name.endswith('diagram.png') else 'actual-campaign-2026')
