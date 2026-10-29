"""Render the application architecture diagrams designed in Figma as SVG.

Figma source: https://www.figma.com/design/PMTeokQEzCz2eW6rMRTKKF (page "Architecture").
Coordinates, colors and labels match the Figma frames one to one, so the site
SVGs can be regenerated without a Figma export. Python stdlib only.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'architecture'
BLUE, INK, MUTED, LINE = '#2355de', '#172538', '#5b687a', '#3b4656'
FONT = "'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"
ZONES = {
    'mine': ('#f3f6ff', BLUE, None, 2),
    'team': ('#f6f7f9', '#a3adbb', '8 6', 1.5),
    'plain': ('#f8fafc', '#d5dde8', None, 1.5),
}
CARD_STROKE = {'mine': ('#7d9be8', 2, None), 'team': ('#a3adbb', 1.5, '6 5'), 'ext': ('#c3cede', 1.5, None)}


def load_icons():
    icons = {}
    for path in sorted((OUT / 'icons').glob('*.svg')):
        text = path.read_text(encoding='utf-8')
        box = re.search(r'viewBox="([^"]+)"', text).group(1)
        root = re.search(r'<svg([^>]*)>', text).group(1)
        attrs = ' '.join(re.findall(r'(?:fill|stroke|stroke-width|stroke-linecap|stroke-linejoin)="[^"]*"', root))
        inner = re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', text, flags=re.S)
        icons[path.stem] = (box, f'<g {attrs}>{inner}</g>' if attrs else inner)
    for path in OUT.glob('*.svg'):
        for m in re.finditer(r'<symbol id="icon-([a-z0-9-]+)" viewBox="([^"]+)">(.*?)</symbol>', path.read_text(encoding='utf-8'), re.S):
            icons.setdefault(m.group(1), (m.group(2), m.group(3)))
    return icons


ICONS = load_icons()


def text_width(value, size):
    return sum(size * (1.0 if ord(c) > 0x2e80 else 0.56) for c in value)


class Diagram:
    def __init__(self, title, desc, height):
        self.title, self.desc, self.height = title, desc, height
        self.parts, self.used = [], set()

    def text(self, x, y, value, size, weight=400, fill=INK, anchor='middle'):
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(value)}</text>')

    def pill(self, label, cx, cy, fill='#fff', color=LINE, size=13, weight=500, radius=6):
        w = text_width(label, size) + 16
        self.parts.append(f'<rect x="{cx - w / 2:.1f}" y="{cy - 11:.1f}" width="{w:.1f}" height="22" rx="{radius}" fill="{fill}"/>')
        self.text(cx, cy + size * 0.36, label, size, weight, color)

    def zone(self, x, y, w, h, label, kind, badge=None):
        fill, stroke, dash, width = ZONES[kind]
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        self.text(x + 22, y + 30, label, 15, 700, BLUE if kind == 'mine' else MUTED, 'start')
        if badge:
            bw = text_width(badge, 12) + 20
            self.parts.append(f'<rect x="{x + w - 18 - bw:.1f}" y="{y + 14}" width="{bw:.1f}" height="22" rx="11" fill="{BLUE if kind == "mine" else "#e3e8ef"}"/>')
            self.text(x + w - 18 - bw / 2, y + 29.5, badge, 12, 700, '#fff' if kind == 'mine' else MUTED)

    def card(self, x, y, w, h, icons, title, sub, kind, tag=None):
        stroke, width, dash = CARD_STROKE[kind]
        if tag:
            stroke, width = BLUE, 3
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fff" stroke="{stroke}" stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        if tag:
            self.pill(tag, x + w / 2, y, BLUE, '#fff', 12, 700, 11)
        lines = sub.split('\n') if sub else []
        block = 40 + 6 + 23 + (6 + 17.5 * len(lines) if lines else 0)
        top = y + (h - block) / 2
        row = 40 * len(icons) + 10 * (len(icons) - 1)
        for i, name in enumerate(icons):
            self.used.add(name)
            self.parts.append(f'<use href="#icon-{name}" x="{x + w / 2 - row / 2 + i * 50:.1f}" y="{top:.1f}" width="40" height="40"/>')
        self.text(x + w / 2, top + 46 + 17, title, 17, 700)
        for i, line in enumerate(lines):
            self.text(x + w / 2, top + 75 + 13 + 17.5 * i, line, 13, 400, MUTED)

    def arrow(self, pts, label=None, at=None, both=False, head=True, key=False):
        d = 'M ' + ' L '.join(f'{px} {py}' for px, py in pts)
        end, start = ('arrow-key', 'arrow-key-start') if key else ('arrow', 'arrow-start')
        markers = (f' marker-end="url(#{end})"' if head else '') + (f' marker-start="url(#{start})"' if both and head else '')
        self.parts.append(f'<path d="{d}" fill="none" stroke="{BLUE if key else LINE}" stroke-width="{3.5 if key else 2}" stroke-linejoin="round"{markers}/>')
        if label:
            self.pill(label, *at, color=BLUE if key else LINE, weight=700 if key else 500)

    def note(self, label, cx, cy):
        self.pill(label, cx, cy, '#fdf0f4', '#b4446c', 12, 700, 11)

    def legend(self, x, y, key=False):
        if key:
            self.parts.append(f'<path d="M {x} {y + 9} L {x + 26} {y + 9}" stroke="{BLUE}" stroke-width="3.5"/>')
            self.text(x + 34, y + 14, '핵심 연동 구간', 13, 500, MUTED, 'start')
            x += 34 + text_width('핵심 연동 구간', 13) + 22
        for kind, label in (('mine', '내 담당'), ('team', '팀원 구현'), ('ext', '외부 서비스·저장소')):
            stroke, _, dash = CARD_STROKE[kind] if kind != 'mine' else (BLUE, 0, None)
            fill = '#f3f6ff' if kind == 'mine' else '#fff'
            self.parts.append(f'<rect x="{x}" y="{y + 2}" width="22" height="14" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"' + (' stroke-dasharray="4 3"' if dash else '') + '/>')
            self.text(x + 30, y + 14, label, 13, 500, MUTED, 'start')
            x += 30 + text_width(label, 13) + 22

    def save(self, filename):
        defs = ['<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#3b4656"/></marker>',
                '<marker id="arrow-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 Z" fill="#3b4656"/></marker>',
                f'<marker id="arrow-key" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/></marker>',
                f'<marker id="arrow-key-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M10 0 L0 5 L10 10 Z" fill="{BLUE}"/></marker>']
        for name in sorted(self.used):
            box, inner = ICONS[name]
            defs.append(f'<symbol id="icon-{name}" viewBox="{box}">{inner.replace("currentColor", BLUE)}</symbol>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="{self.height}" viewBox="0 0 1320 {self.height}" role="img" aria-labelledby="title desc" font-family="{FONT}">\n'
               f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.desc)}</desc>\n'
               '<!-- Designed in Figma (PMTeokQEzCz2eW6rMRTKKF). Technology icons: Devicon (MIT); functional icons: Lucide (ISC). -->\n'
               f'<defs>{"".join(defs)}</defs>\n<rect width="1320" height="{self.height}" fill="#fff"/>\n' + '\n'.join(self.parts) + '\n</svg>\n')
        (OUT / filename).write_text(svg, encoding='utf-8')


def stm():
    d = Diagram('STM-Simulator 애플리케이션 아키텍처', 'Electron 앱의 격리된 Renderer에서 IDE 작업 화면과 회로 편집을 제공하고, C 인터프리터 회로 시뮬레이터와 Cortex-M4 펌웨어 에뮬레이터가 같은 회로 모델을 구동. Preload의 제한된 IPC로 Main 프로세스가 프로젝트 파일 저장, ARM GCC·GDB 도구, GitHub Release 자동 업데이트를 처리.', 880)
    d.zone(230, 40, 830, 780, 'Electron 앱 · Windows 포터블 EXE', 'mine', '1인 · AI 코딩 도구 협업')
    d.zone(260, 90, 760, 530, 'Renderer · contextIsolation · sandbox', 'plain')
    d.card(40, 130, 170, 130, ['user-round'], 'STM32 학습자', '보드 없이 실습', 'ext')
    d.card(290, 140, 330, 110, ['file-code'], 'IDE 작업 화면', 'Monaco 편집기 · 명령 팔레트 · 장치 Docs', 'mine')
    d.card(660, 140, 330, 110, ['network'], '회로 편집', '부품 · 배선 · 핀 계산 · draft 검증', 'mine')
    d.card(290, 310, 330, 130, ['c'], '회로 시뮬레이터', 'HAL C 소스 해석 · 컴파일 없음\nNVIC · DMA · 회로 검사', 'mine')
    d.card(660, 310, 330, 130, ['microchip'], '펌웨어 에뮬레이터', 'ARM ELF · Cortex-M4 명령어 실행\nSTM32F446 · F103 주변장치', 'mine')
    d.card(475, 480, 330, 110, ['microchip'], '회로 모델', '빵판 · 부품 · 배선 · 전압 · 전류 계산', 'mine')
    d.card(290, 660, 270, 110, ['shield-check'], 'Preload', '제한된 IPC만 노출', 'mine')
    d.card(640, 650, 350, 130, ['electron'], 'Main 프로세스', '파일 저장 트랜잭션 · 진단 JSONL\n네이티브 도구 실행 · 업데이트', 'mine')
    d.card(1100, 315, 190, 120, ['terminal'], 'ARM GCC · GDB', 'OpenOCD · ST-LINK\n실물 보드 기록', 'ext')
    d.card(1100, 490, 190, 120, ['save'], '프로젝트 파일', '.stm32lab · 폴더 저장\n자동 저장 v2', 'ext')
    d.card(1100, 650, 190, 120, ['git-branch'], 'GitHub Release', 'EXE · ZIP · SHA256\n자동 업데이트', 'ext')
    d.arrow([(210, 195), (290, 195)], '코드 · 회로 편집', (250, 171))
    d.arrow([(455, 250), (455, 310)], 'main.c 해석', (455, 280))
    d.arrow([(990, 195), (1005, 195), (1005, 535), (805, 535)], '회로 반영', (1005, 460))
    d.arrow([(455, 440), (455, 535), (475, 535)], 'GPIO 변화', (455, 490))
    d.arrow([(760, 440), (760, 480)], '주변장치 상태', (760, 460))
    d.arrow([(1100, 375), (990, 375)], '빌드한 ELF', (1058, 351))
    d.arrow([(425, 620), (425, 660)], 'IPC 호출', (425, 640), both=True)
    d.arrow([(560, 715), (640, 715)], 'IPC', (600, 691), both=True)
    d.arrow([(990, 670), (1040, 670), (1040, 550), (1100, 550)], '저장', (1040, 610), both=True)
    d.arrow([(990, 735), (1100, 735)], '업데이트 확인', (1045, 759))
    d.legend(40, 845)
    d.save('stm-application.svg')


def cons():
    d = Diagram('CONS 애플리케이션 아키텍처', 'BLE Beacon 신호를 AltBeacon 기반 Beacon 연동 모듈이 UUID Region으로 수신하고, 실내 측위가 Spring Boot 비콘 좌표 서버와 Retrofit으로 좌표를 맞춰 위치를 계산. 계산한 실내 좌표는 Unity 연동(UnityPlayerActivity·Intent)으로 Unity AR 장면에 전달. Beacon 연동과 Unity 연동이 핵심 연동 구간.', 840)
    d.zone(240, 40, 830, 480, 'Android 앱 · Java', 'plain')
    d.zone(520, 560, 550, 200, 'Beacon Server', 'mine', '내 담당')
    d.card(40, 100, 160, 120, ['globe'], '지하철 공공 API', '도착 · 환승 정보', 'ext')
    d.card(265, 100, 200, 120, ['android'], 'Android 화면', '노선도 · 도착 · 환승 안내', 'team')
    d.card(555, 100, 200, 120, ['database'], 'Room', '역 · 시간표 로컬 DB', 'team')
    d.card(40, 305, 160, 140, ['bluetooth'], 'BLE Beacon', 'UUID · Major · Minor\nRSSI 신호', 'ext')
    d.card(265, 290, 200, 170, ['android', 'bluetooth'], 'Beacon 연동', 'AltBeacon · UUID Region\nRanging · Minor 층 판별\nRSSI 수신', 'mine', '핵심 연동')
    d.card(555, 290, 200, 170, ['network'], '실내 측위', 'RSSI 거리 추정 · 비콘 선별\n좌표 계산 · 5회 평균\n본인·팀원 공동', 'mine')
    d.card(845, 290, 200, 170, ['android', 'unity'], 'Unity 연동', 'Unity 모듈 포함 · 빌드 설정\nUnityPlayerActivity\n좌표 · 층 높이 변환', 'mine', '핵심 연동')
    d.card(1130, 290, 160, 170, ['unity'], 'Unity AR', 'NavMesh 경로\nAR 길안내 · 팀원', 'team')
    d.card(555, 610, 200, 130, ['spring'], 'Spring Boot', 'JPA · 비콘 좌표 API', 'mine')
    d.card(845, 610, 200, 130, ['mysql'], 'MySQL', '비콘 좌표 · 층 정보', 'mine')
    d.arrow([(200, 160), (265, 160)], 'Retrofit', (232, 136), both=True)
    d.arrow([(465, 160), (555, 160)], '조회', (510, 136), both=True)
    d.arrow([(365, 220), (365, 290)], '탐색 시작', (365, 255))
    d.arrow([(200, 375), (265, 375)], 'BLE', (232, 351), key=True)
    d.arrow([(465, 375), (555, 375)], 'RSSI 목록', (510, 351))
    d.arrow([(755, 375), (845, 375)], '실내 좌표', (800, 351))
    d.arrow([(1045, 375), (1130, 375)], 'Intent', (1087, 351), key=True)
    d.note('트러블슈팅 · 지원 중단 API 교체', 365, 486)
    d.note('트러블슈팅 · 모듈 빌드 설정', 945, 486)
    d.arrow([(705, 460), (705, 610)], 'Retrofit · REST  비콘 좌표', (705, 538), both=True)
    d.arrow([(755, 675), (845, 675)], 'JPA', (800, 651), both=True)
    d.legend(40, 798, key=True)
    d.save('cons-application.svg')


def bookies():
    d = Diagram('BOOKIES 애플리케이션 아키텍처', 'Web Browser와 Android App이 EC2의 Spring Boot Web Service에 JSP·REST API로 접속하고, Web Service는 JDBC로 RDS Oracle 19c에 연결. 팀원이 구현한 DRM의 Packager가 암호화 전자책을 S3에 올리고 Distributor가 URL·키를 DRM Agent에 전달.', 850)
    d.zone(250, 40, 1030, 420, 'AWS VPC', 'plain')
    d.zone(280, 90, 750, 340, 'EC2 · Ubuntu 22.04  ·  RDS', 'mine', '내 담당')
    d.zone(250, 500, 1030, 240, 'DRM · 전자책 암호화·배포', 'team', '팀원 구현')
    d.card(40, 170, 170, 130, ['globe'], 'Web Browser', 'JSP 화면', 'ext')
    d.card(40, 380, 170, 130, ['android'], 'Android App', '앱 화면 · 팀원 구현', 'team')
    d.card(320, 150, 340, 170, ['java', 'spring'], 'Web Service · Spring Boot', 'JSP Web · Android REST API\nGradle WAR · 외부 Tomcat', 'mine')
    d.card(760, 150, 230, 140, ['oracle'], 'RDS Oracle 19c', 'Docker 개발 DB → RDS 이전\n퍼블릭 액세스 차단', 'mine')
    d.card(1060, 150, 200, 140, ['cloud'], 'Amazon S3', '암호화 전자책 저장', 'ext')
    d.card(300, 560, 230, 130, ['package'], 'Packager', '전자책 암호화 · 업로드', 'team')
    d.card(640, 560, 230, 130, ['server'], 'Distributor', 'Presigned URL · 키 발급', 'team')
    d.card(1030, 560, 220, 130, ['book-open'], 'DRM Agent', '전용 eBook 뷰어', 'team')
    d.arrow([(210, 235), (320, 235)], 'HTTPS · JSP', (265, 211), both=True)
    d.arrow([(210, 445), (490, 445), (490, 320)], 'REST API · JSON', (350, 445), both=True)
    d.arrow([(660, 220), (760, 220)], 'JDBC', (710, 196), both=True)
    d.arrow([(415, 560), (415, 478), (1120, 478), (1120, 290)], '암호화 파일 업로드', (760, 478))
    d.arrow([(870, 625), (1030, 625)], 'URL · 키 전달', (950, 601))
    d.arrow([(1200, 560), (1200, 290)], '다운로드', (1200, 410))
    d.legend(40, 800)
    d.save('bookies-application.svg')


def arabica():
    d = Diagram('Arabica 애플리케이션 아키텍처', 'React 화면이 Spring Boot API를 호출. 정책·예약이 비동기 실행기를 거쳐 SSH·Bash로 운영 서버 덤프를 실행하고, scp로 받은 결과 파일을 5분 주기로 판독해 DR 저장소에서 업로드·복원 검증. 인증 상태는 Redis, 정책·이력은 MariaDB에 저장.', 880)
    d.zone(250, 40, 640, 770, 'Spring Boot API · MariaDB', 'mine', '내 담당')
    d.card(40, 100, 170, 130, ['react'], 'React · TS', '웹 화면 · 팀원 구현', 'team')
    d.card(40, 320, 170, 130, ['redis'], 'Redis', '로그인 상태 · 중복 로그인', 'ext')
    d.card(290, 100, 260, 130, ['shield-check'], '인증 · 계정', 'JWT 15분/7일 · Argon2', 'mine')
    d.card(290, 270, 260, 130, ['database'], '이력 · 복원 API', '백업·복원 이력 · 복원 실행', 'mine')
    d.card(590, 100, 260, 130, ['calendar-clock'], '정책 · 예약', '전체·증분·차등 · 매시 정각 실행', 'mine')
    d.card(590, 270, 260, 130, ['terminal'], '비동기 실행기', '@Async · Apache SSHD', 'mine')
    d.card(590, 440, 260, 130, ['database-backup'], '결과 판독 · 검증', '5분 주기 · 테이블·행 수 비교', 'mine')
    d.card(330, 660, 450, 130, ['mariadb'], 'MariaDB', '정책 · 백업·복원 이력 · 용량', 'mine')
    d.card(1010, 180, 260, 150, ['server'], '운영 서버', 'VM · K8s의 MySQL · Redis\n덤프 스크립트 실행', 'ext')
    d.card(1010, 430, 260, 150, ['folder-open'], 'DR 저장소', '업로드 · 복원 검증\n보관 기간 정리', 'ext')
    d.arrow([(210, 165), (290, 165)], 'HTTP · JSON', (250, 141), both=True)
    d.arrow([(290, 205), (250, 205), (250, 385), (210, 385)], '토큰 상태', (250, 295), both=True)
    d.arrow([(720, 230), (720, 270)], '예약 실행', (790, 250))
    d.arrow([(850, 335), (920, 335), (920, 240), (1010, 240)], 'SSH · Bash 덤프', (920, 288))
    d.arrow([(1010, 305), (960, 305), (960, 485), (850, 485)], 'scp 결과 파일', (960, 395))
    d.arrow([(850, 535), (1010, 535)], '업로드 · 복원 검증', (930, 511))
    d.arrow([(420, 400), (420, 660)], 'JPA', (420, 530), both=True)
    d.arrow([(720, 570), (720, 660)], '검증 결과 기록', (720, 625))
    d.legend(40, 840)
    d.save('backup-application.svg')


def cmp():
    d = Diagram('CMP 애플리케이션 아키텍처', 'React 화면이 Spring WebFlux API를 호출. 로그인·세션은 NSS 토큰을 관리하고, 조회 API가 WebClient로 NSS·NBU API를 비동기 호출한 뒤 테넌트·cluster·namespace 매핑 필터로 응답을 구분. 파일 배포는 경로를 검증해 설치 파일 폴더를 ZIP으로 제공.', 760)
    d.zone(260, 40, 640, 600, 'Spring WebFlux API · RHEL VM · HTTPS', 'mine', '백엔드 · 내 담당')
    d.card(40, 100, 180, 130, ['react'], 'React', 'Admin · Tenant 화면\n팀원 구현', 'team')
    d.card(300, 100, 240, 130, ['shield-check'], '로그인 · 세션', 'NSS 토큰 · HttpOnly 쿠키\n토큰 주기 갱신', 'mine')
    d.card(640, 100, 230, 130, ['network'], '조회 API', '사용량 · 대시보드 · K8s 정책', 'mine')
    d.card(300, 280, 240, 130, ['key-round'], '테넌트 매핑 필터', 'Tenant · cluster · namespace', 'mine')
    d.card(640, 280, 230, 130, ['cable'], 'WebClient', 'Mono · 비동기 외부 호출', 'mine')
    d.card(300, 480, 240, 130, ['folder-open'], '파일 배포', '경로 검증 · ZIP 다운로드', 'mine')
    d.card(1010, 100, 260, 130, ['server'], 'NSS API', '토큰 · Tenant · 백업 Job', 'ext')
    d.card(1010, 300, 260, 130, ['database-backup'], 'NBU API', 'K8s cluster · namespace · image', 'ext')
    d.card(1010, 480, 260, 130, ['folder-open'], '설치 파일 폴더', 'Solution Suite 파일 · 문서', 'ext')
    d.arrow([(220, 165), (300, 165)], 'HTTPS · JSON', (260, 141), both=True)
    d.arrow([(755, 230), (755, 280)], '외부 조회', (822, 255))
    d.arrow([(640, 345), (540, 345)], '응답 필터링', (590, 321))
    d.arrow([(870, 320), (935, 320), (935, 165), (1010, 165)], 'NSS API', (935, 240), both=True)
    d.arrow([(870, 370), (1010, 370)], 'NBU API', (940, 370), both=True)
    d.arrow([(540, 545), (1010, 545)], '설치 파일 읽기', (780, 545))
    d.legend(40, 700)
    d.save('integration-application.svg')


def wallet():
    d = Diagram('Wallet 애플리케이션 아키텍처', 'Wallet 앱·Dashboard·내부 서비스의 암호화 요청을 RSA·AES로 복호화하고 XSS·SQLi 입력 검사 후 Dispatcher가 업무 Bean을 선택. 업무 Bean은 MyBatis로 PostgreSQL, web3j로 Ledger와 연동하고, 알림 모듈이 Firebase FCM·SMS 서비스에 발송 요청.', 880)
    d.zone(270, 40, 640, 560, 'Brooklyn Wallet API · Spring Boot', 'mine', '내 담당')
    d.card(40, 90, 180, 120, ['smartphone'], 'Wallet 앱', '앱 화면 · 팀원 구현', 'team')
    d.card(40, 250, 180, 120, ['globe'], 'Dashboard', '관리자 화면', 'team')
    d.card(40, 410, 180, 120, ['server'], '내부 서비스', 'Store · Foundation', 'ext')
    d.card(310, 95, 240, 120, ['key-round'], '요청 복호화', 'RSA·AES 혼합 암호화\n/api · /dashboard · /internal', 'mine')
    d.card(310, 255, 240, 110, ['shield-check'], '입력 검사', 'XSS·SQLi 패턴 · AntiSamy', 'mine')
    d.card(310, 405, 240, 110, ['network'], 'Dispatcher', 'method → 업무 Bean', 'mine')
    d.card(640, 240, 230, 150, ['wallet'], '업무 Bean', '회원 · 지갑 · 친구 · 인증\nQR · SSE 로그인', 'mine')
    d.card(640, 440, 230, 110, ['bell-ring'], '알림', 'FCM · SMS 발송 요청', 'mine')
    d.card(1010, 90, 260, 120, ['postgresql'], 'PostgreSQL', 'MyBatis · JPA', 'mine')
    d.card(1010, 270, 260, 130, ['cable'], 'Ledger', 'web3j JSON-RPC\n송금 · 스테이킹', 'ext')
    d.card(1010, 440, 260, 120, ['firebase'], 'Firebase FCM', '앱 푸시 전달', 'mine')
    d.card(640, 660, 230, 120, ['radio'], 'SMS 서비스', '인증코드 · 안내 문자', 'mine')
    d.arrow([(220, 150), (310, 150)], '암호화 요청', (265, 126))
    d.arrow([(220, 310), (248, 310), (248, 150)], head=False)
    d.arrow([(220, 470), (248, 470), (248, 310)], head=False)
    d.arrow([(430, 215), (430, 255)])
    d.arrow([(430, 365), (430, 405)])
    d.arrow([(550, 460), (595, 460), (595, 315), (640, 315)])
    d.arrow([(755, 390), (755, 440)])
    d.arrow([(870, 280), (940, 280), (940, 150), (1010, 150)], 'MyBatis', (940, 215), both=True)
    d.arrow([(870, 335), (1010, 335)], 'web3j', (940, 335), both=True)
    d.arrow([(870, 500), (1010, 500)], '푸시 요청', (940, 500))
    d.arrow([(755, 550), (755, 660)], '인증 문자', (755, 625))
    d.legend(40, 830)
    d.save('wallet-application.svg')


def store():
    d = Diagram('Store 애플리케이션 아키텍처', 'Store Web이 Controller에 HTTP·SSE로 접속하고 상품·배송지, SSE 로그인, KRDC 결제 서비스가 MyBatis로 PostgreSQL에 저장. KRDC 결제는 Wallet API에 RSA·AES 암호화 요청을 보내고, Wallet 앱의 QR 승인 결과를 Wallet API가 Store에 전달. 상품 이미지는 MinIO URL로 제공.', 880)
    d.zone(260, 40, 650, 770, 'TimeSquare Store API · PostgreSQL', 'mine', '내 담당')
    d.card(40, 85, 180, 130, ['globe'], 'Store Web', '상품 · 결제 화면\n팀원 구현', 'team')
    d.card(40, 250, 180, 130, ['cloud'], 'MinIO', 'S3 SDK · 상품 이미지', 'ext')
    d.card(300, 100, 570, 100, ['network'], 'Controller', '/api/store · /api/owner · /api/sse', 'mine')
    d.card(300, 250, 170, 130, ['package'], '상품 · 배송지', '카테고리 · 상품 조회', 'mine')
    d.card(500, 250, 170, 130, ['radio'], 'SSE 로그인', '인증 상태 저장\n1초 간격 조회', 'mine')
    d.card(700, 250, 170, 130, ['wallet'], 'KRDC 결제', '소수 6자리 변환\n오류 필드 처리', 'mine')
    d.card(300, 440, 570, 110, ['database'], 'MyBatis · HikariCP', 'DAO · Mapper', 'mine')
    d.card(420, 660, 330, 130, ['postgresql'], 'PostgreSQL', 'MySQL → PostgreSQL 전환 · 49개 테이블', 'mine')
    d.card(1010, 230, 250, 150, ['spring'], 'Wallet API', '인증 승인 · KRDC 송금', 'ext')
    d.card(1010, 470, 250, 130, ['smartphone'], 'Wallet 앱', 'QR 로그인 승인', 'team')
    d.arrow([(220, 150), (300, 150)], 'HTTP · SSE', (260, 126), both=True)
    d.arrow([(300, 315), (220, 315)], '이미지 URL', (260, 291))
    for x in (385, 585, 785):
        d.arrow([(x, 200), (x, 250)])
        d.arrow([(x, 380), (x, 440)])
    d.arrow([(585, 550), (585, 660)], 'SQL', (585, 605), both=True)
    d.arrow([(870, 300), (1010, 300)], '결제 요청 (RSA·AES)', (940, 276))
    d.arrow([(1135, 230), (1135, 150), (870, 150)], '인증 승인 결과', (1000, 150))
    d.arrow([(1135, 470), (1135, 380)], 'QR 로그인 승인', (1135, 425))
    d.legend(40, 840)
    d.save('store-application.svg')


if __name__ == '__main__':
    for build in (stm, cons, bookies, arabica, cmp, wallet, store):
        build()
    print('Rendered 7 architecture diagrams.')
