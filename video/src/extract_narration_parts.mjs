import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '../..');
const sourcePath = process.env.NARRATION_SOURCE
  ? path.resolve(process.env.NARRATION_SOURCE)
  : path.join(root, 'video/narration.txt');
const partsDir = process.env.NARRATION_PARTS_DIR
  ? path.resolve(process.env.NARRATION_PARTS_DIR)
  : path.join(root, 'build/video/narration-parts');
const source = fs.readFileSync(sourcePath, 'utf8');
const output = path.join(partsDir, 'text');
fs.mkdirSync(output, { recursive: true });

const sections = source
  .split(/^##\s+.+$/gm)
  .map((section) => section.trim().replace(/\n+/g, ' '))
  .filter(Boolean);

const names = ['intro', 'libre', 'pandora', 'china', 'outro'];
if (sections.length !== names.length) {
  throw new Error(`Expected ${names.length} narration sections, found ${sections.length}`);
}

for (const [index, name] of names.entries()) {
  fs.writeFileSync(path.join(output, `${name}.txt`), `${sections[index]}\n`);
}

console.log(`Prepared ${names.length} narration inputs in ${output}`);
