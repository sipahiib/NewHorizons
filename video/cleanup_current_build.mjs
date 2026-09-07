import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const targets=[
 'build/video/editorial-en','build/video/narration-parts-en',
 'build/video/current-qa','build/video/stock-qa','build/video/narration-en.wav',
 'build/reels/work','build/reels/overlays','build/reels/audio','build/reels/current-qa',
];
const reports=['video/current_video_verification.json','video/current_reels_verification.json'];
for(const file of reports){
 const data=JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));
 for(const r of Array.isArray(data)?data:[data]){
  if(!r.visualReview||r.visualReview.startsWith('pending'))throw new Error('Complete visual QA before cleanup');
  if(!fs.statSync(path.join(root,r.file)).isFile())throw new Error('Missing verified delivery');
 }
}
const walk=p=>{const s=fs.lstatSync(p);if(s.isSymbolicLink())throw new Error(`Unexpected symlink: ${p}`);return s.isDirectory()?fs.readdirSync(p).flatMap(n=>walk(path.join(p,n))):[{file:path.relative(root,p),bytes:s.size}];};
const inventory=targets.filter(t=>fs.existsSync(path.join(root,t))).flatMap(t=>walk(path.join(root,t)));
const manifest={purpose:'Disposable render intermediates, extracted QA frames and temporary narration only',files:inventory,count:inventory.length,bytes:inventory.reduce((n,f)=>n+f.bytes,0),executed:false,preserved:['build/video/newhorizons.mp4','build/reels/01-sports-biomechanics.mp4','build/reels/02-hands-on-science.mp4','build/reels/03-ai-archaeology.mp4','all source assets, scripts, narration texts, manifests, branding and verification reports']};
console.log(JSON.stringify({count:manifest.count,bytes:manifest.bytes,targets},null,2));
if(process.argv.includes('--execute')){
 const prior=JSON.parse(fs.readFileSync(path.join(root,'video/cleanup_manifest.json'),'utf8'));
 if(JSON.stringify(prior.files)!==JSON.stringify(inventory))throw new Error('Cleanup inventory changed; inspect a fresh dry-run');
 for(const t of targets)fs.rmSync(path.join(root,t),{recursive:true,force:true});
 manifest.executed=true;
}
fs.writeFileSync(path.join(root,'video/cleanup_manifest.json'),JSON.stringify(manifest,null,2)+'\n');
