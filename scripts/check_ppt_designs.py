"""Check the slide-sized design artifacts and their retained editable content."""
import json
import re
from pathlib import Path
from PIL import Image
from design_board import ROOT, AWARDS, TIMELINE, UART, SKILLS

base=ROOT/'output/design-review/ppt-ready'
normalize=lambda value: re.sub(r'\s+','',value)
expected=['Jang MoonSu','2024.10.02','2026.09.14','OPIc  IL','Intermediate Low','STM-Simulator',
          'localStorage','자동 저장 · JSON 문자열','9600 baud','260ms에 입력','20ms 한 단계 실행']
expected += [value for row in AWARDS for value in row]
expected += [value for row in TIMELINE for value in row]
expected += [value for _,value in UART]
expected += [label for _,items in SKILLS for _,label in items]

for theme in ['a','b']:
    pages=sorted((base/theme).glob('*.layout.json'))
    assert len(pages)==8, f'{theme}: eight pages required'
    all_text=[]
    for page in pages:
        d=json.loads(page.read_text(encoding='utf-8'))
        assert (d['width'],d['height'])==(1600,900)
        boxes=[]
        for o in d['objects']:
            if o['type']=='image':
                assert (ROOT/o['source']).exists()
                assert 0<=o['x'] and o['x']+o['w']<=1600 and o['y']+o['h']<=900
            if o['type']!='text':continue
            x=o['x']-(o['width'] if o['anchor']=='end' else o['width']/2 if o['anchor']=='middle' else 0)
            box=(x,o['y'],x+o['width'],o['y']+o['size'],o['text'])
            assert x>=0 and box[2]<=1600 and box[3]<=900, f'{page.name}: overflow: {o["text"]}'
            assert '\n' not in o['text'], 'Unrendered line break'
            boxes.append(box)
            all_text.append(o['text'])
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                assert not (min(a[2],b[2])>max(a[0],b[0])+1 and min(a[3],b[3])>max(a[1],b[1])+1), f'{page.name}: text collision: {a[4]} / {b[4]}'
        png=page.with_name(page.name.replace('.layout.json','.png'))
        assert Image.open(png).size==(1600,900)
    combined=normalize(''.join(all_text))
    for fact in expected:assert normalize(fact) in combined, f'{theme}: missing {fact}'
    print(f'{theme}: 8 slide dimensions, object bounds, text collisions, required facts and source assets OK')
