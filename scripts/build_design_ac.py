"""Static, vector-based portfolio design alternatives A and C.

Both boards deliberately reuse only verified portfolio copy and supplied assets.
They are review artifacts; neither changes the published portfolio.
"""
from design_board import (Board, TIMELINE, SKILLS, AWARDS, ABOUT, STM_POINTS,
                          OLD, IMPROVED, UART, qualification, icon, width, ROOT)


ASSET = ROOT / 'assets'


def rule(b, x, y, w, color):
    b.line(x, y, x + w, y, color, 2)


def a_skill_row(b, x, y, group, items):
    b.text(x, y, group, 23, 750, '#6845D7')
    cx = x
    for name, label in items:
        icon(b, name, cx, y + 52, 32)
        b.text(cx + 44, y + 56, label, 21, 650, '#211C37')
        cx += max(170, width(label, 21, 650) + 78)


def make_a():
    p = '#6845D7'; pale = '#F2EEFF'; ink = '#211C37'; muted = '#635E73'
    b = Board('a-frontend-design', 'A안 · 강한 타이포그래피 포트폴리오', 7500, '#FFFFFF')
    # Introduction: an editorial violet field separated sharply from project work.
    b.rect(0, 0, 1600, 1370, p)
    b.text(100, 74, '장문수  ·  Jang MoonSu', 30, 760, '#FFFFFF')
    b.text(100, 130, '소개', 20, 650, pale)
    b.text(270, 130, 'STM-Simulator', 20, 650, pale)
    b.text(510, 130, 'GitHub', 20, 650, pale)
    rule(b, 100, 183, 1400, '#A996EE')
    b.text(100, 285, '백엔드에서', 86, 820, '#FFFFFF')
    b.text(100, 405, '하드웨어 학습까지', 86, 820, '#FFFFFF')
    b.text(100, 525, '연결하는 개발자', 86, 820, '#FFFFFF')
    b.para(105, 685, 'Java 기반 서버 개발 경험을 바탕으로\nAndroid·센서 데이터 연동과 STM32 HAL 학습을 이어갑니다.', 690, 27, 600, pale, 48)
    b.rect(104, 875, 230, 66, '#FFFFFF', 0)
    b.text(129, 894, '프로젝트 보기', 22, 750, p)
    b.image(ASSET / 'profile.webp', 1045, 245, 380, 475, 0, 'slice')
    b.line(1015, 810, 1450, 810, '#A996EE', 2)
    b.text(1045, 850, 'Java · Android · IoT', 24, 700, '#FFFFFF')
    b.text(1045, 902, '학습과 구현의 연결', 24, 600, pale)
    # Evidence sections have generous white space and no repeated card grid.
    b.text(100, 1480, '경력', 55, 820, ink)
    b.text(100, 1560, '경험을 축적하며 개발의 범위를 넓혔습니다.', 26, 600, muted)
    rule(b, 100, 1625, 1400, '#DAD3ED')
    y = 1680
    for date, role, org in TIMELINE:
        b.text(100, y, date, 22, 750, p)
        b.text(430, y, role, 27, 760, ink)
        b.text(1080, y + 3, org, 22, 600, muted)
        rule(b, 100, y + 58, 1400, '#E7E1F2')
        y += 96

    b.rect(0, 2100, 1600, 850, pale)
    b.text(100, 2200, '기술', 55, 820, ink)
    b.text(100, 2285, '실제 사용한 도구를 역할별로 정리했습니다.', 26, 600, muted)
    y = 2385
    for group, items in SKILLS:
        a_skill_row(b, 100, y, group, items)
        y += 132

    b.text(100, 3130, '수상 · 자격', 55, 820, ink)
    b.text(100, 3215, '학습 과정과 결과를 기록한 이력입니다.', 26, 600, muted)
    rule(b, 100, 3280, 900, '#DAD3ED')
    y = 3335
    for date, org, title, award in AWARDS:
        b.text(100, y, date, 19, 700, p)
        b.text(285, y, org, 20, 680, muted)
        b.para(285, y + 38, title, 650, 23, 730, ink, 34)
        b.text(945, y + 18, award, 23, 800, p, 'end')
        y += 112
    qualification(b, 1080, 3305, 330, p, ink, pale)

    # Project half: dark, wide, screenshot-led composition.
    b.rect(0, 4100, 1600, 3400, ink)
    b.text(100, 4210, 'STM-Simulator', 70, 820, '#FFFFFF')
    b.text(100, 4310, '2026.09 — 현재  ·  1인', 24, 750, '#C8B9FF')
    b.text(100, 4365, '회로와 C/HAL 학습을 한 화면에서 연결한 데스크톱 학습 도구', 27, 600, pale)
    b.bullets(100, 4440, STM_POINTS, 1300, 23, 600, pale, 6)
    b.text(100, 4570, 'Electron · JavaScript · HTML / CSS / SVG · C · STM32 HAL 학습', 23, 650, '#C8B9FF')
    b.image(ASSET / 'stm-simulator.webp', 100, 4615, 1400, 838, 0)
    b.text(100, 5540, '애플리케이션 구조', 33, 820, '#FFFFFF')
    b.image(ASSET / 'architecture/stm-application.svg', 300, 5600, 1000)
    b.text(100, 6310, '확인 흐름 개선', 29, 820, '#FFFFFF')
    b.text(100, 6370, '기존 실습 준비', 24, 750, '#C8B9FF')
    yy = b.bullets(100, 6420, OLD, 700, 23, 600, pale, 8)
    b.text(100, yy + 20, '개선 사항', 24, 750, '#C8B9FF')
    b.bullets(100, yy + 68, IMPROVED, 700, 23, 600, pale, 8)
    b.image(ASSET / 'stm-led-demo-poster.webp', 880, 6310, 600, 460, 0)
    b.text(880, 6790, 'HAL LED 예제 화면', 22, 650, pale)
    b.line(100, 6880, 1500, 6880, '#635E73')
    b.text(100, 6930, 'UART 시뮬레이션의 시간 경계 오류 수정', 38, 820, '#FFFFFF')
    for i, (label, value) in enumerate(UART):
        yy = 7020 + i * 90
        b.text(100, yy, label, 23, 750, '#C8B9FF')
        b.para(245, yy, value, 630, 23, 600, pale, 34)
    b.image(ASSET / 'stm-uart-verified.webp', 990, 7030, 480, 162, 0)
    b.text(990, 7220, 'RX·TX 모두 ‘HAL log’ 일치', 25, 750, '#FFFFFF')
    b.para(990, 7275, '9600 baud · 260ms에 입력\n20ms 한 단계 실행', 480, 22, 600, pale, 34)
    b.save()


def c_rail_item(b, y, label, active=False):
    color = '#157567' if active else '#54716C'
    if active:
        b.rect(38, y - 7, 7, 36, color, 0)
    b.text(65, y, label, 21, 760 if active else 620, color)


def make_c():
    green = '#157567'; mint = '#EEF6F4'; ink = '#173A35'; muted = '#52736D'
    b = Board('c-ui-ux-pro-max', 'C안 · 탐색 레일 기반 기술 포트폴리오', 6560, '#FFFFFF')
    # Fixed navigation rail (a static visual concept, no implied interaction).
    b.rect(0, 0, 220, 6560, mint)
    b.rect(219, 0, 1, 6560, '#CFE2DD')
    b.image(ASSET / 'profile.webp', 42, 54, 128, 128, 64, 'slice')
    b.text(41, 220, '장문수', 29, 800, ink)
    b.text(41, 267, 'Jang MoonSu', 18, 720, muted)
    b.text(41, 303, 'Developer', 19, 650, muted)
    for y, label, active in [(370,'소개',True),(434,'경력',False),(498,'기술',False),
                             (562,'수상',False),(626,'자격',False),(770,'STM',False),
                             (834,'아키텍처',False),(898,'개선',False),(962,'UART',False)]:
        c_rail_item(b, y, label, active)
    b.line(41, 1060, 177, 1060, '#CFE2DD', 2)
    b.text(41, 1095, 'Java · Android · IoT', 18, 700, muted)
    b.text(41, 1135, 'STM32 HAL 학습', 18, 700, muted)

    x = 300; w = 1220
    b.text(x, 84, '소개', 23, 750, green)
    b.text(x, 145, '백엔드부터', 82, 830, ink)
    b.text(x, 257, '하드웨어 학습까지', 82, 830, ink)
    b.para(x, 385, '서버 개발, Android·센서 데이터 연동 경험을 바탕으로\nIoT와 STM32 HAL 학습을 지속하는 개발자입니다.', 790, 28, 620, muted, 48)
    b.text(x, 555, '핵심 기여', 25, 800, ink)
    y = 620
    for item in ABOUT:
        b.rect(x, y + 14, 12, 12, green, 0)
        b.text(x + 30, y, item, 27, 720, ink)
        y += 62
    b.rect(x, 875, w, 1, '#D6E7E2')
    b.text(x, 945, '경력', 48, 830, ink)
    b.text(x, 1020, '백엔드 실무 경험과 SW·보안·임베디드 교육', 24, 600, muted)
    y = 1100
    for date, role, org in TIMELINE:
        b.text(x, y, date, 21, 760, green)
        b.text(x + 290, y, role, 26, 760, ink)
        b.text(x + 800, y + 2, org, 21, 600, muted)
        b.line(x, y + 55, x + w, y + 55, '#D6E7E2', 2)
        y += 92

    b.rect(x, 1545, w, 1, '#D6E7E2')
    b.text(x, 1620, '기술', 48, 830, ink)
    b.para(x, 1695, '실제 사용한 기술을 역할별로 모았습니다.', 720, 24, 600, muted, 40)
    y = 1795
    for group, items in SKILLS:
        b.text(x, y, group, 23, 800, green)
        cx = x + 290
        for name, label in items:
            icon(b, name, cx, y - 5, 34)
            b.text(cx + 46, y, label, 22, 680, ink)
            cx += max(190, width(label, 22, 680) + 76)
        b.line(x, y + 57, x + w, y + 57, '#D6E7E2', 1)
        y += 95

    b.text(x, 2235, '수상과 자격', 48, 830, ink)
    b.text(x, 2310, '수상 이력과 자격 정보를 한 흐름으로 확인합니다.', 24, 600, muted)
    y = 2390
    for date, org, title, award in AWARDS:
        b.text(x, y, date, 19, 750, green)
        b.text(x + 190, y, org, 20, 650, muted)
        b.text(x + 490, y, title, 21, 730, ink)
        b.text(x + 1190, y, award, 21, 800, green, 'end')
        b.line(x, y + 42, x + w, y + 42, '#D6E7E2', 1)
        y += 65
    b.rect(x, 2820, 580, 175, mint, 0)
    b.text(x + 26, 2845, '정보처리기사', 28, 800, ink)
    b.text(x + 26, 2900, '한국산업인력공단 · 취득일 2024.10.02', 21, 650, muted)
    b.rect(x + 620, 2820, 580, 175, mint, 0)
    b.text(x + 646, 2845, 'OPIc  IL', 28, 800, ink)
    b.text(x + 646, 2900, 'Intermediate Low · 취득일 2026.09.14', 21, 650, muted)

    # Project evidence follows the portfolio narrative: overview, screen, architecture, then findings.
    b.rect(220, 3150, 1380, 3410, mint)
    b.text(x, 3260, 'STM-Simulator', 62, 830, ink)
    b.text(x, 3355, '2026.09 — 현재  ·  1인', 24, 760, green)
    b.text(x, 3410, '회로 편집, 주변장치 설정, 지원 범위의 C/HAL 동작 모델을 연결한 학습 도구', 26, 620, muted)
    b.bullets(x, 3480, STM_POINTS, 1180, 23, 620, ink, 6)
    b.text(x, 3625, 'Electron · JavaScript · HTML / CSS / SVG · C · STM32 HAL 학습', 23, 650, green)
    b.image(ASSET / 'stm-simulator.webp', x, 3680, 1240, 743, 0)
    b.text(x, 4525, '애플리케이션 구조', 32, 820, ink)
    b.text(x, 4580, '구성 요소와 연결 범위를 실제 도식으로 확인합니다.', 23, 600, muted)
    b.image(ASSET / 'architecture/stm-application.svg', x, 4650, 1240)
    b.text(x, 5485, '확인 흐름 개선', 31, 820, ink)
    b.text(x, 5545, '기존 실습 준비', 23, 750, green)
    yy = b.bullets(x, 5590, OLD, 650, 23, 620, ink, 7)
    b.text(x, yy + 18, '개선 사항', 23, 750, green)
    b.bullets(x, yy + 64, IMPROVED, 650, 23, 620, ink, 7)
    b.image(ASSET / 'stm-led-demo-poster.webp', x + 750, 5500, 470, 360, 0)
    b.text(x + 750, 5880, 'HAL LED 예제 화면', 22, 650, muted)
    b.line(x, 5980, x + w, 5980, '#B8D3CB')
    b.text(x, 6020, 'UART 시뮬레이션의 시간 경계 오류 수정', 34, 820, ink)
    for i, (label, value) in enumerate(UART):
        yy = 6100 + i * 91
        b.text(x, yy, label, 22, 750, green)
        b.para(x + 120, yy, value, 520, 23, 620, ink, 34)
    b.image(ASSET / 'stm-uart-verified.webp', x + 740, 6100, 480, 162, 0)
    b.text(x + 740, 6290, 'RX·TX 모두 ‘HAL log’ 일치', 24, 750, ink)
    b.para(x + 740, 6342, '9600 baud · 260ms에 입력\n20ms 한 단계 실행', 480, 22, 600, muted, 34)
    b.save()


if __name__ == '__main__':
    make_a()
    make_c()
