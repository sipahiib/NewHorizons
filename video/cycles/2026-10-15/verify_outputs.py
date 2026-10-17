"""Actual-output technical evidence; never substitutes for full audiovisual acceptance."""
from pathlib import Path
import json,subprocess,hashlib,io,array,math,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;O=ROOT/'build/video'/C.name/'qa';O.mkdir(parents=True,exist_ok=True)
results=[]
for id in ['main','r1','r2']:
 m=json.loads((C/f'{id}_manifest.json').read_text());file=ROOT/m.get('candidateOutput',m.get('output'));meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(file)]));v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio');dur=float(meta['format']['duration']);checks=dict(resolution=(v['width']==m['width'] and v['height']==m['height']),fps=v['avg_frame_rate']=='60/1',videoCodec=v['codec_name']=='h264',audioCodec=a['codec_name']=='aac',duration=abs(dur-m['duration'])<.03,frames=int(v['nb_read_frames'])==round(m['duration']*60))
 proc=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(file),'-f','null','-'],capture_output=True);checks['fullDecode']=proc.returncode==0 and not proc.stderr
 raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(file),'-vn','-ac','1','-ar','16000','-f','s16le','-']);pcm=array.array('h',raw);rms=[math.sqrt(sum(x*x for x in pcm[i:i+160])/len(pcm[i:i+160])) for i in range(0,len(pcm),160)];voiced=[i for i,x in enumerate(rms) if x>327.68];last=(voiced[-1]+1)*.01;gap=dur-last
 loud=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(file),'-af','loudnorm=I=-16:LRA=7:TP=-1.5:print_format=json','-f','null','-'],capture_output=True,text=True).stderr;match=re.findall(r'\{[\s\S]*?\}',loud);loudness=json.loads(match[-1]) if match else None
 metrics=dict(lastAboveMinus40DbSeconds=last,finalSpeechGap=gap,fullScaleSamples=sum(abs(x)>=32767 for x in pcm),peakDbfs=20*math.log10(max(abs(x) for x in pcm)/32768),loudness=loudness)
 if id!='main':checks.update(sevenSegments=len(m['scenes'])==7,speechEndsWithin45=last<=45,finalGapAtMost4=gap<=4)
 else:checks.update(ceiling310=dur<=310.03,opening16=m['openingSeconds']==16,closing10=m['sections'][-1]['duration']==10)
 times=[];cursor=0
 for sec in m['sections'] if id=='main' else [dict(scenes=m['scenes'])]:
  for s in sec.get('scenes',[]):times+=[cursor+min(.2,s['duration']/2),cursor+s['duration']/2,cursor+s['duration']-.1];cursor+=s['duration']
 if id=='main':times += [4.9,5,5.49,5.51,11.9,12,15.9,16,30,35.49,35.51,m['sections'][0]['duration']+5.49,m['sections'][0]['duration']+5.51,dur-10,dur-9,dur-7,dur-4,dur-.1]
 else:times += [5.49,5.51,41.9,42,44.9]
 images=[]
 for i,t in enumerate(sorted(set(times))):
  rawim=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(t),'-i',str(file),'-frames:v','1','-f','image2pipe','-vcodec','png','-']);p=O/f'{id}-{t:.3f}.png';p.write_bytes(rawim);im=Image.open(io.BytesIO(rawim));im.thumbnail((320,180) if id=='main' else (180,320));images.append((t,im))
 cw,ch=(340,210) if id=='main' else (200,350);canvas=Image.new('RGB',(cw*5,ch*((len(images)+4)//5)),'#10202b');d=ImageDraw.Draw(canvas)
 for i,(t,im) in enumerate(images):x=i%5*cw;y=i//5*ch;canvas.paste(im,(x,y));d.text((x+3,y+ch-23),f'{id} {t:.3f}s',fill='white')
 canvas.save(O/f'{id}-contact.jpg')
 report=dict(id=id,file=str(file.relative_to(ROOT)),duration=dur,frames=int(v['nb_read_frames']),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),checks=checks,metrics=metrics,technicalPass=all(checks.values()),fullAudiovisualAcceptance=False)
 results.append(report);(C/'output_verification.json').write_text(json.dumps(results,indent=2)+'\n');print(id,report['technicalPass'],metrics['finalSpeechGap'],flush=True)
