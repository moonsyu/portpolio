"""Slides 1–4 for the editable eight-slide A/B portfolio presentation.

The coordinator owns saving and rendering.  This module only returns Slide objects.
"""
from ppt_design_base import THEMES, new_slide, icon
from design_board import TIMELINE, SKILLS, AWARDS, ABOUT, width


ASSET = 'assets/profile.webp'


def _profile(s, x, y, size=300):
    s.image(ASSET, x, y, size, size * 605 / 500, 0, 'meet')


def _intro(s, theme):
    s = new_slide(theme, 1, None)
    ink, accent, muted, soft, line = (theme[k] for k in ('ink', 'accent', 'muted', 'soft', 'line'))
    if theme['key'] == 'a':
        s.text(72, 70, '장문수', 42, 800, ink)
        s.text(72, 132, 'Jang MoonSu', 27, 650, muted)
        s.text(72, 258, '백엔드에서', 72, 820, ink)
        s.text(72, 350, '하드웨어 학습까지', 72, 820, ink)
        s.text(72, 442, '연결하는 개발자', 72, 820, ink)
        s.bullets(76, 570, ABOUT, 760, 30, 650, ink, 20)
        s.rect(1090, 142, 350, 413, soft, 0)
        _profile(s, 1115, 167, 300)
        s.line(1090, 625, 1440, 625, line, 2)
        s.text(1090, 664, 'Java · Android · IoT', 28, 700, accent)
    else:
        s.rect(72, 105, 430, 504, soft, 0)
        _profile(s, 112, 145, 350)
        s.text(72, 664, '장문수', 38, 800, ink)
        s.text(72, 720, 'Jang MoonSu', 27, 650, muted)
        s.text(610, 170, '백엔드에서', 72, 820, ink)
        s.text(610, 262, '하드웨어 학습까지', 72, 820, ink)
        s.text(610, 354, '연결하는 개발자', 72, 820, ink)
        s.bullets(614, 490, ABOUT, 800, 30, 650, ink, 20)
        s.line(610, 710, 1440, 710, line, 2)
        s.text(610, 748, 'Java · Android · IoT · STM32 HAL 학습', 28, 700, accent)
    return s


def _career(s, theme):
    s = new_slide(theme, 2, '경력', '학습과 실무 경험')
    ink, accent, muted, soft, line = (theme[k] for k in ('ink', 'accent', 'muted', 'soft', 'line'))
    if theme['key'] == 'a':
        y = 245
        for date, role, institution in TIMELINE:
            s.text(90, y, date, 26, 750, accent)
            s.text(375, y, role, 32, 780, ink)
            s.text(970, y + 3, institution, 28, 620, muted)
            s.line(72, y + 68, 1528, y + 68, line, 2)
            y += 135
    else:
        cols = [72, 440, 805, 1160]
        for x, (date, role, institution) in zip(cols, TIMELINE):
            s.rect(x, 248, 300, 445, soft, 0)
            s.text(x + 24, 280, date, 26, 760, accent)
            s.line(x + 24, 337, x + 276, 337, line, 2)
            s.para(x + 24, 372, role, 252, 31, 780, ink, 46)
            institution = institution.replace('삼성청년SW·AI아카데미', '삼성청년SW·\nAI아카데미')
            s.para(x + 24, 525, institution, 252, 28, 620, muted, 40)
    return s


def _skills(s, theme):
    s = new_slide(theme, 3, '기술', '실제 사용한 도구')
    ink, accent, muted, soft, line = (theme[k] for k in ('ink', 'accent', 'muted', 'soft', 'line'))
    cols = [72, 438, 804, 1170]
    for x, (group, items) in zip(cols, SKILLS):
        s.rect(x, 235, 340, 520, soft, 0)
        s.text(x + 22, 267, group, 29, 780, accent)
        s.line(x + 22, 322, x + 318, 322, line, 2)
        y = 358
        for name, label in items:
            icon(s, name, x + 23, y - 3, 32)
            s.text(x + 73, y, label, 28, 680, ink)
            y += 88
    return s


def _award_row(s, y, date, institution, title, award, theme):
    ink, accent, muted, line = (theme[k] for k in ('ink', 'accent', 'muted', 'line'))
    s.text(72, y, institution, 26, 650, accent)
    s.text(1040, y, date, 26, 650, muted, 'end')
    s.text(72, y + 36, title, 30, 720, ink)
    s.text(1040, y + 36, award, 30, 800, accent, 'end')
    s.line(72, y + 79, 1040, y + 79, line, 1)


def _qualifications(s, theme):
    ink, accent, muted, soft = (theme[k] for k in ('ink', 'accent', 'muted', 'soft'))
    s.rect(1132, 235, 396, 230, soft, 0)
    s.text(1160, 265, '정보처리기사', 32, 800, ink)
    s.text(1160, 324, '한국산업인력공단', 28, 650, muted)
    s.text(1160, 382, '취득일  2024.10.02', 28, 720, accent)
    s.rect(1132, 500, 396, 230, soft, 0)
    s.text(1160, 530, 'OPIc  IL', 32, 800, ink)
    s.text(1160, 589, 'Intermediate Low', 28, 650, muted)
    s.text(1160, 647, '취득일  2026.09.14', 28, 720, accent)


def _awards(s, theme):
    s = new_slide(theme, 4, '수상 · 자격', '수상 이력과 자격 정보')
    ink, muted = theme['ink'], theme['muted']
    y = 230
    for row in AWARDS:
        _award_row(s, y, *row, theme)
        y += 95
    _qualifications(s, theme)
    return s


def make_profile_slides(theme):
    """Return pages 1–4 for theme ``a`` or ``b`` without saving files."""
    if isinstance(theme, str):
        theme = THEMES[theme]
    return [_intro(None, theme), _career(None, theme), _skills(None, theme), _awards(None, theme)]
