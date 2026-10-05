# 장문수 개발 포트폴리오

- 웹사이트: [moonsyu.github.io/portpolio](https://moonsyu.github.io/portpolio/)
- 구성: HTML·CSS·JavaScript 기반 정적 사이트
- 프로젝트: STM-Simulator → CONS → BOOKIES → Arabica → CMP → Wallet → Store
- 소개: Java 백엔드, IoT 연동, 학습 도구 개발 경험
- 순서: 소개(01) → 프로젝트(02) → 연락처(03)
- 보유 기술: 기술 아이콘과 이름을 함께 표시
- 수상·자격: 별도 목록, 수상 기관·행사명·일자 및 자격·어학 등급·취득일 표시
- 기능: 소개·프로젝트 탐색, 상세 내용 항상 표시, 이미지 드래그·휠 확대, 실행 GIF 재생·일시정지, 반응형 레이아웃
- 애플리케이션 아키텍처: 기술·기능 아이콘, 모듈별 영역, 요청·응답·저장 흐름을 표현한 SVG 도식 7개

## 최신 내용 수정 · 2026-10-05

- 프로젝트 요약 막대·개요 이미지 하단 캡션 제거; 기존 디자인 유지.
- 데이터·배포 기술에 MySQL·MariaDB·PostgreSQL 아이콘 추가.
- STM TESTING·REGRESSION 및 BOOKIES 별도 QnA 구역 제거; CONS 측위 비교를 IMPLEMENTATION 맨 앞으로 이동.
- BOOKIES의 Jakarta·javax 및 WAR EL 의존성 변경을 실제 Git 코드 전후 이미지로 표시.
- Arabica·CMP·Wallet XSS 흐름도, Store 외래키 참조 변경 도식 추가.
- Wallet 구현 항목을 DB Migration·SSE/QR 로그인·SMS/FCM 알림으로 정리.
- Store 마이그레이션 FK 4개 수정과 Wallet DB 전환을 구분; 근거가 연결되지 않은 Wallet FK 장애 후보는 보류.
- 후속 요청: Wallet 바로 아래에 7번 Store 독립 프로젝트 추가. DB 오류 사례를 Store로 이동하고 개요·아키텍처·DB 전환/관계 정리/SSE 구현 내용 추가.
- 상세 출처·표현 범위·검증: [2026-10-05 반영 기록](docs/portfolio-refinements-20261005.md).
- 아래 날짜별 항목은 이전 변경 이력. PDF는 이번 웹 변경에 맞춰 재생성하지 않음.

## 회사 프로젝트 추가 · 2026-10-04

- 기존 스타일·반응형 레이아웃·이미지 확대 동작을 유지하고 회사 프로젝트 3개 추가.
- Arabica: 정책·예약 백업, 비동기 실행과 결과 판독·검증 분리, 장시간 백업의 Thread 점유 문제.
- CMP: NSS·NBU API 연동, MVC→WebFlux 전환, 테넌트별 조회 범위 수정, 평균·P95·오류율을 함께 비교한 부하 시험.
- Wallet: 사용자 식별자 분리, DB 제품 전환, XSS 정제값 반영. 계좌·Entity/SQL·SSE 매핑 트러블슈팅은 사용자 요청으로 제거.
- 추가 보완 설계·회고 페이지는 보류. 현재 구현과 Git에서 확인한 변경만 사용.
- 기존 회사 프로젝트 도식 8개를 재사용. 출처·포함 범위는 [콘텐츠 반영 기록](docs/company-projects-content.md)에 정리.
- 이번 변경은 웹페이지에만 반영. 다운로드 PDF는 기존 프로젝트 구성 유지.

## 프로젝트 내용 보강 · 2026-10-04

- 기존 디자인 유지. 트러블슈팅 제목 6개 수정, 지정 사례 5개 제거.
- STM-Simulator: JSON/localStorage 자동 저장, 프로젝트 입출력, 테스트 도구·케이스 기준, UART 24조건 회귀 검사 추가.
- CONS: 비콘 수집·층 판별·좌표 계산·서버/Unity 연동 담당 내용과 측위 비교 조건 추가.
- BOOKIES: QnA·Android REST API 구현, 실습 환경의 Spring/JDK/Tomcat 전환, WAR 접속 오류의 EL 의존성 보완 추가.
- 애플리케이션 아키텍처 6개의 하단 설명·확대 안내 문구 제거. 이미지 확대 기능 유지.
- STM·Beacon GIF 이미지를 클릭하거나 키보드로 선택해 재생/정지 전환. 별도 버튼·캡션 제거.
- SSE의 최초 구현·피드백 반영과 과도한 외래키 관계 문제는 별도 조사. 이번 웹페이지에 해당 사례를 다시 추가하지 않음.
- 상세 근거·표현 범위: [프로젝트 보강 기록](docs/project-content-refinements.md).

## 로컬 실행

```powershell
python -m http.server 8080
```

- 브라우저에서 `http://localhost:8080` 접속
- 별도 패키지 설치·빌드 과정 없음

## 파일

- `index.html`: 소개·프로젝트·경력·연락처
- `styles.css`: 반응형 디자인·인쇄·모션 감소 설정
- `app.js`: 이미지 확대·탐색 상태 표시
- `assets/`: 포트폴리오에 사용한 실제 프로젝트 화면·프로필 사진
- `assets/architecture/`: 애플리케이션 아키텍처 SVG·아이콘·출처·라이선스
- `assets/evidence/`: BOOKIES 실제 Git 코드의 전후 발췌 렌더
- `assets/flows/`: 확인된 처리 흐름·관계 변경을 재구성한 도식
- `scripts/build_troubleshooting_flows.mjs`: 처리 흐름·Store FK 변경 도식 생성기
- `scripts/build_store_diagrams.py`: 기존 디자인을 사용하는 Store 개요·애플리케이션 아키텍처 생성기
- `scripts/build_architectures.py`: 아키텍처 도식 생성 스크립트(Python 표준 라이브러리)
- `.nojekyll`: 정적 파일 배포 설정

## 포트폴리오 전면 개편 계획

- [개발자 포트폴리오 제작 기준](docs/portfolio-redesign/README.md)
- [35페이지 구성과 내용별 수정·확인 사항](docs/portfolio-redesign/페이지_구성_및_확인사항.md)
- Canva Almost White and Black 템플릿 기반 PPTX 제작 계획. 최신 내용 결정일: 2026-10-02.
- 2026-10-04 `remote-codex`에서 이전. 현재 웹사이트와 PDF에 적용한 결과가 아닌 제작 기준 문서.

## 배포

- GitHub Pages: `main` 브랜치의 `/` 경로에서 배포
- `main`에 변경 사항 푸시 시 사이트 갱신
- 프로젝트 사이트 하위 경로에서 작동하도록 CSS·JavaScript·이미지에 상대 경로 사용

## 콘텐츠 범위

- 기존 18쪽 포트폴리오의 프로젝트·화면을 웹 형식으로 재구성
- 특정 기업 지원 문구를 일반 개발자 소개로 변경
- 프로젝트 전체 시스템과 개인 구현 항목을 구분
- STM-Simulator: 지원 C/HAL 동작 모델 기반 학습용 도구
- CONS 측위 결과: 기존 프로젝트 측정 기록의 관찰 범위
- 프로젝트 화면·브랜드·도서 표지 등 제삼자 자산의 권리는 각 권리자에게 귀속
- 원본 발표 파일·내부 근거 자료·자격 증명은 포함하지 않음

## 아키텍처 편집 및 아이콘 출처

```powershell
python scripts/build_architectures.py
```

- 기술 아이콘: [Devicon](https://github.com/devicons/devicon), MIT 라이선스
- 기능 아이콘: [Lucide](https://github.com/lucide-icons/lucide), ISC 라이선스
- 원본 아이콘·고정 커밋별 다운로드 경로: `assets/architecture/icon-sources.json`
- 회사 프로젝트 도식에 포함된 아이콘 출처: `assets/architecture/company-icon-sources.json` (동일 라이선스·고정 커밋)
- 라이선스 전문: `assets/architecture/DEVICON-LICENSE.txt`, `assets/architecture/LUCIDE-LICENSE.txt`
- 기술 로고는 사용 기술의 식별 목적으로 표시하며 각 상표권은 해당 권리자에게 귀속
- 결과 SVG에 아이콘을 포함하여 외부 CDN 연결 없이 렌더링

## 실행 화면 및 접근성

- 프로젝트 개요: 상단 번호·프로젝트명, 왼쪽 실행 화면 또는 서비스 개념도, 오른쪽 소개·참여 정보·기존 설명 3개·기술 아이콘 순서
- 프로젝트 상단 오른쪽 분류 문구 제거; 기술 스택은 아이콘만 표시하고 마우스·키보드 포커스 시 이름 제공
- 보유 기술 AI 항목: OpenCode, OpenClaw, Harness Engineering, Ponytail; 해당 항목은 공식 로고 대신 Lucide 기능 아이콘 사용
- STM LED GIF: 실제 애플리케이션의 HAL GPIO LED 예제를 실행 버튼 클릭 전부터 기록
- 기록 범위: 시작 버튼, LED 점멸, 실행 시간·전류 표시; 원본 화면을 잘라 GIF로 변환
- 모션 감소 설정에서는 정지 이미지로 시작하며 GIF 이미지 클릭·Enter·Space로 재생/정지 전환
- GIF 정지 시 기존 정지 이미지를 표시하고 재생 시 GIF를 다시 시작
- 확대 이미지: 좌클릭·터치 드래그, 휠 확대·축소, 화면 맞춤 및 방향키 이동
- 일반 페이지의 아키텍처 영역에서는 세로 휠 입력을 페이지로 전달

## PDF 다운로드 및 갱신

- 상단 `PDF 다운로드` 버튼으로 포트폴리오 파일 저장
- 출력: `output/pdf/Jang-MoonSu-Portfolio.pdf`
- 상단 `웹·앱 PDF` 버튼: `output/pdf/Jang-MoonSu-Web-App-Portfolio.pdf` 별도 편집본 저장
- 별도본: STM-Simulator·임베디드 학습 기술·SSAFY 임베디드 트랙 및 전역 IoT·하드웨어 소개 제외
- 사용자 지정 유지 항목: CONS 소개·아키텍처·개선·트러블슈팅과 모바일 연동 기술, BOOKIES 전체 내용
- 형식: PPT와 같은 16:9 가로 슬라이드, 1280 × 720 pt
- 수상 페이지: 왼쪽 수상 세로 목록·가로 구분선, 오른쪽 자격·어학 카드
- 마지막 연락처 페이지: 본문과 같은 밝은 배경·푸른색 링크
- 웹페이지의 색상·강조·좌우 배치를 반영하고 각 구역을 독립 슬라이드로 출력
- 순서: 표지 → 소개 → 기술 스택 → 수상·자격 → 프로젝트 목록 → 프로젝트별 개요·아키텍처·구현·트러블슈팅 → 연락처
- 개요와 아키텍처를 서로 다른 페이지로 분리하고 글자를 선택·검색할 수 있도록 출력
- 소개·수상·자격·프로젝트·개선·트러블슈팅 내용: `index.html`에서 추출
- 기존 프로젝트 화면·아키텍처 사용, 새 이미지 생성 불필요
- GIF는 실행 화면 한 장과 온라인 재생 링크로 표시해 웹페이지의 좌우 배치 유지
- PDF 갱신 요청 시 사이트 내용에 맞춰 별도 생성. 2026-10-04 회사 프로젝트 추가는 웹 전용이며 기존 PDF에 미반영.
- 준비: `python -m pip install -r scripts/requirements-pdf.txt`, `npm install`
- 두 파일 생성: `python scripts/build_pdf.py`
- 선택 생성: `--variant full` 또는 `--variant web-app`
- 기본 글꼴: Windows 맑은 고딕, PDF에 글꼴 포함
- 다른 환경: `--font-dir`로 `malgun.ttf`·`malgunbd.ttf` 폴더 지정
- 공유 Node 패키지 환경: `--node-modules`로 패키지 폴더 지정

## 트러블슈팅 검증 자료

- 공통 형식: 문제 → 원인 → 해결 / 실제 동작 화면; 화면의 출처·검증 결과 제목은 본문에서 생략
- `assets/stm-uart-verified.webp`: 수정된 STM 앱에서 9600 baud·260ms 입력·20ms 단계 실행으로 RX/TX 일치를 직접 확인한 실행 모니터 화면(2026.09.23)
- `assets/cons-unity-runtime.webp`: 캡스톤1 개발 시스템 발표 7쪽의 Android–Unity AR 실행 화면; 빌드 성공 로그가 아닌 통합 앱 실행 결과
- `assets/cons-beacon-rssi.gif`: 디지털 학회 추계 자료의 `좌표 측위 영상.mp4` 01:00–01:12에서 실제 비콘 이름·RSSI 수신 목록을 연속 crop·resize한 12초 GIF(5fps 추출, UI·수치 합성 없음)
- Beacon 영상의 범위: 수신 목록·RSSI 변화 확인; 원본에 버튼 조작이 있으므로 자동 갱신·위치 정확도·특정 API 변경의 효과로 확대 해석하지 않음
- Beacon GIF: 재생·일시정지 제공, 모션 감소 설정에서는 `cons-beacon-rssi-poster.webp` 표시
- BOOKIES: DB 이전·Web 배포·접근 제어의 구현 내용 유지, 개선 효과로 표현한 별도 박스 제외
- 이미지 확대 화면: 닫기 버튼만 표시, 드래그·휠·방향키·두 번 클릭/0 키 화면 맞춤 유지
