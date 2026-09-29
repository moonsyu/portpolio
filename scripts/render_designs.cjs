// Render vector design boards without browser automation.
const path = require('node:path');
const sharp = require('sharp');
const out = path.resolve(__dirname, '../output/design-review');
const names = process.argv.slice(2);
const boards = names.length ? names : ['a-frontend-design', 'b-impeccable', 'c-ui-ux-pro-max'];
(async () => {
  for (const name of boards) {
    const file = path.join(out, name);
    const info = await sharp(file + '.svg', { limitInputPixels: false }).png().toFile(file + '.png');
    console.log(`${name}: ${info.width} × ${info.height}`);
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
