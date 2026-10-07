"""Generate actual-output verification artifacts. Run with the bundled Pillow runtime.

Only invoke a named output after render completion. Does not rerender media.
"""
from pathlib import Path
import argparse, array, hashlib, io, json, math, re, subprocess, wave
from PIL import Image, ImageDraw, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[3]
CYCLE = Path(__file__).resolve().parent

def run(args):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace'))
    return p

def pcm(path, start=None, duration=None):
    cmd = ['ffmpeg','-nostdin','-v','error']
    if start is not None: cmd += ['-ss',str(start)]
    cmd += ['-i',str(path)]
    if duration is not None: cmd += ['-t',str(duration)]
    cmd += ['-vn','-ac','1','-ar','16000','-f','s16le','-']
    a = array.array('h',run(cmd).stdout)
    return a

def envelope(a):
    return [math.sqrt(sum(x*x for x in a[i:i+160])/len(a[i:i+160])) for i in range(0,len(a),160)]

def correlation(a,b):
    n=min(len(a),len(b)); a=a[:n]; b=b[:n]
    ma=sum(a)/n; mb=sum(b)/n
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))

def main(key):
    manifest=json.loads((CYCLE/f'{key}_manifest.json').read_text())
    file=ROOT/manifest.get('candidateOutput',manifest.get('output',''))
    folder=ROOT/(f'build/video/{CYCLE.name}/verification' if key=='main' else f'build/reels/{CYCLE.name}/verification')/f'qa-{key}'
    folder.mkdir(parents=True,exist_ok=True)
    result={'output':str(file.relative_to(ROOT)), 'sha256':hashlib.file_digest(file.open('rb'),'sha256').hexdigest()}
    probe=run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(file)])
    (folder/'probe.json').write_bytes(probe.stdout)
    data=json.loads(probe.stdout); result['streams']=data['streams']; result['format']=data['format']
    decode=run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(file),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    (folder/'decode.log').write_bytes(decode.stderr); result['full_file_decode']='passed'
    snd=run(['ffmpeg','-nostdin','-hide_banner','-i',str(file),'-vn','-af','ebur128=peak=true,silencedetect=noise=-40dB:d=0.4','-f','null','-'])
    (folder/'sound.log').write_bytes(snd.stderr)
    txt=snd.stderr.decode(); summary=txt[txt.rfind('Summary:'):]
    result['loudness_summary']=summary
    silences=[]; pending=None
    for line in txt.splitlines():
        m=re.search(r'silence_start: ([\d.]+)',line)
        if m: pending=float(m.group(1))
        m=re.search(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',line)
        if m: silences.append({'start':pending,'end':float(m.group(1)),'duration':float(m.group(2))}); pending=None
    result['silences_below_minus40dB_minimum_0_4s']=silences
    a=pcm(file); env=envelope(a)
    with wave.open(str(folder/'decoded-audio.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(a.tobytes())
    peak=max(abs(x) for x in a)
    voiced=[i for i,x in enumerate(env) if x >= 32768*10**(-40/20)]
    result['pcm_metrics']={'mono_sample_rate':16000,'samples':len(a),'peak_dbfs':20*math.log10(peak/32768), 'full_scale_samples':sum(abs(x)>=32767 for x in a),'last_above_minus40dB_rms_window_end':(voiced[-1]+1)*0.01,'final_below_threshold_gap':manifest['duration']-(voiced[-1]+1)*0.01}
    waveim=Image.new('RGB',(1600,280),'#111820');d=ImageDraw.Draw(waveim)
    for i in range(1550):
        lo=int(i*len(env)/1550);hi=max(lo+1,int((i+1)*len(env)/1550)); val=max(env[lo:hi])/32768
        d.line((25+i,245,25+i,245-min(210,val*650)),fill='#69e0bb')
    d.text((25,15),f'{key}: RMS envelope, 10 ms windows; -40 dB final gap {result["pcm_metrics"]["final_below_threshold_gap"]:.2f}s',fill='white')
    waveim.save(folder/'waveform.png')
    # Compare actual AAC waveform envelopes to the approved source, without
    # claiming pronunciation or complete listening verification.
    if key=='main':
        actual=pcm(file,300,10); ref=pcm(ROOT/manifest['sections'][-1]['audio']); offset=300
    else:
        actual=a;ref=pcm(ROOT/manifest['audio']); offset=0
    result['approved_audio_envelope_correlation']={'offset_seconds':offset,'reference':manifest['sections'][-1]['audio'] if key=='main' else manifest['audio'], 'correlation_at_scheduled_start':correlation(envelope(actual),envelope(ref)), 'limitation':'Waveform identity/alignment evidence, not narration comprehension or listening.'}
    scenes=[];t=0
    if key=='main':
        for section in manifest['sections']:
            for scene in section.get('scenes',[{'duration':section['duration'],'kind':'closing','label':'CTA'}]):
                scenes.append((t,scene));t+=scene['duration']
    else:
        for scene in manifest['scenes']:scenes.append((t,scene));t+=scene['duration']
    samples=[]
    for i,(start,scene) in enumerate(scenes):
        for tag,time in [('start',start),('middle',start+scene['duration']/2),('end',start+scene['duration']-1/60)]:
            samples.append((f'scene-{i:02d}-{tag}',time,i,scene.get('label',scene['kind'])))
    extras=[0,4.983333,5,11.983333,12,15.983333,16,159.983333,160,299.983333,300,300.5,302,305,308,309.983333] if key=='main' else [41.983333,42,42.5,43.5,44.983333]
    for i,time in enumerate(extras): samples.append((f'boundary-{i:02d}',time,None,'boundary/CTA'))
    cells=[]
    for name,time,index,label in samples:
        dest=folder/f'{name}-{time:.3f}.jpg'
        raw=run(['ffmpeg','-nostdin','-v','error','-ss',f'{time:.6f}','-i',str(file),'-frames:v','1','-q:v','2','-f','image2pipe','-vcodec','mjpeg','-pix_fmt','yuvj420p','-strict','-1','-']).stdout
        dest.write_bytes(raw)
        im=Image.open(io.BytesIO(raw)); im.thumbnail((480,300) if key=='main' else (270,480))
        cw,ch=(500,340) if key=='main' else (290,530)
        cell=Image.new('RGB',(cw,ch),'#162127');cell.paste(im,((cw-im.width)//2,5));cd=ImageDraw.Draw(cell);cd.text((7,ch-36),f'{name} {time:.3f}s',fill='white');cd.text((7,ch-21),label[:43],fill='white');cells.append(cell)
    # Keep sheets manageable for inspection: five scene rows per page.
    for page in range((len(cells)+14)//15):
        group=cells[page*15:(page+1)*15];cw,ch=group[0].size
        sheet=Image.new('RGB',(cw*3,ch*((len(group)+2)//3)),'#162127')
        for i,cell in enumerate(group):sheet.paste(cell,((i%3)*cw,(i//3)*ch))
        sheet.save(folder/f'contact-{page:02d}.jpg',quality=90)
    if key != 'main':
        # Independently observed center region: full source fitted inside
        # 1080x760, centered at (540,980), over its blurred duplicate.
        checks=[]; comparison=[]; start=0
        for i,scene in enumerate(manifest['scenes']):
            source_path=ROOT/scene['file']
            if scene['kind']=='motion':
                raw=run(['ffmpeg','-nostdin','-v','error','-ss',str(scene.get('seek',0)),'-i',str(source_path),'-frames:v','1','-f','image2pipe','-vcodec','png','-']).stdout
                source=Image.open(io.BytesIO(raw)).convert('RGB')
            else: source=Image.open(source_path).convert('RGB')
            actual=Image.open(folder/f'scene-{i:02d}-start-{start:.3f}.jpg').convert('RGB')
            factor=min(1080/source.width,760/source.height)
            ww=int(source.width*factor)//2*2;hh=int(source.height*factor)//2*2
            ref=source.resize((ww,hh),Image.Resampling.BICUBIC)
            x=(1080-ww)//2;y=(1960-hh)//2
            rendered=actual.crop((x,y,x+ww,y+hh))
            mae=sum(ImageStat.Stat(ImageChops.difference(ref,rendered)).mean)/3
            checks.append({'scene':i,'source':scene['file'],'native_size':list(source.size),'expected_full_frame_rectangle':[x,y,ww,hh],'mean_absolute_rgb_difference':mae,'interpretation':'Complete source including edges fitted into actual center. Compression/resampling differences remain.'})
            a=ref.copy();a.thumbnail((400,280));b=rendered.copy();b.thumbnail((400,280))
            cell=Image.new('RGB',(840,320),'#162127');cell.paste(a,(10,10));cell.paste(b,(430,10));ImageDraw.Draw(cell).text((10,295),f'scene{i}: complete source vs actual center; MAE={mae:.2f}',fill='white');comparison.append(cell);start+=scene['duration']
        out=Image.new('RGB',(840,320*len(comparison)),'#162127')
        for i,cell in enumerate(comparison):out.paste(cell,(0,320*i))
        out.save(folder/'full-frame-comparison.jpg')
        (folder/'full-frame-preservation.json').write_text(json.dumps(checks,indent=2)+'\n')
    result['frame_samples']=[{'time':time,'file':str((folder/f'{name}-{time:.3f}.jpg').relative_to(ROOT)),'scene':index} for name,time,index,label in samples]
    result['evidence_folder']=str(folder.relative_to(ROOT))
    (folder/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':key,'sha256':result['sha256'],'full_file_decode':result['full_file_decode'],'pcm_metrics':result['pcm_metrics'],'loudness_summary':summary,'envelope':result['approved_audio_envelope_correlation'],'evidence_folder':result['evidence_folder']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',choices=['main','r1','r2']);main(p.parse_args().output)
