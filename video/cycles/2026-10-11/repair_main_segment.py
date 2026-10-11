"""Replace one clean re-fetched source excerpt before initial main output QA."""
raise SystemExit('Superseded by user media revision. Use current main_manifest.json and render.py; old excerpt contains an editorial caption.')
import subprocess,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
source=ROOT/'assets/motion'/C.name/'main/arcjet-opening-repaired.mp4';out=ROOT/'build/video'/C.name/'work/m1-04.mp4';card=ROOT/'build/video'/C.name/'work/youtube-30s.png'
graph="[0:v]split=2[f][b];[b]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,gblur=sigma=12,eq=brightness=-0.38:saturation=0.55,scale=1920:1080[bg];[f]scale=1920:1080:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=60[base];[base][1:v]overlay=0:0:shortest=1:enable='gte(t,2)*lt(t,7.5)'[v]"
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-filter_complex_threads','1','-ss','30','-i',str(source),'-loop','1','-framerate','60','-i',str(card),'-filter_complex',graph,'-map','[v]','-t','14','-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(out)],check=True)
(C/'SOURCE_QA_CORRECTION.json').write_text(json.dumps({'reason':'one native HLS fetch had corrupt packet in30–44secondexcerpt; clean first50seconds re-fetched withfail-on-error','sourceFile':str(source.relative_to(ROOT)),'sourceSha256':hashlib.file_digest(source.open('rb'),'sha256').hexdigest(),'replacedSegment':str(out.relative_to(ROOT)),'segmentSha256':hashlib.file_digest(out.open('rb'),'sha256').hexdigest(),'topicOrFramingChange':False},indent=2)+'\n')
