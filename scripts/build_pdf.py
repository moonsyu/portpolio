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
WEB_APP_OUTPUT = ROOT / 'output/pdf/Jang-MoonSu-Web-App-Portfolio.pdf'
INK, BLUE, MUTED, LINE, PAPER = map(colors.HexColor,
    ['#194878', '#195FCE', '#3F6695', '#D5E2F3', '#F7FAFF'])
# PowerPoint widescreen source coordinates; all text remains selectable in the PDF.
W, H = 1600, 900
M, CW = 72, W - 144


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


def web_app_document(doc):
    """Create the requested omission-only edition from the public source."""
    def remove(node, predicate):
        node.children = [c for c in node.children
                         if not isinstance(c, Element) or not predicate(c)]
        for child in direct(node):
            remove(child, predicate)

    # The requested separate edition excludes STM-Simulator completely.
    # CONS remains intact under the user's explicit exception.
    remove(doc, lambda n: n.tag == 'article' and n.attrs.get('id') == 'stm')
    remove(doc.one(cls='project-index'), lambda n: n.tag == 'a' and
           n.attrs.get('href') == '#stm')
    remove(doc, lambda n: 'timeline-item' in n.attrs.get('class', '').split()
           and 'SSAFY' in n.text())
    remove(doc, lambda n: 'skill-group' in n.attrs.get('class', '').split()
           and n.one(tag='h3').text() not in {'백엔드', '데이터 · 배포', '모바일 · 연동'})
    title = doc.one(id='hero-title')
    subtitle = Element('span')
    subtitle.children = ['모바일 연동 · 클라우드 배포']
    title.children = ['Java 백엔드 개발', subtitle]
    doc.one(cls='hero-description').children = [
        'Java 백엔드 개발과 Android·서버 연동 경험', Element('br'),
        'CONS·BOOKIES의 구현 및 문제 해결 기록']
    # Keep the broader profile software-focused; preserve all CONS project pages.
    points = doc.one(cls='about-points')
    bookies_roles = doc.one(id='bookies').one(cls='project-description').one(tag='ul')
    mobile_point = Element('li')
    mobile_point.children = ['Android·서버 연동']
    points.children = [points.select(tag='li')[0], mobile_point, bookies_roles.select(tag='li')[1]]
    for i, number in enumerate(doc.select(cls='index-number'), 1):
        number.children = [f'{i:02d}']
    for i, number in enumerate(doc.select(cls='project-number'), 1):
        number.children = [f'{i:02d}']
    return doc


class Slides:
    def __init__(self, site, count, output=OUTPUT, variant='full'):
        self.pdf = canvas.Canvas(str(output), pagesize=(W, H),
                                 pageCompression=1, invariant=1)
        self.pdf.setTitle('장문수 | '+('Web & App Portfolio' if variant=='web-app' else 'Developer Portfolio'))
        self.pdf.setAuthor('Jang MoonSu')
        self.pdf.setPageSize((W, H))
        self.site, self.count, self.page, self.variant = site, count, 0, variant
        self.legacy = False

    def _legacy(self, *values):
        return tuple(v * 1.25 for v in values) if self.legacy else values

    def box(self, x, y, width, height):
        """Return a PDF annotation rectangle from source-layout coordinates."""
        x, y, width, height = self._legacy(x, y, width, height)
        return (x, H-y-height, x+width, H-y)

    def text(self, value, x, y, width, size=22, color=INK, bold=True,
             leading=None, bottom=None, markup=False):
        leading = leading or size*1.5
        if bottom is None:
            bottom = 654 if self.legacy else 814
        x, y, width, size, leading, bottom = self._legacy(x, y, width, size, leading, bottom)
        style = ParagraphStyle('slide', fontName='CareerBold' if bold else 'Career',
                               fontSize=size, leading=leading,
                               textColor=color, wordWrap='LTR')
        para = Paragraph(value if markup else escape(value), style)
        _, height = para.wrap(width, H)
        if y + height > bottom:
            raise ValueError(f'Slide {self.page+1} overflow at {y+height:.1f}: {value}')
        para.drawOn(self.pdf, x, H-y-height)
        return (y + height) / 1.25 if self.legacy else y + height

    def line(self, x, y, width, color=LINE):
        x, y, width = self._legacy(x, y, width)
        self.pdf.setStrokeColor(color)
        self.pdf.setLineWidth(1)
        self.pdf.line(x, H-y, x+width, H-y)

    def panel(self, x, y, width, height, fill=colors.white, border=LINE):
        x, y, width, height = self._legacy(x, y, width, height)
        self.pdf.setFillColor(fill)
        self.pdf.setStrokeColor(border)
        self.pdf.roundRect(x, H-y-height, width, height, 12, fill=1, stroke=1)

    def start(self, label, title, subtitle=None, dark=False):
        self.pdf.setFillColor(INK if dark else PAPER)
        self.pdf.rect(0, 0, W, H, stroke=0, fill=1)
        x, content_width = (56, 1168) if self.legacy else (M, CW)
        self.text(label, x, 32, content_width, 16, colors.HexColor('#a5bbff') if dark else BLUE)
        end = self.text(title, x, 64, content_width, 42,
                        colors.white if dark else INK, leading=58)
        if subtitle:
            end = self.text(subtitle, x, end+7, content_width, 27,
                            colors.white if dark else INK, leading=39)
        return end+28

    def finish(self, anchor, dark=False):
        self.page += 1
        color = colors.HexColor('#b3bfd1') if dark else MUTED
        fy, fb = (676, 714) if self.legacy else (844, 875)
        self.line(M if not self.legacy else 56, fy, CW if not self.legacy else 1168,
                  colors.HexColor('#405067') if dark else LINE)
        self.text('Jang MoonSu / PORTFOLIO', M if not self.legacy else 56, fy+9,
                  700, 13, color, bottom=fb)
        self.text(f'{self.page:02d} / {self.count:02d}', W-175 if not self.legacy else 1140,
                  fy+9, 120 if not self.legacy else 96, 13, color, bottom=fb)
        self.pdf.bookmarkPage(anchor)
        if self.variant == 'full':
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
        self.pdf.linkURL(href, self.box(x, y, width, end-y), relative=0)
        return end

    def picture(self, path, x, y, width, height):
        x, y, width, height = self._legacy(x, y, width, height)
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


def build(font_dir, node_modules=None, variant='full', output=None):
    for name, filename in [('Career', 'malgun.ttf'), ('CareerBold', 'malgunbd.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily('Career', normal='Career', bold='CareerBold')
    pdfmetrics.registerFontFamily('CareerBold', normal='CareerBold', bold='CareerBold')
    doc = Document((ROOT / 'index.html').read_text(encoding='utf-8')).root
    if variant == 'web-app':
        doc = web_app_document(doc)
    output = output or (WEB_APP_OUTPUT if variant == 'web-app' else OUTPUT)
    projects = doc.select(tag='article', cls='project')
    site = next(n.attrs['href'] for n in doc.select(tag='link')
                if n.attrs.get('rel') == 'canonical')
    # Four profile pages, optional web/app project index, project sections, contact.
    include_index = variant == 'web-app' and len(projects) > 1
    total = 5 + int(include_index) + sum(1+len(p.select(cls='detail-section')) for p in projects)
    output.parent.mkdir(parents=True, exist_ok=True)
    deck = Slides(site, total, output, variant)

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

        # Pages 1–4 mirror the approved PPT-ready profile layouts without a separate cover.
        hero = doc.one(cls='hero')
        profile = hero.one(cls='profile-heading')
        title = doc.one(id='hero-title')
        deck.pdf.setFillColor(PAPER)
        deck.pdf.rect(0, 0, W, H, stroke=0, fill=1)
        deck.panel(72, 116, 390, 575, colors.white)
        deck.picture(image_path(profile.one(tag='img')), 105, 148, 324, 360)
        deck.text(profile.one(tag='h3').text(), 105, 548, 324, 38, INK)
        deck.text(profile.one(tag='p').text(), 105, 612, 324, 28, BLUE)
        if variant == 'web-app':
            deck.text('Java 백엔드 개발', 560, 202, 900, 70, INK, leading=86)
            deck.text(title.one(tag='span').text(), 560, 302, 900, 62, BLUE, leading=78)
            deck.text(doc.one(cls='about-copy').text(), 564, 465, 850, 30, BLUE, leading=46)
            deck.bullets(doc.one(cls='about-points').select(tag='li'), 568, 540, 800, 28, 18, bottom=812)
        else:
            deck.text('백엔드에서', 560, 178, 900, 72, INK, leading=88)
            deck.text(title.one(tag='span').text(), 560, 276, 900, 72, BLUE, leading=88)
            deck.text('연결하는 개발자', 560, 374, 900, 72, INK, leading=88)
            deck.text(doc.one(cls='about-copy').text(), 564, 510, 850, 30, BLUE, leading=46)
            deck.bullets(doc.one(cls='about-points').select(tag='li'), 568, 586, 800, 28, 18, bottom=812)
        deck.finish('home')

        y = deck.start('소개', '경력', '학습과 실무 경험')
        cy = 238
        for row in doc.select(cls='timeline-item'):
            deck.text(row.one(tag='dt').text(), 90, cy, 280, 26, BLUE)
            dd = row.one(tag='dd')
            label = ''.join(c for c in dd.children if isinstance(c, str)).strip()
            deck.text(label, 370, cy, 610, 32, INK)
            deck.text(dd.one(tag='span').text(), 1000, cy+3, 500, 26, MUTED)
            deck.line(72, cy+72, CW)
            cy += 132
        deck.finish('about')

        y = deck.start('소개', '기술', '실제 사용한 도구')
        gap, col_width = 26, (CW-3*26)/4
        for i, group in enumerate(doc.select(cls='skill-group')):
            x, top = M+(col_width+gap)*i, 236
            deck.panel(x, top, col_width, 520, colors.white)
            deck.text(group.one(tag='h3').text(), x+22, top+24, col_width-44, 29, BLUE)
            deck.line(x+22, top+78, col_width-44)
            for j, item in enumerate(group.select(tag='li')):
                sy = top+118+j*88
                deck.picture(image_path(item.one(tag='img')), x+22, sy, 32, 32)
                deck.text(item.one(tag='span').text(), x+68, sy-2, col_width-90, 28, INK)
        deck.finish('skills')

        deck.start('소개', '수상 · 자격', '수상 이력과 자격 정보')
        award_width, qx, qw = 980, 1120, 408
        deck.text('수상', M, 220, award_width, 29, BLUE)
        deck.text('자격 · 어학', qx, 220, qw, 29, BLUE)
        for i, award in enumerate(doc.one(cls='award-list').select(tag='li')):
            top = 278 + i*87
            deck.text(award.one(cls='award-organizer').text(), M, top, 720, 22, MUTED)
            deck.text(award.one(tag='time').text(), M+810, top, 170, 22, MUTED)
            title = award.one(tag='h4')
            plain_title = ''.join(
                '' if isinstance(c, Element) and 'award-grade' in c.attrs.get('class', '').split()
                else (c.text() if isinstance(c, Element) else c) for c in title.children).strip()
            grade = next((n.text() for n in title.select(cls='award-grade')), '')
            title_end = deck.text(escape(plain_title)+' <font color="#195FCE">'+escape(grade)+'</font>',
                                 M, top+34, award_width, 27, INK, leading=36, markup=True)
            if title_end > top+70:
                raise ValueError('Award title must fit on one line: '+plain_title)
            deck.line(M, top+77, award_width)
        for i, item in enumerate(doc.one(cls='qualification-list').select(tag='li')):
            top, height = (270, 190) if i == 0 else (486, 280)
            deck.panel(qx, top, qw, height, colors.white)
            cy = deck.text(item.one(tag='h4').text(), qx+24, top+24, qw-48, 31, INK)+16
            for grade in item.select(cls='qualification-grade'):
                grade_name = ''.join(c for c in grade.children if isinstance(c, str)).strip()
                cy = deck.text(grade_name, qx+24, cy, qw-48, 28, BLUE)+5
                cy = deck.text(grade.one(tag='span').text(), qx+24, cy, qw-48, 26, MUTED)+15
            for row in direct(item.one(tag='dl')):
                label_end = deck.text(row.one(tag='dt').text(), qx+24, cy, 100, 22, MUTED)
                value_end = deck.text(row.one(tag='dd').text(), qx+132, cy, qw-156, 22, BLUE)
                cy = max(label_end, value_end)+8
            if cy > top+height-16:
                raise ValueError('Qualification card needs more height: '+item.one(tag='h4').text())
        deck.finish('credentials')

        # Existing project-page composition was authored at 1280×720; retain its
        # geometry by scaling it on the 1600×900 PDF canvas.
        deck.legacy = True
        legacy_m, legacy_w, legacy_h, legacy_cw = 56, 1280, 720, 1168

        if include_index:
            y = deck.start('02 / SELECTED WORK', '프로젝트')
            for i, item in enumerate(doc.one(cls='project-index').select(tag='a')):
                top = y+166*i
                deck.panel(legacy_m, top, legacy_cw, 142)
                deck.text(item.one(cls='index-number').text(), legacy_m+30, top+38, 85, 32, BLUE)
                deck.text(item.one(tag='strong').text(), legacy_m+124, top+25, legacy_cw-170, 34)
                deck.text(item.one(tag='small').text(), legacy_m+124, top+82, legacy_cw-170, 22, MUTED)
                rect = deck.box(legacy_m, top, legacy_cw, 142)
                if variant=='web-app':
                    deck.pdf.linkAbsolute('', item.attrs['href'][1:], rect)
                else:
                    deck.pdf.linkURL(site+item.attrs['href'], rect, relative=0)
            deck.finish('projects')

        for project in projects:
            name, anchor = project.one(tag='h3').text(), project.attrs['id']
            y = deck.start(project.one(cls='project-category').text(), name)
            figure(project.one(cls='project-visual'), legacy_m, y+8, 640, 480,
                   colors.HexColor('#fff4df' if anchor=='bookies' else '#eaf0f8'))
            desc = project.one(cls='project-description')
            x, width = 737, legacy_w-legacy_m-737
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
                    deck.panel(legacy_m, y-7, legacy_cw, 650-y)
                    deck.picture(image_path(fig.one(tag='img')), legacy_m+12, y,
                                 legacy_cw-24, 596-y)
                    deck.text(caption(fig), legacy_m+25, 612, legacy_cw-50, 19, MUTED, markup=True)
                elif section.select(cls='case-facts'):
                    fact = section.one(cls='case-facts')
                    fig = section.one(tag='figure')
                    is_measurement = section.attrs['aria-labelledby']=='cons-measurement'
                    fx, ix = (738, legacy_m) if is_measurement else (legacy_m, 636)
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
                    gap, width = 28, (legacy_cw-56)/3
                    for i, card in enumerate(cards):
                        x = legacy_m+(width+gap)*i
                        deck.panel(x, y+26, width, 365)
                        deck.text(f'{i+1:02d}', x+26, y+55, width-52, 25, BLUE)
                        deck.text(card.one(tag='h5').text(), x+26, y+119, width-52, 26)
                        deck.bullets(card.select(tag='li'), x+26, y+188, width-52, 22, 22)
                deck.finish(section.attrs['aria-labelledby'])

        y = deck.start('03 / CONTACT', '장문수', '개발 기록과 연락처')
        for i, item in enumerate(doc.one(cls='contact-links').select(tag='a')):
            top = y+57+118*i
            spans = item.select(tag='span')
            deck.text(spans[0].text(), legacy_m, top, 220, 23, MUTED)
            deck.link(spans[-1].text().replace('↗', '').strip(), item.attrs['href'],
                      legacy_m+270, top-3, legacy_cw-270, 29, BLUE)
            deck.line(legacy_m, top+64, legacy_cw)
        deck.finish('contact')
    assert deck.page == total, (deck.page, total)
    deck.pdf.save()
    print(f'Created {output} ({total} slides, 16:9, {W} x {H} pt)')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--font-dir', type=Path,
                        default=Path(os.environ.get('WINDIR', 'C:/Windows'))/'Fonts')
    parser.add_argument('--node-modules', type=Path)
    parser.add_argument('--variant', choices=['all', 'full', 'web-app'], default='all')
    args = parser.parse_args()
    for variant in (['full', 'web-app'] if args.variant=='all' else [args.variant]):
        build(args.font_dir, args.node_modules, variant)
