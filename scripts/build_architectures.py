"""Build self-contained, editable application architecture SVGs (Python stdlib)."""
from pathlib import Path
from html import escape
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'architecture'
ICONS = OUT / 'icons'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


class Diagram:
    def __init__(self, title, description, height=800):
        self.title, self.description, self.height = title, description, height
        self.parts, self.used = [], set()

    def text(self, x, y, value, size=20, bold=False, anchor='middle', fill='#20252c'):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{fill}">{escape(value)}</text>')

    def box(self, x, y, w, h, title=None, fill='#fff', stroke='#20252c', width=3):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
        if title:
            self.text(x+w/2, y+34, title, 23, True)

    def icon(self, name, x, y, size=64, color='#20252c'):
        self.used.add(name)
        self.parts.append(f'<use href="#icon-{name}" x="{x}" y="{y}" width="{size}" height="{size}" color="{color}"/>')

    def node(self, icon, x, y, title, subtitle=None, size=64, color='#20252c'):
        self.icon(icon, x-size/2, y, size, color)
        self.text(x, y+size+29, title, 22, True)
        if subtitle:
            for i, line in enumerate(subtitle if isinstance(subtitle, list) else [subtitle]):
                self.text(x, y+size+56+25*i, line, 18, fill='#475467')

    def arrow(self, points, label=None, label_xy=None, both=False, dashed=False):
        d='M '+' L '.join(f'{x} {y}' for x,y in points)
        self.parts.append(f'<path d="{d}" fill="none" stroke="#20252c" stroke-width="2.8" stroke-linejoin="round" marker-end="url(#arrow)"'+(' marker-start="url(#arrow-start)"' if both else '')+(' stroke-dasharray="7 6"' if dashed else '')+'/>')
        if label:
            x,y=label_xy
            width=sum(10 if ord(c)<128 else 17 for c in label)+16
            self.parts.append(f'<rect x="{x-width/2}" y="{y-18}" width="{width}" height="25" rx="3" fill="#fff"/>')
            self.text(x,y,label,18)

    def save(self, filename):
        symbols=[]
        for name in sorted(self.used):
            tree=ET.fromstring((ICONS/f'{name}.svg').read_text(encoding='utf-8'))
            view=tree.attrib.get('viewBox','0 0 24 24')
            attrs=' '.join(f'{k}="{escape(v)}"' for k,v in tree.attrib.items() if k not in ['width','height','viewBox','class'] and not k.startswith('{'))
            inner=''.join(ET.tostring(child,encoding='unicode') for child in tree)
            inner=re.sub(r'id="([^"]+)"',lambda m:f'id="{name}-{m[1]}"',inner)
            inner=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{name}-{m[1]})',inner)
            symbols.append(f'<symbol id="icon-{name}" viewBox="{view}"><g {attrs}>{inner}</g></symbol>')
        svg=f'''<svg xmlns="{NS}" width="1320" height="{self.height}" viewBox="0 0 1320 {self.height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.description)}</desc>
<!-- Technology icons: Devicon (MIT); functional icons: Lucide (ISC). See accompanying license files. -->
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 Z" fill="#20252c"/></marker><marker id="arrow-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 10 0 L 0 5 L 10 10 Z" fill="#20252c"/></marker>{''.join(symbols)}</defs>
<rect width="1320" height="{self.height}" fill="#fff"/>
<g font-family="Segoe UI, Apple SD Gothic Neo, Malgun Gothic, sans-serif">{''.join(self.parts)}</g></svg>'''
        ET.fromstring(svg)
        (OUT/filename).write_text(svg,encoding='utf-8')
        return self.used


def stm():
    d=Diagram('STM-Simulator 애플리케이션 아키텍처','사용자의 회로와 코드 편집, Renderer의 상태 관리와 지원 C/HAL 동작 모델, Preload IPC, Node.js Main의 파일 입출력, localStorage 자동 저장',800)
    d.icon('electron',518,25,48);d.text(580,58,'Electron Desktop Application',27,True,anchor='start')
    d.node('user-round',82,241,'사용자',size=68)
    d.box(200,114,450,355,'Renderer · JavaScript')
    for name,x in [('html5',263),('css3',366),('javascript',469)]:d.icon(name,x,174,55)
    d.text(425,260,'HTML · CSS · SVG 화면 / 프로젝트 상태',20)
    d.node('network',327,302,'회로·설정',size=54,color='#2355de')
    d.node('microchip',524,302,'C/HAL 동작 모델',size=54,color='#2355de')
    d.arrow([(384,332),(458,332)],both=True)
    d.box(758,210,176,178,'Preload')
    d.node('network',846,265,'브리지 · IPC',size=48)
    d.box(1042,114,245,355,'Main · Node.js')
    d.icon('nodejs',1132,174,65)
    d.node('folder-open',1164,290,'파일 입출력',['대화상자 · 검증','읽기 · 쓰기'],size=53)
    d.arrow([(126,281),(194,281)],'편집',(160,252))
    d.arrow([(657,281),(752,281)],'요청·응답',(704,246),both=True)
    d.arrow([(940,281),(1036,281)],'IPC',(988,250),both=True)
    d.box(260,579,326,159)
    d.node('save',423,600,'localStorage','자동 저장 (JSON 문자열)',size=47,color='#2355de')
    d.arrow([(423,475),(423,572)],'저장·복원',(423,531),both=True)
    d.box(1000,579,287,159)
    d.node('file-code',1144,600,'프로젝트 파일','.stm32lab · .ioc · C · CSV',size=47)
    d.arrow([(1164,475),(1164,572)],'파일 읽기·쓰기',(1164,531),both=True)
    d.text(660,785,'STM-Simulator · 지원 범위의 C/HAL 동작을 모델링한 학습용 애플리케이션',17,fill='#667085')
    return d.save('stm-application.svg')


def cons():
    d=Diagram('CONS 애플리케이션 아키텍처','BLE 비콘 신호를 Android에서 수집하고 위치를 계산. Retrofit으로 Spring Boot 서버와 비콘 좌표 교환. Android는 Unity AR 길안내와 사용자 좌표 연동, Room에서 역·노선도 조회. 서버는 MySQL에 비콘 정보 저장.',850)
    d.box(254,84,518,627,'Mobile Application')
    d.node('user-round',91,165,'사용자',size=62)
    d.node('bluetooth',91,395,'BLE Beacon','RSSI 신호',size=64,color='#2355de')
    d.box(288,171,449,220,fill='#f8fafc',stroke='#c8d0dc',width=1.6)
    d.icon('android',318,207,76)
    d.text(437,230,'Android 앱',24,True,anchor='start')
    d.text(437,268,'BLE 수집 · 실내 위치 추정',19,anchor='start')
    d.text(437,305,'Retrofit · 서버 데이터 연동',19,anchor='start')
    d.arrow([(136,215),(280,215)],'앱 사용',(208,190))
    d.arrow([(132,433),(214,433),(214,310),(280,310)],'BLE / RSSI',(205,415))
    d.node('unity',399,515,'Unity','AR 길안내',size=63)
    d.node('database',623,515,'Room','역·노선도 정보',size=63,color='#299c72')
    d.arrow([(399,397),(399,503)],'사용자 좌표',(399,452),both=True)
    d.arrow([(623,397),(623,503)],'역·노선도 조회',(623,452),both=True)
    d.box(944,138,316,230,'Server Application')
    d.node('spring',1102,200,'Spring Boot','비콘 좌표 API',size=62)
    d.arrow([(778,260),(938,260)],'Retrofit / REST',(858,219),both=True)
    d.text(858,299,'비콘 좌표',18)
    d.box(965,501,274,194,'Data Storage')
    d.node('mysql',1102,551,'MySQL','비콘 정보',size=60)
    d.arrow([(1102,374),(1102,495)],'조회·저장',(1102,437),both=True)
    d.node('globe',513,749,'유실물 찾기',size=38)
    d.arrow([(513,397),(513,741)],'Internet 연결',(513,703))
    return d.save('cons-application.svg')


def bookies():
    d=Diagram('BOOKIES 애플리케이션 아키텍처','Web Browser와 Android App이 Spring Boot Web Service에 연결. Web은 JPA/JDBC로 Oracle RDS와, 파일 연동으로 S3와 연결. Packager는 S3에 암호화 파일을 저장하고, Distributor는 S3에서 파일을 받아 DRM Agent Client에 전달.',900)
    d.box(20,170,210,440,'Clients')
    d.node('globe',125,232,'Web Browser',size=65,color='#2355de')
    d.node('android',125,417,'Android App',size=65)
    d.box(330,80,965,430,'Application Services')
    d.icon('amazonwebservices',357,120,63)
    d.text(433,153,'EC2 · Ubuntu 22.04',18,anchor='start',fill='#667085')
    d.box(365,188,310,265,'Web Service',fill='#f8fafc',stroke='#c8d0dc',width=1.6)
    d.icon('java',432,250,64);d.icon('spring',546,250,64)
    d.text(520,356,'Java · Spring Boot',22,True)
    d.text(520,396,'WAR 애플리케이션',19,fill='#475467')
    d.node('package',850,237,'Packager','전자책 패키징',size=64)
    d.node('server',1140,237,'Distributor','전자책 전달',size=64)
    d.arrow([(237,271),(359,271)],'Web',(290,248),both=True)
    d.arrow([(237,460),(286,460),(286,367),(359,367)],'REST API',(283,419),both=True)
    d.box(350,680,280,180,'Database')
    d.node('oracle',490,728,'Oracle RDS','Oracle DB 19c',size=60)
    d.arrow([(480,459),(480,674)],'JPA / JDBC',(480,607),both=True)
    d.box(725,680,285,180,'Object Storage')
    d.node('cloud',867,728,'Amazon S3','암호화 전자책',size=60,color='#349447')
    d.arrow([(605,459),(605,600),(785,600),(785,674)],'파일 연동',(660,592),both=True)
    d.arrow([(850,367),(850,674)],'암호화 파일 저장',(850,559))
    d.arrow([(953,674),(953,557),(1140,557),(1140,367)],'파일 조회',(1046,549))
    d.box(1060,680,235,180,'Client')
    d.node('book-open',1177,731,'DRM Agent Client',size=57)
    d.arrow([(1200,269),(1260,269),(1260,648),(1177,648),(1177,674)],'전자책 전달',(1250,612))
    return d.save('bookies-application.svg')


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    used=stm() | cons() | bookies()
    print('Built 3 architecture SVGs; icons:', ', '.join(sorted(used)))
