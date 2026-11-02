const fs = require('fs');
const path = require('path');
const runtime = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const { instance } = require(path.join(runtime, '@viz-js/viz/dist/viz.cjs'));
const sharp = require(path.join(runtime, 'sharp'));
const root = '/workspace/scratch/b65e59c0fbe4/projects/SAR-Issue-23-Object-Model';
const assets = path.join(root, 'docs/assets/issue23');
const analysis = '/workspace/scratch/b65e59c0fbe4/analysis/issue23_object_model_2026-10-28';

(async () => {
  const viz = await instance();
  const result = [];
  for (const name of fs.readdirSync(assets).filter(x => x.endsWith('.dot')).sort()) {
    const source = fs.readFileSync(path.join(assets, name), 'utf8');
    const svg = viz.renderString(source, {format: 'svg', engine: 'dot'});
    const destination = path.join(assets, name.replace('.dot', '.svg'));
    fs.writeFileSync(destination, svg);
    const png = path.join(analysis, name.replace('.dot', '.png'));
    await sharp(Buffer.from(svg)).resize({width: 1700}).png().toFile(png);
    const metadata = await sharp(png).metadata();
    result.push({name, svg: destination, png, png_width: metadata.width, png_height: metadata.height});
  }
  fs.writeFileSync(path.join(analysis, 'diagram_render_results.json'), JSON.stringify(result, null, 2) + '\n');
  process.stdout.write(JSON.stringify(result, null, 2));
})().catch(error => {process.stderr.write(String(error)); process.exit(1);});
