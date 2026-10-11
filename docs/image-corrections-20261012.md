# 프로젝트 개요 이미지 수정 · 2026-10-12

- 사용자 요청: 일반판 22·27·32·36쪽 개요 이미지 수정, 웹·앱판의 동일 프로젝트와 웹페이지에 함께 반영.
- 편집 도구: 기본 내장 `image_gen` 사용. CLI/API 경로 미사용.
- 원본 문서 유지. Arabica·CMP·Wallet은 실제 캡처를 입력으로 만든 표시용 편집본이며, 원본과 픽셀이 동일한 실행 근거로 취급하지 않음.
- 원본 문서·원본 미디어 해시 및 편집본 해시: [`sources.json`](../assets/overview/sources.json).

## 변경 파일

- [Arabica](../assets/overview/arabica-dashboard-full.png): 상단 `UWS-BackUp` → `Arabica`.
- [CMP](../assets/overview/cmp-solution-suite.png): 상단 브랜드 → 구름 아이콘·`CMP`, 접속 카드 → 지구본 아이콘·`Web 사이트 접속`, 두 번째 카드 → 서버 아이콘·`외부 서비스 연동`.
- [Wallet](../assets/overview/wallet-main.png): 인사말의 사용자 이름 → `Nuri!`.
- [Store](../assets/overview/store-main.jpg): 메뉴가 닫힌 기존 1440×900 브라우저 캡처 복원. 포트폴리오 커밋 `432a7ac`의 파일과 SHA-256 동일. 메뉴에 가리지 않는 작품·소개·Artwork/Goods/Artist 메뉴 표시.

## 이미지 편집 프롬프트

- Arabica:

```text
Use case: text-localization. Edit target: the supplied actual application screenshot, 1918 x 904. Change ONLY the white brand label at the extreme upper left of the blue header from 'UWS-BackUp' to the exact text 'Arabica'. Keep the existing same white bold sans-serif style and vertical alignment. Preserve the full screenshot, its original dimensions/aspect ratio, blue header, sidebar, Korean texts, all numbers, donut chart 64.6%, graphs, controls, whitespace and bottom cropping exactly. This is a precise one-label replacement for a portfolio screenshot; do not redesign, redraw, crop or reinterpret any other element.
```

- CMP:

```text
Use case: text-localization and precise-object-edit. Edit target: this actual desktop web screenshot. Keep the entire screenshot with original 1911:886 landscape aspect ratio, exact flat colors, sharp UI text, every region and data unchanged EXCEPT the following three local regions. 1. Upper left sidebar branding 'veneta.enterprise' and its star icon: replace with a small simple white cloud-outline icon and the exact bold white text 'CMP', maintaining alignment and black/charcoal background. 2. First large service tile in main area: replace the red NetBackup logo with a simple blue globe/web-outline icon; replace its 'NetBackup™ Self Service' title with exact text 'Web 사이트 접속'. 3. Second large service tile: replace red Arctera logo with a simple gray server-outline icon; replace 'Arctera™ InfoScale' with exact text '외부 서비스 연동'. Preserve the second tile's existing light/disabled appearance. IMPORTANT: keep sidebar menu texts, 'Solution Suite', '백업 및 복구', all descriptive Korean body copy, Download and Docs buttons, header icons, positions, sizes, white space, and overall flat screenshot presentation exactly unchanged. No new panels or text, no aesthetic redesign, no gradients, no perspective or photograph effect, no cropping. This is a label/icon replacement in a portfolio illustration of the real UI, not a new application design.
```

- Wallet:

```text
Use case: text-localization. Edit target: this full-height actual mobile Wallet screenshot. Change ONLY the bold Korean user name '혁수 권!' below 'Hello.' in the top greeting to exact text 'Nuri!' (N-u-r-i and an exclamation mark), in the same black bold sans-serif size and same position. 'Hello.' stays untouched above it. Preserve the entire original 1080:2400 portrait aspect ratio, all screen boundaries, status bar, marble background, profile icon, bell, menu, the KRDC / 5,000 / KRW balance, Mint/Send/DApp icons, Korean vPoint banner, 'Explore Mintand Mining features', bottom navigation Home/Wallet/My QR/Benefit/Friends, all other text, colors, spacing, shapes, and existing artifacts. No added phone frame. No crop. No restyle. This must remain the same application screenshot with only a substituted display name, not a redesigned UI.
```

## 확인 범위

- 출력 이미지의 지정 문구·아이콘 직접 확인.
- Store는 이미지 생성 없이 기존 실제 브라우저 캡처 재사용.
- PDF 페이지·원문·링크·레이아웃 검증 결과: [PDF 갱신 기록](pdf-refresh-20261012.md).
