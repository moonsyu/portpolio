# 장문수 개발 포트폴리오

- 웹사이트: [moonsyu.github.io/portpolio](https://moonsyu.github.io/portpolio/)
- 구성: HTML·CSS·JavaScript 기반 정적 사이트
- 프로젝트: STM-Simulator → CONS → BOOKIES
- 소개: Java 백엔드, IoT 연동, 학습 도구 개발 경험
- 기능: 프로젝트 바로가기, 상세 내용 펼치기, 이미지 확대, 반응형 레이아웃
- 애플리케이션 아키텍처: 기술·기능 아이콘, 모듈별 영역, 요청·응답·저장 흐름을 표현한 SVG 도식 3개

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
- `scripts/build_architectures.py`: 아키텍처 도식 생성 스크립트(Python 표준 라이브러리)
- `.nojekyll`: 정적 파일 배포 설정

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
- 라이선스 전문: `assets/architecture/DEVICON-LICENSE.txt`, `assets/architecture/LUCIDE-LICENSE.txt`
- 기술 로고는 사용 기술의 식별 목적으로 표시하며 각 상표권은 해당 권리자에게 귀속
- 결과 SVG에 아이콘을 포함하여 외부 CDN 연결 없이 렌더링
