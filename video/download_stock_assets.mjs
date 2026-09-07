// Uses Pexels' public Free download route. No browser cookies, impersonation,
// authentication bypass, challenge solving or guessed CDN file names.
import fs from 'node:fs/promises';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile);
const root=path.resolve(import.meta.dirname,'..');
const source=await fs.readFile(path.join(root,'video/SOURCES.md'),'utf8');
const rows=[...source.matchAll(/^\| ([MR]\d-\d\d) \| \[([^\]]+)\]\((https:\/\/www\.pexels\.com\/video\/[^)]+)\)/gm)]
  .map(m=>({id:m[1],credit:m[2],page:m[3],assetId:m[3].match(/-(\d+)\/$/)[1]}));
if(rows.length!==30) throw new Error(`Expected 30 source-approved stock candidates, found ${rows.length}`);
const dir=path.join(root,'assets/motion/2026-09-07/stock');
await fs.mkdir(dir,{recursive:true});
const report=[];
async function inspect(file) {
  const {stdout}=await run('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file]);
  const m=JSON.parse(stdout),v=m.streams.find(s=>s.codec_type==='video');
  if(!v || !(Number(m.format.duration)>0)) throw new Error('Not a usable video');
  return {width:v.width,height:v.height,fps:v.avg_frame_rate,duration:Number(m.format.duration),bytes:Number(m.format.size),codec:v.codec_name};
}
let next=0;
async function worker() {
  while(next<rows.length) {
    const row=rows[next++],target=path.join(dir,`${row.id}.mp4`),part=target+'.part';
    const route=`https://www.pexels.com/download/video/${row.assetId}/`;
    let effectiveUrl=null;
    try {
      let exists=false;
      try {await fs.access(target);exists=true;}catch{}
      if(!exists) {
        try {await fs.access(part);throw new Error(`Partial file exists; inspect before retry: ${part}`);}catch(e){if(e.code!=='ENOENT')throw e;}
        const r=await run('curl',['--fail','--location','--silent','--show-error','--connect-timeout','20','--max-time','180','--max-filesize','524288000','--output',part,'--write-out','%{url_effective}',route],{maxBuffer:1024*1024});
        effectiveUrl=r.stdout.trim();
        if(!effectiveUrl.startsWith('https://videos.pexels.com/')) throw new Error('Unexpected download destination');
        await inspect(part);
        await fs.rename(part,target);
      }
      const meta=await inspect(target);
      const sample=await run('ffmpeg',['-nostdin','-v','error','-i',target,'-t','9','-vf','fps=1,scale=160:-2','-an','-f','framemd5','pipe:1']);
      const hashes=sample.stdout.split('\n').filter(l=>l&&!l.startsWith('#')).map(l=>l.split(',').at(-1).trim());
      const uniqueSamples=new Set(hashes).size;
      report.push({...row,file:path.relative(root,target),downloadRoute:route,effectiveUrl,licence:'https://www.pexels.com/license/',...meta,uniqueSamples,visualReview:'pending',minimumDurationMet:meta.duration>=(row.id.startsWith('M')?9:6)});
      console.log(`OK ${row.id}: ${meta.width}x${meta.height}, ${meta.duration.toFixed(3)}s, ${uniqueSamples} distinct samples`);
    } catch(e) {
      report.push({...row,downloadRoute:route,status:'failed',error:String(e.message).slice(0,700)});
      console.log(`FAILED ${row.id}: ${String(e.message).slice(0,250)}`);
    }
  }
}
await Promise.all([worker(),worker()]);
report.sort((a,b)=>a.id.localeCompare(b.id));
await fs.writeFile(path.join(root,'video/stock_assets.json'),JSON.stringify({checkedAt:new Date().toISOString(),method:'Public Pexels Free download link; no access-control evasion',assets:report},null,2)+'\n');
const failed=report.filter(r=>r.status==='failed');
console.log(`RESULT ${report.length-failed.length}/${report.length} downloaded and probed; visual review still required`);
if(failed.length)process.exitCode=1;
