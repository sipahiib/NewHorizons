from pathlib import Path
import subprocess
C=Path(__file__).resolve().parent;R=C.parents[2];a=R/'build/video/2026-11-13/audio'
def run(args):subprocess.run(['ffmpeg','-nostdin','-y','-v','error',*map(str,args)],check=True)
# Preserve speech: detected speech ends 4.693 s and 3.572 s respectively; retain margin.
for n,end in [('opening-teaser',3.9)]:run(['-i',a/(n+'.mp3'),'-af',f'atrim=end={end},asetpts=PTS-STARTPTS','-c:a','pcm_s16le',a/(n+'-trim.wav')])
run(['-i',a/'opening-hook-final.mp3','-filter_complex','[0:a]asplit=2[x][y];[x]atrim=start=0.18:end=2.65,asetpts=PTS-STARTPTS[a0];[y]atrim=start=3.05:end=5.55,asetpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=0:a=1[out]','-map','[out]','-c:a','pcm_s16le',a/'opening-hook-final-trim.wav'])
parts=[('opening-hook-final-trim.wav',5),('opening-support-revised.mp3',7),('opening-teaser-trim.wav',4),('context.mp3',5),('flowave-context.mp3',5),('main-lead.mp3',73)]
args=[]; graph=[]
for i,(name,d) in enumerate(parts):args+=['-i',a/name];graph.append(f'[{i}:a]aresample=48000,apad,atrim=duration={d}[a{i}]')
graph.append(''.join(f'[a{i}]' for i in range(len(parts)))+f'concat=n={len(parts)}:v=0:a=1[out]')
run(args+['-filter_complex',';'.join(graph),'-map','[out]','-c:a','pcm_s16le',a/'main-lead-assembled.wav'])
