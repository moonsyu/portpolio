# 프로젝트 내용·시각 근거 정리 · 2026-10-05

- 적용 대상: `portpolio` GitHub Pages.
- 기존 디자인 유지; 후속 요청에 따라 Wallet 다음에 Store 독립 프로젝트 추가. PDF·경력기술서 저장소 변경 없음.
- 조회 원본·회사 코드·내부 ERD·주소·자격 증명은 공개 저장소에 포함하지 않음.

## 반영 내용

- 데이터·배포 기술: MySQL, MariaDB, PostgreSQL 아이콘과 이름 추가.
- 프로젝트 상세의 펼침·접기 요약 막대와 개요 이미지 하단 캡션 제거. 본문은 항상 표시.
- STM: 실행 결과 설명을 로직·프로그램 중심으로 변경; TESTING·REGRESSION 구역 제거.
- CONS: 측위 비교 구역을 첫 IMPLEMENTATION으로 이동; Beacon API 교체 내역 구체화.
- BOOKIES: Web 파트 팀장 표시; 별도 QnA 구현 구역 제거; Jakarta·javax 전환과 WAR 의존성의 실제 Git 코드 전후를 세로 이미지로 배치.
- Arabica: DB 스케줄·외부 백업·복원 제목 수정; 백업 Thread 점유 문제와 실행/결과 확인 분리 흐름도 반영.
- CMP: 외부 API 동기 대기와 WebFlux·Mono 응답 처리 비교 흐름도 반영.
- Wallet: DB Migration, SSE·QR 로그인 연동, SMS·FCM 알림으로 구현 항목 구성; XSS 요청 본문 반영 흐름도 추가.
- Store: 처음 Wallet 하위에 표시했던 DB 마이그레이션 FK 오류를 후속 요청에 따라 7번 Store 독립 프로젝트로 이동.
- Store 독립 구성: 개요 → 애플리케이션 아키텍처 → 구현 → 기존 FK 트러블슈팅. Wallet의 DB 전환 구현 이력은 유지하고 오류 사례만 분리.

## Store 독립 프로젝트 근거

- 개요·개인 구현: DB 전환, 스키마 관계 수정, Wallet 인증과 웹 SSE 연동. 전체 커머스 기능을 단독 개발했다고 표현하지 않음.
- 아키텍처: 웹 API/SSE → Store Controller·Service → MyBatis DAO/Mapper → PostgreSQL; Wallet App → Wallet API → Store 인증 승인 전달.
- Store `6e9899b`의 `NetWorkController.java`, `NetworkServiceImpl.java`, `LoginDAO.java`와 `pom.xml`에서 일반 요청·기능 분기·MyBatis·기술 구성 확인.
- SSE 이력: Store `3cd78a8` 메모리 연결 관리, `04a3d22` 인증 상태 DB 저장·조회·SSE 결과 반환; Wallet `739d9159` 인증 결과 전달.
- SSE DB 저장 내용은 인증 상태이며 Java Sink 객체가 아님. MyBatis 호출까지 전체 비동기·논블로킹이라고 주장하지 않음.
- 아키텍처는 일반 요청·SSE·저장 경로 중심의 요약. 별도 프로필 조회 등 모든 API를 나열하지 않음; Store에서 Wallet DB로 직접 접근하는 연결은 없음.
- 관계 구조: `822f953`의 FK 참조 교정과 `a134f73`/`43d5a71`의 후속 중간 매핑·복합키 정리를 별도 구현 항목으로 구분.
- 생성: `python scripts/build_store_diagrams.py`; 기존 Diagram 도구와 이미 등록된 Devicon/Lucide 아이콘 사용.

## CONS API 교체 근거

- Android Git `6a3d0cb`, 2024-05-11, `BeaconBackgroundService.java` 변경 전후 확인.
- 전후 동일 import: `org.altbeacon.beacon.BeaconManager`.
- 전후 동일 라이브러리: `org.altbeacon:android-beacon-library:2.20.6`.
- 변경: `bind → bindInternal`, `unbind → unbindInternal`, `startRangingBeaconsInRegion → startRangingBeacons`.
- API 호출 위치·탐색 필터 변경도 포함된 커밋; 라이브러리 자체를 다른 제품으로 교체한 사례로 표현하지 않음.
- 기존 Beacon GIF는 실제 수신 목록 기록; 특정 API 변경 전후의 통제 실험이나 위치 정확도 증거로 사용하지 않음.

## BOOKIES 코드 이미지 근거

- 이미지: 실제 Git 파일의 선택한 행을 가독성 있게 렌더링한 코드 화면. 당시 IDE·오류 로그·성공 콘솔의 캡처는 아님.
- `bookies-namespace-before.png` / `bookies-namespace-after.png`:
  - 기준 `7f15814`와 부모 `6f4ae9f`, 2025-02-18.
  - `build.gradle`: Spring Boot `3.0.4 → 2.7.8`, Servlet API `5.0.0 → 4.0.4`, JSTL `2.0.0 → 1.2`.
  - `QnaController.java`: `jakarta.servlet.http` → `javax.servlet.http`.
  - `Qna.java`: `jakarta.persistence` → `javax.persistence`.
  - 선택 행: Boot 5행; Servlet/JSTL 이전 53–55행·이후 59–61행; Controller 9–10행; Entity 4행.
  - `jakarta.servlet:jakarta.servlet-api:4.0.4`는 실제 코드 표기 그대로 보존. Maven 좌표 이름과 Java package namespace는 구분.
  - Boot `2.6.5`와 Tomcat `9.0.58`은 후속 조정이며 위 namespace 전환 시점과 합치지 않음.
- `bookies-el-before.png` / `bookies-el-after.png`:
  - 기준 `e557f0a`와 부모 `52371d6`, 2025-02-20.
  - `build.gradle` 이전 76–78행·이후 76–84행.
  - `org.glassfish:javax.el:3.0.0`, `org.apache.tomcat.embed:tomcat-embed-el:9.0.58` 추가.
  - 같은 커밋에 devtools 설정 변경도 존재; EL만 변경했다고 단정하지 않음.
  - 당시 구체 예외·HTTP 상태·수정 후 실행 로그는 미확보. 합성 오류·성공 화면 사용 안 함.
- 기술 대조: [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide), [Spring Boot 2.7.8 문서](https://docs.spring.io/spring-boot/docs/2.7.8/reference/html/).

## 흐름도 근거와 범위

- 생성: `node scripts/build_troubleshooting_flows.mjs`.
- 산출: `assets/flows/` SVG 4개; 코드·보고서에서 확인한 흐름을 공개 가능한 일반 개념으로 재구성.
- Arabica:
  - UWS의 `Arabica_흐름도.pptx`, `Arabica_최종_보고서.pptx`와 백업/결과 확인 코드를 함께 대조.
  - Git `cbc77cba` 비동기 진입, `c4ffc58f` 원격 백그라운드 실행, `dde065e5` 결과 검증, `56827f66` 5분 fixed-delay 확인.
  - `10개 이상의 DB 백업 시 오류`는 사용자가 제공한 경험. 해당 수치를 자동 재현하거나 동시 실행 한계로 측정했다는 뜻은 아님.
  - 주기적 결과 파일 확인 구조; Spring Event 기반 처리나 작업 큐 기반 상태 관리로 표현하지 않음.
- CMP:
  - 기존 MVC 동기 외부 API 호출과 WebClient·Mono 응답 처리 흐름을 비교.
  - 별도 BENCHMARK의 OS 비교 결과를 MVC/WebFlux 전환 효과로 합치지 않음.
- Wallet XSS:
  - 기존 정제값 반영 근거에 맞춰 JSON 순회 → 문자열 정제 → 값 교체 → 요청 본문 재구성 표현.
  - 실제 공격 재현·보안 인증·모든 XSS 차단을 입증한 도식으로 사용하지 않음.

## Wallet 구현 근거

- DB 전환: `0026c7c9`의 MariaDB → PostgreSQL SQL 문법 변경 및 개인 프로젝트 기록.
- SSE·QR: `363cd22b`와 개인 주간보고의 QR 승인 연동; Store 구독·Wallet 승인 결과 전달 구분. QR 스캐너 UI 개발로 확대하지 않음.
- SMS: `099ab144` 인증·안내 문자 처리, `8d8624d5` 전송 결과 기록.
- FCM: `d5c9c874` 알림 전송, `f4066f39` 수신 토큰 등록.

## Store와 Wallet DB 사건 구분

- Store:
  - Git `822f953`, 2025-10-14, 본인 작성 `schema.sql migration` 커밋.
  - 장바구니·결제 옵션 연결의 FK 4개: 비유일 상품·옵션 컬럼 참조 → 기존 부모 PK 참조.
  - 수정 전 FK 행: 523, 536, 694, 711. 수정 후: 498, 511, 667, 678.
  - 참조 대상의 PK 선언과 추가 UNIQUE 부재를 원본 DDL에서 대조.
  - 같은 주간보고의 Store 마이그레이션·DB 리뷰 기록과 대조.
  - 원자료의 DB 제품 표기는 MySQL → PostgreSQL. Wallet의 MariaDB 표기를 Store에 옮기지 않음.
  - 장애 경험은 사용자 진술, 수정 내용은 Git 전후 근거. 재실행 성공 로그·운영 무결성 검증 결과는 추가하지 않음.
  - 10월 16–20일의 중간 매핑 테이블 정리·FK 재설정은 별도 후속 변경이며 한 번의 장애 해결로 합치지 않음.
- Wallet:
  - 전체 refs의 주요 DDL 85개 스냅샷과 JPA 변경 이력 검사.
  - 사용자께서 제외한 통화 FK 변경은 이번 사례에서 제외.
  - `278d7a08` 중복 컬럼 쓰기 권한 분리, `f6b3f500` 엔티티 ID 추가 등은 확인했으나 찾는 마이그레이션 실패와 직접 연결되지 않아 사례 추가 보류.
- 기술 대조: [PostgreSQL 외래키 제약 문서](https://www.postgresql.org/docs/16/ddl-constraints.html#DDL-CONSTRAINTS-FK).

## 직접 검증

- 개요 7개: 상단 분류 문구 제거, 기존 오른쪽 설명 3개 유지, 기술 스택을 이름 접근성이 있는 아이콘 목록으로 통일.
- 소개의 AI 항목에 사용자 지정 OpenCode·OpenClaw·Harness Engineering·Ponytail 추가.
- CONS Beacon 문제·원인·해결 문구를 사용자 지정 내용으로 변경하고 import 유지 문구 제거.
- 트러블슈팅 10개를 문제 → 원인 → 해결 형식으로 통일.
- 변경 전후 Git 코드와 발췌 이미지 대조.
- 360, 390, 768, 1024, 1440px에서 페이지 가로 넘침·내용 표시 확인.
- 삭제 구역·캡션, CONS 순서, BOOKIES 전후 이미지 세로 배치, 이미지 로딩·앵커·접근성 이름 확인.
- GIF 클릭 재생/정지, 확대 화면 닫기, 좌클릭 드래그·휠 확대, 일반 아키텍처 영역 세로 스크롤 확인.
- 회사 원본·내부 ERD·설정·자격 증명 미포함 확인.
