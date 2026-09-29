"""A/B slide-ready design images; each source page is independently editable geometry."""
import json
from ppt_design_base import THEMES, new_slide, icon, STM_POINTS, OLD, IMPROVED, UART, OUT
from ppt_profile_layout import make_profile_slides

def overview(t):
    s=new_slide(t,5,'STM-Simulator','Electron 기반 회로 배선·주변장치 설정 시뮬레이터')
    s.image('assets/stm-simulator.webp',72,226,988,592)
    if t['key']=='b': s.rect(1085,218,443,607,t['soft'],16)
    s.text(1110,232,'2026.09 — 현재',30,700,t['accent'])
    s.text(1110,282,'1인 프로젝트',30,700,t['ink'])
    s.text(1110,337,'구현 범위',32,750,t['ink'])
    s.bullets(1110,390,STM_POINTS,392,28,650,t['ink'],14)
    s.text(1110,710,'Electron · JavaScript',28,650,t['accent'])
    s.text(1110,752,'HTML / CSS / SVG · C',28,650,t['accent'])
    s.text(1110,794,'STM32 HAL 학습',28,650,t['accent'])
    return s

def architecture(t):
    s=new_slide(t,6,'STM-Simulator','애플리케이션 아키텍처')
    icon(s,'user-round',100,387,60)
    s.text(130,470,'사용자',30,700,t['ink'],'middle')
    s.rect(255,230,450,350,t['soft'],16,t['line'],2)
    s.text(289,263,'Renderer',36,750,t['ink'])
    icon(s,'javascript',622,258,48)
    s.text(289,329,'HTML · CSS · SVG',30,650,t['ink'])
    s.text(289,385,'회로·설정 / 프로젝트 상태',28,650,t['ink'])
    icon(s,'microchip',289,468,36)
    s.text(341,468,'지원 C/HAL 동작 모델',28,700,t['accent'])
    s.rect(800,320,245,210,'#FFFFFF',16,t['line'],2)
    icon(s,'network',901,344,42)
    s.text(922,408,'Preload',34,750,t['ink'],'middle')
    s.text(922,466,'브리지 · IPC',28,650,t['ink'],'middle')
    s.rect(1140,230,388,350,t['soft'],16,t['line'],2)
    s.text(1174,263,'Main',36,750,t['ink'])
    icon(s,'nodejs',1446,258,48)
    s.text(1174,329,'Node.js',30,650,t['ink'])
    icon(s,'folder-open',1174,393,40)
    s.text(1228,395,'파일 입출력',30,700,t['ink'])
    s.para(1174,466,'대화상자 · 검증\n읽기 · 쓰기',330,28,650,t['ink'],43)
    s.arrow(172,425,248,425)
    s.text(207,370,'편집',26,650,t['muted'],'middle')
    s.arrow(712,425,793,425,True)
    s.text(752,272,'요청·응답',25,650,t['muted'],'middle')
    s.arrow(1052,425,1133,425,True)
    s.text(1092,370,'IPC',26,650,t['muted'],'middle')
    s.arrow(480,590,480,664,True)
    s.text(510,615,'저장·복원',28,650,t['muted'])
    s.arrow(1334,590,1334,664,True)
    s.text(1360,615,'읽기·쓰기',28,650,t['muted'])
    s.rect(255,675,450,115,'#FFFFFF',16,t['line'],2)
    icon(s,'save',282,706,46)
    s.text(350,694,'localStorage',30,750,t['ink'])
    s.text(350,744,'자동 저장 · JSON 문자열',26,650,t['accent'])
    s.rect(1140,675,388,115,'#FFFFFF',16,t['line'],2)
    icon(s,'file-code',1163,695,40)
    s.text(1220,697,'프로젝트 파일',30,750,t['ink'])
    s.text(1163,750,'.stm32lab · .ioc · C · CSV',25,650,t['accent'])
    return s

def improvement(t):
    s=new_slide(t,7,'STM-Simulator','개선 사항 · 설정과 배선, 실행 결과를 한 화면에서 확인')
    s.text(72,240,'기존 실습 준비',34,750,t['muted'])
    y=s.bullets(72,306,OLD,670,32,650,t['ink'],14)
    s.line(72,495,718,495,t['line'])
    s.text(72,535,'개선 사항',34,750,t['accent'])
    s.bullets(72,601,IMPROVED,670,32,700,t['ink'],14)
    s.image('assets/stm-led-demo-poster.webp',820,224,708,543)
    s.text(820,790,'HAL LED 예제 화면',28,650,t['muted'])
    return s

def uart(t):
    s=new_slide(t,8,'STM-Simulator','트러블슈팅 · UART 시뮬레이션의 시간 경계 오류 수정')
    for i,(label,body) in enumerate(UART):
        y=240+i*147
        s.text(72,y,label,30,750,t['accent'])
        s.para(245,y,body,600,32,650,t['ink'],48)
        if i<3:s.line(72,y+116,833,y+116,t['line'])
    s.rect(916,232,612,567,t['soft'],16)
    s.image('assets/stm-uart-verified.webp',947,285,550,186)
    s.text(947,520,'RX·TX 모두 ‘HAL log’ 일치',31,750,t['ink'])
    s.text(947,600,'9600 baud',30,700,t['accent'])
    s.text(947,654,'260ms에 입력',30,650,t['ink'])
    s.text(947,708,'20ms 한 단계 실행',30,650,t['ink'])
    return s

def build():
    result=[]
    for theme in THEMES.values():
        pages=make_profile_slides(theme)+[overview(theme),architecture(theme),improvement(theme),uart(theme)]
        for page in pages:
            page.save()
        result.extend(pages)
    return result

if __name__=='__main__':build()
