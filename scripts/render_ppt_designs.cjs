const path = require('node:path');
const fs = require('node:fs/promises');
const sharp = require('sharp');
const root = path.resolve(__dirname, '../output/design-review/ppt-ready');
const provenance = 'Static 16:9 portfolio design comp, not a browser or PowerPoint capture. Existing source content and assets from moonsyu/portpolio at 47bd953. Layout and editable object coordinates retained in source SVG and layout.json. Noto Sans KR and Manrope, SIL OFL 1.1.';
(async()=>{
  for (const theme of ['a','b']) {
    const dir=path.join(root,theme);
    const files=(await fs.readdir(dir)).filter(f=>f.endsWith('.svg')).sort();
    const thumbs=[];
    for (let i=0;i<files.length;i++) {
      const file=path.join(dir,files[i]);
      const png=file.replace(/\.svg$/,'.png');
      await sharp(file).png().withMetadata({comments:[provenance]}).toFile(png);
      thumbs.push({input:await sharp(png).resize(768,432).toBuffer(),left:24+(i%2)*784,top:24+Math.floor(i/2)*448});
    }
    await sharp({create:{width:1600,height:1824,channels:3,background:'#E3E5E8'}}).composite(thumbs).png().toFile(path.join(root,theme+'-overview.png'));
    console.log(`${theme}: ${files.length} slides, 1600x900; contact sheet 1600x1824`);
  }
})().catch(e=>{console.error(e);process.exitCode=1;});
