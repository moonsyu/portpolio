# 소개–STM Simulator 디자인 비교

- 요청: UI/UX 스킬 3개를 각각 적용한 포트폴리오 디자인 이미지.
- 범위: 소개, 경력·교육, 기술 스택, 수상·자격, STM 개요, 애플리케이션 구조, 개선, UART 트러블슈팅.
- 산출물: 정적 데스크톱 UI 시안. 브라우저 캡처나 실제 기능 구현 완료를 의미하지 않음.
- 운영 사이트의 `index.html`, `styles.css`, `app.js`, 기존 PDF: 변경 없음.
- 기존 문구·화면의 기준: `moonsyu/portpolio` 커밋 `47bd953`.

| 시안 | 적용 스킬 | 디자인 방향 | 이미지 |
|---|---|---|---|
| A | frontend-design | 큰 타이포그래피, 보라색 소개 영역, 어두운 STM 사례 영역 | [1600×7500 PNG](a-frontend-design.png) |
| B | Impeccable | 청회색, 경력 4열, 큰 실행 화면, 작업물 중심 구성 | [1600×6180 PNG](b-impeccable.png) |
| C | UI/UX Pro Max | 왼쪽 목차, 청록색, 정렬된 이력과 기술 행, 순차적인 사례 탐색 | [1600×6560 PNG](c-ui-ux-pro-max.png) |

## 스타일 결정

- 공통: Noto Sans KR + Manrope, 굵은 한국어 본문, 실제 기술 아이콘·프로필·STM 화면 사용.
- A: 강조 `#6845D7`, 본문 `#211C37`, 보조 `#635E73`, 배경 `#FFFFFF`·`#F2EEFF`.
- B: 강조 `#276986`, 본문 `#19333F`, 보조 `#526873`, 배경 `#F8FBFC`·`#E4F0F5`.
- C: 강조 `#157567`, 본문 `#173A35`, 보조 `#52736D`, 배경 `#FFFFFF`·`#EEF6F4`.
- Impeccable: 현재 제품 맥락 확인, 선택적 사용자 선호 질문, 콘셉트 시드 `be90c2ff`를 거친 작업물 카탈로그 방향.
- UI/UX Pro Max: 디자인 시스템 검색 및 1회 재검색 수행. 포트폴리오에 맞지 않는 추천 스타일 대신 탐색·대비·간격 원칙을 적용.
- 최종 적용 디자인 미선택: 세 시안의 비교 기록이며 운영 사이트 전체 디자인 규칙을 교체하지 않음.

## 내용과 이미지

- 이름: Jang MoonSu.
- 수상: 6개 대회명·기관·수상·날짜 보존.
- 자격: 정보처리기사 2024.10.02, OPIc IL / Intermediate Low 2026.09.14 보존.
- STM: 지원 범위의 C/HAL 동작 모델로 한정. 실물 보드 구동 경험이나 새로운 성과를 추가하지 않음.
- UART: 시간 단위 변환 오차, 수신 판정 허용 오차 적용, 24개 조건 회귀 검증 보존.
- 화면 출처: 기존 `assets/profile.webp`, `stm-simulator.webp`, `stm-led-demo-poster.webp`, `stm-uart-verified.webp`, `architecture/stm-application.svg`.
- PNG의 LED 장면: 기존 GIF의 정적 포스터. 이미지 자체에서 애니메이션이 실행되지는 않음.
- SVG 렌더러 호환 처리: 기존 WebP 픽셀을 PNG로 변환하여 내부 임베딩.
- 기존 기술 아이콘의 라이선스: 저장소 내 기존 라이선스 유지.

## 생성 및 확인

- 생성 소스: `scripts/design_board.py`, `scripts/build_design_ac.py`, `scripts/build_design_b.py`.
- 렌더링: `scripts/render_designs.cjs`의 Sharp SVG→PNG 변환.
- 텍스트: SVG 내 글리프 윤곽선으로 보존. `.text.json`에 별도 검토 가능한 문구 저장.
- 자동 확인: `python scripts/check_designs.py` — 텍스트 경계·텍스트 겹침·이력 및 UART 핵심 내용 보존.
- 육안 확인: 세 PNG와 필요한 부분 확대본의 실제 이미지 표시·영역 구성 확인.
- Impeccable detector: 변경 SVG 대상 결과 `[]`. HTML/CSS 구현 검증을 의미하지 않음.
- 반응형·키보드·스크롤·클릭 동작: 이번 정적 시안의 검증 범위에 포함하지 않음.

## 재생성

- Python 의존성: `fontTools`, `Pillow`.
- Node 의존성: `sharp`.
- `PORTFOLIO_DESIGN_FONTS` 환경변수: 아래 두 TTF 파일을 둔 디렉터리 지정. 기본값 `../portpolio-work/design-fonts`.
- [Noto Sans KR](https://github.com/google/fonts/tree/main/ofl/notosanskr): `NotoSansKR[wght].ttf`를 `NotoSansKR.ttf`로 저장.
- [Manrope](https://github.com/google/fonts/tree/main/ofl/manrope): `Manrope[wght].ttf`를 `Manrope.ttf`로 저장.
- 두 글꼴: SIL Open Font License 1.1. 라이선스는 `licenses/`에 포함.
- 이 시안의 글꼴 SHA-256:
  - Noto Sans KR: `194018e6b2b293a7964f037b25c0249ce1418bc9ab3c971060a03aa57861e252`.
  - Manrope: `3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6`.

```powershell
python scripts/check_designs.py
node scripts/render_designs.cjs
python -c "import sys; sys.path.insert(0,'scripts'); from design_board import OUT,provenance_png; [provenance_png(p) for p in OUT.glob('*.png')]"
```

## 작업 분담

- `/root/three_design_plan`: 구조·스킬 적용 계획. 요청 설정 `gpt-6-astra/xhigh`, 완료.
- `/root/portfolio_design_ac`: A/C 시안 초안 및 배치 수정. 요청 설정 `gpt-5.6-terra/medium`, 완료.
- 주 에이전트: B 시안, 공통 렌더러, A/C 내용 통합, 이미지 생성·검증·최종 전달.
- `/root/design_image_qa`: 정적 이미지 독립 검토. 요청 설정 `gpt-5.6-terra/medium`, 완료. 세 PNG 전체 및 구간 확대 확인 결과 PASS; 중대 잘림·겹침·내용 누락 없음.
- 요청 모델과 실제 런타임 설정을 구분하며, 도구가 실제 모델 정보를 반환하지 않아 별도 확인하지 않음.
