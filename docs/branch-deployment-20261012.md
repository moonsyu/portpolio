# 브랜치별 포트폴리오 배포 · 2026-10-12

- 사용자 확정: `main`은 웹·앱, `embedded`는 STM·하드웨어 학습 포함 전체 구성. `web` 브랜치 미생성.
- `main`: `/portpolio/`, CONS·BOOKIES·Arabica·CMP·Wallet·Store, 웹·앱 PDF 35쪽.
- `embedded`: `/portpolio/embedded/`, STM-Simulator·CONS·BOOKIES·Arabica·CMP·Wallet·Store, 전체 PDF 40쪽.
- 각 웹페이지의 `PDF 다운로드` 버튼은 1개. PDF 자체의 다운로드 버튼은 계속 제외.
- PDF 생성기 기본값은 HTML의 `portfolio-variant` 기준 자동 선택. 웹·앱 소스로 전체본 생성 시 오류 처리.
- 공개 배포물에는 각 경로에 맞는 PDF 1개만 포함.
- 전체본 PDF의 포트폴리오 내부 웹 링크 75개는 `/embedded/`로 연결, 웹·앱 PDF 링크 65개는 루트로 연결.
- 두 PDF 총 75쪽 렌더: 기존 화면과 픽셀 동일. 페이지 수·본문 누락·깨진 이미지·레이아웃·링크 검사 통과.
- 조립 테스트 5개 통과: 브랜치 콘텐츠·자산 분리, 누락 자산 차단, PDF 오매핑 차단, 기존 출력 보존, 소스 경로 보호.
- 실제 조립 결과: 루트에 6개 프로젝트, `/embedded/`에 7개 프로젝트. 웹페이지 내부 앵커·로컬 자산·PDF 링크 검사 통과.
- 워크플로: 어느 브랜치에 푸시해도 최신 두 브랜치를 함께 배포. `portfolio-pages` 동시 실행 제한 적용.
- 배포 추적: 각 주소의 `deployment.json`에 원본 브랜치·커밋·URL 기록.

## PDF 해시

- `main`: SHA-256 `68cfa11fc7e28090483e696d9e13e741790f05cde56cffffeb0da5b671a7e0ff`.
- `embedded`: SHA-256 `41637dec67f7d2b73b7f6e2155b47cf325d2bea9db05ea8e6523b886950fb440`.
