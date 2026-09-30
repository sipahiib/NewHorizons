import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {createRequire} from 'node:module';

const sharp = createRequire(import.meta.url)('../../../.tools-node/node_modules/sharp');
const root = path.resolve(import.meta.dirname, '../../..');
const cycle = '2026-09-30';
const base = `assets/motion/${cycle}/reels`;
const work = `build/reels/${cycle}/work`;
fs.mkdirSync(path.join(root, work), {recursive: true});

const configs = {
  r1: {
    title: ['WHO GETS HEARD', 'IN AI RESEARCH?'],
    files: ['source-card-1.png', 'talking-laptop.mp4', 'source-card-2.png',
      'video-call-notes.mp4', 'source-card-3.png', 'video-call.mp4', 'man-video-interview.mp4'],
    output: '01-future-of-ai.mp4',
  },
  r2: {
    title: ['A PLAN FOR LESS', 'MEDITERRANEAN WATER'],
    files: ['source-card-1.png', 'greek-coast.mp4', 'source-card-2.png',
      'dry-reservoir.mp4', 'source-card-3.png', 'vineyard-irrigation.mp4', 'water-tap.mp4'],
    output: '02-the-planet-earth.mp4',
  },
};

for (const [id, config] of Object.entries(configs)) {
  // The top title panel's fill opacity changes from .94 to .64.
  // The former series line and entire lower information card are absent.
  const titleSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
    <rect x="50" y="155" width="980" height="270" rx="30" fill="#061b23" fill-opacity=".64"/>
    <text x="90" y="285" fill="white" font-family="Arial" font-size="53" font-weight="bold">${config.title[0]}</text>
    <text x="90" y="360" fill="white" font-family="Arial" font-size="53" font-weight="bold">${config.title[1]}</text>
  </svg>`;
  await sharp(Buffer.from(titleSvg)).png().toFile(path.join(root, work, `${id}-overlay.png`));

  const contextSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
    <rect x="160" y="540" width="760" height="65" rx="18" fill="#061b23" fill-opacity=".9"/>
    <text x="540" y="582" text-anchor="middle" fill="white" font-family="Arial" font-size="28">CONTEXT • NOT EVENT FOOTAGE</text>
  </svg>`;
  await sharp(Buffer.from(contextSvg)).png().toFile(path.join(root, work, `${id}-context.png`));

  // Keep the required calls to action as unboxed text in the final three seconds.
  const ctaSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
    <text x="540" y="1585" text-anchor="middle" fill="white" stroke="#061b23" stroke-width="5" paint-order="stroke" font-family="Arial" font-size="37" font-weight="bold">YouTube @newhorizons_21</text>
    <text x="540" y="1645" text-anchor="middle" fill="white" stroke="#061b23" stroke-width="5" paint-order="stroke" font-family="Arial" font-size="35" font-weight="bold">Instagram • Like &amp; Follow</text>
  </svg>`;
  await sharp(Buffer.from(ctaSvg)).png().toFile(path.join(root, work, `${id}-cta.png`));

  const scenes = config.files.map((file, index) => ({
    kind: file.endsWith('.mp4') ? 'motion' : 'still',
    file: `${base}/${id}/${file}`,
    duration: index === 6 ? 9 : 6,
    label: 'context',
    loop: true,
  }));
  const hashes = Object.fromEntries([...new Set(scenes.map(scene => scene.file))].map(file => [
    file, createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'),
  ]));
  const manifest = {
    cycle, status: 'prepared-for-review', output: `build/reels/${cycle}/${config.output}`,
    audio: `build/video/${cycle}/audio/${id}.mp3`, overlay: `${work}/${id}-overlay.png`,
    contextOverlay: `${work}/${id}-context.png`, ctaOverlay: `${work}/${id}-cta.png`,
    ctaStartInFinalScene: 6, duration: 45, fps: 60, width: 1080, height: 1920,
    scenes, hashes,
  };
  fs.writeFileSync(path.join(root, `video/cycles/${cycle}/${id}_manifest.json`),
    JSON.stringify(manifest, null, 2) + '\n');
}
console.log('Prepared revised Reel overlays and manifests.');
