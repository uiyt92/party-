# 프로젝트 구조

## 1. 구조 개요

```text
.
├── projects/                 # 활성 제품 소스
│   ├── katalk-standard/
│   └── cna-night/
├── templates/                # 공용 템플릿·신규 프로젝트 스타터
├── scripts/                  # 표준 CLI·OCR·과거 도구
├── tests/                    # Python 단위 테스트
├── dist/                     # 검증된 배포 산출물
├── build/                    # 빌드·렌더 중간물
├── references/               # 외부 참고자료·OCR 파생물
├── docs/                     # 운영 문서·연구 기록
├── archive/                  # 과거 버전·초안·작업 흔적
└── local/                    # 비밀정보·로컬 전용 파일
```

## 2. 제품별 정본

### 카톡의 정석

| 산출물 | 조판 정본 | 편집용 원고 |
|---|---|---|
| 기본편 | `projects/katalk-standard/typst/book.typ` | `projects/katalk-standard/manuscript/basic/` |
| 심화편 | `projects/katalk-standard/typst/advanced.typ` | `projects/katalk-standard/manuscript/advanced/` |
| 요약본 | `projects/katalk-standard/typst/summary.typ` | 요약본 Typst 내부 |

기본편·심화편의 Markdown과 Typst는 자동 동기화되지 않는다. 현재 시각적으로 검증된 조판을 보존하기 위해 Typst 파일을 빌드 정본으로 명시했다. 과거 변환기는 장 목록과 제목이 오래되어 `scripts/legacy/`로 격리했다.

### CNA NIGHT

| 역할 | 경로 |
|---|---|
| 빌드 엔트리 | `projects/cna-night/typst/book.typ` |
| 테마 | `projects/cna-night/typst/theme.typ` |
| 도식 렌더러 | `projects/cna-night/typst/diagrams.typ` |
| 원고 정본 | `projects/cna-night/manuscript/` |

CNA NIGHT는 `book.typ`이 Markdown 원고를 직접 읽는다. 따라서 원고가 콘텐츠 정본이고 Typst 파일은 구성·디자인 정본이다.

## 3. 빌드 흐름

```text
projects/*/project.json
        +
Typst 엔트리·원고·템플릿
        |
        v
scripts/project.py build
        |
        v
build/pdf/ 임시 PDF
        |
  PDF 구조 검증
        |
        v
dist/pdf/ 정식 PDF
```

검증 항목은 PDF 열기, 페이지 존재, 대표 페이지 텍스트 추출이다. 실제 배포 전에는 `build/rendered/`의 전체 페이지 렌더와 접촉 시트도 사람이 확인한다.

## 4. 배포물 분류

- `dist/pdf/`: 정식 교재 PDF 네 종
- `dist/slides/`: 강의 슬라이드, 스크립트, HTML 의존 이미지
- `dist/handouts/`: 사전과제와 워크북
- `dist/packages/coaching/`: 코칭 패키지용 독립 산출물

`dist/`는 전달 가능한 파일만 둔다. 미리보기, 페이지 PNG, 임시 PDF는 `build/`에 둔다.

## 5. 보존·제외 정책

- `references/pdf/`: 외부 또는 경쟁 교재 PDF. 로컬 보존, Git 제외.
- `references/ocr/`: OCR 결과. 검색·검토에 사용하며 소스 정본은 아님.
- `archive/legacy-output/`: 이전 브랜드 PDF와 잘못 포장된 중복 파일.
- `archive/drafts/`: 통합 전 초안.
- `archive/ai-runs/`: 과거 AI 작업 결과.
- `local/secrets/`: API 인증정보. 항상 Git 제외.
- `.claude/worktrees/`: 도구가 관리하는 로컬 작업트리. 프로젝트 산출물이 아님.

## 6. Git 경계

이 폴더는 독립 Git 저장소다. 상위 `C:/Users/SuperNatural1/Code` 저장소와 분리되어 있다. `archive/`, `build/`, `local/`, 외부 참고 PDF는 `.gitignore`로 제외되며, 활성 소스·문서·검증된 배포물은 저장소에서 관리한다.
