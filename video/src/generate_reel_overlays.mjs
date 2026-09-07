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
  'AFTER SURGERY, WHO DOES THE WORK?',
  'ONE FOLD. A SLOWER FALL?',
  'CAN AI LEARN ANCIENT BUILDING RULES?',
];

for (const [i, title] of titles.entries()) {
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
    <rect x="50" y="80" width="980" height="190" rx="24" fill="#06131f" fill-opacity=".80"/>
    <rect x="50" y="80" width="12" height="190" rx="6" fill="#30d5c8"/>
    <text x="540" y="196" text-anchor="middle" fill="white" font-family="Arial" font-size="${title.length > 30 ? 42 : 50}" font-weight="700">${esc(title)}</text>
  </svg>`);
  await sharp(svg).webp({ lossless: true }).toFile(path.join(out, `title${i + 1}.webp`));
}

const cta = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
  <rect x="90" y="1370" width="900" height="360" rx="38" fill="#06131f" fill-opacity=".91" stroke="#8bdcf0" stroke-opacity=".40" stroke-width="3"/>
  <text x="540" y="1465" text-anchor="middle" fill="white" font-family="Arial" font-size="48" font-weight="700">LIKE  •  FOLLOW</text>
  <rect x="170" y="1500" width="740" height="100" rx="24" fill="#e82949"/>
  <text x="540" y="1566" text-anchor="middle" fill="white" font-family="Arial" font-size="36" font-weight="800">YOUTUBE  @newhorizons_21</text>
  <text x="540" y="1675" text-anchor="middle" fill="#c6dde1" font-family="Arial" font-size="31" font-weight="700">FOLLOW ON INSTAGRAM</text>
</svg>`);
await sharp(cta).webp({ lossless: true }).toFile(path.join(out, 'cta.webp'));

for (const [name, text] of Object.entries({
  stock: 'Illustrative stock footage',
  sports: 'Illustrative stock — not study participants',
  athens: 'Athens / Acropolis — illustrative stock',
})) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><rect x="40" y="285" width="1000" height="55" rx="10" fill="#06131f" fill-opacity=".84"/><text x="540" y="322" text-anchor="middle" font-family="Arial" font-size="28" fill="white">${text}</text></svg>`;
  await sharp(Buffer.from(svg)).webp({lossless:true}).toFile(path.join(out, `${name}.webp`));
}
