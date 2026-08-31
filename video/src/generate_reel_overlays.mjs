import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const sharp = require('../../.tools-node/node_modules/sharp');
const root = path.resolve('.');
const out = path.join(root, 'build/reels/overlays');
fs.mkdirSync(out, { recursive: true });

const esc = (s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const titles = [
  'ONE SENSOR, TWO READINGS',
  'PANDORA CLEANS THE SIGNAL',
  'POSITRONS FOR THE FCC',
  'THE DOUBLE-HIGGS SEARCH',
  'AI, 6G AND SMART FACTORIES',
];

for (const [i, title] of titles.entries()) {
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
    <rect x="50" y="80" width="980" height="190" rx="24" fill="#06131f" fill-opacity=".80"/>
    <rect x="50" y="80" width="12" height="190" rx="6" fill="#30d5c8"/>
    <text x="540" y="196" text-anchor="middle" fill="white" font-family="Arial" font-size="52" font-weight="700">${esc(title)}</text>
  </svg>`);
  await sharp(svg).webp({ lossless: true }).toFile(path.join(out, `title${i + 1}.webp`));
}

const cta = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect x="90" y="1400" width="900" height="330" rx="38" fill="#06131f" fill-opacity=".90" stroke="#8bdcf0" stroke-opacity=".35" stroke-width="3"/>
  <text x="540" y="1490" text-anchor="middle" fill="white" font-family="Arial" font-size="48" font-weight="700">LIKE  •  FOLLOW</text>
  <rect x="170" y="1515" width="740" height="100" rx="24" fill="#e82949"/>
  <text x="540" y="1580" text-anchor="middle" fill="white" font-family="Arial" font-size="37" font-weight="800">YOUTUBE  @newhorizons_21</text>
  <text x="540" y="1685" text-anchor="middle" fill="#c6dde1" font-family="Arial" font-size="30" font-weight="700">FOLLOW ON INSTAGRAM</text>
</svg>`);
await sharp(cta).webp({ lossless: true }).toFile(path.join(out, 'cta.webp'));
