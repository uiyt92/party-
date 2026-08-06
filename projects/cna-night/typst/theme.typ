// =============================================================
//  ROAD TO MOTEL — 전용 강력 테마 (Bold / Edgy)
//  다크 표지·파트, 헤비 헤드라인(Montserrat 900 / Pretendard 900),
//  강한 레드 액센트. 본문은 가독성 위해 라이트 + 넉넉한 간격 유지.
//  헤드라인: Montserrat(라틴) / Pretendard Black(한글)
//  본문: Pretendard
// =============================================================

// ---- 컬러 토큰 (강한 레드 계열) ----
#let rtm-red     = rgb("#E11D2A")   // 시그니처 레드
#let rtm-red-dk  = rgb("#8E0F18")   // 딥 레드
#let rtm-ink     = rgb("#17171A")   // 본문 잉크
#let rtm-dark    = rgb("#0E0E12")   // 다크 페이지 배경
#let rtm-muted   = rgb("#8A8A93")   // 보조 텍스트
#let rtm-line    = rgb("#E4E4E8")   // 구분선
#let rtm-tint    = rgb("#FBF2F2")   // 핵심 박스 배경(연한 레드)
#let rtm-tint2   = rgb("#F4F4F6")   // 대화/보조 박스 배경
#let rtm-psych   = rgb("#7c3aed")   // 심리 보라(유지)

// ---- 본문 래퍼 ----
#let book(title: "", subtitle: "", author: "", body) = {
  set document(title: title, author: author)
  set text(font: "Pretendard", size: 10.5pt, fill: rtm-ink, lang: "ko")
  set par(justify: true, leading: 1.5em, spacing: 1.95em)

  // ===== 표지 (다크 풀블리드) =====
  set page(paper: "a5", margin: 0pt, fill: rtm-dark)
  page(numbering: none)[
    #set text(fill: white)
    #place(top + left, dx: 2.2cm, dy: 2.2cm)[
      #box(fill: rtm-red, inset: (x: 9pt, y: 5pt), radius: 3pt)[
        #text(font: "Pretendard", size: 9pt, weight: 800, fill: white, tracking: 2pt)[R-19 · ADULT]
      ]
    ]
    #v(1fr)
    #block(inset: (x: 2.2cm))[
      #text(font: "Pretendard", size: 48pt, weight: 900, fill: white, tracking: -1pt)[CNA]
      #v(-10pt)
      #text(font: "Pretendard", size: 48pt, weight: 900, fill: rtm-red, tracking: -1pt)[NIGHT]
      #v(16pt)
      #line(length: 30%, stroke: 3pt + rtm-red)
      #v(16pt)
      #text(font: "Pretendard", size: 12pt, weight: 600, fill: rgb("#D8D8DE"))[#subtitle]
    ]
    #v(1fr)
    #block(inset: (x: 2.2cm))[
      #text(size: 9pt, fill: rtm-muted, font: "Pretendard")[#author]
    ]
    #v(2.2cm)
  ]

  // ===== 목차 (라이트) =====
  set page(paper: "a5", margin: (x: 2.2cm, y: 2.4cm), fill: white)
  page(numbering: none)[
    #text(font: "Pretendard", size: 12pt, weight: 800, fill: rtm-red, tracking: 3pt)[CONTENTS]
    #v(4pt)
    #text(font: "Pretendard", size: 22pt, weight: 900, fill: rtm-ink)[목차]
    #v(6pt)
    #line(length: 44pt, stroke: 3pt + rtm-red)
    #v(24pt)
    #show outline.entry: it => {
      set text(size: 11pt, fill: rtm-ink, weight: 500)
      v(10pt)
      it
    }
    #outline(title: none, depth: 1)
  ]

  // ===== 본문 페이지 (라이트, 가독성 우선) =====
  set page(
    paper: "a5",
    margin: (x: 2.0cm, top: 2.3cm, bottom: 1.9cm),
    fill: white,
    numbering: "1",
    number-align: center,
    footer-descent: 1.0em,
    footer: context {
      let n = counter(page).at(here()).first()
      align(center, text(size: 8.5pt, fill: rtm-muted, font: "Pretendard", weight: 600)[#n])
    },
  )

  // 섹션 제목 (h1) — 헤비 블랙 + 두꺼운 레드 바
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    block(above: 0em, below: 1.7em)[
      #box(fill: rtm-red, width: 34pt, height: 7pt, radius: 1.5pt)
      #v(12pt)
      #text(font: "Pretendard", size: 24pt, weight: 900, fill: rtm-ink)[#it.body]
    ]
  }
  // 소제목 (h2) — 헤비 + 레드 틱
  show heading.where(level: 2): it => block(above: 2.0em, below: 1.0em)[
    #text(font: "Pretendard", size: 13.5pt, weight: 800, fill: rtm-red-dk)[▍ ] #text(font: "Pretendard", size: 13.5pt, weight: 800, fill: rtm-ink)[#it.body]
  ]

  // 인용 박스 (핵심/왜통할까/대화 등) — 레드 좌측 바 카드
  show quote.where(block: true): it => block(
    width: 100%,
    fill: rtm-tint,
    inset: (x: 15pt, y: 12pt),
    radius: 6pt,
    stroke: (left: 3pt + rtm-red),
    above: 1.4em,
    below: 1.4em,
  )[#it.body]

  // 표 (판별표 등) — 레드 헤더
  show table.cell.where(y: 0): set text(fill: white, weight: 700, size: 9.5pt)
  set table(
    stroke: (x: none, y: 0.6pt + rtm-line),
    inset: (x: 8pt, y: 7pt),
    fill: (_, y) => if y == 0 { rtm-red-dk } else { none },
  )

  set text(hyphenate: false)
  body
}

// ---- 파트 구분 (다크 풀블리드, 강력) ----
#let part-divider(label, title) = {
  pagebreak(weak: true)
  set page(paper: "a5", margin: 0pt, fill: rtm-dark, numbering: none, footer: none)
  page[
    #set text(fill: white)
    #place(top + left, dx: 2.2cm, dy: 2.4cm)[
      #line(length: 34pt, stroke: 3pt + rtm-red)
    ]
    #v(1fr)
    #block(inset: (x: 2.2cm))[
      #box(fill: rtm-red, inset: (x: 12pt, y: 6pt), radius: 3pt)[
        #text(font: "Pretendard", size: 11pt, weight: 900, fill: white, tracking: 3pt)[#upper(label)]
      ]
      #v(18pt)
      #text(font: "Pretendard", size: 23pt, weight: 900, fill: white)[#title]
    ]
    #v(1fr)
  ]
}
