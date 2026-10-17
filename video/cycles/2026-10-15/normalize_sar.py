"""Correct square-pixel H264/container metadata without re-encoding imagery."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;report=[]
for id in ['main','r2']:
 m=json.loads((C/f'{id}_manifest.json').read_text());p=ROOT/m.get('candidateOutput',m.get('output'));old=p.with_name(p.stem+'-pre-sar-correction.mp4');tmp=p.with_name(p.stem+'-square.mp4')
 if not old.exists():old.write_bytes(p.read_bytes())
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(old),'-map','0','-c','copy','-bsf:v','h264_metadata=sample_aspect_ratio=1/1','-aspect',f'{m["width"]}:{m["height"]}','-movflags','+faststart',str(tmp)],check=True);tmp.replace(p)
 report.append(dict(output=id,operation='H264 VUI and container SAR set1:1; video/audio packets copied',preservedOriginal=str(old.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(C/'SAR_CORRECTION.json').write_text(json.dumps(report,indent=2)+'\n');print('Square-pixel metadata normalised for main and R2; content not re-encoded.')
