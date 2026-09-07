import fs from 'node:fs/promises';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createRequire} from 'node:module';
const run=promisify(execFile);
const require=createRequire(import.meta.url);
const sharp=require('../.tools-node/node_modules/sharp');
const root=path.resolve(import.meta.dirname,'..');
const entries=(await fs.readFile(path.join(root,'video/main_motion_scenes.tsv'),'utf8'))
  .split('\n').filter(l=>l && !l.startsWith('#')).map(l=>l.split('|'));
if(entries.length!==10) throw new Error('Expected exactly ten scenes');
const report=[], tiles=[];
for(let i=0;i<entries.length;i++) {
  const [,relative,duration]=entries[i], file=path.join(root,relative);
  const {stdout}=await run('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',file]);
  const meta=JSON.parse(stdout),video=meta.streams.find(s=>s.codec_type==='video');
  if(!video || video.width!==1920 || video.height!==1080 || video.r_frame_rate!=='60/1' || video.avg_frame_rate!=='60/1' || video.codec_name!=='h264' || Number(video.nb_read_frames)!==660 || Math.abs(Number(meta.format.duration)-Number(duration))>.001 || meta.streams.some(s=>s.codec_type==='audio')) throw new Error(`Metadata mismatch: ${relative}`);
  const hashes=await run('ffmpeg',['-nostdin','-v','error','-i',file,'-vf','fps=1,scale=160:90','-f','framemd5','pipe:1']);
  const records=hashes.stdout.split('\n').filter(l=>l && !l.startsWith('#'));
  const unique=new Set(records.map(l=>l.split(',').at(-1).trim())).size;
  if(unique!==11) throw new Error(`Frozen/duplicate sampled frame: ${relative}`);
  // Full-frame mean-difference freeze detection mislabels small moving objects
  // against these intentionally static dark backgrounds. Instead check exact
  // decoded-frame runs at all 60 fps, plus distinct one-second samples above.
  const full=await run('ffmpeg',['-nostdin','-v','error','-i',file,'-vf','scale=480:270','-f','framemd5','pipe:1']);
  let last='',runLength=0,maxRepeatedFrames=0;
  for(const l of full.stdout.split('\n').filter(l=>l && !l.startsWith('#'))) {
    const hash=l.split(',').at(-1).trim();
    runLength=hash===last?runLength+1:1;last=hash;
    maxRepeatedFrames=Math.max(maxRepeatedFrames,runLength);
  }
  if(maxRepeatedFrames>=60) throw new Error(`One-second identical-frame run: ${relative}`);
  const analysis=await run('ffmpeg',['-nostdin','-v','info','-i',file,'-vf','blackdetect=d=0.2:pix_th=0.02:pic_th=0.98','-an','-f','null','-'],{maxBuffer:4*1024*1024});
  if(/black_start:/.test(analysis.stderr)) throw new Error(`Detected black interval: ${relative}`);
  for(let j=0;j<2;j++) {
    const {stdout:png}=await run('ffmpeg',['-nostdin','-v','error','-ss',String(j?8:2),'-i',file,'-frames:v','1','-vf','scale=480:270','-f','image2pipe','-vcodec','png','pipe:1'],{encoding:'buffer',maxBuffer:4*1024*1024});
    tiles.push({input:png,left:j*480,top:i*270});
  }
  report.push({file:relative,width:video.width,height:video.height,fps:60,frames:660,duration:11,codec:'h264',audio:'none — silent motion asset',uniqueSampledFrames:unique,maxRepeatedFrames,blackIntervalDetected:false});
  console.log(`PASS ${path.basename(file)}`);
}
await fs.writeFile(path.join(root,'video/main_motion_verification.json'),JSON.stringify({checkedAt:new Date().toISOString(),status:'technical checks passed; visual contact sheet requires review',totalSeconds:110,clips:report},null,2)+'\n');
const sheet=path.join(root,'build/video/main-motion-qa.jpg');
await sharp({create:{width:960,height:2700,channels:3,background:'#071525'}}).composite(tiles).jpeg({quality:90}).toFile(sheet);
console.log(sheet);
