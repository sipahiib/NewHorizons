import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {createRequire} from 'node:module';
const sharp = createRequire(import.meta.url)('../../../.tools-node/node_modules/sharp');

const root = path.resolve(import.meta.dirname, '../../..');
const work = 'build/video/2026-09-26/work';
fs.mkdirSync(path.join(root, work), {recursive:true});
const run = args => { const r=spawnSync('ffmpeg', args, {encoding:'utf8'}); if(r.status!==0) throw Error(r.stderr); };

for (const [name, seek] of [['thermal-pre',0.0],['thermal-post',1.0]]) {
  run(['-nostdin','-y','-v','error','-ss',String(seek),'-i',path.join(root,'assets/motion/2026-09-26/main/m1/thermal-blink.gif'),'-frames:v','1',path.join(root,`assets/motion/2026-09-26/main/m1/${name}.png`)]);
}

const stories = {
  m1:{title:'A NEW CRATER CHANGED THE MOON', source:'McGetchin crater • NASA LRO / UCLA', note:'Thermal measurements • not impact footage'},
  m2:{title:'META WANTS MUSE IN AI GLASSES', source:'Meta Connect announcement and demo', note:'Company material • availability varies'},
  m3:{title:'HAFNIA SHOWS ANTIFERROELECTRIC ORDER', source:'University of Nebraska / Science', note:'Research result • applications remain prospective'},
  m4:{title:'EVOLUTION REWIRED HUMAN CARTILAGE', source:'Nature paper • CC BY 4.0', note:'Cell and tissue research • not a treatment study'},
  m5:{title:'A CONTROLLED FAULT TEST IN THE ALPS', source:'BedrettoLab FEAR 3 report', note:'Early experiment report • not earthquake prediction'}
};
for (const [id,s] of Object.entries(stories)) {
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
  <rect x="74" y="62" width="1180" height="170" rx="26" fill="#071a22" fill-opacity=".92"/>
  <text x="112" y="122" fill="#66dec8" font-family="Arial" font-size="27" letter-spacing="4">NEW HORIZONS • ${id.toUpperCase()}</text>
  <text x="112" y="190" fill="white" font-family="Arial" font-size="48" font-weight="bold">${s.title}</text>
  <rect x="74" y="914" width="1180" height="116" rx="24" fill="#071a22" fill-opacity=".92"/>
  <text x="112" y="963" fill="white" font-family="Arial" font-size="29">${s.source}</text>
  <text x="112" y="1004" fill="#c6dce1" font-family="Arial" font-size="25">${s.note}</text>
  </svg>`;
  await sharp(Buffer.from(svg)).png().toFile(path.join(root,work,`${id}-overlay.png`));
}
const contextual=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect x="1370" y="62" width="476" height="58" rx="18" fill="#071a22" fill-opacity=".93"/><text x="1608" y="101" text-anchor="middle" fill="white" font-family="Arial" font-size="24">CONTEXT FOOTAGE</text></svg>`;
await sharp(Buffer.from(contextual)).png().toFile(path.join(root,work,'context-overlay.png'));
const historical=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect x="1310" y="62" width="536" height="58" rx="18" fill="#071a22" fill-opacity=".93"/><text x="1578" y="101" text-anchor="middle" fill="white" font-family="Arial" font-size="24">HISTORICAL LRO CONTEXT</text></svg>`;
const siteContext=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect x="1260" y="62" width="586" height="58" rx="18" fill="#071a22" fill-opacity=".93"/><text x="1553" y="101" text-anchor="middle" fill="white" font-family="Arial" font-size="24">BEDRETTO SITE CONTEXT • 2010/2019</text></svg>`;
const teaserOverlay=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect x="74" y="62" width="1080" height="116" rx="24" fill="#071a22" fill-opacity=".92"/><text x="112" y="134" fill="white" font-family="Arial" font-size="44" font-weight="bold">AND FOUR OTHER BREAKTHROUGHS...</text></svg>`;
await sharp(Buffer.from(historical)).png().toFile(path.join(root,work,'historical-overlay.png'));
await sharp(Buffer.from(siteContext)).png().toFile(path.join(root,work,'site-context-overlay.png'));
await sharp(Buffer.from(teaserOverlay)).png().toFile(path.join(root,work,'teaser-overlay.png'));
const closing=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#041820"/><stop offset=".55" stop-color="#0a3441"/><stop offset="1" stop-color="#0d5663"/></linearGradient></defs>
<rect width="1920" height="1080" fill="url(#g)"/><circle cx="300" cy="180" r="240" fill="#43d7c4" fill-opacity=".12"/><circle cx="1620" cy="900" r="320" fill="#66a8ff" fill-opacity=".11"/>
<rect x="390" y="275" width="1140" height="530" rx="48" fill="white" fill-opacity=".10" stroke="white" stroke-opacity=".20" stroke-width="3"/>
<text x="960" y="465" text-anchor="middle" fill="white" font-family="Arial" font-size="72" font-weight="bold">LIKE • SUBSCRIBE</text>
<text x="960" y="565" text-anchor="middle" fill="#9df0e2" font-family="Arial" font-size="42">More discoveries, clearly explained.</text>
<rect x="690" y="630" width="540" height="84" rx="42" fill="#ff5a67"/><text x="960" y="687" text-anchor="middle" fill="white" font-family="Arial" font-size="34" font-weight="bold">SUBSCRIBE</text>
</svg>`;
const bell=`<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180"><path d="M90 24c-28 0-46 22-46 54v31l-15 22h122l-15-22V78c0-32-18-54-46-54Z" fill="#ffe36b"/><circle cx="90" cy="145" r="15" fill="#ffe36b"/></svg>`;
await sharp(Buffer.from(closing)).png().toFile(path.join(root,work,'closing.png'));
await sharp(Buffer.from(bell)).png().toFile(path.join(root,work,'closing-bell.png'));

const teaserSpecs=[
  ['AI glasses','assets/motion/2026-09-26/main/m2/meta-muse-glasses.mp4',8,false],
  ['Hafnia','assets/motion/2026-09-26/main/m3/hafnia-scan.mp4',1,false],
  ['Cartilage biology • context','assets/motion/2026-09-26/main/m4/lab-scientists.mp4',1,false],
  ['Fault experiment • context','assets/motion/2026-09-26/main/m5/tunnel-machinery.mp4',1,false]
];
const teaserSegments=[];
for (let i=0;i<teaserSpecs.length;i++) {
  const [label,file,seek]=teaserSpecs[i];
  const labelSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect x="630" y="850" width="660" height="92" rx="24" fill="#071a22" fill-opacity=".94"/><text x="960" y="910" text-anchor="middle" fill="white" font-family="Arial" font-size="38" font-weight="bold">${label}</text></svg>`;
  const labelFile=path.join(root,work,`teaser-${i+1}.png`);
  const segment=path.join(root,work,`teaser-${i+1}.mp4`);
  await sharp(Buffer.from(labelSvg)).png().toFile(labelFile);
  run(['-nostdin','-y','-v','error','-ss',String(seek),'-i',path.join(root,file),'-loop','1','-framerate','60','-i',labelFile,'-filter_complex','[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,fps=60[base];[base][1:v]overlay=0:0:shortest=1[v]','-map','[v]','-t','2','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60',segment]);
  teaserSegments.push(segment);
}
const teaserList=path.join(root,work,'teaser-concat.txt');
fs.writeFileSync(teaserList,teaserSegments.map(p=>`file '${p}'`).join('\n')+'\n');
run(['-nostdin','-y','-v','error','-f','concat','-safe','0','-i',teaserList,'-c','copy',path.join(root,work,'opening-teaser.mp4')]);

const M='assets/motion/2026-09-26/main';
const sections=[
 {id:'m1',duration:120,audio:'build/video/2026-09-26/audio/m1.mp3',scenes:[
  {kind:'still',file:`${M}/m1/crater-close.jpg`,duration:5},{kind:'motion',file:`${M}/m1/lro-launch.mp4`,seek:145,duration:7,label:'historical'},
  {kind:'motion',file:`${work}/opening-teaser.mp4`,duration:8,teaser:true},{kind:'still',file:`${M}/m1/thermal-pre.png`,duration:25},
  {kind:'motion',file:`${M}/m1/lro-assembly.webm`,seek:20,duration:25,label:'historical'},{kind:'still',file:`${M}/m1/thermal-post.png`,duration:25},
  {kind:'motion',file:`${M}/m1/lro-launch.mp4`,seek:205,duration:25,label:'historical'}
 ]},
 {id:'m2',duration:60,audio:'build/video/2026-09-26/audio/m2.mp3',scenes:[
  {kind:'still',file:`${M}/m2/meta-muse-glasses.jpg`,duration:12},{kind:'motion',file:`${M}/m2/meta-muse-glasses.mp4`,seek:0,duration:12},
  {kind:'still',file:`${M}/m2/meta-glasses-screen.jpg`,duration:12},{kind:'motion',file:`${M}/m2/meta-muse-glasses.mp4`,seek:18,duration:12},
  {kind:'motion',file:`${M}/m2/meta-muse-glasses.mp4`,seek:36,duration:12}
 ]},
 {id:'m3',duration:60,audio:'build/video/2026-09-26/audio/m3.mp3',scenes:[
  {kind:'still',file:`${M}/m3/hafnia-atom-map.png`,duration:12},{kind:'motion',file:`${M}/m3/hafnia-scan.mp4`,duration:12,loop:true},
  {kind:'still',file:`${M}/m3/hafnia-field-diagram.png`,duration:12},{kind:'motion',file:`${M}/m3/microscope.mp4`,seek:2,duration:12,context:true},
  {kind:'motion',file:`${M}/m3/electrical-testing.mp4`,seek:8,duration:12,context:true}
 ]},
 {id:'m4',duration:60,audio:'build/video/2026-09-26/audio/m4.mp3',scenes:[
  {kind:'still',file:`${M}/m4/nature-fig1.png`,duration:12},{kind:'motion',file:`${M}/m4/lab-scientists.mp4`,seek:1,duration:12,context:true},
  {kind:'still',file:`${M}/m4/nature-fig4.png`,duration:12},{kind:'motion',file:`${M}/m4/lab-working.mp4`,seek:1,duration:12,context:true},
  {kind:'motion',file:`${M}/m4/lab-microscope.mp4`,seek:5,duration:12,context:true}
 ]},
 {id:'m5',duration:60,audio:'build/video/2026-09-26/audio/m5.mp3',scenes:[
  {kind:'still',file:`${M}/m5/bedretto-entrance.jpg`,duration:15,label:'site'},{kind:'motion',file:`${M}/m5/tunnel-machinery.mp4`,seek:1,duration:10,context:true},
  {kind:'still',file:`${M}/m5/bedretto-interior.jpg`,duration:15,label:'site'},{kind:'motion',file:`${M}/m5/tunnel-workers.mp4`,duration:10,loop:true,context:true},
  {kind:'motion',file:`${M}/m5/tunnel-walkway.mp4`,seek:4,duration:10,loop:true,context:true}
 ]},
 {id:'closing',duration:10,audio:'build/video/2026-09-26/audio/closing.mp3',closing:true}
];
const inputs=[...new Set(sections.flatMap(s=>s.scenes?.map(x=>x.file)||[]))];
const hashes=Object.fromEntries(inputs.map(file=>[file,createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')]));
const manifest={cycle:'2026-09-26',status:'prepared-for-review',candidateOutput:'build/video/2026-09-26/newhorizons.mp4',finalOutput:'build/video/newhorizons.mp4',duration:370,fps:60,width:1920,height:1080,titleDisplaySeconds:4,sections,hashes,
 overlays:Object.fromEntries(Object.keys(stories).map(id=>[id,`${work}/${id}-overlay.png`])),contextOverlay:`${work}/context-overlay.png`,historicalOverlay:`${work}/historical-overlay.png`,siteContextOverlay:`${work}/site-context-overlay.png`,teaserOverlay:`${work}/teaser-overlay.png`,closing:`${work}/closing.png`,closingBell:`${work}/closing-bell.png`};
fs.writeFileSync(path.join(root,'video/cycles/2026-09-26/main_manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log('Prepared main overlays, derived stills and 370-second manifest; no render.');
