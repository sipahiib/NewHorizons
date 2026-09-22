import path from 'node:path';
import fs from 'node:fs/promises';
import {createRequire} from 'node:module';

const legacyFlag = '--legacy-2026-09-10';
if (!process.argv.includes(legacyFlag)) {
  throw new Error(`Historical cover generator; current policy forbids covers. Pass ${legacyFlag} only to reproduce the archived cycle.`);
}

const require = createRequire(import.meta.url);
const sharp = require('../.tools-node/node_modules/sharp');
const root = path.resolve(import.meta.dirname, '..');
const coverDir = path.join(root, 'assets/covers/2026-09-10');

const covers = [
  {
    background: 'generated/01-sports-biomechanics-background.png',
    output: '01-sports-biomechanics.png',
    title: 'FATIGUE — OR SPEED?',
  },
  {
    background: 'generated/02-planet-earth-background.png',
    output: '02-planet-earth.png',
    title: "EARTH'S LIGHT BALANCE",
  },
];

await fs.mkdir(coverDir, {recursive: true});
for (const cover of covers) {
  const title = cover.title.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
  const overlay = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
    <rect x="90" y="150" width="900" height="142" rx="24" fill="#06131f" fill-opacity="0.86" stroke="#5adbd1" stroke-opacity="0.72" stroke-width="3"/>
    <rect x="90" y="150" width="12" height="142" rx="6" fill="#30d5c8"/>
    <text x="540" y="239" text-anchor="middle" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="56" font-weight="700" letter-spacing="1">${title}</text>
  </svg>`);
  await sharp(path.join(coverDir, cover.background))
    .resize(1080, 1920, {fit: 'cover', position: 'centre'})
    .composite([{input: overlay, top: 0, left: 0}])
    .png({compressionLevel: 9})
    .toFile(path.join(coverDir, cover.output));
  console.log(path.join('assets/covers/2026-09-10', cover.output));
}
