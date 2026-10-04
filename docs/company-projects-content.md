# 회사 프로젝트 웹 콘텐츠 반영 기록

- 반영일: 2026-10-04.
- 대상: `index.html`의 Arabica·CMP·Wallet 프로젝트와 프로젝트 탐색 링크.
- 사용자 범위: 현재까지 확보한 프로젝트 내용 추가. 디자인 변경·보완 설계·회고 페이지·PDF 생성은 제외.
- 유지: 기존 소개·STM-Simulator·CONS·BOOKIES 본문, `styles.css`, `app.js`, 기존 이미지와 PDF.
- 구성: 기존 project·detail·case-facts·flow 컴포넌트 재사용. 상세 내용은 기본 펼침.
- 원본 회사 코드·설정·계정·서버 주소·보고서는 공개 저장소에 복사하지 않음.

## 근거와 표현 범위

| 프로젝트·사례 | 확인한 근거 | 반영한 내용과 경계 |
| --- | --- | --- |
| Arabica 실행 분리 | 개인 Git `cbc77cba`, `c4ffc58f`, `9fe50eea`, `7e5e1818`, `dde065e5`, `56827f66` | 비동기 진입·원격 백그라운드 실행·주기적 결과 판독과 검증·이력 기록. Spring Event 전환, 복원 전체의 비동기화, 점유율·처리량 개선 수치는 주장하지 않음 |
| Arabica 복원 이력 | 개인 Git `70b70478` | 문자열 왕복 변환 대신 날짜·시간 객체 전달·저장. 당시 성공 화면·재시험 로그로 표현하지 않음 |
| Arabica 차등 백업 | 개인 Git `16d41794` | 명령 포맷과 스크립트 인자 불일치 수정. 실제 계정·인자 값은 포함하지 않음 |
| CMP API 연동 | 개인 주간보고, NSS 코드, CMP v2.0 산출물·API 명세 | NSS·NBU 연동과 테넌트별 정책 조회. v2.1의 후속 변경을 개인 기여로 포함하지 않음 |
| CMP WebFlux 전환 | 2025-06-30~07-04 주간보고, WebClient·Mono 코드, 사용자 확인 | 데이터 증가·외부 API 응답 대기와 처리 구조 전환. 특정 예외·개선율·평균 응답 감소 수치는 추가하지 않음 |
| CMP 성능 시험 | 개인 성능 시험 자료와 기존 공개 도식 | 사용자 확인에 따라 동일 호스트 사양. 3만·20만 건, 동시 사용자 1·5·10명, 각 1분. OS별 평균·P95·오류율 비교를 MVC/WebFlux 전후 시험과 구분 |
| Wallet 식별자·DB 전환 | 개인 Git `0026c7c9`, `58f279ae`, `870e4a3c`, `a994eba5` | MariaDB→PostgreSQL 구문 변경과 내부 PK·소셜 식별자 분리를 별도 구현으로 소개. 운영 데이터 무손실 이전 주장은 제외 |
| Wallet Entity·SQL 매핑 | 개인 Git `b6d5c097`, `7ccb21ce` | 테이블·컬럼명·enum 매핑 수정. Bean 순환 의존 장애로 설명하지 않음 |
| Wallet 계좌 저장 | 개인 Git `494ae46f`, `ca62dab3`, `384bda8c` | 반환 Map과 INSERT 파라미터·ID 타입 불일치 수정. PK 변경을 직접 원인으로 단정하지 않음 |
| Wallet·Store 로그인 | Wallet 개인 Git `739d9159`, Store 개인 Git `04a3d22`, `49b70eb`, `56a6421` | Wallet 인증 결과 전달과 Store SSE 상태 관리·매핑 수정의 담당 경계 표시. 객체 자체의 DB 저장·다중 인스턴스 장애·Dispatcher JSON 래핑 장애 주장은 제외 |
| Wallet 요청 정제 | 개인 Git `53cb1ba5`, `69387475`, `6fad4298` | 정책 리소스 로딩, JSON 값 교체·본문 재구성, 정책 객체 재사용. 모든 XSS 차단·보안 시험 통과·성능 개선율은 주장하지 않음 |

- Git 수정은 확인했지만 당시 실행 캡처·회귀 시험 결과가 없는 사례는 코드 변경과 처리 흐름으로만 설명.
- 처리 도식은 구현 구조 설명용. 당시 성공 화면이나 재현 시험 결과로 표시하지 않음.
- Redis 복구, 스케줄 삭제 후 이력 보존은 사용자 제외 지시에 따라 사용하지 않음.
- 추가 보완 설계(작업 ID·상태 관리, 완료 알림, 권한 보강, 전용 실행기)는 미구현 제안으로 이번 웹 반영에서 제외.

## 재사용한 시각 자료

- 기존 `career-portpolio/assets/architecture/`의 아래 도식을 내용 검토 후 바이트 변경 없이 복사.
  - `backup-overview.svg`, `backup-application.svg`.
  - `integration-overview.svg`, `integration-application.svg`, `integration-tenant-policy.svg`, `integration-benchmark-stability.svg`.
  - `wallet-overview.svg`, `wallet-application.svg`.
- 원격 실행·XSS 등 새로 구체화한 사례는 기존 HTML 흐름도 스타일 재사용.
- 기존 XSS 도식의 테스트 성공 문구와 MVC/WebFlux 응답시간 수치 도식은 새 근거 범위와 맞지 않아 가져오지 않음.
- 포함 아이콘 출처: `assets/architecture/company-icon-sources.json`. 기존 Devicon MIT·Lucide ISC 라이선스 전문 유지.
- 별도 증빙 화면 합성·이미지 생성·새 디자인 시안 제작 없음.

## 문서 구분

- 35페이지 구성안은 별도 제작 계획이며 현재 HTML을 35페이지로 변경한 결과가 아님.
- 기존 PDF는 회사 프로젝트 추가 전 버전. 웹 다운로드 링크의 설명에도 구분 표시.

## 확인 결과

- 1440·1024·768·390·360px 화면 폭에서 페이지 가로 넘침 없음.
- 6개 프로젝트 순서, 내부 링크·접근성 제목 참조, 이미지 로딩, 상세 기본 펼침 확인.
- 이미지 좌클릭 드래그·휠 확대·닫기, 상세 접기·펼치기 확인.
- 기존 소개·STM-Simulator·CONS·BOOKIES·연락처 본문 DOM 동일. CSS·JavaScript·PDF 변경 없음.
- 재사용 SVG 8개는 기존 파일과 동일. 외부 파일 참조·스크립트 없이 자체 렌더링.
- 데스크톱·모바일 실행 화면 직접 확인. 새로운 API·DB 실행 성공을 재현한 시험은 아님.
