"""16:9 design source with text and object coordinates retained for later PPT editing."""
import json
from pathlib import Path
from design_board import Board, OUT, ROOT, width, TIMELINE, SKILLS, AWARDS, ABOUT, STM_POINTS, OLD, IMPROVED, UART

THEMES = {
    'a': dict(key='a', ink='#30323D', accent='#70687D', muted='#666975', soft='#F3F1F5', line='#DAD7E0', paper='#FFFFFF'),
    'b': dict(key='b', ink='#24353D', accent='#365E6E', muted='#5B6970', soft='#EDF3F5', line='#CEDBE0', paper='#FAFCFD'),
}

class Slide(Board):
    def __init__(self, theme, number, name):
        self.theme, self.number, self.objects = theme, number, []
        super().__init__(f"ppt-ready/{theme['key']}/{number:02d}-{name}", name, 900, theme['paper'], 1600)

    def rect(self, x, y, w, h, fill, radius=0, stroke=None, sw=1):
        self.objects.append(dict(type='rect', x=x, y=y, w=w, h=h, fill=fill, radius=radius, stroke=stroke, strokeWidth=sw))
        return super().rect(x, y, w, h, fill, radius, stroke, sw)

    def line(self, x1, y1, x2, y2, color='#DDD6EE', sw=1):
        self.objects.append(dict(type='line', x1=x1, y1=y1, x2=x2, y2=y2, color=color, strokeWidth=sw))
        return super().line(x1, y1, x2, y2, color, sw)

    def text(self, x, y, value, size=32, weight=600, color=None, anchor='start'):
        color = color or self.theme['ink']
        self.objects.append(dict(type='text', x=x, y=y, text=value, size=size, weight=weight, color=color, anchor=anchor,
                                 width=width(value,size,weight), fontLatin='Manrope', fontKorean='Noto Sans KR'))
        return super().text(x, y, value, size, weight, color, anchor)

    def image(self, path, x, y, w, h=None, radius=0, fit='meet'):
        bottom = super().image(path, x, y, w, h, radius, fit)
        p = Path(path)
        source = p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
        self.objects.append(dict(type='image', source=source, x=x, y=y, w=w, h=bottom-y, radius=radius, fit=fit))
        return bottom

    def arrow(self, x1, y1, x2, y2, both=False):
        color = self.theme['accent']
        self.objects.append(dict(type='arrow', x1=x1,y1=y1,x2=x2,y2=y2,color=color,both=both))
        ident = f'arrow{len(self.defs)}'
        self.defs.append(f'<marker id="{ident}" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>')
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2" fill="none" marker-end="url(#{ident})"'+(f' marker-start="url(#{ident})"' if both else '')+'/>')

    def save(self):
        (OUT / self.filename).parent.mkdir(parents=True,exist_ok=True)
        super().save()
        data=dict(width=1600,height=900,ratio='16:9',theme=self.theme,objects=self.objects)
        (OUT/(self.filename+'.layout.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def new_slide(theme, number, title, subtitle=None):
    s=Slide(theme,number,['intro','career','skills','awards','stm-overview','stm-architecture','stm-improvement','stm-uart'][number-1])
    if title:
        s.text(72,52,title,52,780,theme['ink'])
        if subtitle:s.text(72,126,subtitle,28,600,theme['muted'])
        s.line(72,184,1528,184,theme['line'])
    s.text(72,850,'Jang MoonSu',20,650,theme['muted'])
    s.text(1528,850,f'{number} / 8',20,650,theme['muted'],'end')
    return s

def icon(s, name, x, y, size=42):
    return s.image(f'assets/architecture/icons/{name}.svg',x,y,size,size)
