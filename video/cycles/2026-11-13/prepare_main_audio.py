from pathlib import Path
import json,subprocess,os
C=Path(__file__).resolve().parent;R=C.parents[2];out=R/'build/video/2026-11-13/audio';out.mkdir(parents=True,exist_ok=True)
s=(C/'NARRATION_PLAN.md').read_text();t=s.split('## Main opening and lead — flexible tidal turbine blades\n\n')[1].split('\n\n## Second story')[0]; opening,body=t.split('\n\n',1)
phrases=['Could a rubber blade make tidal power tougher?','Researchers have tested a turbine blade that bends with the current.','And later, Hubble shows how gravity can turn galaxies into cosmic lenses.']
assert ' '.join(phrases)==opening
story2=s.split('## Second story — Hubble and Roman\n\n')[1].split('\n\n## Closing')[0]
parts={'hook':phrases[0],'support':phrases[1],'teaser':phrases[2],'lead':body,'second':story2,'closing':'That was our latest news. Stay with science, and stay tuned.'}
env=os.environ.copy();env['PYTHONPATH']=str(R/'build/video/2026-11-03/tts-runtime');results={}
for k,v in parts.items():
 text=out/(k+'.txt');text.write_text(v+'\n');media=out/('main-'+k+'.mp3')
 subprocess.run([str(R/'.tools-edge-tts/bin/python'),'-m','edge_tts','--voice','en-GB-RyanNeural','--rate=-2%','--file',str(text),'--write-media',str(media)],env=env,check=True)
 d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(media)]));results[k]=d;print(k,d,flush=True)
 (C/'main_audio_measurements.json').write_text(json.dumps(results,indent=2)+'\n')
