# 프로젝트 작업 가이드

이 저장소는 Typst 기반 교재 출판 프로젝트다. 활성 제품은 `katalk-standard`, `cna-night`, `cna-party-edition` 세 개이며, 정식 배포 PDF는 `dist/pdf/`의 다섯 파일이다.

## 표준 명령

```powershell
python scripts/project.py list
python scripts/project.py build all
python scripts/project.py verify
python -m unittest discover -s tests -v
```

개별 빌드 ID는 `katalk-basic`, `katalk-advanced`, `katalk-summary`, `cna-night`, `cna-party-book`이다.

## 정본

- Katalk 기본편: `projects/katalk-standard/typst/book.typ`
- Katalk 심화편: `projects/katalk-standard/typst/advanced.typ`
- Katalk 요약본: `projects/katalk-standard/typst/summary.typ`
- CNA NIGHT: `projects/cna-night/typst/book.typ` + `projects/cna-night/manuscript/*.md`
- CNA Party Edition: `projects/cna-party-edition/typst/book.typ` + `projects/cna-party-edition/manuscript/*.md`

Katalk Markdown은 편집용 원고다. `scripts/legacy/md_to_typ.py`로 현재 Typst 정본을 덮어쓰지 않는다. CNA NIGHT는 Markdown이 빌드 입력이므로 원고 경로를 바꾸면 `typst/book.typ`도 함께 갱신한다. CNA Party Edition은 `projects/cna-party-edition/manuscript/`의 장별 Markdown이 콘텐츠 정본이고, `projects/cna-party-edition/typst/book.typ`과 같은 Typst 파일이 구성·디자인 정본이다.

## 디렉터리 규칙

- `projects/`: 활성 제품 소스
- `templates/`: 공용 Typst 템플릿과 신규 프로젝트 스타터
- `dist/`: 검증된 배포물
- `build/`: 빌드·렌더 중간물, Git 제외
- `references/`: 외부 PDF와 OCR 결과
- `docs/`: 구조·산출물·연구 문서
- `archive/`: 과거 버전과 작업 흔적, Git 제외
- `local/`: 비밀키 등 로컬 전용 파일, Git 제외

## 변경 규칙

1. 콘텐츠를 수정하는 작업과 폴더·빌드 구조를 수정하는 작업을 섞지 않는다.
2. 새 CLI 동작은 실패 테스트를 먼저 작성한다.
3. PDF는 `scripts/project.py build`로 스테이징·검증 후 배포한다.
4. 최종 전달 전 다섯 PDF를 전부 열고 페이지 수, 텍스트, 렌더링을 확인한다.
5. `local/secrets/gcp-key.json`의 내용은 출력·문서화·커밋하지 않는다.

과거 프로젝트 가이드는 `docs/research/legacy-project-guide.md`, 상세 변경 이력은 `docs/research/reviews/변경이력.md`에 보존되어 있다.
