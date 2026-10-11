# PDF 갱신 · 2026-10-12

- 기준: 현재 `index.html`·`styles.css`·프로젝트 자산.
- 사용자 예시: 표지·소개·기술 스택·수상/자격·프로젝트 목록·각 프로젝트 개요·각 상세 구간을 독립 페이지로 분리.
- 일반판 40쪽, 웹·앱판 35쪽. 1440×810px 기준 16:9 가로 레이아웃.
- 일반판: STM-Simulator·CONS·BOOKIES·Arabica·CMP·Wallet·Store.
- 웹·앱판: STM·임베디드 학습 기술·SSAFY 임베디드 트랙·전역 IoT/하드웨어 소개 제외. 사용자 예외인 CONS 전체와 AI 기술 스택 유지.
- Arabica 회고는 웹과 동일하게 추가 보완안·미구현 표시 유지.
- 이미지 예시를 통째로 붙이지 않고 현재 HTML에서 본문·아이콘·기존 화면·도식을 재사용.
- GIF는 기존 poster 이미지와 웹 실행 링크 사용.
- 웹 본문·스타일 유지. Arabica·CMP·Wallet·Store 개요 이미지와 다운로드 링크 캐시 갱신.
- 개요 이미지 표시 문구·아이콘 및 Store 캡처 변경: [이미지 수정 기록](image-corrections-20261012.md).

## 검증

- 일반판 40쪽·웹·앱판 35쪽, 총 75쪽 렌더 완료.
- 페이지별 원문 텍스트 전부 PDF에 존재. 누락 0건·문자 대체 오류 0건.
- 페이지별 이미지 로드 실패·가로 넘침·하단 잘림 검사 통과.
- 수상 6개 항목·자격 2개 카드가 하나의 페이지에 모두 표시됨을 직접 확인.
- 한글 선택·검색, 40개/35개 페이지 북마크, 내부 목차 이동·공개 웹 링크 유지.
- 비공개 파일 경로 링크 0건. PDF 엄격 읽기 검사 통과.
- 모든 페이지 연락처·프로필·기술 아이콘·프로젝트 그림 직접 검토. 상세 코드 비교·수상·아키텍처·회고·Store 흐름도 추가 확대 확인.
- 이미지 수정 후 총 75쪽 재렌더·이전 PDF 대조 완료. 일반판 22·27·32·36쪽, 웹·앱판 17·22·27·31쪽만 변경. 나머지 67쪽 픽셀 동일.
- 변경된 8쪽 직접 검토: Arabica 로고, CMP 아이콘·카드 이름, Wallet Nuri 표시, Store 메뉴에 가리지 않는 메인 화면 확인.

## 생성 방식

- `python scripts/build_pdf.py`: 두 판 생성.
- `scripts/build_pdf.cjs`: 격리된 로컬 문서 렌더러. 웹 앱 실행·외부 API 요청 없음.
- `scripts/pdf.css`: PDF 전용 페이지 배치. 웹 디자인 유지.
- `scripts/verify_pdf.py`: 원문 대조·페이지 수·링크 검사·북마크 삽입.
- 인쇄 시 transform만 적용하면 마지막 목록 항목이 잘리는 문제를 CSS zoom으로 해결.

## 출력 파일

- `output/pdf/Jang-MoonSu-Portfolio.pdf`: 8,695,155 bytes / SHA-256 `bd991b5f9e065eb1e3eb401cd5a363033ce2a38fa4f677c45b2919ccf690a1ce`.
- `output/pdf/Jang-MoonSu-Web-App-Portfolio.pdf`: 7,569,896 bytes / SHA-256 `773d1eaa185828a27265ae76f38ff5eb5451f2289cbc4b9924bc407191c3a811`.

## 페이지 구성

| 일반판 | 웹·앱판 | 내용 |
| ---: | ---: | --- |
| 1 | 1 | 표지 |
| 2 | 2 | 소개 |
| 3 | 3 | 보유 기술 스택 |
| 4 | 4 | 수상 · 자격 · 어학 |
| 5 | 5 | 프로젝트 |
| 6 | 제외 | STM-Simulator · 개요 |
| 7 | 제외 | STM-Simulator · 애플리케이션 아키텍처 |
| 8 | 제외 | STM-Simulator · 설정·배선·로직 실행 결과를 앱에서 확인 |
| 9 | 제외 | STM-Simulator · 회로·설정 자동 저장과 프로젝트 파일 입출력 |
| 10 | 제외 | STM-Simulator · UART 시뮬레이션의 시간 경계 오류 |
| 11 | 6 | CONS · 개요 |
| 12 | 7 | CONS · 애플리케이션 아키텍처 |
| 13 | 8 | CONS · 측위 데이터 분포와 5회 좌표 평균 |
| 14 | 9 | CONS · Beacon, Unity 연동 및 실내 측위 구현 |
| 15 | 10 | CONS · 지원 중단된 API에 의한 Android ↔ Beacon 인식 문제 |
| 16 | 11 | CONS · Android ↔ Unity 모듈 연동 문제 |
| 17 | 12 | BOOKIES · 개요 |
| 18 | 13 | BOOKIES · 애플리케이션 아키텍처 |
| 19 | 14 | BOOKIES · Oracle DB 이전 및 Web 서비스 배포 |
| 20 | 15 | BOOKIES · Spring Boot 버전 변경에 따른 Jakarta·javax 호환성 문제 |
| 21 | 16 | BOOKIES · 외부 Tomcat WAR 배포 환경의 클라우드 접속 오류 |
| 22 | 17 | Arabica · 개요 |
| 23 | 18 | Arabica · 정책·예약 실행·이력을 연결하는 백엔드 |
| 24 | 19 | Arabica · DB 백업 스케줄 관리와 외부 서버 백업·복원 |
| 25 | 20 | Arabica · DB 백업 시 장시간 Thread 점유 문제 |
| 26 | 21 | Arabica · 비동기 실행 다음으로, 완료 확인과 실행 권한 보완 |
| 27 | 22 | CMP · 개요 |
| 28 | 23 | CMP · NSS·NBU 외부 API와 테넌트별 조회 연동 |
| 29 | 24 | CMP · 대량 데이터 조회 시 외부 API 응답 대기로 인한 처리 지연 |
| 30 | 25 | CMP · Kubernetes 백업 연동 확장에 따른 테넌트별 정책 조회 문제 |
| 31 | 26 | CMP · 평균 응답시간·P95·오류율을 함께 비교 |
| 32 | 27 | Wallet · 개요 |
| 33 | 28 | Wallet · 보안 필터·Dispatcher·업무 API 요청 처리 |
| 34 | 29 | Wallet · 보안 처리·Web–App 로그인·알림 연동 |
| 35 | 30 | Wallet · XSS 정제 결과를 실제 요청 본문에 반영 |
| 36 | 31 | Store · 개요 |
| 37 | 32 | Store · 커머스 API·Wallet 인증·데이터 저장 연동 |
| 38 | 33 | Store · DB 전환·관계 구조 정리·SSE 인증 연동 |
| 39 | 34 | Store · Store DB 마이그레이션의 외래키 참조 오류 |
| 40 | 35 | 연락처 |
