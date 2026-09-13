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
const selected = scenes.filter((scene) => scene.kind !== 'still');
if (selected.length !== 25) throw new Error(`Expected 25 story scenes, found ${selected.length}`);
const visualReview = process.env.VISUAL_REVIEW === 'pass'
  ? 'pass — midpoint contact sheet and source timeline visually inspected; real footage and contextual correspondence confirmed'
  : 'pending';
const out = path.join(root,'build/video/current-main-preflight');
await fs.mkdir(out,{recursive:true});
const tiles=[];
const checks=[];
for (const [index,scene] of selected.entries()) {
  const input=path.join(root,scene.relative);
  const {stdout:probeText}=await run('ffprobe',['-v','error','-show_streams','-show_format','-of','json',input]);
  const probe=JSON.parse(probeText),video=probe.streams.find((stream)=>stream.codec_type==='video');
  const sourceDuration=Number(probe.format.duration);
  if (!video || scene.seek+scene.duration>sourceDuration+0.02) throw new Error(`Scene exceeds source: ${scene.relative}`);
  const sampleAt=scene.seek+scene.duration/2;
  const {stdout:frame}=await run('ffmpeg',['-nostdin','-v','error','-ss',String(sampleAt),'-i',input,'-frames:v','1','-vf','scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2:black','-f','image2pipe','-vcodec','png','pipe:1'],{encoding:'buffer',maxBuffer:8*1024*1024});
  const column=index%5,row=Math.floor(index/5);
  tiles.push({input:frame,left:column*320,top:row*210});
  const id=`M${Math.floor(index/5)+1}-${String(index%5+1).padStart(2,'0')}`;
  const label=Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="320" height="30"><rect width="320" height="30" fill="#0b2233"/><text x="8" y="21" fill="white" font-family="Arial" font-size="15">${id} · ${sampleAt.toFixed(1)}s · ${video.width}×${video.height}</text></svg>`);
  tiles.push({input:label,left:column*320,top:row*210+180});
  checks.push({id,source:scene.relative,seek:scene.seek,duration:scene.duration,sourceDuration,width:video.width,height:video.height,sampleAt,visualReview});
}
await sharp({create:{width:1600,height:1050,channels:3,background:'#07111d'}}).composite(tiles).jpeg({quality:92}).toFile(path.join(out,'contact.jpg'));
await fs.writeFile(path.join(root,'video/current_main_preflight.json'),JSON.stringify({generatedAt:new Date().toISOString(),scheduleSeconds:370,storyScenes:checks,visualReview},null,2)+'\n');
console.log(`Prepared ${checks.length} selected-story samples`);
