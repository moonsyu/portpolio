"""Impeccable concept: a developer's exhibition catalogue, rendered as a static comp."""
from design_board import Board, ABOUT, TIMELINE, SKILLS, AWARDS, STM_POINTS, OLD, IMPROVED, UART, qualification, icon


def build():
    ink, blue, muted, paper, pale = '#19333F', '#276986', '#526873', '#F8FBFC', '#E4F0F5'
    b = Board('b-impeccable', 'Impeccable — 작업물 중심 카탈로그 시안', 6180, paper)
    b.text(90,29,'MoonSu',30,800,ink)
    b.text(1030,35,'소개',22,700,ink)
    b.text(1160,35,'STM-Simulator',22,700,ink)
    b.text(1430,35,'GitHub',22,700,ink)
    b.line(90,96,1510,96,'#BCCFD6')

    b.rect(0,128,1600,568,ink)
    b.image('assets/profile.webp',100,235,228,276)
    b.text(100,544,'장문수',36,750,'#FFFFFF')
    b.text(400,182,'Jang MoonSu',92,750,'#FFFFFF')
    b.text(403,310,'Java Backend Developer',34,650,'#C4E2EF')
    b.bullets(403,389,ABOUT,1000,27,600,'#FFFFFF',14)
    b.rect(400,579,220,62,'#FFFFFF',14)
    b.text(436,594,'프로젝트 보기',24,750,ink)
    b.text(670,595,'GitHub에서 개발 기록 보기',24,650,'#D8EAF1')

    b.text(90,769,'경력 및 교육',46,750,ink)
    for i,(date,title,sub) in enumerate(TIMELINE):
        x=90+i*365
        b.text(x,855,date,21,700,blue)
        b.line(x,899,x+316,899,'#9AB5C1',2)
        y=b.para(x,925,title,316,26,750,ink,39)
        b.para(x,y+9,sub,316,21,600,muted,32)

    b.text(90,1120,'보유 기술 스택',46,750,ink)
    for i,(name,items) in enumerate(SKILLS):
        x=90+i*365
        b.text(x,1210,name,23,750,blue)
        for j,(symbol,label) in enumerate(items):
            yy=1270+j*58
            icon(b,symbol,x,yy+1,34)
            b.text(x+49,yy+2,label,22,650,ink)

    b.line(90,1540,1510,1540,'#BCCFD6')
    b.text(90,1590,'수상',46,750,ink)
    b.text(1120,1590,'자격 · 어학',40,750,ink)
    for i,(date,org,title,grade) in enumerate(AWARDS):
        y=1674+i*100
        b.text(90,y,date,20,650,muted)
        b.text(265,y,org,20,700,blue)
        b.text(265,y+35,title+' '+grade,22,750,ink)
        b.line(90,y+82,1060,y+82,'#D2E0E5')
    qualification(b,1120,1674,390,blue,ink,pale)

    b.rect(0,2370,1600,1350,pale)
    b.text(90,2435,'STM-Simulator',74,750,ink)
    b.text(1510,2464,'2026.09 — 현재  /  1인 프로젝트',23,700,blue,'end')
    b.text(90,2543,'Electron 기반 회로 배선·주변장치 설정 시뮬레이터',34,750,ink)
    b.bullets(90,2615,STM_POINTS,1390,24,650,ink,9)
    b.text(90,2770,'Electron · JavaScript · HTML / CSS / SVG · C · STM32 HAL 학습',23,650,blue)
    b.image('assets/stm-simulator.webp',90,2825,1420,850)

    b.text(90,3790,'애플리케이션 아키텍처',46,750,ink)
    b.text(90,3860,'Electron의 Renderer · Preload · Main과 로컬 저장 흐름',25,650,muted)
    b.image('assets/architecture/stm-application.svg',130,3940,1340,812)

    b.line(90,4802,1510,4802,'#BCCFD6')
    b.text(90,4850,'설정·배선·LED 실행 결과를 한 화면에서',44,750,ink)
    b.text(90,4935,'기존 실습 준비',25,750,blue)
    y=b.bullets(90,4987,OLD,660,23,600,ink,8)
    b.text(90,y+25,'개선 사항',25,750,blue)
    b.bullets(90,y+78,IMPROVED,660,23,650,ink,8)
    b.image('assets/stm-led-demo-poster.webp',836,4940,660,506)
    b.text(836,5466,'HAL LED 예제 화면',22,650,muted)

    b.line(90,5540,1510,5540,'#BCCFD6')
    b.text(90,5584,'UART 시뮬레이션의 시간 경계 오류 수정',43,750,ink)
    for i,(label,body) in enumerate(UART):
        y=5675+i*91
        b.text(90,y,label,23,750,blue)
        b.para(239,y,body,642,23,650,ink,34)
    b.image('assets/stm-uart-verified.webp',1000,5700,480,162)
    b.text(1000,5890,'RX·TX 모두 ‘HAL log’ 일치',25,750,ink)
    b.para(1000,5944,'9600 baud · 260ms에 입력\n20ms 한 단계 실행',480,22,600,muted,34)
    b.line(90,6100,1510,6100,'#BCCFD6')
    b.text(90,6128,'Jang MoonSu',23,750,ink)
    b.text(1510,6128,'소개부터 STM-Simulator까지',21,650,muted,'end')
    b.save()


if __name__ == '__main__':
    build()
