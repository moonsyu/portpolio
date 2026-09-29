"""Vector design-review boards with exact Korean copy and existing assets.

Text is outlined using SIL OFL fonts so PNGs do not depend on host fallback fonts.
These are static UI comps, not browser captures or new project evidence.
"""
from pathlib import Path
from html import escape
import base64
import json
import io
import mimetypes
import os
import re
import urllib.request
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/design-review'
FONTS = Path(os.environ.get('PORTFOLIO_DESIGN_FONTS', str(ROOT.parent / 'portpolio-work/design-fonts')))


class Face:
    def __init__(self, filename, weight):
        font = TTFont(FONTS / filename)
        self.units = font['head'].unitsPerEm
        self.map = font.getBestCmap()
        self.glyphs = font.getGlyphSet(location={'wght': weight})
        self.key = f'{Path(filename).stem}-{weight}'


_faces = {}
def face(c, weight):
    family = 'Manrope.ttf' if ord(c) < 127 else 'NotoSansKR.ttf'
    key = (family, weight)
    if key not in _faces:
        _faces[key] = Face(family, weight)
    return _faces[key]


def width(value, size=24, weight=600):
    return sum(face(c, weight).glyphs[face(c, weight).map.get(ord(c), '.notdef')].width
               / face(c, weight).units * size for c in value)


class Board:
    def __init__(self, filename, title, height, bg='#FFFFFF', width=1600):
        self.filename, self.title, self.height, self.width = filename, title, height, width
        self.parts, self.defs, self.glyph_ids, self.texts = [], [], {}, []
        self.rect(0, 0, width, height, bg)

    def rect(self, x, y, w, h, fill, radius=0, stroke=None, sw=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')

    def line(self, x1, y1, x2, y2, color='#DDD6EE', sw=1):
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{sw}"/>')

    def text(self, x, y, value, size=24, weight=600, color='#211C37', anchor='start'):
        self.texts.append(value)
        if anchor == 'end': x -= width(value, size, weight)
        elif anchor == 'middle': x -= width(value, size, weight)/2
        rendered = []
        for c in value:
            f = face(c, weight)
            name = f.map.get(ord(c), '.notdef')
            key = (f.key, name)
            if key not in self.glyph_ids:
                ident = 'g' + str(len(self.glyph_ids))
                self.glyph_ids[key] = ident
                pen = SVGPathPen(f.glyphs)
                f.glyphs[name].draw(pen)
                self.defs.append(f'<path id="{ident}" d="{pen.getCommands()}"/>')
            scale = size / f.units
            rendered.append(f'<use href="#{self.glyph_ids[key]}" transform="translate({x:.3f} {y+size*.92:.3f}) scale({scale:.7f} {-scale:.7f})"/>')
            x += f.glyphs[name].width * scale
        self.parts.append(f'<g fill="{color}" aria-label="{escape(value)}">'+''.join(rendered)+'</g>')
        return y+size*1.4

    def para(self, x, y, value, max_width, size=24, weight=600, color='#211C37', leading=None):
        leading = leading or size*1.55
        for paragraph in value.split('\n'):
            line = ''
            for word in paragraph.split(' '):
                candidate = (line+' '+word).strip()
                if line and width(candidate,size,weight)>max_width:
                    self.text(x,y,line,size,weight,color);y+=leading;line=word
                else: line=candidate
            if line:self.text(x,y,line,size,weight,color);y+=leading
        return y

    def bullets(self, x, y, values, max_width, size=24, weight=600, color='#211C37', gap=10):
        for value in values:
            self.rect(x,y+size*.57,5,5,color,2.5)
            y = self.para(x+22,y,value,max_width-22,size,weight,color)+gap
        return y

    def image(self, path, x, y, w, h=None, radius=0, fit='meet'):
        path = Path(path)
        if not path.is_absolute(): path=ROOT/path
        if h is None:
            if path.suffix == '.svg':
                original = path.read_text(encoding='utf-8')
                vb = re.search(r'viewBox="([^"]+)"',original).group(1).split()
                h=w*float(vb[3])/float(vb[2])
            else:
                iw,ih=Image.open(path).size;h=w*ih/iw
        # librsvg does not decode WebP embedded in SVG. Preserve its pixels in PNG.
        if path.suffix.lower() == '.webp':
            buffer = io.BytesIO()
            with Image.open(path) as raster:
                raster.save(buffer, format='PNG')
            mime, data = 'image/png', buffer.getvalue()
        else:
            mime, data = mimetypes.guess_type(path)[0] or 'image/png', path.read_bytes()
        uri = 'data:'+mime+';base64,'+base64.b64encode(data).decode()
        clip=''
        if radius:
            cid=f'clip{len(self.defs)}'
            self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}"/></clipPath>')
            clip=f' clip-path="url(#{cid})"'
        self.parts.append(f'<image href="{uri}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid {fit}"{clip}/>')
        return y+h

    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        p=OUT/(self.filename+'.svg')
        p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img"><title>{escape(self.title)}</title><desc>소개부터 STM-Simulator까지의 정적 디자인 비교 시안. 기존 실제 화면과 내용 사용.</desc><defs>'+''.join(self.defs)+'</defs>'+''.join(self.parts)+'</svg>',encoding='utf-8')
        (OUT/(self.filename+'.text.json')).write_text(json.dumps(self.texts,ensure_ascii=False,indent=2),encoding='utf-8')
        print(p)


TIMELINE = [
    ('2026.07 — 현재','SSAFY 16기 · 임베디드 트랙','삼성청년SW·AI아카데미'),
    ('2025.06 — 2026.03','주식회사 유더블유에스','Java 백엔드 · Quantum Computing TFT'),
    ('2024.09 — 2025.03','SK Shieldus Rookies','모의해킹 · 클라우드 보안 과정 수료'),
    ('2019.03 — 2025.02','한신대학교','컴퓨터공학부')]
SKILLS = [
    ('백엔드',[('java','Java'),('spring','Spring Boot'),('database','JPA / JDBC'),('network','REST API')]),
    ('데이터 · 배포',[('oracle','Oracle'),('amazonwebservices','AWS EC2 / RDS / S3'),('linux','Linux'),('docker','Docker')]),
    ('모바일 · 연동',[('android','Android'),('bluetooth','BLE'),('network','Retrofit'),('unity','Unity 연동')]),
    ('학습 도구 · 임베디드 학습',[('electron','Electron'),('javascript','JavaScript'),('c','C'),('microchip','STM32 HAL 학습')])]
AWARDS = [
    ('2025.03.13','SK Shieldus Rookies','슈퍼루키상','금상'),
    ('2024.11.19','한신대학교 SW교육센터','2024 혁신 AI·SW페스티벌 캡스톤디자인','동상'),
    ('2024.11.08','한국디지털콘텐츠학회','2024 추계종합학술대회 대학생 논문경진대회','은상'),
    ('2024.06.29','한국디지털콘텐츠학회','2024 하계종합학술대회 대학생 논문경진대회','은상'),
    ('2023.11.14','한신대학교 컴퓨터공학부','제29회 소프트웨어공모전','은상'),
    ('2022.11.15','한신대학교 컴퓨터공학부','제28회 소프트웨어공모전','동상')]
ABOUT = ['Java 기반 백엔드 서버 개발','Android·서버·센서 데이터 연동','IoT·하드웨어 영역으로 학습과 구현 확장']
STM_POINTS = ['회로 편집과 주변장치 설정 기능 구현','지원 범위의 C/HAL 동작 모델과 장치 상태 연동','HAL 예제에서 설정·회로를 함께 확인하는 실습 환경']
OLD = ['핀·주변장치 설정과 코드 작성 도구를 각각 확인','핀맵과 회로 배선 조건을 대조하며 실행 준비']
IMPROVED = ['설정과 배선을 오가던 확인 흐름을 하나의 작업 화면으로 통합','지원 C/HAL 동작 모델과 회로 상태를 연결해 예제 실행 결과 확인']
UART = [('문제','특정 입력 시점에서 UART 에코의 일부 문자 누락'),('원인','µs → ms → µs 변환 오차로 수신 시점 오판'),('해결','기존 송신 기준의 허용 오차를 수신 판정에도 적용'),('회귀 검증','입력 시점·baud·tick을 교차한 24개 조건 검증')]


def qualification(b,x,y,w,color='#6845D7',ink='#211C37',surface='#F2EEFF'):
    b.rect(x,y,w,200,surface,16)
    b.text(x+28,y+26,'정보처리기사',30,750,ink)
    b.text(x+28,y+84,'한국산업인력공단',22,600,ink)
    b.text(x+28,y+126,'취득일  2024.10.02',22,650,color)
    b.rect(x,y+222,w,232,surface,16)
    b.text(x+28,y+248,'OPIc',30,750,ink)
    b.text(x+28,y+299,'IL',40,800,color)
    b.text(x+98,y+311,'Intermediate Low',22,650,ink)
    b.text(x+28,y+381,'취득일  2026.09.14',22,650,color)


def icon(b, name,x,y,size=34):
    b.image(f'assets/architecture/icons/{name}.svg',x,y,size,size)


def provenance_png(path):
    im=Image.open(path)
    info=PngImagePlugin.PngInfo()
    info.add_text('Description','Code-rendered portfolio design comp, not a browser screenshot. Existing portfolio content and screenshots; no new project evidence.')
    info.add_text('Source','moonsyu/portpolio at 47bd953; generated SVG and scripts in output/design-review and scripts; Noto Sans KR and Manrope under SIL OFL 1.1.')
    im.save(path,pnginfo=info,optimize=True)
