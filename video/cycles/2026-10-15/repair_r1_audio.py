"""Bounded QA correction: shift original speech0.5s; preserve45s visual stream."""
from pathlib import Path
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;m=json.loads((C/'r1_manifest.json').read_text());file=ROOT/m['output'];old=file.with_name(file.stem+'-pre-audio-correction.mp4');tmp=file.with_name(file.stem+'-corrected.mp4')
if not old.exists():old.write_bytes(file.read_bytes())
m['leadingSilence']=0.5;(C/'r1_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(old),'-i',str(ROOT/m['audio']),'-map','0:v','-map','1:a','-af','aresample=48000,adelay=500:all=1,loudnorm=I=-16:LRA=7:TP=-1.5,apad,atrim=duration=45','-t','45','-c:v','copy','-bsf:v','h264_metadata=sample_aspect_ratio=1/1','-aspect','9:16','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(tmp)],check=True)
tmp.replace(file)
(C/'AUDIO_QA_CORRECTION.json').write_text(json.dumps(dict(output='r1',reason='actual final speech gap4.319seconds exceeds4-second limit',leadingSilenceSeconds=.5,timeStretch=False,textChanged=False,duration=45,preservedOriginal=str(old.relative_to(ROOT)),oldSha256=hashlib.sha256(old.read_bytes()).hexdigest(),newSha256=hashlib.sha256(file.read_bytes()).hexdigest(),sar='1:1',independentRecheck='pending'),indent=2)+'\n')
print('R1 audio shifted0.5s; video copied with square-pixel metadata; independent recheck pending.')
