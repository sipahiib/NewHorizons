import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {createRequire} from 'node:module';
const sharp = createRequire(import.meta.url)('../../../.tools-node/node_modules/sharp');

const root = path.resolve(import.meta.dirname, '../../..');
const source = 'assets/motion/2026-09-26/reels/r2/nisar-observations.mp4';
const work = 'build/reels/2026-09-26/work';
fs.mkdirSync(path.join(root,work),{recursive:true});
const run=(args)=>{const r=spawnSync('ffmpeg',args,{encoding:'utf8'}); if(r.status!==0)throw Error(r.stderr);};
const hashes={};
for (const [name,seek] of [['early',5],['middle',9],['late',16.66]]) {
 const file=`assets/motion/2026-09-26/reels/r2/${name}.png`;
 run(['-nostdin','-y','-v','error','-ss',String(seek),'-i',path.join(root,source),'-frames:v','1',path.join(root,file)]);
 hashes[file]=createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex');
}
hashes[source]=createHash('sha256').update(fs.readFileSync(path.join(root,source))).digest('hex');
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
<rect x="54" y="185" width="972" height="300" rx="28" fill="#071a22" fill-opacity=".94"/>
<text x="94" y="253" fill="#66dec8" font-family="Arial" font-size="30" letter-spacing="4">THE PLANET EARTH</text>
<text x="94" y="333" fill="white" font-family="Arial" font-size="57" font-weight="bold">A VOLCANO,</text>
<text x="94" y="403" fill="white" font-family="Arial" font-size="57" font-weight="bold">WATCHED BY RADAR</text>
<rect x="54" y="1350" width="972" height="315" rx="28" fill="#071a22" fill-opacity=".94"/>
<text x="94" y="1415" fill="white" font-family="Arial" font-size="35">NISAR radar observations</text>
<text x="94" y="1468" fill="#c6dce1" font-family="Arial" font-size="29">Dec 2025–Aug 2026 • NASA SVS</text>
<text x="94" y="1521" fill="#c6dce1" font-family="Arial" font-size="29">Processed data • not live optical video</text>
<text x="94" y="1589" fill="#66dec8" font-family="Arial" font-size="32">YouTube @newhorizons_21</text>
<text x="94" y="1634" fill="white" font-family="Arial" font-size="30">Instagram • Like &amp; Follow</text>
</svg>`;
await sharp(Buffer.from(svg)).png().toFile(path.join(root,work,'r2-overlay.png'));
const recap=`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><rect x="270" y="535" width="540" height="64" rx="20" fill="#071a22" fill-opacity=".9"/><text x="540" y="578" text-anchor="middle" fill="white" font-family="Arial" font-size="30">Full sequence recap</text></svg>`;
await sharp(Buffer.from(recap)).png().toFile(path.join(root,work,'r2-recap.png'));
const scenes=[
 {kind:'still',file:'assets/motion/2026-09-26/reels/r2/early.png',duration:6},
 {kind:'motion',file:source,seek:5,duration:4},
 {kind:'still',file:'assets/motion/2026-09-26/reels/r2/middle.png',duration:6},
 {kind:'motion',file:source,seek:9,duration:4},
 {kind:'motion',file:source,seek:12,duration:4},
 {kind:'still',file:'assets/motion/2026-09-26/reels/r2/late.png',duration:6},
 {kind:'motion',file:source,seek:0,duration:17,tailFreeze:0.3,recap:true}
];
const manifest={cycle:'2026-09-26',status:'prepared-for-review',output:'build/reels/2026-09-26/02-planet-earth.mp4',
 audio:'build/video/2026-09-26/audio/r2.mp3',overlay:`${work}/r2-overlay.png`,recapOverlay:`${work}/r2-recap.png`,
 duration:47,fps:60,width:1080,height:1920,sourcePage:'https://svs.gsfc.nasa.gov/5675',
 download:'https://svs.gsfc.nasa.gov/vis/a000000/a005600/a005675/nisar_volcano_annotated.mp4',
 rights:'NASA-created observed-data visualisation; NASA media guidelines; credit NASA Scientific Visualization Studio. No third-party restriction identified on item page.',
 sourceDuration:16.7,sourceResolution:[3840,2160],sourceFps:30,hashes,scenes};
fs.writeFileSync(path.join(root,'video/cycles/2026-09-26/r2_manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log('Prepared R2 sources, overlays and seven-scene manifest; no render.');
