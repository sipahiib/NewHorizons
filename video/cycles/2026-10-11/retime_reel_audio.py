"""Bounded QA correction: preserve video stream, position approved narration without stretching."""
import json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
fixes=[]
for key in ['r1','r2']:
 m=json.loads((C/f'{key}_manifest.json').read_text());out=ROOT/m['output'];old=out.parent/'work'/f'{key}-before-audio-correction.mp4';out.rename(old)
 before=hashlib.file_digest(old.open('rb'),'sha256').hexdigest()
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(old),'-i',str(ROOT/m['audio']),'-filter_complex',f'[1:a]aresample=48000,adelay={int(m["leadingSilence"]*1000)}:all=1,loudnorm=I=-16:LRA=7:TP=-1.5,apad,atrim=duration=45[a]','-map','0:v:0','-map','[a]','-t','45','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(out)],check=True)
 fixes.append({'output':key,'beforeSha256':before,'afterSha256':hashlib.file_digest(out.open('rb'),'sha256').hexdigest(),'leadingSilence':m['leadingSilence'],'videoOperation':'stream copy; scene composition unchanged','audioOperation':'delay only; no stretch'})
(C/'AUDIO_QA_CORRECTION.json').write_text(json.dumps(fixes,indent=2)+'\n')
