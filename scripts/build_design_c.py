"""Archived C design generator; excluded from the current portfolio redesign."""
from design_board import (Board, TIMELINE, SKILLS, AWARDS, ABOUT, STM_POINTS,
                          OLD, IMPROVED, UART, qualification, icon, width, ROOT)


ASSET = ROOT / 'assets'


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
    make_c()
