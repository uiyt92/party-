# CNA 파티 독립 교재 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `[CNA] Party Edition` 44장 슬라이드를 바탕으로, 혼자 읽고 첫 대화부터 번호 교환까지 실행할 수 있는 35~45쪽짜리 밝은 A5 독립 교재를 만든다.

**Architecture:** `projects/cna-party-edition/`을 독립 제품 경계로 사용한다. 장별 Markdown이 콘텐츠 정본이고, `book.typ`이 순서를 조립하며, `theme.typ`은 밝은 교재 레이아웃과 반복 카드, `diagrams.typ`은 벡터 도식과 원고 토큰 렌더링을 담당한다. 기존 `scripts/project.py`가 매니페스트를 자동 발견해 검증 전 PDF는 `build/pdf/`, 검증된 PDF는 `dist/pdf/`로 승격한다.

**Tech Stack:** Typst 0.14.x, `@preview/cmarker:0.1.6`, Python 3.12+, `unittest`, `pypdf`, Pillow, Poppler (`pdfinfo`, `pdftoppm`)

---

## File map

### Create

- `projects/cna-party-edition/project.json` — 빌드 ID와 배포 파일명
- `projects/cna-party-edition/README.md` — 제품 정본, 범위, 빌드 명령
- `projects/cna-party-edition/manuscript/00-prologue.md` — 독자 진단과 전체 프레임
- `projects/cna-party-edition/manuscript/01-environment.md` — 환경 분석과 첫인상
- `projects/cna-party-edition/manuscript/02-positioning.md` — 기버·셀프 어뮤즈·서브 호스트
- `projects/cna-party-edition/manuscript/03-rapport.md` — 관찰·페이싱·대화 깊이
- `projects/cna-party-edition/manuscript/04-influence.md` — 희소성·프레임·자격 부여·반전
- `projects/cna-party-edition/manuscript/05-number-exchange.md` — 고점 포착과 번호 교환
- `projects/cna-party-edition/manuscript/06-checklist.md` — 실행 카드와 복기표
- `projects/cna-party-edition/typst/book.typ` — 책 조립 순서와 메타데이터
- `projects/cna-party-edition/typst/theme.typ` — A5 레이아웃과 카드 컴포넌트
- `projects/cna-party-edition/typst/diagrams.typ` — 벡터 도식과 특수 토큰 렌더러
- `tests/test_cna_party_project.py` — 제품 구조·원고·최종 PDF 회귀 테스트
- `dist/pdf/CNA_파티의_주도권.pdf` — 검증된 최종 배포본

### Modify

- `README.md` — 정식 PDF 표에 새 책 추가
- `docs/ARTIFACT_INVENTORY.md` — 페이지 수, 파일 크기, SHA-256 기록
- `docs/PROJECT_STRUCTURE.md` — 활성 제품과 정본 설명 추가

### Local-only reference and QA

- `references/pdf/[CNA] Party Edition.pdf` — 원본 슬라이드, Git 제외
- `build/rendered/cna-party-book/` — 전체 페이지 PNG와 컨택트 시트, Git 제외
- `build/rendered-high/cna-party-book/` — 대표 페이지 고해상도 PNG, Git 제외

## Editorial contract

- 제목: `파티의 주도권`
- 부제: `첫 대화부터 번호 교환까지, 호감과 긴장감을 설계하는 실전 커뮤니케이션`
- 시리즈: `CNA Party Edition`
- 저자: `PREDIC / SUPER NATURAL`
- 최종 파일: `CNA_파티의_주도권.pdf`
- 목표: 39~42쪽, 허용: 35~45쪽
- 문체: 친근한 현장 코치형 대화체
- 전개: 현장 장면 → 원리 → `BAD MOVE` → `BETTER MOVE` → `SCRIPT` → `MISSION` → 복기
- 범위 끝: 번호 교환과 깔끔한 퇴장
- 제외: 이후 카톡, 애프터 운영, 성적 접촉, 강압·기만·취중 이용

---

### Task 1: Register the product and preserve the source reference

**Files:**
- Create: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/project.json`
- Create: `projects/cna-party-edition/README.md`
- Local copy: `references/pdf/[CNA] Party Edition.pdf`

- [ ] **Step 1: Write the failing manifest test**

Create `tests/test_cna_party_project.py`:

```python
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "cna-party-edition"


class CnaPartyManifestTests(unittest.TestCase):
    def test_manifest_registers_stable_deliverable(self):
        payload = json.loads(
            (PROJECT / "project.json").read_text(encoding="utf-8")
        )

        self.assertEqual(payload["slug"], "cna-party-edition")
        self.assertEqual(payload["title"], "파티의 주도권")
        self.assertEqual(payload["deliverables"], [
            {
                "id": "cna-party-book",
                "source": "typst/book.typ",
                "output": "CNA_파티의_주도권.pdf",
            }
        ])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm the expected failure**

Run:

```powershell
python -m unittest tests.test_cna_party_project -v
```

Expected: `ERROR` with `FileNotFoundError` for `projects/cna-party-edition/project.json`.

- [ ] **Step 3: Copy the source into the ignored reference area**

Run:

```powershell
Copy-Item -LiteralPath 'C:\Users\SuperNatural1\Downloads\[CNA] Party Edition.pdf' -Destination 'references\pdf\[CNA] Party Edition.pdf'
git check-ignore -v 'references/pdf/[CNA] Party Edition.pdf'
```

Expected: `Copy-Item` succeeds and `git check-ignore` reports the `references/pdf/*.pdf` rule. Do not stage this PDF.

- [ ] **Step 4: Create the product manifest**

Create `projects/cna-party-edition/project.json`:

```json
{
  "slug": "cna-party-edition",
  "title": "파티의 주도권",
  "deliverables": [
    {
      "id": "cna-party-book",
      "source": "typst/book.typ",
      "output": "CNA_파티의_주도권.pdf"
    }
  ]
}
```

- [ ] **Step 5: Document the product boundary**

Create `projects/cna-party-edition/README.md` with these exact operational facts:

````markdown
# 파티의 주도권

`[CNA] Party Edition` 강의 슬라이드를 독립 교재로 전면 재집필한 A5 Typst 제품이다.

## 정본

- 콘텐츠: `manuscript/*.md`
- 구성·디자인: `typst/*.typ`
- 참고 슬라이드: `references/pdf/[CNA] Party Edition.pdf` (Git 제외)
- 배포본: `dist/pdf/CNA_파티의_주도권.pdf`

## 범위

파티 전 준비부터 첫 대화, 감정과 프레임 설계, 번호 교환까지 다룬다. 번호 교환 이후 카톡과 애프터 운영은 포함하지 않는다.

## 빌드

```powershell
python scripts/project.py build cna-party-book
python scripts/project.py verify cna-party-book
```
````

- [ ] **Step 6: Run tests and confirm the manifest is discoverable**

Run:

```powershell
python -m unittest tests.test_cna_party_project -v
python scripts/project.py list
```

Expected: the test passes; `list` includes `cna-party-book`, `projects\cna-party-edition\typst\book.typ`, and `dist\pdf\CNA_파티의_주도권.pdf`.

- [ ] **Step 7: Commit the product registration**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/project.json projects/cna-party-edition/README.md
git commit -m "feat: register CNA party book product"
```

---

### Task 2: Create the book entry and bright A5 theme

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/typst/book.typ`
- Create: `projects/cna-party-edition/typst/theme.typ`

- [ ] **Step 1: Add a failing source-contract test**

Add this class above the `if __name__` block in `tests/test_cna_party_project.py`:

```python
class CnaPartyTypstContractTests(unittest.TestCase):
    def test_book_and_theme_expose_required_contract(self):
        book = (PROJECT / "typst" / "book.typ").read_text(encoding="utf-8")
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")

        for text in [
            "파티의 주도권",
            "첫 대화부터 번호 교환까지",
            "PREDIC / SUPER NATURAL",
            "render-rich",
        ]:
            self.assertIn(text, book)

        for function_name in [
            "#let book(",
            "#let part-divider(",
            "#let field-note(",
            "#let bad-move(",
            "#let better-move(",
            "#let frame-card(",
            "#let mission-card(",
        ]:
            self.assertIn(function_name, theme)
```

- [ ] **Step 2: Run the contract test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyTypstContractTests -v
```

Expected: `ERROR` because `typst/book.typ` does not exist.

- [ ] **Step 3: Create the book assembly entry**

Create `projects/cna-party-edition/typst/book.typ`:

```typst
// 파티의 주도권 — 빌드 엔트리
// 실행: python scripts/project.py build cna-party-book
#import "theme.typ": *
#import "diagrams.typ": render-rich

#show: book.with(
  title: "파티의 주도권",
  subtitle: "첫 대화부터 번호 교환까지, 호감과 긴장감을 설계하는 실전 커뮤니케이션",
  series: "CNA Party Edition",
  author: "PREDIC / SUPER NATURAL",
)

#render-rich("../manuscript/00-prologue.md")

#part-divider("PART 1", "들어가기 전에 이미 승부는 시작된다")
#render-rich("../manuscript/01-environment.md")

#part-divider("PART 2", "참가자가 아니라 분위기의 공급자가 되어라")
#render-rich("../manuscript/02-positioning.md")

#part-divider("PART 3", "상대의 주파수 안으로 들어가라")
#render-rich("../manuscript/03-rapport.md")

#part-divider("PART 4", "호감과 긴장감을 의도적으로 설계하라")
#render-rich("../manuscript/04-influence.md")

#part-divider("PART 5", "고점에서 번호를 교환하라")
#render-rich("../manuscript/05-number-exchange.md")

#part-divider("FIELD CARD", "다음 파티를 위한 실행 카드")
#render-rich("../manuscript/06-checklist.md")
```

- [ ] **Step 4: Implement the theme API**

Create `projects/cna-party-edition/typst/theme.typ`. Use these exact tokens and public functions; keep all helper functions private to this file:

```typst
#let lime = rgb("#A8E63A")
#let lime-dark = rgb("#527A12")
#let navy = rgb("#142033")
#let ink = rgb("#202833")
#let muted = rgb("#697586")
#let line = rgb("#DCE3EA")
#let paper = rgb("#FFFEFA")
#let bad = rgb("#C84A4A")
#let bad-soft = rgb("#FFF2F0")
#let better = rgb("#167D73")
#let better-soft = rgb("#EEF9F7")
#let blue-soft = rgb("#F0F5FA")

#let book(title: "", subtitle: "", series: "", author: "", body) = {
  set document(title: title, author: author)
  set text(font: "Pretendard", size: 10.2pt, fill: ink, lang: "ko", hyphenate: false)
  set par(justify: true, leading: 1.35em, spacing: 1.55em)

  set page(paper: "a5", margin: 0pt, fill: paper)
  page(numbering: none)[
    #place(top + left, dx: 1.8cm, dy: 1.8cm)[
      #box(fill: navy, radius: 3pt, inset: (x: 9pt, y: 5pt))[
        #text(size: 8.5pt, weight: 800, fill: white, tracking: 1.4pt)[#upper(series)]
      ]
    ]
    #v(1fr)
    #block(inset: (x: 1.8cm))[
      #line(length: 38pt, stroke: 4pt + lime)
      #v(16pt)
      #text(size: 34pt, weight: 900, fill: navy, tracking: -1pt)[#title]
      #v(15pt)
      #text(size: 11pt, weight: 600, fill: muted)[#subtitle]
    ]
    #v(1fr)
    #block(inset: (x: 1.8cm, bottom: 1.8cm))[
      #text(size: 8.5pt, weight: 600, fill: muted)[#author]
    ]
  ]

  page(numbering: none)[
    #v(1fr)
    #text(size: 16pt, weight: 900, fill: navy)[#title]
    #v(10pt)
    #text(size: 9pt, fill: muted)[#subtitle]
    #v(24pt)
    #line(length: 100%, stroke: 0.8pt + line)
    #v(14pt)
    #text(size: 8.5pt, fill: ink)[초판 2026년 · #author]
    #v(8pt)
    #text(size: 8pt, fill: muted)[이 교재는 소셜 파티 현장의 커뮤니케이션 훈련을 위한 자료다. 상대의 판단 능력이 흐려졌거나 명시적인 거절이 나온 상황에서는 설득을 중단한다.]
    #v(8pt)
    #text(size: 8pt, fill: muted)[저작권자의 허락 없이 본문과 도식을 상업적으로 복제하거나 배포할 수 없다.]
  ]

  set page(paper: "a5", margin: (x: 1.9cm, y: 2.1cm), fill: paper)
  page(numbering: none)[
    #text(size: 9pt, weight: 800, fill: lime-dark, tracking: 2pt)[CONTENTS]
    #v(5pt)
    #text(size: 22pt, weight: 900, fill: navy)[목차]
    #v(8pt)
    #line(length: 38pt, stroke: 3pt + lime)
    #v(20pt)
    #show outline.entry: it => { set text(size: 10pt, fill: ink); v(7pt); it }
    #outline(title: none, depth: 1)
  ]

  set page(
    paper: "a5",
    margin: (x: 1.85cm, top: 2.05cm, bottom: 1.7cm),
    fill: paper,
    numbering: "1",
    header: context {
      align(right, text(size: 7.5pt, weight: 600, fill: muted)[파티의 주도권])
    },
    footer: context {
      align(center, text(size: 8pt, weight: 700, fill: muted)[#counter(page).display()])
    },
  )

  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    block(below: 1.4em)[
      #line(length: 30pt, stroke: 4pt + lime)
      #v(9pt)
      #text(size: 22pt, weight: 900, fill: navy)[#it.body]
    ]
  }
  show heading.where(level: 2): it => block(above: 1.6em, below: 0.7em)[
    #text(size: 13pt, weight: 850, fill: navy)[#it.body]
  ]
  show quote.where(block: true): it => block(
    width: 100%, fill: blue-soft, radius: 6pt,
    inset: (x: 13pt, y: 10pt), stroke: (left: 3pt + navy),
    above: 1em, below: 1em,
  )[#it.body]
  set table(
    stroke: (x: none, y: 0.6pt + line),
    inset: (x: 7pt, y: 6pt),
    fill: (_, y) => if y == 0 { navy } else { none },
  )
  show table.cell.where(y: 0): set text(fill: white, weight: 750, size: 8.5pt)
  body
}

#let part-divider(label, title) = {
  pagebreak(weak: true)
  set page(paper: "a5", margin: 0pt, fill: navy, numbering: none, header: none, footer: none)
  page[
    #v(1fr)
    #block(inset: (x: 1.9cm))[
      #box(fill: lime, radius: 3pt, inset: (x: 10pt, y: 5pt))[
        #text(size: 9pt, weight: 900, fill: navy, tracking: 1.5pt)[#label]
      ]
      #v(18pt)
      #text(size: 22pt, weight: 900, fill: white)[#title]
    ]
    #v(1fr)
  ]
}

#let card(label, accent, fill-color, body) = block(
  width: 100%, fill: fill-color, radius: 7pt,
  inset: (x: 13pt, y: 11pt), stroke: (left: 3pt + accent),
  above: 1em, below: 1em,
)[
  #text(size: 8pt, weight: 900, fill: accent, tracking: 1pt)[#label]
  #v(5pt)
  #text(size: 9.2pt, fill: ink)[#body]
]

#let field-note(body) = card("FIELD NOTE", lime-dark, rgb("#F5FAEA"), body)
#let bad-move(body) = card("BAD MOVE", bad, bad-soft, body)
#let better-move(body) = card("BETTER MOVE", better, better-soft, body)
#let frame-card(body) = card("FRAME", navy, blue-soft, body)
#let mission-card(body) = card("MISSION", lime-dark, rgb("#F5FAEA"), body)
```

- [ ] **Step 5: Run the Typst contract test**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyTypstContractTests -v
```

Expected: PASS. The PDF is not built yet because `diagrams.typ` and manuscripts are intentionally absent.

- [ ] **Step 6: Commit the entry and theme**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/typst/book.typ projects/cna-party-edition/typst/theme.typ
git commit -m "feat: add bright CNA party book theme"
```

---

### Task 3: Add vector diagrams and rich manuscript tokens

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/typst/diagrams.typ`

- [ ] **Step 1: Add a failing diagram-contract test**

Add this method to `CnaPartyTypstContractTests`:

```python
    def test_diagram_renderer_supports_required_visuals_and_cards(self):
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(
            encoding="utf-8"
        )
        for key in [
            "party_map",
            "positioning_loop",
            "rapport_ladder",
            "influence_curve",
            "number_window",
            "level_test",
        ]:
            self.assertIn(f"{key}:", diagrams)
        for kind in ["field", "bad", "better", "frame", "mission"]:
            self.assertIn(f"{kind}:", diagrams)
        self.assertIn("#let render-rich(path)", diagrams)
```

- [ ] **Step 2: Run the diagram test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyTypstContractTests.test_diagram_renderer_supports_required_visuals_and_cards -v
```

Expected: `ERROR` because `typst/diagrams.typ` does not exist.

- [ ] **Step 3: Implement the diagram set**

Create `projects/cna-party-edition/typst/diagrams.typ`. Import cmarker and the five card functions from `theme.typ`. Implement six diagrams using Typst `box`, `grid`, `stack`, `line`, `rect`, `circle`, and `text` only:

```typst
#import "@preview/cmarker:0.1.6"
#import "theme.typ": lime, lime-dark, navy, ink, muted, line, field-note, bad-move, better-move, frame-card, mission-card

#let diagram-frame(title, body) = block(
  width: 100%, fill: white, radius: 8pt,
  stroke: 0.8pt + line, inset: 12pt, above: 1.2em, below: 1.2em,
)[
  #text(size: 9pt, weight: 850, fill: navy)[#title]
  #v(10pt)
  #body
]

#let step(number, title, note) = grid(
  columns: (20pt, 1fr), gutter: 8pt, align: horizon,
  box(width: 18pt, height: 18pt, radius: 9pt, fill: lime,
    align(center + horizon, text(size: 8pt, weight: 900, fill: navy)[#number])),
  box(width: 100%, fill: rgb("#F3F6F9"), radius: 5pt, inset: (x: 9pt, y: 6pt))[
    #text(size: 8.5pt, weight: 750, fill: ink)[#title]
    #h(5pt)
    #text(size: 7.5pt, fill: muted)[#note]
  ],
)

#let party-map = diagram-frame("파티를 읽는 세 개의 렌즈", grid(
  columns: (1fr, 1fr, 1fr), gutter: 7pt,
  step("1", "환경", "자리·진행·소음"),
  step("2", "경쟁자", "누가 공간을 쓰나"),
  step("3", "타깃", "상태·무리·몰입도"),
))

#let positioning-loop = diagram-frame("분위기의 공급자 루프", stack(dir: ttb, spacing: 6pt,
  step("1", "관찰", "불편과 빈틈 찾기"),
  step("2", "공급", "에너지·배려·연결"),
  step("3", "반응", "웃음·질문·시선 확인"),
  step("4", "이동", "한 사람에게 고정되지 않기"),
))

#let rapport-ladder = diagram-frame("대화를 깊게 만드는 네 층", stack(dir: ttb, spacing: 5pt,
  step("1", "감정", "지금 어떻게 느끼는가"),
  step("2", "취향", "무엇을 좋아하고 피하는가"),
  step("3", "가치관", "왜 그것이 중요한가"),
  step("4", "경험", "어떤 사건이 그것을 만들었나"),
))

#let influence-curve = diagram-frame("호감과 긴장감은 직선이 아니다", align(center,
  stack(dir: ltr, spacing: 9pt,
    rect(width: 18pt, height: 18pt, fill: rgb("#DDE5EC"), radius: 2pt),
    rect(width: 18pt, height: 34pt, fill: lime, radius: 2pt),
    rect(width: 18pt, height: 24pt, fill: rgb("#DDE5EC"), radius: 2pt),
    rect(width: 18pt, height: 48pt, fill: lime-dark, radius: 2pt),
    rect(width: 18pt, height: 38pt, fill: rgb("#DDE5EC"), radius: 2pt),
    rect(width: 18pt, height: 62pt, fill: navy, radius: 2pt),
  )
))

#let number-window = diagram-frame("번호 교환 창이 열리는 순서", stack(dir: ttb, spacing: 6pt,
  step("1", "상호 투자", "상대도 질문하고 머문다"),
  step("2", "공동 맥락", "둘만 아는 소재가 생긴다"),
  step("3", "다음 명분", "이어갈 구체적 이유가 생긴다"),
  step("4", "짧은 제안", "설명하지 말고 교환한다"),
))

#let level-test = diagram-frame("현장 레벨 테스트", stack(dir: ttb, spacing: 5pt,
  step("1", "입장", "혼자 있어도 경직되지 않는다"),
  step("2", "대화", "낯선 사람에게 말을 건다"),
  step("3", "포지셔닝", "테이블의 흐름에 기여한다"),
  step("4", "프레임", "상대 반응에 끌려가지 않는다"),
  step("5", "전환", "고점에서 번호를 교환한다"),
))
```

- [ ] **Step 4: Implement a single-pass token renderer**

Append to the same file:

```typst
#let DIAGRAMS = (
  party_map: party-map,
  positioning_loop: positioning-loop,
  rapport_ladder: rapport-ladder,
  influence_curve: influence-curve,
  number_window: number-window,
  level_test: level-test,
)

#let CALLOUTS = (
  field: field-note,
  bad: bad-move,
  better: better-move,
  frame: frame-card,
  mission: mission-card,
)

// Standalone tokens:
// [[DIAGRAM:party_map]]
// [[CALLOUT:bad|한 줄 요약]]
#let render-rich(path) = {
  let raw = read(path)
  let pattern = regex("\[\[(DIAGRAM:[a-z0-9_]+|CALLOUT:[a-z_]+\|[^\]]+)\]\]")
  let chunks = raw.split(pattern)
  let tokens = raw.matches(pattern).map(match => match.text)

  for (index, chunk) in chunks.enumerate() {
    cmarker.render(chunk)
    if index < tokens.len() {
      let inner = tokens.at(index).replace("[[", "").replace("]]", "")
      if inner.starts-with("DIAGRAM:") {
        let key = inner.replace("DIAGRAM:", "")
        if key in DIAGRAMS { DIAGRAMS.at(key) }
      } else {
        let payload = inner.replace("CALLOUT:", "").split("|")
        let kind = payload.first()
        let message = payload.slice(1).join("|")
        if kind in CALLOUTS { CALLOUTS.at(kind)(message) }
      }
    }
  }
}
```

- [ ] **Step 5: Run the diagram contract test**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyTypstContractTests -v
```

Expected: both Typst contract tests pass.

- [ ] **Step 6: Commit diagrams and renderer**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/typst/diagrams.typ
git commit -m "feat: add CNA party book diagrams"
```

---

### Task 4: Write the prologue and environment chapter

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/manuscript/00-prologue.md`
- Create: `projects/cna-party-edition/manuscript/01-environment.md`

- [ ] **Step 1: Add failing content tests**

Add this class above the `if __name__` block:

```python
class CnaPartyManuscriptTests(unittest.TestCase):
    def assert_chapter(self, filename, minimum_chars, headings, tokens):
        text = (PROJECT / "manuscript" / filename).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text), minimum_chars)
        for heading in headings:
            self.assertIn(heading, text)
        for token in tokens:
            self.assertIn(token, text)

    def test_prologue_and_environment_are_self_contained(self):
        self.assert_chapter(
            "00-prologue.md",
            1600,
            [
                "# 파티는 말보다 먼저 시작된다",
                "## 초보자와 무성과자가 같은 곳에서 무너지는 이유",
                "## 파티는 동적 포지셔닝 게임이다",
                "## 이 책을 사용하는 법",
            ],
            ["[[DIAGRAM:level_test]]", "[[CALLOUT:field|"],
        )
        self.assert_chapter(
            "01-environment.md",
            3200,
            [
                "# 공간을 먼저 읽어라",
                "## 자리 배치는 대화보다 솔직하다",
                "## 경쟁자를 분석하는 기준",
                "## 타깃의 상태를 읽는 법",
                "## 자기소개는 정보를 말하는 시간이 아니다",
            ],
            ["[[DIAGRAM:party_map]]", "[[CALLOUT:bad|", "[[CALLOUT:better|", "[[CALLOUT:mission|"],
        )
```

- [ ] **Step 2: Run the content test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_prologue_and_environment_are_self_contained -v
```

Expected: `ERROR` because `00-prologue.md` is absent.

- [ ] **Step 3: Write the prologue from scratch**

Write `00-prologue.md` to 1,800~2,400 Korean characters. It must:

- open with a beginner entering a party and immediately scanning for one attractive person;
- contrast that beginner with an experienced attendee who talks a lot but leaves no impression;
- define a party as a changing field of attention, status, comfort, and tension;
- explain that the goal is not universal approval but a repeatable process;
- include `[[DIAGRAM:level_test]]` after the reader diagnostic;
- include `[[CALLOUT:field|파티에서는 무슨 말을 했는지보다, 들어온 뒤 누구의 상태를 어떻게 바꿨는지가 더 오래 남는다.]]`;
- explain how to use `BAD MOVE`, `BETTER MOVE`, `SCRIPT`, and `MISSION` without mentioning slide numbers.

- [ ] **Step 4: Write PART 1 from scratch**

Write `01-environment.md` to 3,500~4,500 Korean characters. Cover these scenes in order:

1. entrance pause: spend the first 60~90 seconds reading the room instead of targeting;
2. seat map: identify center, edge, traffic route, isolated pair, established group;
3. competitor scan: distinguish loud attention from actual influence;
4. target-state scan: friend dependence, fatigue, conversation saturation, openness;
5. appearance: call it an entry ticket, then show why behavior data replaces the halo;
6. self-introduction: convert occupation and hobbies into emotion, imagination, and social context;
7. a two-column bad/better script comparing résumé-style introduction with a story-bearing introduction.

Use all required tokens from the test. Place `[[DIAGRAM:party_map]]` immediately after the three-lens explanation. End with a mission that instructs the reader to draw the room before starting a target conversation.

- [ ] **Step 5: Run the chapter test**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_prologue_and_environment_are_self_contained -v
```

Expected: PASS.

- [ ] **Step 6: Commit the opening chapters**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/00-prologue.md projects/cna-party-edition/manuscript/01-environment.md
git commit -m "feat: write CNA party opening chapters"
```

---

### Task 5: Write the positioning chapter

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/manuscript/02-positioning.md`

- [ ] **Step 1: Add the failing positioning test**

Add this method to `CnaPartyManuscriptTests`:

```python
    def test_positioning_chapter_builds_social_value(self):
        self.assert_chapter(
            "02-positioning.md",
            3500,
            [
                "# 분위기를 공급하는 사람이 되어라",
                "## 특정성에서 빠져나오기",
                "## 기버는 착한 사람이 아니라 주도하는 사람이다",
                "## 셀프 어뮤즈",
                "## 서브 호스트 프레임",
                "## 거절을 사회적 굳은살로 바꾸기",
            ],
            ["[[DIAGRAM:positioning_loop]]", "[[CALLOUT:frame|", "[[CALLOUT:mission|"],
        )
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_positioning_chapter_builds_social_value -v
```

Expected: `ERROR` because `02-positioning.md` is absent.

- [ ] **Step 3: Write PART 2**

Write `02-positioning.md` to 4,000~5,000 Korean characters. It must:

- show how over-investing in one person changes posture, gaze, timing, and perceived scarcity;
- redefine giver behavior as noticing and resolving friction rather than pleasing everyone;
- show three micro-actions: introduce two strangers, repair an awkward pause, offer a context-appropriate small convenience;
- distinguish self-amusement from loud performance;
- describe the sub-host as someone who moves attention and energy without pretending to be the organizer;
- include one failure case where excessive helping becomes service-staff positioning;
- include one experienced non-achiever case where monopolizing one conversation lowers social proof;
- use `[[DIAGRAM:positioning_loop]]` after the observe→supply→reaction→move loop;
- use `[[CALLOUT:frame|당신의 위치는 스스로 주장해서 생기지 않는다. 다른 사람들의 반응이 반복해서 당신을 중심으로 가리킬 때 생긴다.]]`;
- end with a mission: create three positive interactions before approaching the primary target.

- [ ] **Step 4: Run the positioning test**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_positioning_chapter_builds_social_value -v
```

Expected: PASS.

- [ ] **Step 5: Commit PART 2**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/02-positioning.md
git commit -m "feat: write CNA party positioning chapter"
```

---

### Task 6: Write the rapport and first-conversation chapter

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/manuscript/03-rapport.md`

- [ ] **Step 1: Add the failing rapport test**

Add this method to `CnaPartyManuscriptTests`:

```python
    def test_rapport_chapter_teaches_observable_conversation_flow(self):
        self.assert_chapter(
            "03-rapport.md",
            4800,
            [
                "# 상대의 주파수 안으로 들어가라",
                "## 말보다 먼저 상태를 읽는다",
                "## 페이싱은 흉내가 아니다",
                "## 감정에서 경험까지 내려가는 네 층",
                "## 스몰토크는 역추적이다",
                "## 5감을 6감으로 바꾸는 법",
                "## 첫 대화 전체 예시",
            ],
            ["[[DIAGRAM:rapport_ladder]]", "[[CALLOUT:bad|", "[[CALLOUT:better|", "[[CALLOUT:mission|"],
        )
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_rapport_chapter_teaches_observable_conversation_flow -v
```

Expected: `ERROR` because `03-rapport.md` is absent.

- [ ] **Step 3: Write PART 3**

Write `03-rapport.md` to 5,500~6,500 Korean characters. Include:

- observable state cues: body direction, response latency, breath, volume, eye movement, friend checking;
- pacing examples for high-energy, cautious, tired, and socially saturated states;
- a warning that mirroring every gesture looks mechanical;
- the four-layer path `감정 → 취향 → 가치관 → 경험` with `[[DIAGRAM:rapport_ladder]]`;
- a bad interview sequence made of facts and serial questions;
- a better sequence that follows one emotional clue downward;
- the 5-sense to 6-sense method: observation → personal association → compact metaphor;
- three rewritten examples based on venue light, music, and crowded movement;
- a complete first-conversation script with annotations showing state read, pacing, emotional question, self-disclosure, and exit;
- a low-response branch where the reader exits without trying to rescue the conversation;
- a mission to make three observations before asking a personal question.

Use a blockquote headed `**SCRIPT**` for multi-line dialogue. Use one-line callout tokens only for summaries so the renderer remains deterministic.

- [ ] **Step 4: Run the rapport test**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_rapport_chapter_teaches_observable_conversation_flow -v
```

Expected: PASS.

- [ ] **Step 5: Commit PART 3**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/03-rapport.md
git commit -m "feat: write CNA party rapport chapter"
```

---

### Task 7: Write the influence and tension chapter

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/manuscript/04-influence.md`

- [ ] **Step 1: Add the failing influence test**

Add this method to `CnaPartyManuscriptTests`:

```python
    def test_influence_chapter_preserves_strategic_core(self):
        self.assert_chapter(
            "04-influence.md",
            4800,
            [
                "# 호감과 긴장감을 의도적으로 설계하라",
                "## 희소성은 바쁜 척이 아니다",
                "## 프레임을 먼저 제시하는 사람이 해석을 만든다",
                "## 자격 부여",
                "## 가벼움 뒤에 반전을 배치하라",
                "## 미래 투사는 약속이 아니라 장면이다",
                "## 긴장감을 회수하는 법",
            ],
            ["[[DIAGRAM:influence_curve]]", "[[CALLOUT:frame|", "[[CALLOUT:bad|", "[[CALLOUT:better|", "[[CALLOUT:mission|"],
        )
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_influence_chapter_preserves_strategic_core -v
```

Expected: `ERROR` because `04-influence.md` is absent.

- [ ] **Step 3: Write PART 4**

Write `04-influence.md` to 5,500~6,500 Korean characters. Preserve the manipulative/strategic framing explicitly:

- define influence as controlling interpretation, attention, investment, and timing rather than merely exchanging information;
- explain scarcity through selective attention and willingness to leave, not fabricated schedules;
- show how a frame changes the meaning of the same party behavior;
- explain qualification as making the other person reveal and invest in qualities beyond appearance;
- contrast shallow appearance praise with attitude-based qualification;
- use playful/light positioning first, then reveal professional discipline or a serious standard as contrast;
- define future projection as a vivid shared scene that creates continuity, without promising a relationship;
- use `[[DIAGRAM:influence_curve]]` to show tension rising through approach and release;
- include a case where constant challenge becomes contempt and lowers safety;
- include a case where nonstop validation removes tension;
- provide a complete sequence: playful observation → standard/frame → qualification question → earned acknowledgment → contrast → shared scene;
- include `[[CALLOUT:frame|호감은 많이 주는 사람이 이기는 게임이 아니다. 상대가 당신의 관심을 얻기 위해 조금씩 투자하게 만드는 구조가 중요하다.]]`;
- state the hard boundary once: impaired judgment, explicit refusal, or visible distress ends the technique rather than becoming an obstacle to overcome;
- end with a mission to use one qualification question and leave space for the answer.

- [ ] **Step 4: Run the influence test**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_influence_chapter_preserves_strategic_core -v
```

Expected: PASS.

- [ ] **Step 5: Commit PART 4**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/04-influence.md
git commit -m "feat: write CNA party influence chapter"
```

---

### Task 8: Write number exchange and field checklist chapters

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Create: `projects/cna-party-edition/manuscript/05-number-exchange.md`
- Create: `projects/cna-party-edition/manuscript/06-checklist.md`

- [ ] **Step 1: Add the failing closing-chapter test**

Add this method to `CnaPartyManuscriptTests`:

```python
    def test_closing_chapters_end_at_number_exchange(self):
        self.assert_chapter(
            "05-number-exchange.md",
            2600,
            [
                "# 고점에서 번호를 교환하라",
                "## 번호보다 먼저 명분을 만든다",
                "## 교환 창이 열렸다는 신호",
                "## 짧게 제안하고 설명하지 않는다",
                "## 거절을 처리하는 가장 좋은 방식",
                "## 먼저 떠나는 사람이 여운을 만든다",
            ],
            ["[[DIAGRAM:number_window]]", "[[CALLOUT:bad|", "[[CALLOUT:better|", "[[CALLOUT:mission|"],
        )
        self.assert_chapter(
            "06-checklist.md",
            1200,
            [
                "# 다음 파티를 위한 실행 카드",
                "## 입장 전",
                "## 첫 10분",
                "## 첫 대화",
                "## 번호 교환",
                "## 집에 돌아온 뒤 복기",
            ],
            ["[[DIAGRAM:level_test]]", "[[CALLOUT:field|"],
        )
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_closing_chapters_end_at_number_exchange -v
```

Expected: `ERROR` because `05-number-exchange.md` is absent.

- [ ] **Step 3: Write PART 5**

Write `05-number-exchange.md` to 3,000~4,000 Korean characters. Include:

- why asking after a dead conversation turns the number into a consolation prize;
- three prerequisites: mutual investment, shared context, next-step reason;
- `[[DIAGRAM:number_window]]` immediately after the prerequisites;
- observable green signals and ambiguous signals without pretending they guarantee consent;
- three short number-exchange scripts: shared place, shared interest, playful continuation;
- one direct script for confident readers and one softer script for beginners;
- bad examples that over-explain, beg, or negotiate after refusal;
- a refusal response that preserves composure and returns to the room;
- the high-point exit: exchange, one closing line, leave before energy collapses;
- a mission to attempt the exchange only after naming the continuation reason in one sentence.

Do not include post-exchange KakaoTalk messages or date scheduling details.

- [ ] **Step 4: Write the field card appendix**

Write `06-checklist.md` to 1,500~2,200 Korean characters. Use Markdown checklists and compact tables for:

- appearance and logistics before entry;
- the first 10 minutes: map room, make three low-stakes interactions, find social center;
- first conversation: state cue, pacing, emotional clue, one self-disclosure;
- influence: standard, qualification, contrast, release;
- number exchange: investment, shared context, next reason, short ask;
- after-action review with columns `관찰 / 내가 한 행동 / 상대 반응 / 다음 실험`;
- a five-level self-score using `[[DIAGRAM:level_test]]`;
- `[[CALLOUT:field|한 번의 번호보다 중요한 것은 다음 파티에서도 반복할 수 있는 행동을 남기는 것이다.]]`.

- [ ] **Step 5: Run all manuscript tests**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests -v
```

Expected: all manuscript tests pass.

- [ ] **Step 6: Commit the closing chapters**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/05-number-exchange.md projects/cna-party-edition/manuscript/06-checklist.md
git commit -m "feat: complete CNA party book manuscript"
```

---

### Task 9: Compile, enforce the page budget, and add artifact regression coverage

**Files:**
- Modify as required: `projects/cna-party-edition/manuscript/*.md`
- Modify as required: `projects/cna-party-edition/typst/theme.typ`
- Modify: `tests/test_cna_party_project.py`
- Create: `dist/pdf/CNA_파티의_주도권.pdf`

- [ ] **Step 1: Run all unit tests before compilation**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: 26 tests pass: the existing 18 tests plus eight CNA party source-contract tests.

- [ ] **Step 2: Add a failing final-artifact test**

Add this class above the `if __name__` block in `tests/test_cna_party_project.py` before the first PDF build:

```python
class CnaPartyArtifactTests(unittest.TestCase):
    def test_distribution_pdf_is_release_ready(self):
        from pypdf import PdfReader

        path = ROOT / "dist" / "pdf" / "CNA_파티의_주도권.pdf"
        self.assertTrue(path.is_file())
        reader = PdfReader(str(path))
        self.assertGreaterEqual(len(reader.pages), 35)
        self.assertLessEqual(len(reader.pages), 45)
        cover_text = reader.pages[0].extract_text() or ""
        self.assertIn("파티의 주도권", cover_text)
        self.assertIn("CNA", cover_text)
        all_text = "".join(page.extract_text() or "" for page in reader.pages)
        self.assertGreaterEqual(len(all_text), 15000)
```

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyArtifactTests -v
```

Expected: FAIL at `path.is_file()` because the distribution PDF has not been built.

- [ ] **Step 3: Compile the new book**

Run:

```powershell
python scripts/project.py build cna-party-book
```

Expected: exit code 0 and a `built cna-party-book` line containing numeric page and sample-character counts.

If Typst reports a syntax or unknown-key error, fix only the named theme, diagram, or manuscript token, rerun the same build, and preserve the last verified `dist/` copy until success.

- [ ] **Step 4: Measure page count and text coverage**

Run:

```powershell
python -c "from pathlib import Path; from pypdf import PdfReader; p=Path('dist/pdf/CNA_파티의_주도권.pdf'); r=PdfReader(str(p)); print('pages=',len(r.pages)); print('chars=',sum(len(page.extract_text() or '') for page in r.pages))"
```

Expected: 35~45 pages and at least 15,000 extracted characters across the book.

If below 35 pages, add examples or explanations to the thinnest manuscript chapter; do not inflate margins or font size. If above 45 pages, remove repetition and tighten callout spacing before reducing the body font. Target 39~42 pages.

- [ ] **Step 5: Run the artifact test against the promoted PDF**

Run:

```powershell
python -m unittest tests.test_cna_party_project.CnaPartyArtifactTests -v
```

Expected: the artifact test passes against the PDF promoted in Step 3.

- [ ] **Step 6: Verify the PDF independently**

Run:

```powershell
python scripts/project.py verify cna-party-book
```

Expected: `verified cna-party-book` with the same 35~45 page count.

- [ ] **Step 7: Commit the first release candidate**

```powershell
git add projects/cna-party-edition tests/test_cna_party_project.py dist/pdf/CNA_파티의_주도권.pdf
git commit -m "feat: build CNA party standalone book"
```

---

### Task 10: Render every page and fix visual defects

**Files:**
- Modify as defects require: `projects/cna-party-edition/typst/theme.typ`
- Modify as defects require: `projects/cna-party-edition/typst/diagrams.typ`
- Modify as defects require: `projects/cna-party-edition/manuscript/*.md`
- Regenerate: `dist/pdf/CNA_파티의_주도권.pdf`
- Generate ignored QA: `build/rendered/cna-party-book/*.png`
- Generate ignored QA: `build/rendered-high/cna-party-book/*.png`

- [ ] **Step 1: Render every page at contact-sheet resolution**

Run with the bundled Poppler path:

```powershell
$renderer = 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
New-Item -ItemType Directory -Force 'build\rendered\cna-party-book' | Out-Null
& $renderer -png -r 72 'dist\pdf\CNA_파티의_주도권.pdf' 'build\rendered\cna-party-book\page'
python scripts/pdf_contact_sheets.py 'build\rendered\cna-party-book' --per-sheet 25 --columns 5 --thumbnail-width 180
```

Expected: PNG count equals PDF page count and two contact sheets are produced for a 35~45 page book.

- [ ] **Step 2: Inspect every contact sheet**

Check every thumbnail for:

- blank or accidental near-blank pages;
- clipped titles, author, footer, or table rows;
- cards split in unreadable places;
- broken callout tokens printed literally;
- diagrams exceeding margins;
- missing Korean glyphs;
- headings stranded at page bottoms;
- part dividers followed by unintended blank pages.

Record each defect with page number before changing files.

- [ ] **Step 3: Render representative pages at 150 dpi**

Render the cover, contents, each part divider, one dense script page, every diagram page, and the final checklist. Use `-f N -l N` for each selected page and store them under `build/rendered-high/cna-party-book/`.

Expected: body text is readable, lime accents have adequate contrast, and no content approaches the trim edge.

- [ ] **Step 4: Fix root causes and rebuild after each meaningful batch**

Use these rules:

- fix content overflow by shortening repetition before shrinking type;
- fix repeated layout issues in `theme.typ`, not chapter-by-chapter;
- fix a single diagram in `diagrams.typ` without changing unrelated diagrams;
- keep body text at or above 9.8pt;
- keep callout text at or above 8.8pt;
- do not exceed 45 pages or fall below 35 pages.

After each batch run:

```powershell
python scripts/project.py build cna-party-book
python scripts/project.py verify cna-party-book
```

- [ ] **Step 5: Rerender all pages after the final fix**

Render into a new ignored directory `build/rendered-final/cna-party-book/` rather than relying on stale PNGs. Confirm exact page-count parity and inspect all final contact sheets again.

- [ ] **Step 6: Commit the visually verified release**

```powershell
git add projects/cna-party-edition dist/pdf/CNA_파티의_주도권.pdf
git commit -m "fix: polish CNA party book layout"
```

If no tracked file changed during QA, do not create an empty commit.

---

### Task 11: Update publishing documentation and run the full release gate

**Files:**
- Modify: `README.md`
- Modify: `docs/ARTIFACT_INVENTORY.md`
- Modify: `docs/PROJECT_STRUCTURE.md`
- Verify: `dist/pdf/*.pdf`

- [ ] **Step 1: Run the complete test suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all existing and new tests pass with zero failures or errors.

- [ ] **Step 2: Rebuild and verify the new PDF**

Run:

```powershell
python scripts/project.py build cna-party-book
python scripts/project.py verify all
```

Expected: the new build succeeds, followed by five `verified` lines for `cna-night`, `cna-party-book`, `katalk-basic`, `katalk-advanced`, and `katalk-summary`. Existing Noto Serif KR variable-font warnings may remain, but no Typst errors are allowed.

- [ ] **Step 3: Capture final metadata**

Run:

```powershell
python -c "from pathlib import Path; from hashlib import sha256; from pypdf import PdfReader; p=Path('dist/pdf/CNA_파티의_주도권.pdf'); print(p.name, len(PdfReader(str(p)).pages), p.stat().st_size, sha256(p.read_bytes()).hexdigest(), sep='\t')"
```

Use the printed page count, byte size, and lowercase SHA-256 exactly in the inventory.

- [ ] **Step 4: Add the deliverable to the root README**

Add this row to the `정식 PDF 산출물` table in `README.md`:

```markdown
| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` | `projects/cna-party-edition/typst/book.typ` |
```

Add one sentence below the table stating that the book covers party preparation through first conversation and number exchange.

- [ ] **Step 5: Update the artifact inventory**

In `docs/ARTIFACT_INVENTORY.md`:

- add `cna-party-book` to the formal PDF table using Step 3 metadata;
- state that `references/pdf/[CNA] Party Edition.pdf` is the local 44-page 16:9 source deck;
- record `projects/cna-party-edition/manuscript/` as the content source of truth;
- retain the existing Git tracking policy for `references/pdf/` and `build/`.

- [ ] **Step 6: Update the project structure guide**

In `docs/PROJECT_STRUCTURE.md`, add a `CNA Party Edition` subsection with:

```markdown
### CNA Party Edition

| 역할 | 경로 |
|---|---|
| 빌드 엔트리 | `projects/cna-party-edition/typst/book.typ` |
| 테마 | `projects/cna-party-edition/typst/theme.typ` |
| 도식·토큰 렌더러 | `projects/cna-party-edition/typst/diagrams.typ` |
| 원고 정본 | `projects/cna-party-edition/manuscript/` |

강의 슬라이드는 참고자료이며, 독립 교재의 콘텐츠 정본은 장별 Markdown 원고다.
```

- [ ] **Step 7: Re-run tests after documentation edits**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all existing and new tests pass with zero failures or errors, including the committed final PDF page-budget test.

- [ ] **Step 8: Verify every registered PDF once more**

Run:

```powershell
python scripts/project.py verify all
```

Expected: five `verified` lines, including `cna-party-book` at 35~45 pages.

- [ ] **Step 9: Check repository boundaries and diff quality**

Run:

```powershell
git check-ignore -v 'references/pdf/[CNA] Party Edition.pdf' 'build/rendered-final/cna-party-book/page-01.png'
git ls-files | Select-String -Pattern 'references/pdf|^build/|^local/'
git diff --check
git status --short
```

Expected: the source and render PNG are ignored; `git ls-files` prints no sensitive/reference/build paths; `git diff --check` reports no text-file errors.

- [ ] **Step 10: Commit release documentation**

```powershell
git add README.md docs/ARTIFACT_INVENTORY.md docs/PROJECT_STRUCTURE.md dist/pdf/CNA_파티의_주도권.pdf
git commit -m "docs: add CNA party book release"
```

- [ ] **Step 11: Perform the final completion verification**

Apply `verification-before-completion`: rerun the complete tests and `python scripts/project.py verify all`, read the full output, confirm a clean working tree, and only then report the book as complete.
