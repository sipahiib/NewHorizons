import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'build/video/narration-parts-en/current');
fs.mkdirSync(out, { recursive: true });
const run = (bin, args) => {
  const r = spawnSync(bin, args, { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
  if (r.status !== 0) throw new Error(`${bin}: ${r.stderr || r.stdout}`);
  return r.stdout.trim();
};
const sections = fs.readFileSync(path.join(root, 'video/narration-en.txt'), 'utf8').split(/^## /m).slice(1).map(s => s.slice(s.indexOf('\n')).trim());
const targets = [110, 45, 45, 45, 45, 10];
if (sections.length !== targets.length) throw new Error('Expected six approved narrative sections');
const measurements = [];
for (const [i, text] of sections.entries()) {
  const base = path.join(out, String(i + 1).padStart(2, '0'));
  fs.writeFileSync(`${base}.txt`, text + '\n');
  run(path.join(root, '.tools-edge-tts/bin/python3.14'), ['-m', 'edge_tts', '--voice', 'en-GB-RyanNeural', '--rate=-2%', '--file', `${base}.txt`, '--write-media', `${base}.mp3`]);
  const duration = Number(run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', `${base}.mp3`]));
  const speakingWindow = targets[i] - 0.25;
  const tempo = duration / speakingWindow;
  measurements.push({ section: i + 1, duration, target: targets[i], tempo });
  fs.writeFileSync(path.join(root, 'video/narration_measurements.json'), JSON.stringify(measurements, null, 2) + '\n');
  console.log(JSON.stringify(measurements.at(-1)));
  if (tempo < 0.82 || tempo > 1.22) throw new Error('Revise section text: timing adjustment outside pipeline limits');
  run('ffmpeg', ['-nostdin', '-y', '-v', 'error', '-i', `${base}.mp3`, '-af', `atempo=${tempo.toFixed(8)},aresample=48000,apad,atrim=duration=${targets[i]}`, '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', `${base}.wav`]);
}
const inputs = targets.flatMap((_, i) => ['-i', path.join(out, `${String(i + 1).padStart(2, '0')}.wav`)]);
run('ffmpeg', ['-nostdin', '-y', '-v', 'error', ...inputs, '-filter_complex', '[0:a][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1[out]', '-map', '[out]', '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', path.join(root, 'build/video/narration-en.wav')]);
console.log('Narration assembled: 300 seconds; audiovisual verification still required.');
