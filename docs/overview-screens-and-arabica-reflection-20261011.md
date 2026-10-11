# 실제 화면 배치·Arabica 회고 반영 · 2026-10-11

## 작업 범위

- 대상: `portpolio` GitHub Pages.
- 유지: 기존 색상·글꼴·개요 좌우 구성, 오른쪽 설명 3개·기술 아이콘, 기존 프로젝트 내용.
- 추가: Arabica·CMP·Wallet의 실제 화면, Arabica 트러블슈팅 다음의 추가 보완·회고 구간.
- 확인 대기: Store 화면이 실제 실행 캡처인지 사용자 원본 확인 중. 확인 전 설계 자료를 실제 실행 화면으로 게시하지 않음.
- 제외: PDF·PPT 재생성, 경력기술서 저장소, 전체 디자인 개편.

## 실제 화면 출처

| 프로젝트 | 원본문서·위치 | 선택 화면 | 처리 |
| --- | --- | --- | --- |
| Arabica | `Arabica_웹_사용_가이드.pptx` 6쪽 · `ppt/media/image15.png` | DB·백업 유형·보관 기간·요일별 예약 설정 | 원본 PNG 그대로 추출 |
| CMP | `cmp_사용자_가이드.pptx` 4쪽 · `ppt/media/image19.png` | Solution Suite·외부 백업 서비스 연결 메뉴 | 원본 PNG 그대로 추출 |
| Wallet | `wallet guide.pptx` 2쪽 · `ppt/media/image4.tiff` | SMS 인증번호 확인·재전송 대기 | 픽셀 변경 없는 TIFF→PNG 변환 |
| Wallet | `wallet guide.pptx` 9쪽 · `ppt/media/image20.png` | 결제 PIN 확인 | 픽셀·ICC 프로파일 유지, EXIF·XMP 메타데이터 제거 |

- 원본 문서·미디어·게시 이미지 SHA-256과 크기: [`assets/overview/sources.json`](../assets/overview/sources.json).
- 선택 범위: 서비스 UI의 실제 캡처. 특정 장애 해결의 재시험 성공 증거로 사용하지 않음.
- 개인 역할: 기존 오른쪽의 백엔드·API 담당 설명 유지. 화면을 직접 디자인하거나 프런트엔드를 혼자 개발했다는 주장 없음.
- 제외 화면: 비밀번호·사용자 이름·연락처·계좌·지갑 주소·QR·내부 서버 식별정보가 보이는 후보.
- 이번 작업에서 원본 앱·외부 서버 실행 없음. 과거 가이드의 화면을 원본 픽셀 기준으로 재사용.
- 화면 하단 출처·확대 안내 캡션 추가 없음. 기존 이미지 확대 기능 연결.

## Arabica 현재 구현과 회고 구분

| 구분 | 확인 내용 | 웹 표현 |
| --- | --- | --- |
| 현재 구현 | `cbc77cba`: Async·Executor 추가 | 기존 트러블슈팅 유지 |
| 현재 구현 | `c4ffc58f`: 원격 백그라운드 실행 | 기존 흐름도 유지 |
| 현재 구현 | `7e5e1818`, `dde065e5`: 결과 확인·검증 후 이력 판정 | 기존 구현 설명 유지 |
| 현재 구현 | `56827f66`: 결과 확인 `fixedDelay` 5분 | 주기적 결과 파일 확인의 대기 구간으로 설명 |
| 현재 실행기 설정 | core 4 / max 10 / queue 100 / CallerRunsPolicy | 포화 시 호출 스레드 실행 가능성. 실제 포화 장애 발생·측정 사실로 단정하지 않음 |
| 미구현 제안 | 작업 ID·상태·타임아웃 | 대기·실행·검증·완료/실패의 추적 방향 |
| 미구현 제안 | 인증된 완료 알림 + 주기 재확인 | 누락 감지 보완. 알림 수신만으로 성공 확정하지 않음 |
| 미구현 제안 | 중복 결과 처리·실행량 제한 | 동일 작업 결과 1회 반영, 거절·재시도 정책 검토 |
| 미구현 제안 | 전용 계정·키 인증·호스트 키 검증·명령 제한 | 원격 실행 권한 축소 방향. 보안 개선을 완료한 성과로 표현하지 않음 |

- 근거: 실제 `venetaBackup` Git 이력 및 현재 `AsyncConfig.java`·`BackupController.java`의 해당 설정 재확인.
- 결과 확인의 `fixedDelay`: 앞선 확인 작업 종료 후 5분 간격. 완료 감지 지연을 최대 5분으로 단정하지 않음.
- 현재 구조를 Spring Event·콜백 기반 구현으로 변경하여 설명하지 않음.
- 새 구간과 도식에 `추가 보완안 · 미구현` 표시.
- 성능 개선 수치·보안 검증 완료·실운영 검증 성과 추가 없음.
- SVG 생성: `python scripts/build_arabica_reflection.py`.
- 기능 아이콘: 기존 Lucide 자산 및 저장소의 ISC 라이선스 사용.

## 보완안의 기술 참고

- [Spring Framework Task Execution and Scheduling](https://docs.spring.io/spring-framework/reference/integration/scheduling.html): 실행기 큐·거절 정책, CallerRunsPolicy의 호출 스레드 실행 의미.
- [OpenSSH sshd_config](https://man.openbsd.org/sshd_config): 전용 사용자별 명령·권한 제한 설계의 참고. 현재 프로젝트에 적용했다는 근거로 사용하지 않음.
- 완료 알림·재확인·작업 상태 설계: 현재 파일 기반 확인 구조를 바탕으로 제안한 후속 설계. 실제 구현·도입 이력과 구분.

## 검증

- 직접 브라우저 확인: 360·390·768·1024·1440px에서 가로 넘침 없음.
- 기존 화면의 비율 유지, 모바일 개요 화면과 오른쪽 설명의 세로 배치 확인.
- 새 이미지 확대, 좌클릭 드래그·휠 확대, Escape·닫기 동작 확인.
- 페이지 JavaScript 오류 없음, 이미지 로드 실패 없음.
- 기존 STM-Simulator·CONS·BOOKIES와 기존 아키텍처·트러블슈팅 본문 변경 없음.
- PDF·PPT 변경 없음.

## 조사 위임 및 직접 검토

- 실제 에이전트 ID: `/root/overview_screen_sources`.
- 요청 설정: `gpt-5.6-luna` / `low`; 실제 런타임 모델 별도 검증 정보 없음.
- 배정: 사용자 가이드·보고서의 화면 후보 탐색·미디어 추출. 원본 수정·프로젝트 실행 금지.
- 상태: 조사 완료.
- 최종 선정·개인정보 확인·구현·브라우저 검증: 주 에이전트 직접 수행.
- 후보 판정 조정: 에이전트가 안전 후보로 제시한 Wallet 홈에는 개인 이름이 있어 제외. Store는 문서 이름만으로 실행 화면 여부를 확정하지 않고 사용자 확인 대기.
