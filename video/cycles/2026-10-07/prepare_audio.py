"""Generate cycle-isolated narration; never stretch speech or overwrite past outputs."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CYCLE = Path(__file__).resolve().parent
OUT = ROOT / f'build/video/{CYCLE.name}/audio'
PYTHON = ROOT / '.tools-edge-tts/bin/python3.14'
OUT.mkdir(parents=True, exist_ok=True)
assert 'Status: **approved**' in (CYCLE/'APPROVAL.md').read_text()
data = json.loads((CYCLE / 'narration.json').read_text())
results = []
for section in data['sections']:
    sid = section['id']
    textfile = OUT / f'{sid}.txt'
    audio = OUT / f'{sid}.mp3'
    statefile = OUT / f'{sid}.state.json'
    signature = json.dumps({'text':section['text'],'insertSilence':section.get('insertSilence')},sort_keys=True)
    previous = statefile.read_text() if statefile.exists() else None
    textfile.write_text(section['text'])
    if previous != signature or not audio.exists() or audio.stat().st_size < 1024:
        raw = OUT / f'{sid}.source.mp3'
        target = raw if section.get('insertSilence') else audio
        subprocess.run([str(PYTHON), '-m', 'edge_tts', '--voice', data['voice'],
                        '--rate='+data['rate'], '--file', str(textfile),
                        '--write-media', str(target)], check=True)
        if section.get('insertSilence'):
            at = section['insertSilence']['at']
            seconds = section['insertSilence']['seconds']
            graph = (f'[0:a]atrim=0:{at},asetpts=PTS-STARTPTS[pre];'
                     f'anullsrc=r=24000:cl=mono:d={seconds}[sil];'
                     f'[0:a]atrim=start={at},asetpts=PTS-STARTPTS[post];'
                     '[pre][sil][post]concat=n=3:v=0:a=1[out]')
            subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(raw),
                            '-filter_complex',graph,'-map','[out]','-c:a','libmp3lame','-b:a','128k',str(audio)],check=True)
            # Preserve the approved source narration for correction provenance.
        statefile.write_text(signature)
    duration = float(subprocess.check_output(['ffprobe','-v','error','-show_entries',
                     'format=duration','-of','csv=p=0',str(audio)]))
    result = {'id':sid,'seconds':duration,'target':section['target'],
              'headroom':round(section['target']-duration,3),
              'voice':data['voice'],'rate':data['rate'],'timeStretch':False}
    results.append(result)
    (CYCLE / 'audio_measurements.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(result), flush=True)

if any(x['headroom']<0 for x in results):
    raise SystemExit('Narration exceeds an approved section; revise and measure before assembling.')
ids=['m1_hook','m1_footage','m1_teaser','m1_body']
args=[]
for sid in ids: args += ['-i',str(OUT/f'{sid}.mp3')]
graph=[f'[{i}:a]aresample=48000,apad,atrim=duration={t}[a{i}]' for i,t in enumerate([5,7,4,144])]
graph.append('[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]')
subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*args,'-filter_complex',';'.join(graph),'-map','[a]','-c:a','pcm_s16le',str(OUT/'m1.wav')],check=True)
