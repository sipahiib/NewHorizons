import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const sharp = require('../../.tools-node/node_modules/sharp');
const root = path.resolve('.');
const lang = process.env.VIDEO_LANG === 'en' ? 'en' : 'tr';
const editorialBuild = process.env.EDITORIAL_BUILD
  ? path.resolve(process.env.EDITORIAL_BUILD)
  : path.join(root, 'build/video/editorial');
const out = path.join(editorialBuild, 'title-overlays');
fs.mkdirSync(out, { recursive: true });

const cueSets = { tr: [
  { start: 6.40, end: 11.50, type: 'chapter', title: 'TEK SENSÖR, İKİ HAYATİ ÖLÇÜM', kicker: 'GLİKOZ VE KETON TAKİBİ AYNI SİSTEMDE' },
  { start: 25.00, end: 31.00, type: 'key', title: 'İKİ DEĞER DE DAKİKADA BİR ÖLÇÜLÜYOR' },
  { start: 66.40, end: 71.50, type: 'chapter', title: 'PANDORA GÖZLEMLERE BAŞLADI', kicker: 'ÖTEGEZEGEN ATMOSFERLERİNDEKİ BELİRSİZLİĞİ AZALTACAK' },
  { start: 93.00, end: 100.00, type: 'key', title: 'YILDIZIN ETKİSİ, GEZEGENİN ATMOSFER SİNYALİNDEN AYRILACAK' },
  { start: 120.40, end: 125.50, type: 'chapter', title: '6G VE AKILLI ÜRETİM', kicker: 'YAPAY ZEKÂ, ROBOTLAR VE DÜŞÜK GECİKMELİ BAĞLANTI' },
  { start: 145.00, end: 152.00, type: 'key', title: 'HEDEF: YAKLAŞIK 200 TEMEL YAPAY ZEKÂ STANDARDI' },
  { start: 178.00, end: 188.00, type: 'cta', title: 'BİLİM VE TEKNOLOJİ GÜNDEMİNİ KAÇIRMAYIN' },
], en: [
  { start: 0.15, end: 4.80, type: 'key', title: 'THIS WEEK: AI OPENED THE BLACK BOX' },
  { start: 5.10, end: 11.80, type: 'chapter', title: 'WHY DID THE CAR DO THAT?', kicker: 'CW-NET EXPLAINS THE DECISION IN REAL TIME' },
  { start: 12.20, end: 19.70, type: 'key', title: 'FOUR MORE BREAKTHROUGHS ARE COMING — FIRST, THE BIGGEST ONE' },
  { start: 50.00, end: 57.00, type: 'key', title: 'HUMAN-READABLE CONCEPTS DIRECTLY SHAPE THE PLANNER' },
  { start: 92.00, end: 99.00, type: 'key', title: 'BETTER EXPLANATIONS HELP PEOPLE ANTICIPATE SURPRISES' },
  { start: 120.20, end: 126.20, type: 'chapter', title: 'TINY TISSUES, COMPLEX STRUCTURE', kicker: 'MUSCLE, NERVES AND VESSEL-LIKE CELLS GROW TOGETHER' },
  { start: 149.00, end: 156.00, type: 'key', title: 'AN EARLY RESEARCH PLATFORM — NOT A COMMERCIAL STEAK' },
  { start: 165.20, end: 171.20, type: 'chapter', title: 'FORECASTS FROM ORBIT', kicker: 'AMSR3 MAPS WATER VAPOUR, CLOUDS, RAIN AND SNOW' },
  { start: 192.00, end: 199.00, type: 'key', title: 'BETTER STARTING DATA CAN PRODUCE BETTER RAIN FORECASTS' },
  { start: 210.20, end: 216.20, type: 'chapter', title: 'IMMUNE CELLS CLEAR LIVER SCARS', kicker: 'REM2 MACROPHAGES PHYSICALLY ENGULF SCAR MATERIAL' },
  { start: 237.00, end: 244.00, type: 'key', title: 'A POSSIBLE PATHWAY — NOT YET A HUMAN TREATMENT' },
  { start: 255.20, end: 261.20, type: 'chapter', title: 'DO BRAIN WAVES ORGANISE THOUGHT?', kicker: 'A NEW ANALOGUE-COMPUTING THEORY OF COGNITION' },
  { start: 280.00, end: 287.00, type: 'key', title: 'A TESTABLE THEORY, NOT A SETTLED ANSWER TO CONSCIOUSNESS' },
  { start: 300.00, end: 310.00, type: 'cta', title: 'LIKE, SUBSCRIBE AND STAY CURIOUS' },
] };
const cues = cueSets[lang];
const ctaLabels = lang === 'en'
  ? { like: 'LIKE', subscribe: 'SUBSCRIBE', notification: 'NOTIFICATIONS', notificationSize: 14 }
  : { like: 'BEĞEN', subscribe: 'ABONE OL', notification: 'BİLDİRİM', notificationSize: 19 };

const esc = (value) => value
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;');

const chapterSvg = ({ title, kicker }) => Buffer.from(`
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
  <rect x="70" y="825" width="1510" height="178" rx="20" fill="#08131c" fill-opacity="0.76"/>
  <rect x="70" y="825" width="12" height="178" rx="6" fill="#30d5c8"/>
  <text x="116" y="922" fill="white" font-family="Arial, sans-serif" font-size="65" font-weight="700">${esc(title)}</text>
  ${kicker ? `<text x="118" y="972" fill="#c6dde1" font-family="Arial, sans-serif" font-size="28" font-weight="600" letter-spacing="2">${esc(kicker)}</text>` : ''}
</svg>`);

const keySvg = ({ title }) => {
  const size = title.length > 65 ? 36 : title.length > 52 ? 40 : 47;
  return Buffer.from(`
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
  <rect x="120" y="870" width="1680" height="122" rx="18" fill="#08131c" fill-opacity="0.72"/>
  <text x="960" y="948" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="${size}" font-weight="700">${esc(title)}</text>
</svg>`);
};

const ctaSvg = ({ title }) => Buffer.from(`
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
  <rect x="0" y="600" width="1920" height="480" fill="#020810" fill-opacity="0.58"/>
  <text x="960" y="735" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="48" font-weight="700" letter-spacing="1">${esc(title)}</text>
  <rect x="385" y="790" width="1150" height="178" rx="36" fill="#071521" fill-opacity="0.92" stroke="#8BDCF0" stroke-opacity="0.34" stroke-width="2"/>
  <rect x="386" y="791" width="1148" height="2" rx="1" fill="white" fill-opacity="0.18"/>
  <rect x="433" y="817" width="126" height="126" rx="28" fill="#66B8E0" fill-opacity="0.14"/>
  <text x="496" y="930" text-anchor="middle" fill="#DDF8FF" font-family="Arial, sans-serif" font-size="21" font-weight="700">${ctaLabels.like}</text>
  <rect x="617" y="817" width="604" height="126" rx="28" fill="#E82949"/>
  <text x="919" y="896" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="42" font-weight="800" letter-spacing="1">${ctaLabels.subscribe}</text>
  <rect x="1279" y="817" width="126" height="126" rx="28" fill="#66B8E0" fill-opacity="0.14"/>
  <text x="1342" y="930" text-anchor="middle" fill="#DDF8FF" font-family="Arial, sans-serif" font-size="${ctaLabels.notificationSize}" font-weight="700">${ctaLabels.notification}</text>
</svg>`);

const thumbSvg = Buffer.from(`
<svg xmlns="http://www.w3.org/2000/svg" width="92" height="92" viewBox="0 0 92 92">
  <path d="M36 74H22c-5 0-8-3-8-8V42c0-5 3-8 8-8h14v40Zm8 0V35L56 12c3-6 12-4 12 3v15h8c8 0 13 8 11 15l-7 23c-1 4-6 7-11 7H44Z" fill="#E7FAFF"/>
</svg>`);

const bellSvg = Buffer.from(`
<svg xmlns="http://www.w3.org/2000/svg" width="92" height="92" viewBox="0 0 92 92">
  <path d="M67 36c0-14-9-24-21-24S25 22 25 36c0 21-8 25-13 31h68c-5-6-13-10-13-31ZM37 73h18c-1 6-4 9-9 9s-8-3-9-9Z" fill="#E7FAFF"/>
</svg>`);

const glowSvg = Buffer.from(`
<svg xmlns="http://www.w3.org/2000/svg" width="604" height="126">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="white" stop-opacity="0"/><stop offset="0.5" stop-color="white" stop-opacity="0.38"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient></defs>
  <rect x="2" y="2" width="600" height="122" rx="27" fill="none" stroke="url(#g)" stroke-width="5"/>
</svg>`);

const rows = [];
for (const [index, cue] of cues.entries()) {
  const file = path.join(out, `title${String(index + 1).padStart(2, '0')}.webp`);
  const svg = cue.type === 'chapter' ? chapterSvg(cue) : cue.type === 'cta' ? ctaSvg(cue) : keySvg(cue);
  await sharp(svg).webp({ lossless: true }).toFile(file);
  if (cue.type === 'cta') {
    await sharp(thumbSvg).webp({ lossless: true }).toFile(path.join(out, 'cta-thumb.webp'));
    await sharp(bellSvg).webp({ lossless: true }).toFile(path.join(out, 'cta-bell.webp'));
    await sharp(glowSvg).webp({ lossless: true }).toFile(path.join(out, 'cta-glow.webp'));
  }
  rows.push(`${cue.start.toFixed(2)}|${cue.end.toFixed(2)}|${file}|${cue.type === 'cta' ? 'glass_cta' : 'standard'}`);
}

fs.writeFileSync(path.join(out, 'manifest.tsv'), `${rows.join('\n')}\n`);
console.log(`Generated ${cues.length} sparse title overlays in ${out}`);
