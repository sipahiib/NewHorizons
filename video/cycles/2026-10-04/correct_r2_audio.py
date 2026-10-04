"""Apply the independently identified natural-pause correction without changing speech rate/text."""
from pathlib import Path
import json,subprocess,shutil
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;A=ROOT/f'build/video/{C.name}/audio';R=ROOT/f'build/reels/{C.name}'
assert 'Status: **approved**' in (C/'APPROVAL.md').read_text()
p=C/'narration.json';n=json.loads(p.read_text());s=next(s for s in n['sections'] if s['id']=='r2');s['insertSilence']={'at':23.85,'seconds':0.6,'reason':'Natural sentence pause; corrected actual final speech gap to at most4seconds'};p.write_text(json.dumps(n,indent=2)+'\n')
source=A/'r2.source.mp3'
if not source.exists():shutil.copy2(A/'r2.mp3',source)
g='[0:a]atrim=0:23.85,asetpts=PTS-STARTPTS[pre];anullsrc=r=24000:cl=mono:d=0.6[sil];[0:a]atrim=start=23.85,asetpts=PTS-STARTPTS[post];[pre][sil][post]concat=n=3:v=0:a=1[out]'
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(source),'-filter_complex',g,'-map','[out]','-c:a','libmp3lame','-b:a','128k',str(A/'r2.mp3')],check=True)
(A/'r2.state.json').write_text(json.dumps({'text':s['text'],'insertSilence':s['insertSilence']},sort_keys=True))
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(A/'r2.mp3')]))
q=C/'audio_measurements.json';measure=json.loads(q.read_text())
for v in measure:
 if v['id']=='r2':v.update(seconds=dur,headroom=round(45-dur,3),insertSilence=s['insertSilence'])
q.write_text(json.dumps(measure,indent=2)+'\n')
m=json.loads((C/'r2_manifest.json').read_text());out=ROOT/m['output'];backup=R/'work/r2-before-audio-correction.mp4'
if not backup.exists():shutil.copy2(out,backup)
corrected=R/'work/r2-corrected.mp4'
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(backup),'-i',str(A/'r2.mp3'),'-filter_complex','[1:a]aresample=48000,loudnorm=I=-16:LRA=7:TP=-1.5,apad,atrim=duration=45[a]','-map','0:v','-map','[a]','-t','45','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(corrected)],check=True)
corrected.replace(out)
print('Corrected R2 candidate and measured voice:',dur,flush=True)
