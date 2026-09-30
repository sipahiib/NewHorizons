"""Apply an independently reviewed narration-only correction to the cycle candidate."""
import json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];CYCLE=Path(__file__).resolve().parent
review=(CYCLE/'AUDIO_REVISION_REVIEW.md').read_text()
if 'M5_AUDIO_REVISION_GATE: PASS' not in review:raise SystemExit('Independent audio revision review must pass')
m=json.loads((CYCLE/'main_manifest.json').read_text());work=ROOT/'build/video/2026-09-30/work'

def run(args):subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1',*args],check=True)
args=[]
for section in m['sections']:args+=['-i',str(ROOT/section['audio'])]
graph=[]
for i,section in enumerate(m['sections']):graph.append(f'[{i}:a]aresample=48000,apad,atrim=duration={section["duration"]}[a{i}]')
graph.append(''.join(f'[a{i}]' for i in range(len(m['sections'])))+f'concat=n={len(m["sections"])}:v=0:a=1,loudnorm=I=-16:LRA=7:TP=-1.5[a]')
audio=work/'main-audio-revised.m4a';run([*args,'-filter_complex',';'.join(graph),'-map','[a]','-t','370','-c:a','aac','-b:a','192k','-ar','48000',str(audio)])
current=ROOT/m['candidateOutput'];temp=current.with_name('newhorizons-audio-revised.mp4')
run(['-i',str(current),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-t','370','-c:v','copy','-c:a','copy','-movflags','+faststart',str(temp)])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames','-of','json',str(temp)]))
assert abs(float(probe['format']['duration'])-370)<.03
assert probe['streams'][0]['codec_name']=='h264' and probe['streams'][1]['codec_name']=='aac'
previous=hashlib.sha256(current.read_bytes()).hexdigest();updated=hashlib.sha256(temp.read_bytes()).hexdigest()
backup=current.with_name('newhorizons-before-audio-correction.mp4');current.replace(backup);temp.replace(current)
(CYCLE/'audio_revision_manifest.json').write_text(json.dumps({'previousCandidate':str(backup.relative_to(ROOT)),'previousSha256':previous,'candidate':m['candidateOutput'],'updatedSha256':updated,'videoStreamUnchanged':True,'newM5Seconds':58.632,'reason':'reduce quiet gap before closing CTA'},indent=2)+'\n')
print('Audio-only revision applied',updated)
