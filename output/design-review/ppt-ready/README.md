# A·B 슬라이드형 디자인 시안

- 최신 요청: C안 제외, A안 색감 완화, A·B안의 향후 PPT 전환 고려.
- 산출물: 각 안의 1600×900 PNG 8장, 전체 미리보기, SVG 및 개별 요소 좌표 JSON.
- 현재 단계: **디자인 이미지**. 실제 PPTX 생성·PowerPoint 동작 검증은 이번 산출물에 포함하지 않음.
- 운영 사이트 HTML/CSS/JS 및 PDF: 변경 없음.

## 디자인

- A안: 흰 배경, 차분한 회보라 `#70687D`, 옅은 라벤더 `#F3F1F5`, 본문 `#30323D`.
- B안: 밝은 청회색 배경 `#FAFCFD`, 강조 `#365E6E`, 연한 청회색 면 `#EDF3F5`, 본문 `#24353D`.
- A안의 넓은 보라색 표지·어두운 STM 영역 제거.
- B안의 어두운 소개 배경을 밝게 조정하고, 4열 경력 구성 유지.
- 웹용 메뉴·버튼 제거, 페이지별 제목·본문·이미지·페이지 번호 구성.
- 제목 52px, 본문 28–32px, 표 메타데이터 26px, 페이지 정보 20px 중심.
- 기본 여백 72px, 전체 비율 16:9. 긴 내용을 잘라 페이지를 만드는 방식 대신 의미별 재배치.

## 이미지

- [A안 전체 보기](a-overview.png) · [A안 원본 PNG 8장 ZIP](A-slide-images.zip).
- [B안 전체 보기](b-overview.png) · [B안 원본 PNG 8장 ZIP](B-slide-images.zip).
- 원본 개별 페이지: `a/`, `b/`.

| 페이지 | 주제 | 내용 |
|---|---|---|
| 1 | 소개 | 장문수 / Jang MoonSu, 프로필, 개발 경험 |
| 2 | 경력·교육 | 현재 기록된 네 가지 경력·교육 |
| 3 | 기술 | 네 분류, 16개 기술 아이콘 |
| 4 | 수상·자격 | 수상 6건의 기관·대회·등급·날짜, 기사·OPIc |
| 5 | STM 개요 | 실제 실행 화면, 기간·인원, 구현 범위·기술 |
| 6 | 애플리케이션 아키텍처 | Renderer, Preload, Main, 자동 저장과 파일 입출력 |
| 7 | 개선 | 기존 확인 과정과 통합 화면, HAL LED 예제 화면 |
| 8 | 트러블슈팅 | UART 문제·원인·해결·24개 조건, RX/TX 로그 |

## PPT 전환 준비

- `.layout.json`: 원문 텍스트·글꼴·크기·좌표, 이미지 원본 경로·비율, 사각형·선·화살표를 각각 기록.
- `.svg`: 시안의 벡터 렌더 원본. 글꼴 대체 방지를 위해 표시용 글자는 윤곽선으로 저장.
- PPT를 실제 생성할 때는 JSON의 텍스트·도형을 네이티브 요소로 매핑하고, 실제 화면은 이미지로 배치할 수 있도록 구성.
- `.text.json`: 본문 검토용 원문 목록.
- LED PNG: 기존 GIF의 정적 포스터. 향후 PPTX 생성 시 GIF나 영상 사용 여부 별도 결정 가능.

## 근거와 확인

- 내용 기준: 기존 포트폴리오 커밋 `47bd953` 및 사용자가 확정한 이름·OPIc 기록.
- 기존 프로필·STM 메인 화면·LED 포스터·UART 로그 사용.
- 아키텍처: `assets/architecture/stm-application.svg`의 역할·연결·자동 저장 구분을 가로 슬라이드에 재배치.
- 수상 6건, 정보처리기사 취득일 2024.10.02, OPIc IL 취득일 2026.09.14 보존.
- UART 24개 조건 및 9600 baud / 260ms 입력 / 20ms 실행 조건 보존.
- `scripts/check_ppt_designs.py`: 16:9 규격, 이미지 경로·범위, 텍스트 경계·겹침, 필수 사실 보존 확인.
- 개별 페이지·전체 미리보기를 육안으로 확인.
- Impeccable detector는 비웹 소스에 대해 `[]` 반환. 웹 동작이나 PPTX 호환성 검사로 해석하지 않음.
- 글꼴 출처·라이선스: 상위 README 및 `../licenses/` 참조.

## 재생성

```powershell
python scripts/build_ppt_designs.py
node scripts/render_ppt_designs.cjs
python scripts/check_ppt_designs.py
```

- 글꼴 디렉터리 및 Sharp 환경 설정: 상위 README 참조.
- 생성 코드: `scripts/ppt_design_base.py`, `scripts/ppt_profile_layout.py`, `scripts/build_ppt_designs.py`.
- 검토·압축 전달 파일은 최종 PNG 확정 후 생성.

## 작업 분담

- `/root/three_design_plan`: 8페이지 구성 검토, 요청 `gpt-6-astra/xhigh`, 완료.
- `/root/portfolio_design_ac`: 소개·경력·기술·수상 시안 초안, 요청 `gpt-5.6-terra/medium`, 완료.
- 주 에이전트: 공통 페이지 구조, STM 4페이지, 배치 보완, 렌더·검증·전달.
- `/root/design_image_qa`: 이미지 검토, 요청 `gpt-5.6-terra/medium`, 완료·PASS. 전체 미리보기 및 개별 페이지에서 색감·16:9 구성·가독성·필수 내용·저장 경로 구분 확인.
- 실제 런타임 모델 정보는 도구에서 별도 제공되지 않음.
