# 산출물 및 빌드물 목록

측정일: 2026-08-12

## 1. 분류 기준

| 분류 | 위치 | 의미 |
|---|---|---|
| 정식 산출물 | `dist/pdf/` | 소스에서 다시 만들고 검증할 수 있는 교재 PDF |
| 부속 산출물 | `dist/slides/`, `dist/handouts/`, `dist/packages/` | 강의·워크북·코칭 패키지 |
| 빌드물 | `build/` | PDF 스테이징, 렌더 PNG, 미리보기 |
| 참고자료 | `references/` | 외부 PDF와 OCR 파생물 |
| 보관물 | `archive/` | 과거 버전, 초안, 중복·오분류 파일 |
| 비밀정보 | `local/` | 서비스 계정 키 등 로컬 전용 파일 |

## 2. 정식 PDF 산출물

아래 값은 새 구조에서 빌드와 PDF 검증을 마친 최종 배포본 기준이다. SHA-256은 현재 커밋된 배포 바이트를 식별하며, 같은 소스에서 언제나 같은 해시가 나오는 결정적 빌드를 뜻하지 않는다. Typst는 생성 메타데이터와 타임스탬프를 PDF에 넣으므로 내용과 페이지 수가 같아도 SHA-256이 달라질 수 있다.

일상 작업에서는 변경한 ID만 빌드한 뒤 전체를 검증한다.

```powershell
python scripts/project.py build cna-party-book
python scripts/project.py verify all
```

배포 PDF를 의도적으로 다시 빌드할 때마다 페이지 수, 바이트, SHA-256을 재측정하고 같은 변경에서 이 목록도 갱신한다. `build all`은 모든 정식 PDF와 인벤토리를 함께 새로 확정할 때만 사용한다.

| ID | 파일 | 페이지 | 바이트 | SHA-256 |
|---|---|---:|---:|---|
| `katalk-basic` | `dist/pdf/카톡의정석.pdf` | 210 | 1,510,884 | `9c10d02f02a7ea592c0ff16c0a8800963e6022b24d05ae905a09531a48bc94d6` |
| `katalk-advanced` | `dist/pdf/카톡의정석_심화편.pdf` | 81 | 600,151 | `62ea43b06f6226204dcda3ce2cacef4cc4c3072846c74b38f371f421b1c1f94d` |
| `katalk-summary` | `dist/pdf/카톡의정석_요약본.pdf` | 20 | 213,807 | `ade19c3149189429be7b7b1b5248d859195654ae3f33d9db67e9075872c5e312` |
| `cna-night` | `dist/pdf/CNA_NIGHT.pdf` | 89 | 636,338 | `df5eb5289c142c965ba8c9a4da62d846b25cc9b8bf5796169433cc093192bca9` |
| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` | 41 | 365,262 | `3e47e04ee1d1aa626266e130d3e5cf0659cea87f0a7ab2b5a880ac55f3596499` |

『파티의 주도권』은 `projects/cna-party-edition/manuscript/`의 장별 Markdown이 콘텐츠 정본이고, `projects/cna-party-edition/typst/`가 구성·디자인 정본이다. 참고 슬라이드는 재집필을 위한 로컬 자료이며 독립 교재의 정본이 아니다.

## 3. 부속 산출물

### 슬라이드

- `dist/slides/카톡의정석_강의슬라이드.pptx`
- `dist/slides/답장의기술_강의슬라이드.html`
- `dist/slides/강의스크립트.md`
- `dist/slides/images/` - HTML이 상대경로 `images/...`로 읽는 이미지 20개

### 워크북·사전과제

| 파일 | 페이지 | 상태 |
|---|---:|---|
| `dist/handouts/답장의기술_워크북.pdf` | 8 | 배포 보조자료 |
| `dist/handouts/답장의기술_워크북.html` | - | 편집·웹 배포본 |
| `dist/handouts/답장의기술_사전과제.pdf` | 2 | 배포 보조자료 |
| `dist/handouts/답장의기술_사전과제.html` | - | 편집·웹 배포본 |

### 코칭 패키지

| 파일 | 페이지 | 상태 |
|---|---:|---|
| `dist/packages/coaching/나이트 게임_노바.pdf` | 89 | 고유 PDF |
| `dist/packages/coaching/어프로치_Basic_실전매뉴얼.pdf` | 42 | 고유 PDF |
| `dist/packages/coaching/어프로치_Basic_실전매뉴얼.html` | - | HTML 산출물 |

## 4. 참고 PDF

| 파일 | 페이지 | 바이트 | 용도 |
|---|---:|---:|---|
| `references/pdf/(New)폰게임.pdf` | 65 | 450,188 | 기존 폰게임 참고자료 |
| `references/pdf/카톡101.pdf` | 132 | 62,054,991 | 사례·OCR 원천 |
| `references/pdf/테레사_CONTACT.pdf` | 1,527 | 22,132,730 | 구성·갭 분석 참고자료 |
| `references/pdf/FASTER_SEX - 복사본.pdf` | 49 | 356,854 | CNA NIGHT 재구성 참고자료 |
| `references/pdf/[CNA] Party Edition.pdf` | 44 | 1,581,135 | CNA Party Edition 원본 강의 슬라이드, 16:9·로컬·Git 제외 |

OCR 결과는 `references/ocr/`에 있으며 원천 PDF를 대체하지 않는다. 참고 PDF는 대용량·외부자료이므로 Git에서 제외한다.

## 5. 과거 PDF와 중복 파일

| 파일 | 페이지 | 상태 |
|---|---:|---|
| `archive/legacy-output/답장의기술.pdf` | 192 | 리브랜딩 전 기본편 |
| `archive/legacy-output/답장의기술_심화편.pdf` | 58 | 리브랜딩 전 심화편 |

다음 다섯 파일은 SHA-256이 모두 `b2e618ad5f8d54163d52c6a32669ebb4651301b59ab6bbcdc7b74ad8310a6363`이며, 크기 356,854바이트·49페이지로 완전히 같다.

- `references/pdf/FASTER_SEX - 복사본.pdf`
- `archive/legacy-output/duplicate-coaching/메이드 이론과 실전.pdf`
- `archive/legacy-output/duplicate-coaching/Atoz after_노바.pdf`
- `archive/legacy-output/duplicate-coaching/FASTER_SEX_노바.pdf`
- `archive/legacy-output/duplicate-coaching/LTR 빌드업(영포술).pdf`

즉 코칭 자료 네 파일은 이름과 실제 내용이 일치하지 않는 오분류 복제본이다. 삭제하지 않고 보관하되 현재 배포 패키지에서는 제외했다.

## 6. 빌드·미리보기

- `build/pdf/`: CLI가 생성하는 검증 전 PDF
- `build/rendered/`: 최종 PDF의 페이지 PNG와 컨택트 시트
- `build/previews/legacy/`: 과거 미리보기 PDF·PNG·Typst 파일
- `build/previews/cna-night/`: persona-vibe SVG·PNG

`build/`는 전부 다시 만들 수 있는 중간물이며 Git에서 제외한다.

## 7. 보존 자료

- `archive/drafts/`: phase1, phase2, 슬라이드 초안, 비어 있는 과거 part3 경로
- `archive/ai-runs/`: 과거 `_workspace` 작업 결과
- `archive/legacy-build/main.typ`: 누락 장이 있는 과거 Markdown 직접 렌더 경로
- `scripts/legacy/md_to_typ.py`: 오래된 제목·장 목록을 가진 변환기
- `scripts/legacy/integrate_phase1.py`: 일회성 통합 스크립트

보관 자료는 현재 빌드에 참여하지 않는다.

## 8. 추적 정책

| 경로 | Git 추적 |
|---|---|
| `projects/`, `templates/`, `scripts/`, `tests/`, `docs/` | 예 |
| `dist/` | 예, 전달 가능한 산출물 |
| `references/ocr/` | 예 |
| `references/pdf/` | 아니오 |
| `build/`, `archive/`, `local/` | 아니오 |
