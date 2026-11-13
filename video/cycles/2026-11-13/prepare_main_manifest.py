from pathlib import Path
import json,hashlib
C=Path(__file__).resolve().parent; R=C.parents[2]; med='build/video/2026-11-13/media/main/'; mot='assets/motion/2026-11-13/main/'; work='build/video/2026-11-13/work/'; aud='build/video/2026-11-13/audio/'
def st(f,d):return {'kind':'still','file':med+f,'duration':d,'classification':'contextual' if f=='flowave-2019.png' else 'direct'}
def mv(f,d,seek=0,crop=None):
 s={'kind':'motion','file':mot+f,'duration':d,'seek':seek,'classification':'contextual'}
 if crop:s['crop']=crop
 return s
m1=[mv('ocean-19093263.mp4',5),mv('sequim-turbine-03.avi',7,0,'954:838:160:78'),st('hubble-lenses.jpg',4),mv('sequim-turbine-01.avi',5,0,'954:838:160:78'),st('flowave-2019.png',5),mv('ocean-29509867.mp4',5,5),mv('ocean-29509867.mp4',8,12),mv('ocean-19093263.mp4',8,5),mv('ocean-29509867.mp4',7,2),mv('ocean-29509867.mp4',8,22),mv('ocean-29509867.mp4',7,31),mv('ocean-19093263.mp4',8,4),mv('ocean-19093263.mp4',7,6),mv('ocean-29509867.mp4',8,40),mv('ocean-29509867.mp4',7,50)]
m2=[st('lens-a.png',5),st('lens-b.png',7),mv('roman-launch-nasa.mp4',8,25,'1920:600:0:0'),st('lens-e.png',8),mv('roman-arrival.mp4',8,110),st('lens-i.png',7),mv('hubble-servicing.mp4',8,165),st('hubble-lenses.jpg',5),st('lens-f.png',5)]
assert sum(x['duration'] for x in m1)==99 and sum(x['duration'] for x in m2)==61
m={'cycle':'2026-11-13','status':'prepared-for-review','candidateOutput':'build/video/2026-11-13/newhorizons.mp4','finalOutput':'build/video/newhorizons.mp4','duration':170,'fps':60,'width':1920,'height':1080,'openingSeconds':16,'closingSeconds':10,'sections':[{'id':'tidal','duration':99,'audio':aud+'main-lead-assembled.wav','title':work+'title-tidal.png','scenes':m1,'counts':{'motion':sum(x['kind']=='motion' for x in m1),'stills':sum(x['kind']=='still' for x in m1)}},{'id':'hubble','duration':61,'audio':aud+'main-second.mp3','title':work+'title-hubble.png','scenes':m2,'counts':{'motion':sum(x['kind']=='motion' for x in m2),'stills':sum(x['kind']=='still' for x in m2)}},{'id':'closing','duration':10,'audio':aud+'main-closing.mp3','leadingSilence':2,'closing':True}],'closing':work+'closing-bg.png','closingPanel':work+'closing-panel.png','closingBell':work+'bell.png','subscribeOverlay':work+'subscribe.png','subscribeWindow':[30,35.5]}
paths={x['file'] for x in m1+m2}|{s['audio'] for s in m['sections']}|{work+x for x in ['title-tidal.png','title-hubble.png','closing-bg.png','closing-panel.png','bell.png','subscribe.png']}
m['hashes']={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in sorted(paths)};(C/'main_manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
