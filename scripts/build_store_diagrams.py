"""Render the Store project using the portfolio's existing diagram style."""
import sys
sys.dont_write_bytecode = True
from build_architectures import Diagram


def overview():
    d = Diagram('Store · 커머스 백엔드', 'DB 전환, 관계 구조 수정, Wallet 인증 연동', 820)
    d.text(72, 100, 'Store · 커머스 백엔드', 48, True, anchor='start')
    for n, x, icon, title, subtitle in [
        ('01', 60, 'postgresql', 'DB Migration', 'MySQL → PostgreSQL'),
        ('02', 480, 'network', '스키마 관계', '장바구니 · 결제 옵션'),
        ('03', 900, 'user-round', 'Wallet 연동', 'SSE 인증 상태 전달'),
    ]:
        d.box(x, 220, 360, 450, fill='#f5f8fd', stroke='#c9d6e8', width=1.5)
        d.text(x+34, 260, n, 22, True, anchor='start', fill='#2355de')
        d.icon(icon, x+124, 300, 112, '#2355de')
        d.text(x+180, 505, title, 38, True)
        d.text(x+180, 566, subtitle, 29, fill='#52627b')
    d.save('store-overview.svg')


def application():
    d = Diagram('Store 애플리케이션 아키텍처',
                '웹 클라이언트의 API·SSE 요청, Store Controller와 Service, MyBatis·PostgreSQL 저장 경로 및 Wallet의 인증 결과 전달', 1100)
    d.box(30, 200, 210, 260, 'Web Client')
    d.node('globe', 135, 274, 'Web Browser', 'API · SSE 구독', size=60, color='#2355de')
    d.box(350, 70, 600, 680, 'Store Application')
    d.icon('java', 575, 132, 52)
    d.icon('spring', 655, 132, 52)
    d.text(650, 215, 'Java · Spring Boot / WebFlux', 22, True)
    d.box(395, 250, 510, 90, fill='#f8fafc', stroke='#c8d0dc', width=1.6)
    d.icon('network', 420, 271, 43, '#2355de')
    d.text(686, 306, 'Controller · API / SSE', 25, True)
    d.arrow([(246, 295), (389, 295)], 'HTTP · SSE', (315, 270), both=True)
    d.box(395, 440, 510, 160, 'Service · 기능 분기', fill='#f8fafc', stroke='#c8d0dc', width=1.6)
    d.text(530, 530, '상품·장바구니·결제', 22, True)
    d.text(530, 565, '기능별 처리', 19, fill='#475467')
    d.text(785, 530, 'SSE 인증', 22, True)
    d.text(785, 565, '인증 상태 갱신·조회', 19, fill='#475467')
    d.arrow([(650, 346), (650, 434)], '요청 처리', (650, 397))
    d.box(520, 640, 260, 90, fill='#f8fafc', stroke='#c8d0dc', width=1.6)
    d.text(650, 676, 'MyBatis', 23, True)
    d.text(650, 708, 'DAO · Mapper', 20, fill='#475467')
    d.arrow([(650, 606), (650, 634)])
    d.box(520, 890, 260, 185, 'Data Storage')
    d.node('postgresql', 650, 939, 'PostgreSQL', '상품·주문·인증 상태', size=50)
    d.arrow([(650, 736), (650, 884)], '조회·저장', (650, 817), both=True)
    d.box(1050, 80, 240, 190)
    d.node('android', 1170, 117, 'Wallet App', size=57)
    d.box(1050, 395, 240, 230)
    d.node('spring', 1170, 431, 'Wallet API', 'App 인증 결과', size=59)
    d.arrow([(1170, 276), (1170, 389)], '승인 요청', (1170, 337))
    d.arrow([(1044, 502), (1000, 502), (1000, 295), (911, 295)], '승인 전달', (1002, 376))
    d.save('store-application.svg')


if __name__ == '__main__':
    overview()
    application()
    print('Built Store overview and application architecture.')
