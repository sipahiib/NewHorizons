import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),sharp=require('../.tools-node/node_modules/sharp');
const root=path.resolve(import.meta.dirname,'..'),qa=path.join(root,'build/reels/current-qa');
fs.mkdirSync(qa,{recursive:true});
const run=(bin,args)=>{const r=spawnSync(bin,args,{encoding:'utf8',maxBuffer:8*1024*1024});if(r.status)throw new Error(r.stderr);return r;};
const reports=[],tiles=[];
for(const [row,stem] of ['01-sports-biomechanics','02-hands-on-science','03-ai-archaeology'].entries()){
 const file=path.join(root,'build/reels',stem+'.mp4');
 const meta=JSON.parse(run('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',file]).stdout);
 const v=meta.streams.find(s=>s.codec_type==='video'),a=meta.streams.find(s=>s.codec_type==='audio'),duration=Number(meta.format.duration);
 const speechEnd=Number(run('node',[path.join(root,'video/measure_reel_audio.mjs'),file]).stdout);
 if(v.width!==1080||v.height!==1920||v.r_frame_rate!=='60/1'||v.codec_name!=='h264'||a.codec_name!=='aac'||duration<30||duration>35||speechEnd>30||duration-speechEnd>4.02)throw new Error(`Reel specification mismatch ${stem}: ${JSON.stringify({duration,speechEnd})}`);
 if(Math.abs(Number(v.nb_read_frames)-Math.round(duration*60))>1)throw new Error(`Video frames do not cover full delivery: ${stem}`);
 const scan=run('ffmpeg',['-nostdin','-v','info','-i',file,'-an','-vf','scale=90:160,fps=5,blackdetect=d=0.4:pix_th=0.1:pic_th=0.98','-f','null','-']).stderr;
 if(scan.includes('black_start:'))throw new Error(`Black interval in ${stem}`);
 const sampleTimes=[2,7,13,19,25,duration-1];
 for(const [col,t]of sampleTimes.entries()){
  const frame=path.join(qa,`${stem}-${col}.png`);
  run('ffmpeg',['-nostdin','-y','-v','error','-ss',String(t),'-i',file,'-frames:v','1','-vf','scale=270:480',frame]);
  tiles.push({input:frame,left:col*270,top:row*510});
  const label=Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="270" height="30"><rect width="270" height="30" fill="#091521"/><text x="10" y="22" fill="white" font-size="16" font-family="Arial">R${row+1} · ${t.toFixed(2)} seconds</text></svg>`);
  tiles.push({input:label,left:col*270,top:row*510+480});
 }
 reports.push({file:`build/reels/${stem}.mp4`,width:v.width,height:v.height,fps:v.r_frame_rate,frames:Number(v.nb_read_frames),duration,speechEnd,closingGap:duration-speechEnd,videoCodec:v.codec_name,audioCodec:a.codec_name,voice:'en-GB-RyanNeural',rate:'-2%',timeStretch:false,sourceClips:5,layout:'Full foreground frame centred over dark blurred duplicate; no landscape foreground crop',blackIntervals:0,visualReview:'pending contact-sheet review',audioReview:'Measured signal ending; no claim of full human listening'});
}
await sharp({create:{width:1620,height:1530,channels:3,background:'#091521'}}).composite(tiles).jpeg({quality:92}).toFile(path.join(qa,'contact.jpg'));
fs.writeFileSync(path.join(root,'video/current_reels_verification.json'),JSON.stringify(reports,null,2)+'\n');
console.log(JSON.stringify(reports,null,2));
