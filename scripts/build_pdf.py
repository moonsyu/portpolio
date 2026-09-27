"""Build the downloadable portfolio PDF from index.html and its existing assets.

Dependencies: Python reportlab/Pillow and Node sharp. Fonts are embedded.
"""
from argparse import ArgumentParser
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import os
import subprocess
import tempfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/pdf/Jang-MoonSu-Portfolio.pdf'
INK, BLUE, MUTED, LINE, PAPER = map(colors.HexColor,
    ['#172538', '#2355de', '#47556b', '#dce3ed', '#f4f7fc'])
W, H = A4
M, CW = 38, W - 76


class Element:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def select(self, tag=None, cls=None, id=None):
        result = []
        for child in self.children:
            if isinstance(child, Element):
                if ((not tag or child.tag == tag) and
                    (not cls or cls in child.attrs.get('class', '').split()) and
                    (not id or child.attrs.get('id') == id)):
                    result.append(child)
                result.extend(child.select(tag, cls, id))
        return result

    def one(self, **kwargs):
        found = self.select(**kwargs)
        if len(found) != 1:
            raise ValueError(f'Expected one element: {kwargs}, got {len(found)}')
        return found[0]

    def text(self):
        return ' '.join(''.join(c.text() if isinstance(c, Element) else c
                                for c in self.children).split()).replace('—', '-')


class Document(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__()
        self.root = Element()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == 'br':
            self.stack[-1].children.append(' · ')
        node = Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if tag not in self.VOID:
            if self.stack[-1].tag != tag:
                raise ValueError(f'Unbalanced HTML at {tag}')
            self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def build(font_dir, node_modules=None):
    for name, filename in [('Career', 'malgun.ttf'), ('CareerBold', 'malgunbd.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    doc = Document((ROOT / 'index.html').read_text(encoding='utf-8')).root
    projects = doc.select(tag='article', cls='project')
    total = 2 + sum(len(p.select(cls='detail-section')) for p in projects)
    site = next(n.attrs['href'] for n in doc.select(tag='link') if n.attrs.get('rel') == 'canonical')
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1, invariant=1)
    pdf.setTitle('장문수 | Developer Portfolio')
    pdf.setAuthor('Jang MoonSu')
    page = 0

    def text(value, x, top, width=CW, size=11, color=INK, bold=True, leading=None, bottom=H-42):
        style = ParagraphStyle('portfolio', fontName='CareerBold' if bold else 'Career',
            fontSize=size, leading=leading or size*1.6, textColor=color,
            wordWrap='CJK', splitLongWords=True)
        para = Paragraph(escape(value), style)
        _, height = para.wrap(width, H)
        if top + height > bottom:
            raise ValueError(f'Page {page+1} overflow: {value}')
        para.drawOn(pdf, x, H-top-height)
        return top+height

    def line(y):
        pdf.setStrokeColor(LINE)
        pdf.line(M, H-y, W-M, H-y)

    def footer(anchor='home'):
        nonlocal page
        page += 1
        line(H-35)
        text('Jang MoonSu · PORTFOLIO', M, H-29, 220, 8, MUTED, False, bottom=H-8)
        text(f'{page:02d} / {total:02d}', W-90, H-29, 52, 8, MUTED, False, bottom=H-8)
        pdf.linkURL(site+'#'+anchor, (M,13,M+220,30), relative=0)
        pdf.showPage()

    def heading(label, title):
        text(label, M, 35, size=10, color=BLUE)
        y = text(title, M, 60, size=23, leading=33)
        line(y+16)
        return y+35

    def bullets(items, x, y, width=CW, size=11):
        for item in items:
            y = text('• '+item.text(), x, y, width, size)+7
        return y

    def direct(node, tag=None):
        return [c for c in node.children if isinstance(c, Element) and (not tag or c.tag==tag)]

    def link(label, url, x, y, width=CW):
        end = text(label, x, y, width, 10, BLUE)
        pdf.linkURL(url, (x,H-end,x+width,H-y), relative=0)
        return end

    def caption(fig):
        node = fig.one(tag='figcaption')
        return ' '.join(c.text() if isinstance(c,Element) else c for c in node.children
                        if not isinstance(c,Element) or c.tag!='button').strip()

    with tempfile.TemporaryDirectory(prefix='portfolio-pdf-') as temp:
        temp = Path(temp)
        images = {}
        jobs = []
        for img in doc.select(tag='img'):
            source = img.attrs.get('src')
            if not source or source in images:
                continue
            path = ROOT/source
            if path.suffix == '.svg':
                dest = temp/(path.stem+'.png')
                jobs.append({'source':str(path),'dest':str(dest)})
                images[source]=dest
            else:
                images[source]=path
        manifest = temp/'images.json'
        manifest.write_text(json.dumps(jobs),encoding='utf-8')
        env = os.environ.copy()
        if node_modules:
            env['NODE_PATH']=str(node_modules)
        subprocess.run(['node','-e',"""
const sharp=require('sharp'),fs=require('node:fs');
const jobs=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
(async()=>{for(const j of jobs) await sharp(j.source,{density:192}).png().toFile(j.dest);})()
.catch(e=>{console.error(e);process.exitCode=1;});
""",str(manifest)],check=True,env=env,cwd=ROOT)

        def picture(path, x, y, width, height):
            with Image.open(path) as im:
                ratio=min(width/im.width,height/im.height)
                iw,ih=im.width*ratio,im.height*ratio
                rgba=im.convert('RGBA')
                white=Image.new('RGBA',rgba.size,'white')
                white.alpha_composite(rgba)
                pdf.drawImage(ImageReader(white.convert('RGB')),x+(width-iw)/2,H-y-ih,iw,ih)
                return y+ih

        def figure(fig, y, height):
            nodes = fig.select(tag='img')
            gap=14
            width=(CW-gap*(len(nodes)-1))/len(nodes)
            bottom=y
            for i,node in enumerate(nodes):
                bottom=max(bottom,picture(images[node.attrs['src']],M+(width+gap)*i,y,width,height))
            first=fig.one(tag='figcaption')
            spans=first.select(tag='span')
            label=spans[0].text() if spans else caption(fig)
            return text(label,M,bottom+9,size=10,color=MUTED)+10

        # Profile and skills: the current website remains the content source.
        y=heading('01 / ABOUT','장문수 · Developer Portfolio')
        profile=doc.one(cls='profile-heading')
        picture(images[profile.one(tag='img').attrs['src']],M,y,76,92)
        text(profile.one(tag='p').text(),M+94,y+8,size=21)
        text(doc.one(cls='about-copy').text(),M+94,y+47,size=12,color=BLUE)
        y+=115
        bullets(doc.one(cls='about-points').select(tag='li'),M,y,220,11)
        text('경력 및 교육',M+248,y,CW-248,14,BLUE)
        cy=y+31
        for row in doc.select(cls='timeline-item'):
            cy=text(row.one(tag='dt').text(),M+248,cy,CW-248,9,MUTED)+3
            dd=row.one(tag='dd')
            title=''.join(c for c in dd.children if isinstance(c,str)).strip()
            cy=text(title,M+248,cy,CW-248,11)+2
            cy=text(dd.one(tag='span').text(),M+248,cy,CW-248,10,MUTED)+13
        y=max(487,cy+8)
        text('보유 기술 스택',M,y,size=15,color=BLUE)
        y+=33
        for i,group in enumerate(doc.select(cls='skill-group')):
            x=M+(CW/2+7)*(i%2)
            top=y+85*(i//2)
            text(group.one(tag='h3').text(),x,top,CW/2-14,12)
            for j,item in enumerate(group.select(tag='li')):
                sx=x+(CW/4)*(j%2)
                sy=top+27+25*(j//2)
                picture(images[item.one(tag='img').attrs['src']],sx,sy,17,17)
                text(item.one(tag='span').text(),sx+22,sy,CW/4-28,8.5)
        line(749)
        for i,item in enumerate(doc.one(cls='contact-links').select(tag='a')):
            link(item.select(tag='span')[-1].text().replace('↗','').strip(),item.attrs['href'],M+i*CW/3,760,CW/3-8)
        footer('about')

        y=heading('01 / CREDENTIALS','수상 · 자격 · 어학')
        text('수상',M,y,size=16,color=BLUE)
        cy=y+40
        for award in doc.one(cls='award-list').select(tag='li'):
            cy=text(award.one(cls='award-organizer').text(),M,cy,310,10,BLUE)+4
            cy=text(award.one(tag='h4').text(),M,cy,310,12)+5
            cy=text(award.one(tag='time').text(),M,cy,310,10,MUTED)+24
        qx=M+340
        text('자격 · 어학',qx,y,CW-340,16,BLUE)
        cy=y+40
        for item in doc.one(cls='qualification-list').select(tag='li'):
            cy=text(item.one(tag='h4').text(),qx,cy,CW-340,15)+12
            for grade in item.select(cls='qualification-grade'):
                cy=text(grade.text(),qx,cy,CW-340,12,BLUE)+12
            for row in direct(item.one(tag='dl')):
                cy=text(row.one(tag='dt').text(),qx,cy,CW-340,10,MUTED)+3
                cy=text(row.one(tag='dd').text(),qx,cy,CW-340,11)+12
            cy+=26
        footer('about')

        for i,project in enumerate(projects,1):
            name=project.one(tag='h3').text()
            anchor=project.attrs['id']
            y=heading(f'02 / PROJECT {i:02d}',name)
            desc=project.one(cls='project-description')
            y=text(desc.one(tag='h4').text(),M,y,size=13)+5
            meta=' · '.join(n.text() for n in desc.one(cls='project-meta').select(tag='span'))
            y=text(meta,M,y,size=10,color=MUTED)+8
            y=bullets(desc.one(tag='ul').select(tag='li'),M,y,size=10.5)
            y=text(desc.one(cls='techline').text(),M,y,size=9,color=BLUE)+12
            arch=project.one(cls='application-architecture')
            image=arch.one(tag='img')
            with Image.open(images[image.attrs['src']]) as im:
                arch_height=CW*im.height/im.width
            remaining=H-48-y-arch_height-56
            y=figure(project.one(cls='project-visual'),y,max(75,remaining-30))
            y=text('애플리케이션 아키텍처',M,y,size=11,color=BLUE)+9
            end=picture(images[image.attrs['src']],M,y,CW,arch_height)
            text(arch.one(tag='figcaption').select(tag='span')[0].text(),M,end+7,size=9,color=MUTED)
            footer(anchor)

            for section in project.select(cls='detail-section'):
                if section.select(cls='application-architecture'):
                    continue
                title=section.one(tag='h4').text()
                y=heading(name+' / '+section.one(cls='label').text(),title)
                facts=section.select(cls='case-facts')
                if facts:
                    for row in direct(facts[0]):
                        y=text(row.one(tag='dt').text(),M,y,size=13,color=BLUE)+7
                        y=bullets(row.one(tag='dd').select(tag='li'),M,y,size=12)+12
                else:
                    for card in direct(section.one(cls='implementation-list')):
                        y=text(card.one(tag='h5').text(),M,y,size=14,color=BLUE)+7
                        y=bullets(card.select(tag='li'),M,y,size=12)+18
                figures=section.select(tag='figure')
                if figures:
                    fig=figures[0]
                    node=fig.one(tag='img')
                    src=node.attrs['src']
                    if src.endswith('.gif'):
                        with Image.open(images[src]) as gif:
                            indices=[0,gif.n_frames//2,gif.n_frames-1]
                            width=(CW-24)/3
                            image_end=y
                            for k,index in enumerate(indices):
                                gif.seek(index)
                                frame=temp/f'{anchor}-{section.attrs["aria-labelledby"]}-{k}.png'
                                gif.convert('RGB').save(frame)
                                x=M+(width+12)*k
                                text(['시작','중간','마지막'][k],x,y,width,10,BLUE)
                                image_end=max(image_end,picture(frame,x,y+24,width,H-y-130))
                        y=text(caption(fig),M,image_end+14,size=11)+14
                        link('실행 GIF 보기 - 온라인 포트폴리오',site+'#'+fig.attrs['id'],M,y)
                    else:
                        end=picture(images[src],M,y,CW,H-y-100)
                        text(caption(fig),M,end+12,size=10,color=MUTED)
                else:
                    figure(project.one(cls='project-visual'),y,min(250,H-y-100))
                footer(section.attrs['aria-labelledby'])
        assert page==total
    pdf.save()
    print(f'Created {OUTPUT} ({page} pages)')


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--font-dir',type=Path,default=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts')
    parser.add_argument('--node-modules',type=Path)
    args=parser.parse_args()
    build(args.font_dir,args.node_modules)
