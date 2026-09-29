"""Build small local webfonts containing this site's real content."""
from pathlib import Path
import os
from fontTools import subset
from shutil import copyfile

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path(os.environ.get('PORTFOLIO_DESIGN_FONTS', str(ROOT.parent / 'portpolio-work/design-fonts')))

target=ROOT/'assets/fonts'
target.mkdir(exist_ok=True)
source=(ROOT/'index.html').read_text(encoding='utf-8')+(ROOT/'app.js').read_text(encoding='utf-8')
for name in ('Manrope','NotoSansKR'):
    options=subset.Options()
    options.flavor='woff'
    options.layout_features=['*']
    font=subset.load_font(str(FONTS/(name+'.ttf')),options)
    worker=subset.Subsetter(options=options)
    chars=set(range(32,127)) | ({ord(c) for c in source} if name=='NotoSansKR' else set())
    worker.populate(unicodes=chars)
    worker.subset(font)
    output=target/(name+'.woff')
    subset.save_font(font,str(output),options)
    copyfile(ROOT/'output/design-review/licenses'/(name+'-OFL.txt'),target/(name+'-OFL.txt'))
    print(name,output.stat().st_size)
