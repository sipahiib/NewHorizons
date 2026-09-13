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
const targets = [120, 60, 60, 60, 60, 10];
if (sections.length !== targets.length) throw new Error('Expected six approved narrative sections');
const measurements = [];
let invalid = false;
for (const [i, text] of sections.entries()) {
  const base = path.join(out, String(i + 1).padStart(2, '0'));
  fs.writeFileSync(`${base}.txt`, text + '\n');
  run(path.join(root, '.tools-edge-tts/bin/python3.14'), ['-m', 'edge_tts', '--voice', 'en-GB-RyanNeural', '--rate=-2%', '--file', `${base}.txt`, '--write-media', `${base}.mp3`]);
  const duration = Number(run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', `${base}.mp3`]));
  const headroom = targets[i] - duration;
  measurements.push({ section: i + 1, duration, target: targets[i], headroom, voice:'en-GB-RyanNeural', rate:'-2%', timeStretch:false });
  fs.writeFileSync(path.join(root, 'video/narration_measurements.json'), JSON.stringify(measurements, null, 2) + '\n');
  console.log(JSON.stringify(measurements.at(-1)));
  if (headroom < 0.05 || (i < 5 && headroom > 8) || (i === 5 && headroom > 6)) invalid = true;
  const timingFilter = i === 5
    ? `aresample=48000,adelay=${Math.max(0, Math.round(headroom * 1000))},apad,atrim=duration=${targets[i]}`
    : `aresample=48000,apad,atrim=duration=${targets[i]}`;
  run('ffmpeg', ['-nostdin', '-y', '-v', 'error', '-i', `${base}.mp3`, '-af', timingFilter, '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', `${base}.wav`]);
}
if (invalid) throw new Error('Revise section text: one or more measured narration sections do not fit their natural speaking windows');
const inputs = targets.flatMap((_, i) => ['-i', path.join(out, `${String(i + 1).padStart(2, '0')}.wav`)]);
run('ffmpeg', ['-nostdin', '-y', '-v', 'error', ...inputs, '-filter_complex', '[0:a][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1[out]', '-map', '[out]', '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', path.join(root, 'build/video/narration-en.wav')]);
console.log('Narration assembled: 370 seconds; audiovisual verification still required.');
