import fs from 'node:fs/promises';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createRequire} from 'node:module';
const run=promisify(execFile),require=createRequire(import.meta.url);
const sharp=require('../.tools-node/node_modules/sharp');
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'build/video/stock-qa');
const {assets}=JSON.parse(await fs.readFile(path.join(root,'video/stock_assets.json'),'utf8'));
await fs.mkdir(out,{recursive:true});
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
for(const topic of ['M2','M3','M4','M5','R1','R3']) {
  const group=assets.filter(a=>a.id.startsWith(topic)&&a.file),tiles=[];
  for(let i=0;i<group.length;i++) {
    const a=group[i];
    for(let j=0;j<2;j++) {
      const t=j?Math.min(7,a.duration*.8):Math.min(1,a.duration*.2);
      const {stdout}=await run('ffmpeg',['-nostdin','-v','error','-ss',String(t),'-i',path.join(root,a.file),'-frames:v','1','-vf','scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:black','-f','image2pipe','-vcodec','png','pipe:1'],{encoding:'buffer',maxBuffer:4*1024*1024});
      tiles.push({input:stdout,left:j*480,top:i*302});
    }
    const label=`<svg xmlns="http://www.w3.org/2000/svg" width="960" height="32"><rect width="960" height="32" fill="#102635"/><text x="12" y="22" fill="white" font-family="Arial" font-size="16">${esc(a.id+' | '+a.width+'x'+a.height+' | '+a.duration.toFixed(2)+'s | '+a.credit)}</text></svg>`;
    tiles.push({input:Buffer.from(label),left:0,top:i*302+270});
  }
  if(group.length)await sharp({create:{width:960,height:group.length*302,channels:3,background:'#07111d'}}).composite(tiles).jpeg({quality:88}).toFile(path.join(out,topic+'.jpg'));
  console.log(topic+' '+group.length+' scenes');
}
