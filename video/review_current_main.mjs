import fs from 'node:fs/promises';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createRequire} from 'node:module';

const run = promisify(execFile);
const require = createRequire(import.meta.url);
const sharp = require('../.tools-node/node_modules/sharp');
const root = path.resolve(import.meta.dirname, '..');
const manifest = await fs.readFile(path.join(root,'video/editorial_scenes.tsv'),'utf8');
const scenes = manifest.split('\n').filter((line) => line && !line.startsWith('#')).map((line) => {
  const [kind,relative,duration,seek,layout] = line.split('|');
  return {kind,relative,duration:Number(duration),seek:Number(seek),layout};
});
const selected = scenes;
if (selected.length !== 29) throw new Error(`Expected 29 scenes including closing, found ${selected.length}`);
const visualReview = process.env.VISUAL_REVIEW === 'pass'
  ? 'pass — midpoint contact sheet and source timeline visually inspected; real footage and contextual correspondence confirmed'
  : 'pending';
const out = path.join(root,'build/video/current-main-preflight');
await fs.mkdir(out,{recursive:true});
const tiles=[];
const checks=[];
for (const [index,scene] of selected.entries()) {
  const input=path.join(root,scene.relative);
  let sourceDuration, width, height, sampleAt, frame;
  if (scene.kind === 'still') {
    const metadata = await sharp(input).metadata();
    width = metadata.width; height = metadata.height; sourceDuration = null; sampleAt = null;
    frame = await sharp(input).resize(320,180,{fit:'contain',background:'black'}).png().toBuffer();
  } else {
    const {stdout:probeText}=await run('ffprobe',['-v','error','-show_streams','-show_format','-of','json',input]);
    const probe=JSON.parse(probeText),video=probe.streams.find((stream)=>stream.codec_type==='video');
    sourceDuration=Number(probe.format.duration);
    if (!video || scene.seek+scene.duration>sourceDuration+0.02) throw new Error(`Scene exceeds source: ${scene.relative}`);
    width=video.width; height=video.height; sampleAt=scene.seek+scene.duration/2;
    ({stdout:frame}=await run('ffmpeg',['-nostdin','-v','error','-ss',String(sampleAt),'-i',input,'-frames:v','1','-vf','scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2:black','-f','image2pipe','-vcodec','png','pipe:1'],{encoding:'buffer',maxBuffer:8*1024*1024}));
  }
  const column=index%8,row=Math.floor(index/8);
  tiles.push({input:frame,left:column*320,top:row*210});
  let id;
  if (index < 8) id = `M1-${String(index + 1).padStart(2,'0')}`;
  else if (index < 28) {
    const supportIndex = index - 8;
    id = `M${Math.floor(supportIndex / 5) + 2}-${String((supportIndex % 5) + 1).padStart(2,'0')}`;
  } else id = 'CTA';
  const timing = scene.kind === 'still' ? 'static' : `${sampleAt.toFixed(1)}s`;
  const label=Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="320" height="30"><rect width="320" height="30" fill="#0b2233"/><text x="8" y="21" fill="white" font-family="Arial" font-size="15">${id} · ${timing} · ${width}×${height}</text></svg>`);
  tiles.push({input:label,left:column*320,top:row*210+180});
  checks.push({id,kind:scene.kind,source:scene.relative,seek:scene.seek,duration:scene.duration,sourceDuration,width,height,sampleAt,visualReview});
}
await sharp({create:{width:2560,height:840,channels:3,background:'#07111d'}}).composite(tiles).jpeg({quality:92}).toFile(path.join(out,'contact.jpg'));
await fs.writeFile(path.join(root,'video/current_main_preflight.json'),JSON.stringify({generatedAt:new Date().toISOString(),scheduleSeconds:370,storyScenes:checks,visualReview},null,2)+'\n');
console.log(`Prepared ${checks.length} selected-story samples`);
