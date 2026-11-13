from pathlib import Path
import json,subprocess,os
C=Path(__file__).resolve().parent;R=C.parents[2];out=R/'build/video/2026-11-13/audio'; env=os.environ.copy();env['PYTHONPATH']=str(R/'build/video/2026-11-03/tts-runtime')
parts={'opening-hook':'Could a rubber blade make tidal power tougher? Tests suggest it can.','opening-support':'A model turbine’s bending blades cut damaging load swings.','opening-teaser':'And later, Hubble’s cosmic lenses reveal distant galaxies.'}
results={}
for k,v in parts.items():
 t=out/(k+'.txt');t.write_text(v+'\n');p=out/(k+'.mp3');subprocess.run([str(R/'.tools-edge-tts/bin/python'),'-m','edge_tts','--voice','en-GB-RyanNeural','--rate=-2%','--file',str(t),'--write-media',str(p)],env=env,check=True)
 results[k]=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]));print(k,results[k],flush=True)
(C/'opening_audio_measurements.json').write_text(json.dumps(results,indent=2)+'\n')
