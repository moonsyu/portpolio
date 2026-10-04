# 이전 디자인 기록

- 현재 참고 디자인: Canva의 **Almost White and Black** 템플릿.
- 현재 제작 기준: [포트폴리오 구성안](../../docs/portfolio-redesign/README.md).
- 이 폴더에는 이전 C 시안과 해당 생성·검증 자료만 보관.
- C 시안: UI/UX Pro Max 기반의 과거 비교 기록이며, 현재 검토·적용 대상에서 제외.

## 보관 파일

- [C 시안 PNG](c-ui-ux-pro-max.png): 소개부터 STM Simulator까지의 정적 디자인 이미지.
- `c-ui-ux-pro-max.svg`: 벡터 원본.
- `c-ui-ux-pro-max.text.json`: 문구 기록.
- 내용·화면 기준: 기존 포트폴리오 커밋 `47bd953`.
- 글꼴: Noto Sans KR, Manrope. SIL Open Font License 1.1 원문은 `licenses/`에 보관.

## 생성 도구

- 생성: `scripts/build_design_c.py`, `scripts/design_board.py`.
- 렌더링: `scripts/render_designs.cjs`.
- 확인: `scripts/check_designs.py`.
- Python 의존성: `fontTools`, `Pillow`.
- Node 의존성: `sharp`.
- `PORTFOLIO_DESIGN_FONTS`: `NotoSansKR.ttf`, `Manrope.ttf`가 있는 디렉터리. 기본값 `../portpolio-work/design-fonts`.
- 글꼴 출처: [Noto Sans KR](https://github.com/google/fonts/tree/main/ofl/notosanskr), [Manrope](https://github.com/google/fonts/tree/main/ofl/manrope).
