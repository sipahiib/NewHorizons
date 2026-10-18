"""Generate approved voice in cycle-local storage; measure rather than stretch."""
from pathlib import Path
import json,subprocess,hashlib,os
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;OUT=ROOT/'build/video'/C.name/'audio';OUT.mkdir(parents=True,exist_ok=True)
assert 'approved by user selection' in (C/'APPROVAL.md').read_text()
os.environ['PYTHONPATH']=str(ROOT/'build/video'/C.name/'tts-runtime')
data=json.loads((C/'narration.json').read_text());measure=[]
for s in data['sections']:
 p=OUT/f"{s['id']}.mp3";txt=OUT/f"{s['id']}.txt";txt.write_text(s['text']);signature=hashlib.sha256((s['text']+data['voice']+data['rate']).encode()).hexdigest();state=p.with_suffix('.signature')
 if not p.exists() or not state.exists() or state.read_text()!=signature:
  subprocess.run([str(ROOT/'.tools-edge-tts/bin/python'),'-m','edge_tts','--voice',data['voice'],'--rate='+data['rate'],'--file',str(txt),'--write-media',str(p),'--write-subtitles',str(p.with_suffix('.srt'))],check=True)
  state.write_text(signature)
 seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))
 measure.append(dict(id=s['id'],seconds=seconds,target=s['target'],timeStretch=False))
 (C/'audio_measurements.json').write_text(json.dumps(measure,indent=2)+'\n');print(measure[-1],flush=True)
 if s['target'] is not None and seconds>s['target']:print('OVER TARGET: revise this section before render',flush=True)
