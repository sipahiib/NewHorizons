import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const sharp = require('../.tools-node/node_modules/sharp');
const root = path.resolve(import.meta.dirname, '..');
const file = path.join(root, 'build/video/newhorizons.mp4');
const run = (bin, args) => {
  const r = spawnSync(bin, args, { encoding: 'utf8', maxBuffer: 16 * 1024 * 1024 });
  if (r.status !== 0) throw new Error(r.stderr || `${bin} failed`);
  return r;
};
const probe = JSON.parse(run('ffprobe', ['-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', file]).stdout);
const v = probe.streams.find(s => s.codec_type === 'video');
const a = probe.streams.find(s => s.codec_type === 'audio');
if (v.width !== 1920 || v.height !== 1080 || v.r_frame_rate !== '60/1' || v.codec_name !== 'h264' || Number(v.nb_read_frames) !== 18000 || a.codec_name !== 'aac' || a.sample_rate !== '48000' || Math.abs(Number(probe.format.duration)-300) > .04) throw new Error('Delivery specification mismatch');
const black = run('ffmpeg', ['-nostdin', '-v', 'info', '-i', file, '-an', '-vf', 'scale=160:90,fps=5,blackdetect=d=0.4:pix_th=0.10:pic_th=0.98', '-f', 'null', '-']).stderr;
const silences = run('ffmpeg', ['-nostdin', '-v', 'info', '-i', file, '-vn', '-af', 'silencedetect=noise=-40dB:d=0.5', '-f', 'null', '-']).stderr;
const gaps = [...silences.matchAll(/silence_end: ([\d.]+) \| silence_duration: ([\d.]+)/g)].map(m => ({ end: Number(m[1]), duration: Number(m[2]) }));
const blackEvents = black.split('\n').filter(l => /black_start:/.test(l));
if (blackEvents.length || gaps.some(g => g.duration > 1.6)) throw new Error(`Black or unexpected audio gap: ${JSON.stringify({ blackEvents, gaps })}`);
const times = [2,15,37,75,101,112,140,157,187,202,220,232,247,263,274,288,291,293,294,298];
const qa = path.join(root, 'build/video/current-qa');
fs.mkdirSync(qa, { recursive: true });
const composite = [];
for (const [i,t] of times.entries()) {
  const frame = path.join(qa, `${t}.png`);
  run('ffmpeg', ['-nostdin', '-y', '-v', 'error', '-ss', String(t), '-i', file, '-frames:v', '1', '-vf', 'scale=480:270', frame]);
  const label = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="480" height="30"><rect width="480" height="30" fill="#091521"/><text x="12" y="22" fill="white" font-family="Arial" font-size="18">${t} seconds</text></svg>`);
  composite.push({ input: frame, left: i%4*480, top: Math.floor(i/4)*300 }, { input: label, left: i%4*480, top: Math.floor(i/4)*300+270 });
}
await sharp({ create: { width:1920, height:1500, channels:3, background:'#091521' } }).composite(composite).jpeg({quality:92}).toFile(path.join(qa,'contact.jpg'));
const report = { file:'build/video/newhorizons.mp4', duration: Number(probe.format.duration), width:v.width, height:v.height, fps:v.r_frame_rate, frames:Number(v.nb_read_frames), videoCodec:v.codec_name, audioCodec:a.codec_name, sampleRate:a.sample_rate, blackEvents, maxDetectedSilence:Math.max(...gaps.map(g=>g.duration)), measuredAudioGaps:gaps, visualReview:'pending contact sheet review', audioReview:'signal continuity checked; not a claim of full human listening' };
fs.writeFileSync(path.join(root,'video/current_video_verification.json'), JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({...report,measuredAudioGaps:`${gaps.length} sentence/boundary pauses`},null,2));
