import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const sharp = require('../../.tools-node/node_modules/sharp');
const out = path.resolve(process.env.EDITORIAL_BUILD || 'build/video/editorial-en', 'disclosures');
fs.mkdirSync(out, { recursive: true });
const labels = {
  generic: 'Contextual real footage',
  m1: 'Contextual radio telescope — not FAST',
  m2: 'Contextual laboratory footage — not the GPN-Star study',
  m3: 'Contextual medical footage — not the reported patient or team',
  m4: 'Contextual electronics footage — not Samsung, ASML or High-NA EUV',
  m5: 'Contextual weather footage — not Sentinel-6 observations',
};
for (const [id, text] of Object.entries(labels)) {
  const width = text.length * 13 + 36;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect x="${1880-width}" y="30" width="${width}" height="50" rx="8" fill="#071521" fill-opacity=".85"/><text x="1862" y="63" text-anchor="end" font-family="Arial" font-size="23" fill="white">${text}</text></svg>`;
  await sharp(Buffer.from(svg)).webp({ lossless: true }).toFile(path.join(out, `${id}.webp`));
}
