from pathlib import Path
import subprocess,json,hashlib,re
ROOT=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent;W=ROOT/'build/video'/C.name/'qa';W.mkdir(parents=True,exist_ok=True)
m=json.loads((C/'main_manifest.json').read_text());p=ROOT/m['candidateOutput']
def run(cmd):return subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
(W/'probe.json').write_text(json.dumps(probe,indent=2)+'\n')
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],a['codec_name'])==(1920,1080,'60/1','h264','aac')
assert int(v['nb_frames'])==round(m['duration']*60),(v['nb_frames'],m['duration'])
assert abs(float(probe['format']['duration'])-m['duration'])<.05
r=run(['ffmpeg','-nostdin','-v','error','-i',str(p),'-f','null','-']);(W/'decode.log').write_text(r.stderr);assert r.returncode==0 and not r.stderr,r.stderr
r=run(['ffmpeg','-nostdin','-hide_banner','-i',str(p),'-af','silencedetect=n=-45dB:d=0.35,loudnorm=I=-16:LRA=7:TP=-1.5:print_format=json','-vn','-f','null','-']);(W/'audio-analysis.log').write_text(r.stderr)
r=run(['ffmpeg','-nostdin','-hide_banner','-i',str(p),'-vf','blackdetect=d=0.1:pix_th=0.02','-an','-f','null','-']);(W/'black-analysis.log').write_text(r.stderr)
frames=W/'frames';frames.mkdir(exist_ok=True)
times=[0,2,5.4,5.6,12,16,23,29.9,30.1,35.4,35.6,52,75,105,132,160,190,220,m['duration']-9.8,m['duration']-8,m['duration']-5,m['duration']-.1]
for t in times:
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1',str(frames/f'{t:07.2f}.jpg')],check=True)
result=dict(output=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),duration=float(probe['format']['duration']),frames=int(v['nb_frames']),resolution=[v['width'],v['height']],fps=v['r_frame_rate'],codecs=[v['codec_name'],a['codec_name']],sampleAspectRatio=v.get('sample_aspect_ratio'),fullDecode='passed',technicalProfile='passed',completeListening='pending independent full playback',completeViewing='pending independent full playback',evidence=str(W.relative_to(ROOT)))
(C/'output_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
