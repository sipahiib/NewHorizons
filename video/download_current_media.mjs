import fs from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';

const run = promisify(execFile);
const root = path.resolve(import.meta.dirname, '..');
const manifestArg = process.argv[2];
if (!manifestArg) throw new Error('Pass an explicit approved media manifest path');
const manifestPath = path.resolve(root, manifestArg);
if (!manifestPath.startsWith(root + path.sep)) throw new Error('Manifest must be inside the repository');
const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
if (!['approved-for-download', 'final-selection'].includes(manifest.status)) {
  throw new Error(`Manifest is not active for download: ${manifest.status || 'missing status'}`);
}
const base = path.join(root, 'assets/motion', manifest.cycle);
const report = [];
const selectedIds = new Set(manifest.selection?.selectedIds || []);
const rejectedIds = new Set(manifest.selection?.rejectedIds || []);

async function sha256(file) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(file)) hash.update(chunk);
  return hash.digest('hex');
}

async function probe(file) {
  const {stdout} = await run('ffprobe', ['-v','error','-show_streams','-show_format','-of','json',file]);
  const metadata = JSON.parse(stdout);
  const video = metadata.streams.find((stream) => stream.codec_type === 'video');
  if (!video || !(Number(metadata.format.duration) > 0)) throw new Error('No usable video stream');
  return {
    duration: Number(metadata.format.duration),
    width: video.width,
    height: video.height,
    fps: video.avg_frame_rate,
    codec: video.codec_name,
    bytes: Number(metadata.format.size)
  };
}

for (const asset of manifest.assets) {
  const target = path.join(base, asset.file);
  const partial = `${target}.part`;
  await fs.mkdir(path.dirname(target), {recursive: true});
  try {
    let fetchedThisRun = false;
    try { await fs.access(target); } catch {
      const url = asset.kind === 'pexels'
        ? `https://www.pexels.com/download/video/${asset.assetId}/`
        : asset.download;
      const {stdout} = await run('curl', [
        '--fail','--location','--silent','--show-error','--connect-timeout','20','--max-time','240',
        '--max-filesize','524288000','--output',partial,'--write-out','%{url_effective}',url
      ], {maxBuffer: 1024 * 1024});
      const effectiveUrl = stdout.trim();
      if (asset.kind === 'pexels' && !effectiveUrl.startsWith('https://videos.pexels.com/')) {
        throw new Error(`Unexpected Pexels destination: ${effectiveUrl}`);
      }
      await probe(partial);
      await fs.rename(partial, target);
      fetchedThisRun = true;
    }
    const metadata = await probe(target);
    const visualReview = selectedIds.has(asset.id) ? 'accepted' : rejectedIds.has(asset.id) ? 'rejected' : 'pending';
    const digest = selectedIds.has(asset.id) ? await sha256(target) : undefined;
    report.push({...asset, file: path.relative(root,target), downloaded:true, fetchedThisRun, ...metadata, ...(digest ? {sha256:digest} : {}), visualReview});
    console.log(`OK ${asset.id} ${metadata.width}x${metadata.height} ${metadata.duration.toFixed(3)}s`);
  } catch (error) {
    await fs.rm(partial, {force:true});
    report.push({...asset, status:'failed', error:String(error.message).slice(0,700)});
    console.error(`FAILED ${asset.id}: ${String(error.message).slice(0,250)}`);
  }
}

const reportPath = path.join(root, 'video/current_media_verification.json');
await fs.writeFile(reportPath, JSON.stringify({checkedAt:new Date().toISOString(), assets:report}, null, 2) + '\n');
const failed = report.filter((asset) => asset.status === 'failed');
console.log(`RESULT ${report.length - failed.length}/${report.length} assets available; ${selectedIds.size} selected assets hashed and reviewed`);
if (failed.length) process.exitCode = 1;
