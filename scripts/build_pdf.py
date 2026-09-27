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
    ['#172538', '#2355de', '#47556b', '#dce3ed', '#f8fafc'])
# PowerPoint widescreen: every source section owns one complete slide.
W, H = 1280, 720
M, CW = 56, W - 112


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
        if self.tag == 'br':
            return ' · '
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


def direct(node, tag=None):
    return [c for c in node.children if isinstance(c, Element)
            and (not tag or c.tag == tag)]


def rich(node):
    """Keep source emphasis and line breaks without copying screen controls."""
    if isinstance(node, str):
        return escape(node)
    if node.tag == 'button':
        return ''
    if node.tag == 'br':
        return '<br/>'
    body = ''.join(rich(c) for c in node.children)
    return f'<b>{body}</b>' if node.tag in {'strong', 'b'} else body


class Slides:
    def __init__(self, site, count):
        self.pdf = canvas.Canvas(str(OUTPUT), pagesize=(W, H),
                                 pageCompression=1, invariant=1)
        self.pdf.setTitle('장문수 | Developer Portfolio')
        self.pdf.setAuthor('Jang MoonSu')
        self.pdf.setPageSize((W, H))
        self.site, self.count, self.page = site, count, 0

    def text(self, value, x, y, width, size=22, color=INK, bold=True,
             leading=None, bottom=654, markup=False):
        style = ParagraphStyle('slide', fontName='CareerBold' if bold else 'Career',
                               fontSize=size, leading=leading or size*1.5,
                               textColor=color, wordWrap='LTR')
        para = Paragraph(value if markup else escape(value), style)
        _, height = para.wrap(width, H)
        if y + height > bottom:
            raise ValueError(f'Slide {self.page+1} overflow at {y+height:.1f}: {value}')
        para.drawOn(self.pdf, x, H-y-height)
        return y + height

    def line(self, x, y, width, color=LINE):
        self.pdf.setStrokeColor(color)
        self.pdf.setLineWidth(1)
        self.pdf.line(x, H-y, x+width, H-y)

    def panel(self, x, y, width, height, fill=colors.white, border=LINE):
        self.pdf.setFillColor(fill)
        self.pdf.setStrokeColor(border)
        self.pdf.roundRect(x, H-y-height, width, height, 12, fill=1, stroke=1)

    def start(self, label, title, subtitle=None, dark=False):
        self.pdf.setFillColor(INK if dark else PAPER)
        self.pdf.rect(0, 0, W, H, stroke=0, fill=1)
        self.text(label, M, 32, CW, 16, colors.HexColor('#a5bbff') if dark else BLUE)
        end = self.text(title, M, 64, CW, 42,
                        colors.white if dark else INK, leading=58)
        if subtitle:
            end = self.text(subtitle, M, end+7, CW, 27,
                            colors.white if dark else INK, leading=39)
        return end+28

    def finish(self, anchor, dark=False):
        self.page += 1
        color = colors.HexColor('#b3bfd1') if dark else MUTED
        self.line(M, 676, CW, colors.HexColor('#405067') if dark else LINE)
        self.text('Jang MoonSu / PORTFOLIO', M, 685, 700, 13, color, bottom=714)
        self.text(f'{self.page:02d} / {self.count:02d}', W-133, 685, 80,
                  13, color, bottom=714)
        self.pdf.linkURL(self.site+'#'+anchor, (M, 6, M+265, 36), relative=0)
        self.pdf.showPage()

    def bullets(self, nodes, x, y, width, size=22, gap=10, bottom=654):
        for node in nodes:
            self.text('•', x, y, 20, size, BLUE, bottom=bottom)
            y = self.text(rich(node), x+25, y, width-25, size, bold=False,
                          markup=True, bottom=bottom)+gap
        return y

    def link(self, title, href, x, y, width, size=19, color=BLUE):
        end = self.text(title, x, y, width, size, color)
        self.pdf.linkURL(href, (x, H-end, x+width, H-y), relative=0)
        return end

    def picture(self, path, x, y, width, height):
        if height <= 0:
            raise ValueError('Image has no available slide area')
        with Image.open(path) as source:
            rgba = source.convert('RGBA')
            white = Image.new('RGBA', rgba.size, 'white')
            white.alpha_composite(rgba)
            scale = min(width/source.width, height/source.height)
            iw, ih = source.width*scale, source.height*scale
            self.pdf.drawImage(ImageReader(white.convert('RGB')),
                               x+(width-iw)/2, H-y-(height-ih)/2-ih, iw, ih)


def build(font_dir, node_modules=None):
    for name, filename in [('Career', 'malgun.ttf'), ('CareerBold', 'malgunbd.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily('Career', normal='Career', bold='CareerBold')
    pdfmetrics.registerFontFamily('CareerBold', normal='CareerBold', bold='CareerBold')
    doc = Document((ROOT / 'index.html').read_text(encoding='utf-8')).root
    projects = doc.select(tag='article', cls='project')
    site = next(n.attrs['href'] for n in doc.select(tag='link')
                if n.attrs.get('rel') == 'canonical')
    # Cover, profile, skills, credentials, index, each project section, contact.
    total = 6 + sum(1+len(p.select(cls='detail-section')) for p in projects)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    deck = Slides(site, total)

    with tempfile.TemporaryDirectory(prefix='portfolio-slides-') as temp:
        temp = Path(temp)
        images, jobs = {}, []
        for img in doc.select(tag='img'):
            source = img.attrs.get('src')
            if not source or source in images:
                continue
            path = ROOT / source
            if path.suffix == '.svg':
                dest = temp / (path.stem+'.png')
                jobs.append({'source': str(path), 'dest': str(dest)})
                images[source] = dest
            else:
                images[source] = path
        manifest = temp/'images.json'
        manifest.write_text(json.dumps(jobs), encoding='utf-8')
        env = os.environ.copy()
        if node_modules:
            env['NODE_PATH'] = str(node_modules)
        subprocess.run(['node', '-e', """
const sharp=require('sharp'),fs=require('node:fs');
const jobs=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
(async()=>{for(const j of jobs) await sharp(j.source,{density:192}).png().toFile(j.dest);})()
.catch(e=>{console.error(e);process.exitCode=1;});
""", str(manifest)], check=True, env=env, cwd=ROOT)

        def image_path(node):
            return images[node.attrs['src']]

        def caption(fig):
            node = fig.one(tag='figcaption')
            spans = node.select(tag='span')
            return rich(spans[0] if spans else node)

        def figure(fig, x, y, width, height, fill=colors.white):
            deck.panel(x, y, width, height, fill)
            nodes = fig.select(tag='img')
            inset, gap = 24, 18
            slot = (width-2*inset-gap*(len(nodes)-1))/len(nodes)
            for i, node in enumerate(nodes):
                deck.picture(image_path(node), x+inset+(slot+gap)*i, y+inset,
                             slot, height-100)
            deck.text(caption(fig), x+24, y+height-66, width-48,
                      18, MUTED, markup=True)

        def facts(node, x, y, width):
            for row in direct(node):
                y = deck.text(row.one(tag='dt').text(), x, y, width, 23, BLUE)+6
                y = deck.bullets(row.one(tag='dd').select(tag='li'), x, y,
                                 width, 21, 7)+11
            return y

        # Match the website's cover, typography, colors, and reading order.
        deck.start('MOONSYU / PORTFOLIO', '')
        deck.text(doc.one(cls='hero').one(cls='eyebrow').text(), M, 137, CW, 20, BLUE)
        title = doc.one(id='hero-title')
        deck.text(''.join(c for c in title.children if isinstance(c, str)),
                  M, 203, CW, 65, leading=84)
        deck.text(title.one(tag='span').text(), M, 287, CW, 65, BLUE, leading=84)
        deck.text(rich(doc.one(cls='hero-description')), M, 405, CW, 25,
                  MUTED, markup=True, leading=43)
        deck.link('프로젝트 보기 →', site+'#projects', M, 556, 280, 23)
        deck.link('GitHub →', 'https://github.com/moonsyu', M+310, 556, 210, 23)
        deck.finish('home')

        y = deck.start('01 / ABOUT', '소개')
        profile = doc.one(cls='profile-heading')
        deck.picture(image_path(profile.one(tag='img')), M, y+12, 122, 148)
        deck.text(profile.one(tag='h3').text(), M+150, y+32, 365, 37)
        deck.text(profile.one(tag='p').text(), M+150, y+93, 365, 23, BLUE)
        deck.text(doc.one(cls='about-copy').text(), M, y+198, 510, 29)
        deck.bullets(doc.one(cls='about-points').select(tag='li'), M, y+260, 495, 23, 17)
        x = 635
        deck.text('경력 및 교육', x, y, W-M-x, 29)
        cy = y+61
        for row in doc.select(cls='timeline-item'):
            deck.line(x, cy-9, W-M-x)
            deck.text(row.one(tag='dt').text(), x, cy, 200, 18, MUTED)
            dd = row.one(tag='dd')
            label = ''.join(c for c in dd.children if isinstance(c, str)).strip()
            end = deck.text(label, x+208, cy, W-M-x-208, 23)
            end = deck.text(dd.one(tag='span').text(), x+208, end+5,
                            W-M-x-208, 19, MUTED)
            cy = max(cy+105, end+25)
        deck.finish('about')

        y = deck.start('01 / ABOUT', '보유 기술 스택')
        gap = 28
        width = (CW-gap)/2
        for i, group in enumerate(doc.select(cls='skill-group')):
            x, top = M+(width+gap)*(i%2), y+250*(i//2)
            deck.panel(x, top, width, 226)
            deck.text(group.one(tag='h3').text(), x+24, top+20, width-48, 26)
            for j, item in enumerate(group.select(tag='li')):
                sx, sy = x+24+(width-48)/2*(j%2), top+81+64*(j//2)
                deck.picture(image_path(item.one(tag='img')), sx, sy, 35, 35)
                deck.text(item.one(tag='span').text(), sx+46, sy+1,
                          (width-48)/2-54, 19, leading=26)
        deck.finish('about')

        y = deck.start('01 / ABOUT', '수상 · 자격 · 어학')
        award_width, gap = 363, 20
        for i, award in enumerate(doc.one(cls='award-list').select(tag='li')):
            x, top = M+(award_width+gap)*(i%2), y+166*(i//2)
            deck.panel(x, top, award_width, 149)
            deck.text(award.one(cls='award-organizer').text(), x+18, top+14,
                      award_width-36, 17, BLUE)
            deck.text(award.one(tag='h4').text(), x+18, top+45,
                      award_width-36, 20, leading=29)
            deck.text(award.one(tag='time').text(), x+18, top+116,
                      award_width-36, 16, MUTED)
        qx, qw = 846, W-M-846
        for i, item in enumerate(doc.one(cls='qualification-list').select(tag='li')):
            top = y+i*250
            deck.panel(qx, top, qw, 232)
            cy = deck.text(item.one(tag='h4').text(), qx+25, top+22, qw-50, 30)+17
            for grade in item.select(cls='qualification-grade'):
                cy = deck.text(grade.text(), qx+25, cy, qw-50, 23, BLUE)+15
            for row in direct(item.one(tag='dl')):
                deck.text(row.one(tag='dt').text(), qx+25, cy, 87, 18, MUTED)
                cy = deck.text(row.one(tag='dd').text(), qx+119, cy,
                               qw-144, 18)+13
        deck.finish('about')

        y = deck.start('02 / SELECTED WORK', '프로젝트')
        for i, item in enumerate(doc.one(cls='project-index').select(tag='a')):
            top = y+166*i
            deck.panel(M, top, CW, 142)
            deck.text(item.one(cls='index-number').text(), M+30, top+38, 85, 32, BLUE)
            deck.text(item.one(tag='strong').text(), M+124, top+25, CW-170, 34)
            deck.text(item.one(tag='small').text(), M+124, top+82, CW-170, 22, MUTED)
            deck.pdf.linkURL(site+item.attrs['href'], (M, H-top-142, W-M, H-top), relative=0)
        deck.finish('projects')

        for project in projects:
            name, anchor = project.one(tag='h3').text(), project.attrs['id']
            y = deck.start(project.one(cls='project-category').text(), name)
            figure(project.one(cls='project-visual'), M, y+8, 640, 480,
                   colors.HexColor('#fff4df' if anchor=='bookies' else '#eaf0f8'))
            desc = project.one(cls='project-description')
            x, width = 737, W-M-737
            cy = deck.text(rich(desc.one(tag='h4')), x, y+18, width, 29,
                           markup=True, leading=44)+22
            cy = deck.text('  |  '.join(n.text() for n in desc.one(cls='project-meta').select(tag='span')),
                           x, cy, width, 19, MUTED)+23
            cy = deck.bullets(desc.one(tag='ul').select(tag='li'), x, cy, width, 21, 13)+12
            deck.line(x, cy, width)
            deck.text(rich(desc.one(cls='techline')), x, cy+15, width,
                      19, BLUE, markup=True, leading=30)
            deck.finish(anchor)

            for section in project.select(cls='detail-section'):
                title = section.one(tag='h4').text()
                label = section.one(cls='label').text()
                y = deck.start(label, name, title)
                architecture = section.select(cls='application-architecture')
                if architecture:
                    fig = architecture[0]
                    deck.panel(M, y-7, CW, 650-y)
                    deck.picture(image_path(fig.one(tag='img')), M+12, y,
                                 CW-24, 596-y)
                    deck.text(caption(fig), M+25, 612, CW-50, 19, MUTED, markup=True)
                elif section.select(cls='case-facts'):
                    fact = section.one(cls='case-facts')
                    fig = section.one(tag='figure')
                    is_measurement = section.attrs['aria-labelledby']=='cons-measurement'
                    fx, ix = (738, M) if is_measurement else (M, 636)
                    fw, iw = (486, 640) if is_measurement else (530, 588)
                    facts(fact, fx, y+6, fw)
                    node = fig.one(tag='img')
                    src = node.attrs['src']
                    if src.endswith('.gif'):
                        # One large source frame keeps the same composition as the web slide.
                        # Motion remains accessible through a real, clickable online link.
                        with Image.open(image_path(node)) as gif:
                            gif.seek(gif.n_frames-1)
                            frame = temp/(anchor+'-demo.png')
                            gif.convert('RGB').save(frame)
                        deck.panel(ix, y, iw, 650-y)
                        deck.picture(frame, ix+20, y+20, iw-40, 541-y)
                        deck.text(caption(fig), ix+24, 569, iw-48, 20, markup=True)
                        deck.link('실행 GIF 보기 →', site+'#'+fig.attrs['id'],
                                  ix+24, 609, iw-48, 19)
                    else:
                        figure(fig, ix, y, iw, 650-y)
                else:
                    cards = direct(section.one(cls='implementation-list'))
                    gap, width = 28, (CW-56)/3
                    for i, card in enumerate(cards):
                        x = M+(width+gap)*i
                        deck.panel(x, y+26, width, 365)
                        deck.text(f'{i+1:02d}', x+26, y+55, width-52, 25, BLUE)
                        deck.text(card.one(tag='h5').text(), x+26, y+119, width-52, 26)
                        deck.bullets(card.select(tag='li'), x+26, y+188, width-52, 22, 22)
                deck.finish(section.attrs['aria-labelledby'])

        y = deck.start('03 / CONTACT', '장문수', '개발 기록과 연락처', dark=True)
        for i, item in enumerate(doc.one(cls='contact-links').select(tag='a')):
            top = y+57+118*i
            spans = item.select(tag='span')
            deck.text(spans[0].text(), M, top, 220, 23, colors.HexColor('#b3bfd1'))
            deck.link(spans[-1].text().replace('↗', '').strip(), item.attrs['href'],
                      M+270, top-3, CW-270, 29, colors.white)
            deck.line(M, top+64, CW, colors.HexColor('#405067'))
        deck.finish('contact', dark=True)
    assert deck.page == total, (deck.page, total)
    deck.pdf.save()
    print(f'Created {OUTPUT} ({total} slides, 16:9, {W} x {H} pt)')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--font-dir', type=Path,
                        default=Path(os.environ.get('WINDIR', 'C:/Windows'))/'Fonts')
    parser.add_argument('--node-modules', type=Path)
    args = parser.parse_args()
    build(args.font_dir, args.node_modules)
