import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {createRequire} from 'node:module';
const sharp = createRequire(import.meta.url)('../../../.tools-node/node_modules/sharp');

const root = path.resolve(import.meta.dirname, '../../..');
const work = 'build/reels/2026-09-26/work';
fs.mkdirSync(path.join(root, work), {recursive: true});

const sources = [
  'assets/motion/2026-09-26/reels/r1/avatar-hero.png',
  'assets/motion/2026-09-26/reels/r1/avatar-example-1.png',
  'assets/motion/2026-09-26/reels/r1/avatar-example-2.png',
  'assets/motion/2026-09-26/reels/r1/video-call-overhead.mp4',
  'assets/motion/2026-09-26/reels/r1/video-call-women.mp4',
  'assets/motion/2026-09-26/reels/r1/video-call-woman.mp4'
];
const hashes = Object.fromEntries(sources.map(file => [file, createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex')]));

const base = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
<rect x="54" y="165" width="972" height="310" rx="28" fill="#071a22" fill-opacity=".94"/>
<text x="94" y="232" fill="#66dec8" font-family="Arial" font-size="30" letter-spacing="4">THE FUTURE OF AI</text>
<text x="94" y="315" fill="white" font-family="Arial" font-size="54" font-weight="bold">A FACE CAN PERSUADE.</text>
<text x="94" y="388" fill="white" font-family="Arial" font-size="54" font-weight="bold">VERIFY THE ANSWER.</text>
<rect x="54" y="1400" width="972" height="275" rx="28" fill="#071a22" fill-opacity=".94"/>
<text x="94" y="1468" fill="white" font-family="Arial" font-size="34">Gemini 3.8 Live with Live Avatar</text>
<text x="94" y="1522" fill="#c6dce1" font-family="Arial" font-size="28">Enterprise availability • Google Cloud</text>
<text x="94" y="1594" fill="#66dec8" font-family="Arial" font-size="31">YouTube @newhorizons_21</text>
<text x="94" y="1638" fill="white" font-family="Arial" font-size="29">Instagram • Like &amp; Follow</text>
</svg>`;
const context = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
<rect x="165" y="515" width="750" height="66" rx="18" fill="#071a22" fill-opacity=".92"/>
<text x="540" y="558" text-anchor="middle" fill="white" font-family="Arial" font-size="27">Context: human video call • not Gemini output</text>
</svg>`;
const product = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
<rect x="265" y="515" width="550" height="66" rx="18" fill="#071a22" fill-opacity=".92"/>
<text x="540" y="558" text-anchor="middle" fill="white" font-family="Arial" font-size="27">AI-generated avatar • Google demonstration</text>
</svg>`;
await sharp(Buffer.from(base)).png().toFile(path.join(root, work, 'r1-overlay.png'));
await sharp(Buffer.from(context)).png().toFile(path.join(root, work, 'r1-context.png'));
await sharp(Buffer.from(product)).png().toFile(path.join(root, work, 'r1-product.png'));

const scenes = [
  {kind:'still', file:sources[0], duration:6.5, label:'product'},
  {kind:'motion', file:sources[3], seek:1, duration:5, label:'context'},
  {kind:'still', file:sources[1], duration:6.5, label:'product'},
  {kind:'motion', file:sources[4], seek:0, duration:5, label:'context'},
  {kind:'still', file:sources[2], duration:6.5, label:'product'},
  {kind:'motion', file:sources[5], seek:0, duration:3, loop:true, label:'context'},
  {kind:'motion', file:sources[3], seek:4, duration:12.5, label:'context'}
];
const manifest = {
  cycle:'2026-09-26', status:'prepared-for-review', output:'build/reels/2026-09-26/01-future-of-ai.mp4',
  audio:'build/video/2026-09-26/audio/r1.mp3', overlay:`${work}/r1-overlay.png`, contextOverlay:`${work}/r1-context.png`, productOverlay:`${work}/r1-product.png`,
  duration:45, fps:60, width:1080, height:1920,
  directSource:'https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-8-live-with-live-avatar-is-now-generally-available/',
  contextualSources:['https://www.pexels.com/video/a-person-in-a-video-call-6985210/','https://www.pexels.com/video/women-having-conversation-via-video-call-5904564/','https://www.pexels.com/video/a-woman-in-a-video-call-using-her-laptop-7382309/'],
  rights:'Google Cloud images are brief attributed product screenshots used for reporting; Pexels footage is used under the Pexels licence and persistently labelled as contextual, not Gemini output.',
  hashes, scenes
};
fs.writeFileSync(path.join(root, 'video/cycles/2026-09-26/r1_manifest.json'), JSON.stringify(manifest, null, 2)+'\n');
console.log('Prepared R1 overlays and seven-scene manifest; no render.');
