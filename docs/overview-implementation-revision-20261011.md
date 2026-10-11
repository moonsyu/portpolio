# 개요·구현·Store 흐름도 변경 기록

- 변경일: 2026-10-11.
- 범위: `portpolio` GitHub Pages. 기존 디자인과 프로젝트 순서 유지.
- 제외: PDF·PPT 생성, 원본 문서 수정, 원본 서비스 실행.

## 주요 기술·구간명

| 프로젝트 | 강조 기술 |
|---|---|
| STM-Simulator | STM 학습 · C · Electron |
| CONS | BLE · Unity 연동 · Android |
| BOOKIES | AWS EC2 / RDS / S3 · Spring Boot · Oracle |
| Arabica | Spring Boot · SSH · MariaDB |
| CMP | Spring WebFlux · WebClient · NetBackup API |
| Wallet | Spring Boot · RSA · AntiSamy |
| Store | Spring Boot / WebFlux · PostgreSQL · SSE |

- 주요 기술: 기존 아이콘 중 3개를 앞에 배치하고 크기·테두리로 강조. 나머지 기술 유지.
- 보조 설명: 마우스 및 키보드 포커스의 기술명 툴팁 유지.
- 구현 구간: `IMPLEMENTATION(구현)`.
- 트러블슈팅 구간: `TROUBLESHOOTING(트러블 슈팅)`. Beacon·Unity 번호·분류 꼬리표 제거.
- 애플리케이션 아키텍처: 기존 `APPLICATION ARCHITECTURE` 유지.

## 내용 변경 근거

- CONS 제목: `Beacon, Unity 연동 및 실내 측위 구현`.
- CONS 구현: BLE·UUID 필터링·Minor 층 판별·RSSI 수신 → Retrofit 좌표 조회·좌표 계산 공동 구현 → Android–Unity 좌표 전달·AR 화면 통합.
- 근거: 기존 `docs/project-content-refinements.md`, 개인 근거 저장소의 `CONS/API_호환_추가근거_20261010.md`와 프로젝트 분석.
- 기여 범위: 실내 측위는 공동 구현. Unity 전체·서버 전체의 단독 구현으로 확대하지 않음.
- Wallet: DB Migration 구현 항목을 `보안 기능 구현`으로 교체.
- Wallet 내용: RSA 통신 암호화·키 발급·공개키 만료 검증, AntiSamy 입력 검사·정제 결과의 요청 본문 반영.
- 근거: 개인 근거 저장소 `UWS/Wallet_디지털지갑/프로젝트_분석.md`의 인증·보안 담당 내용 및 기존 XSS 수정 근거.
- 표현 범위: 모든 XSS 차단·보안 인증 획득 등 확인하지 않은 성과 추가 없음.

## 원본 화면

| 적용 위치 | 원본 문서 | 페이지·미디어 | 처리 |
|---|---|---|---|
| Arabica 전체 대시보드 | `백업프로젝트_1차보고서_화면_설계서.pptx` | 4쪽 · `ppt/media/image3.png` | 원본 PNG 그대로 추출 |
| Wallet 메인 | `veta_use_guide-union.pptx` | 36·37쪽 · `ppt/media/image75.tiff` | PNG 변환, 디코딩 픽셀 동일 |
| Wallet 코인 | `veta_use_guide-union.pptx` | 44쪽 · `ppt/media/image88.tiff` | PNG 변환, 디코딩 픽셀 동일 |

- Arabica 출처: `신규입사자/Project/설계/산출물/1차 보고/보고서/`.
- Arabica 4쪽 설명: 헤더·사이드바·화면 전환·스토리지 사용 현황·사용 추이 그래프 구현. 초기 구현 화면이며 최신 운영 화면이나 백업 오류 수정 후 재시험 증거로 사용하지 않음.
- Wallet 출처: `산출물 목록/2025/newyork/wallet/`.
- Wallet: 원본 화면을 그대로 적용하라는 사용자 확인 반영. UI 재제작·생성·잔액 변경 없음. 주소·인증 정보가 노출된 다른 화면은 미사용.
- 화면은 서비스 개요에 사용. 프론트엔드 화면 전체를 개인 구현으로 주장하지 않음.
- 문서·미디어·게시 파일 해시 및 이미지 크기: `assets/overview/sources.json`.
- 이전 화면 파일·출처 기록은 이력으로 유지. 현재 HTML은 새 파일을 참조.

## Store 흐름도·화면 조사

- 흐름도: 변경 전 자식→부모 참조 관계 → 참조 대상 유일성 조건 불충족·마이그레이션 실패 → 기존 부모 PK 참조 교정.
- 장바구니·결제 옵션을 두 열에 배치하고 각 열의 관계를 위에서 아래로 표현.
- 4개 외래키 교정 사실 유지. 도식 내용은 기존 검증된 DDL 차이에 근거.
- 생성기: `scripts/build_troubleshooting_flows.mjs`.
- 출력: `assets/flows/store-migration.svg`, 960×1280.
- Store 실제 웹 화면: `newyork/store`, `veta_prod_01/store`, `time_square`, 프론트 설계 문서, 관련 주간보고·프로젝트 자료 확인.
- 조사 결과: 모바일 기획 화면·코드·흐름도 확인. 요청한 웹 전체 화면의 확실한 캡처 원본 미확보.
- 최초 조치: 개요 이미지 자리 유지, 사용자에게 파일명·폴더 경로 요청. 기획 화면을 실제 실행 화면으로 대체 게시하지 않음.

### Store 실행 화면 후속 반영

- 사용자 제공 경로: `venetaStoreAPP/venetaStoreWeb`.
- 사용자 실행·캡처 요청에 따라 React·Vite 프론트엔드를 로컬 실행하고, `http://127.0.0.1:3000/`의 현재 메인 화면 캡처 적용.
- 적용 파일: `assets/overview/store-main.jpg`. 브라우저 캡처 원본 그대로 사용.
- 화면 확대 요청 반영: 1440×900 데스크톱 뷰포트에서 재캡처. 저장된 원본 이미지 1425×891px.
- 최신 캡처: 좌측 메뉴를 연 상태의 Goods·Log In·support·KR Language 표시.
- 원본 메뉴 너비 `90%` 유지. 메뉴가 메인 화면 대부분을 가리는 실제 동작 그대로 캡처하며, Store 앱 레이아웃 수정 없음.
- 개요 왼쪽 이미지 자리를 교체하고, 원본 비율 유지·클릭 확대 연결. 세로형 이미지의 높이 제한을 제거해 왼쪽 영역 너비에 맞춰 표시.
- 검증 범위: 프론트엔드 렌더. 백엔드 `localhost:8081` 미실행으로 상품 조회 API 연결 실패 상태. 정상 거래·로그인 연동의 증거로 사용하지 않음.
- Store 앱 소스 변경 없음. 실행 화면 전체를 개인 프론트엔드 구현으로 주장하지 않음.
- 후속 이미지 검증: 1440·390px에서 가로 넘침 없음, 모바일 세로 배치·원본 비율 유지 확인. 이미지 로드·확대·닫기 직접 확인.

## 직접 검증

- 360·390·768·1024·1440px에서 7개 프로젝트의 개요·아이콘 가로 넘침 없음.
- 모바일 이미지·설명 세로 배치, 데스크톱 개요 두 열 배치 확인.
- 구간명 통일 및 아키텍처 명칭 7곳 유지 확인.
- Wallet 구현에 DB Migration 제거·보안 기능 반영 확인.
- Arabica·Wallet 이미지 확대와 닫기 동작 확인.
- Store 이미지 좌클릭 드래그·휠 확대·Escape 닫기 확인.
- 기술 아이콘 키보드 툴팁 확인.
- Store 도식의 화살표 10개 모두 하향. SVG 글자 영역이 캔버스 안에 포함됨을 확인하고 실제 렌더 직접 검토.
- 페이지 JavaScript 오류·이미지 로드 실패 없음.
- Wallet PNG 변환 전후 디코딩 픽셀 동일성 확인.

## 자료 탐색 위임

- 실제 에이전트 ID: `/root/overview_screen_sources`.
- 요청 설정: `gpt-5.6-luna` / `low`. 실제 런타임 모델의 별도 확인 정보 없음.
- 배정: 원본 보고서·가이드·주간보고의 화면 후보 탐색. 원본 수정·프로젝트 실행·포트폴리오 편집 금지.
- 상태: 조사 완료. Store 웹 화면 미확보.
- 최종 선정·기여 범위·화면 픽셀·페이지 수정·브라우저 검증: 주 에이전트 직접 수행.
- 후보 보정: Store 기획 문서의 세로 이미지를 데스크톱 실제 화면으로 오인하지 않도록 직접 확인 후 제외.
