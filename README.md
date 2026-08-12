# Typst 교재 출판 프로젝트

『카톡의 정석』 계열, 『CNA NIGHT』, 『CNA Party Edition』을 한 저장소에서 제작·검증·배포하는 Typst 프로젝트입니다. 소스, 최종 산출물, 빌드 중간물, 외부 참고자료, 과거 작업물을 서로 다른 디렉터리로 관리합니다.

## 정식 PDF 산출물

| ID | 산출물 | 빌드 소스 |
|---|---|---|
| `katalk-basic` | `dist/pdf/카톡의정석.pdf` | `projects/katalk-standard/typst/book.typ` |
| `katalk-advanced` | `dist/pdf/카톡의정석_심화편.pdf` | `projects/katalk-standard/typst/advanced.typ` |
| `katalk-summary` | `dist/pdf/카톡의정석_요약본.pdf` | `projects/katalk-standard/typst/summary.typ` |
| `cna-night` | `dist/pdf/CNA_NIGHT.pdf` | `projects/cna-night/typst/book.typ` |
| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` | `projects/cna-party-edition/typst/book.typ` |

『파티의 주도권』은 파티 준비부터 첫 대화와 번호 교환까지를 다루는 독립 교재입니다.

## 빠른 시작

필수 도구는 Typst 0.14.x와 Python 3.12 이상입니다.

```powershell
python -m pip install -r requirements.txt
python scripts/project.py list
python scripts/project.py build cna-party-book
python scripts/project.py verify all
```

일상 작업에서는 변경한 산출물 ID만 빌드하고, 이어서 `verify all`로 정식 PDF 다섯 종을 모두 확인합니다. 위 명령의 `cna-party-book`은 실제 예시이며 다른 교재를 수정했다면 해당 ID로 바꿉니다. `build`는 먼저 `build/pdf/`에 PDF를 만들고 구조 검증을 통과한 파일만 `dist/pdf/`에 반영합니다. 실패하면 기존 배포본은 유지됩니다.

```powershell
python scripts/project.py build all
```

`build all`은 모든 정식 PDF의 배포 바이트를 의도적으로 새로 만들 때만 사용합니다. 실행했다면 페이지 수·바이트·SHA-256을 다시 측정해 `docs/ARTIFACT_INVENTORY.md`를 같은 변경에서 갱신합니다.

## 새 교재 만들기

```powershell
python scripts/project.py new sample-book --title "샘플 교재"
python scripts/project.py build sample-book-book
```

자세한 절차는 [NEW_PROJECT_GUIDE.md](docs/NEW_PROJECT_GUIDE.md)를 참고합니다.

## 문서

- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - 디렉터리 역할과 정본 정책
- [ARTIFACT_INVENTORY.md](docs/ARTIFACT_INVENTORY.md) - 산출물·빌드물·참고자료·과거 파일 분류
- [NEW_PROJECT_GUIDE.md](docs/NEW_PROJECT_GUIDE.md) - 새 프로젝트 시작 및 배포 절차
- [설계 문서](docs/superpowers/specs/2026-08-06-typst-publishing-reorganization-design.md)
- [구현 계획](docs/superpowers/plans/2026-08-06-typst-publishing-reorganization.md)
- [CNA Party Edition 설계 문서](docs/superpowers/specs/2026-08-12-cna-party-book-design.md)
- [CNA Party Edition 구현 계획](docs/superpowers/plans/2026-08-12-cna-party-book.md)

## 중요한 규칙

- Katalk 3종은 `projects/katalk-standard/typst/`의 Typst 파일이 조판 정본입니다. Markdown 원고를 자동 변환해 덮어쓰지 않습니다.
- CNA NIGHT는 `manuscript/`의 Markdown을 빌드 시 직접 읽습니다.
- CNA Party Edition은 `projects/cna-party-edition/manuscript/`의 장별 Markdown이 콘텐츠 정본이고, `projects/cna-party-edition/typst/`가 구성·디자인 정본입니다.
- `references/pdf/`, `archive/`, `build/`, `local/`은 각각 외부자료, 보관자료, 생성물, 비밀정보입니다.
- `local/secrets/gcp-key.json`과 기타 인증정보는 Git에 올리지 않습니다.
- 과거 `md_to_typ.py`는 `scripts/legacy/`에 보관되며 기본 빌드에서는 사용하지 않습니다.
