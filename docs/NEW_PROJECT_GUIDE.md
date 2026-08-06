# 새 Typst 교재 프로젝트 시작하기

## 1. 준비

저장소 루트에서 다음 도구를 확인한다.

```powershell
typst --version
python --version
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Typst 0.14.x, Python 3.12 이상, 전체 테스트 통과가 시작 조건이다.

## 2. 스타터 생성

슬러그는 영문 소문자·숫자·하이픈만 사용한다.

```powershell
python scripts/project.py new sample-book --title "샘플 교재"
```

생성 결과:

```text
projects/sample-book/
├── project.json
├── README.md
├── typst/book.typ
├── manuscript/01-introduction.md
└── assets/.gitkeep
```

같은 경로가 이미 있으면 CLI는 덮어쓰지 않고 실패한다. `../`가 포함된 슬러그도 거부한다.

## 3. 매니페스트

`project.json`은 빌드 ID, Typst 엔트리, 배포 파일명을 연결한다.

```json
{
  "slug": "sample-book",
  "title": "샘플 교재",
  "deliverables": [
    {
      "id": "sample-book-book",
      "source": "typst/book.typ",
      "output": "샘플 교재.pdf"
    }
  ]
}
```

- `id`: 저장소 전체에서 유일해야 한다.
- `source`: 해당 제품 폴더 안의 Typst 파일만 허용한다.
- `output`: `dist/pdf/` 안의 파일명만 허용한다.
- 두 번째 판본이 필요하면 같은 `deliverables` 배열에 별도 ID·소스·파일명을 추가한다.

## 4. 원고와 디자인

- `manuscript/`: Markdown 원고
- `typst/`: 책 구성, 표지 정보, 원고 포함 순서
- `assets/`: 해당 제품만 사용하는 이미지
- `templates/typst/book.typ`: 여러 제품이 공유하는 기본 테마

스타터 `book.typ`은 `@preview/cmarker`로 Markdown을 읽는다. 장을 늘릴 때는 원고 파일을 만들고 원하는 순서대로 추가한다.

```typst
#cmarker.render(read("../manuscript/01-introduction.md"))
#cmarker.render(read("../manuscript/02-core.md"))
```

제품 고유 디자인이 커지면 `typst/theme.typ`으로 분리한다. 다른 제품에 필요하지 않은 테마를 공용 템플릿에 넣지 않는다.

## 5. 빌드와 확인

```powershell
python scripts/project.py list
python scripts/project.py build sample-book-book
python scripts/project.py verify sample-book-book
```

빌드는 다음 순서로 실행된다.

1. `build/pdf/샘플 교재.pdf`로 Typst 컴파일
2. PDF 파서로 페이지와 대표 텍스트 확인
3. 검증 성공 시 `dist/pdf/샘플 교재.pdf`로 승격
4. 실패 시 기존 `dist/` 파일 유지

## 6. 배포 전 체크리스트

- [ ] 제목·저자·부제가 맞다.
- [ ] `python -m unittest discover -s tests -v`가 통과한다.
- [ ] `python scripts/project.py build <id>`가 종료 코드 0이다.
- [ ] `python scripts/project.py verify <id>`가 페이지 수와 텍스트를 확인한다.
- [ ] 전체 페이지를 PNG로 렌더했다.
- [ ] 접촉 시트에서 빈 페이지·잘림·겹침·깨진 글리프가 없다.
- [ ] 표지, 초반, 중간, 마지막 페이지를 원본 크기로 확인했다.
- [ ] 최종 PDF가 `dist/pdf/`에 있고 중간물은 `build/`에만 있다.
- [ ] 참고 PDF나 비밀키가 Git에 포함되지 않았다.

## 7. 자주 발생하는 문제

### Typst import가 실패한다

CLI는 저장소 루트를 `--root`로 전달한다. 상대경로는 현재 Typst 파일의 위치를 기준으로 확인한다. 공용 템플릿을 쓰는 제품 엔트리는 보통 `../../../templates/typst/book.typ`을 import한다.

### 새 ID가 목록에 보이지 않는다

`project.json`이 `projects/<slug>/project.json`에 있는지, JSON 문법이 올바른지 확인한다.

### 기존 PDF가 바뀌지 않는다

컴파일 또는 PDF 검증이 실패하면 승격하지 않는 것이 정상이다. 콘솔 오류를 해결한 뒤 다시 빌드한다.

### 과거 Markdown 변환기를 쓰고 싶다

`scripts/legacy/md_to_typ.py`는 현재 장 목록과 제목을 반영하지 않는다. 현재 Katalk Typst 정본을 덮어쓰는 용도로 사용하지 않는다.
