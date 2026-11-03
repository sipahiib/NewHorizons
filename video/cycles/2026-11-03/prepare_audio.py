"""Generate measured narration from this cycle's approved package."""
from pathlib import Path
import json, subprocess, os
C=Path(__file__).resolve().parent; root=C.parents[2]; out=root/'build/video'/C.name/'audio'; out.mkdir(parents=True,exist_ok=True)
assert 'User approved' in (C/'APPROVAL.md').read_text()
t=(C/'NARRATION_PLAN.md').read_text()
opening=t.split('## Opening, 00:00–00:16\n')[1].split('## Swift')[0].strip().split('\n\n')
sections={'hook':opening[0].split(': ',1)[1], 'support':opening[1].split(': ',1)[1], 'teaser':opening[2].split(': ',1)[1], 'swift':t.split('## Swift\n')[1].split('## Hospital AI')[0].strip(), 'hospital':t.split('## Hospital AI\n')[1].split('## Closing')[0].strip(), 'closing':'That was our latest news. Stay with science, and stay tuned.'}
env=os.environ.copy();env['PYTHONPATH']=str(root/'build/video'/C.name/'tts-runtime')
measure={}
for name, text in sections.items():
 source=out/(name+'.txt'); source.write_text(text)
 f=out/(name+'.mp3')
 subprocess.run([str(root/'.tools-edge-tts/bin/python'),'-m','edge_tts','--voice','en-GB-RyanNeural','--rate=-2%','--file',str(source),'--write-media',str(f)],env=env,check=True)
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)]))
 measure[name]=dur;print(name,dur,flush=True)
 (C/'audio_measurements.json').write_text(json.dumps(measure,indent=2)+'\n')
