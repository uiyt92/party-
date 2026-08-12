// CNA Party Edition — bright A5 theme

// Public color tokens
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
#let book(
  title: "",
  subtitle: "",
  series: "",
  author: "",
  body,
) = {
  set document(title: title, author: author)
  set text(
    font: "Pretendard",
    size: 10.2pt,
    fill: ink,
    lang: "ko",
    hyphenate: false,
  )
  set par(justify: true, leading: 1.35em, spacing: 1.55em)

  // Cover
  page(
    paper: "a5",
    margin: (x: 1.85cm, top: 1.7cm, bottom: 1.7cm),
    fill: paper,
    numbering: none,
    header: none,
    footer: none,
  )[
    #align(left)[
      #box(fill: navy, inset: (x: 9pt, y: 5pt), radius: 3pt)[
        #text(size: 8pt, weight: 700, fill: white, tracking: 1.1pt)[#upper(series)]
      ]
    ]
    #v(1fr)
    #text(size: 31pt, weight: 900, fill: navy, tracking: -0.7pt)[#title]
    #v(14pt)
    #rect(width: 72pt, height: 4pt, fill: lime)
    #v(14pt)
    #text(size: 11.2pt, weight: 500, fill: muted)[#subtitle]
    #v(1fr)
    #text(size: 9pt, weight: 700, fill: navy, tracking: 0.7pt)[#author]
  ]

  // Copyright and usage page
  page(
    paper: "a5",
    margin: (x: 1.85cm, top: 2.05cm, bottom: 1.7cm),
    fill: paper,
    numbering: none,
    header: none,
    footer: none,
  )[
    #v(1fr)
    #text(size: 16pt, weight: 800, fill: navy)[#title]
    #v(7pt)
    #text(size: 9.2pt, fill: muted)[#subtitle]
    #v(18pt)
    #rect(width: 42pt, height: 3pt, fill: lime)
    #v(18pt)
    #text(size: 9.2pt, weight: 700, fill: navy)[초판 2026년 · #author]
    #v(12pt)
    #text(size: 8.8pt, fill: muted)[
      이 책은 소셜 파티에서의 커뮤니케이션 훈련을 위한 교육 자료입니다.
      상대의 판단력이 흐려진 상태이거나 명시적으로 거절하면 설득을 즉시 멈추십시오.
    ]
    #v(10pt)
    #text(size: 8.4pt, fill: muted)[
      저작권자의 서면 허락 없이 이 책의 일부 또는 전체를 복제·배포·전송할 수 없습니다.
    ]
  ]

  // Contents
  page(
    paper: "a5",
    margin: (x: 1.85cm, top: 2.05cm, bottom: 1.7cm),
    fill: paper,
    numbering: none,
    header: none,
    footer: none,
  )[
    #text(size: 9pt, weight: 800, fill: navy, tracking: 2.4pt)[CONTENTS]
    #v(5pt)
    #text(size: 23pt, weight: 900, fill: navy)[목차]
    #v(8pt)
    #rect(width: 52pt, height: 4pt, fill: lime)
    #v(22pt)
    #show outline.entry: it => {
      set text(size: 9.5pt, weight: 600, fill: ink)
      v(8pt)
      it
    }
    #outline(title: none, depth: 1)
  ]

  // Body pages
  set page(
    paper: "a5",
    margin: (x: 1.85cm, top: 2.05cm, bottom: 1.7cm),
    fill: paper,
    numbering: "1",
    number-align: center,
    header-ascent: 0.7em,
    footer-descent: 0.8em,
    header: context {
      align(right, text(size: 7.8pt, weight: 600, fill: muted)[파티의 주도권])
    },
    footer: context {
      let page-number = counter(page).at(here()).first()
      align(center, text(size: 8.2pt, weight: 600, fill: muted)[#page-number])
    },
  )
  counter(page).update(1)

  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    block(above: 0em, below: 1.6em)[
      #rect(width: 48pt, height: 4pt, fill: lime)
      #v(11pt)
      #text(size: 24pt, weight: 900, fill: navy, tracking: -0.4pt)[#it.body]
    ]
  }
  show heading.where(level: 2): it => block(above: 1.9em, below: 0.85em)[
    #text(size: 14pt, weight: 800, fill: navy)[#it.body]
  ]

  show quote.where(block: true): it => block(
    width: 100%,
    fill: blue-soft,
    inset: (x: 14pt, y: 11pt),
    radius: 5pt,
    stroke: (left: 3pt + navy),
    above: 1.3em,
    below: 1.3em,
  )[#it.body]

  show table.cell.where(y: 0): set text(fill: white, weight: 700, size: 9.2pt)
  set table(
    stroke: (x: none, y: 0.6pt + line),
    inset: (x: 7pt, y: 6pt),
    fill: (_, y) => if y == 0 { navy } else { none },
  )

  body
}

#let part-divider(label, title) = {
  pagebreak(weak: true)
  page(
    paper: "a5",
    margin: 0pt,
    fill: navy,
    numbering: none,
    header: none,
    footer: none,
  )[
    #v(1fr)
    #block(inset: (x: 1.85cm))[
      #text(size: 10pt, weight: 800, fill: lime, tracking: 2.2pt)[#upper(label)]
      #v(16pt)
      #text(size: 24pt, weight: 900, fill: white, tracking: -0.3pt)[#title]
      #v(16pt)
      #rect(width: 52pt, height: 4pt, fill: lime)
    ]
    #v(1fr)
  ]
}

#let field-note(body) = block(
  width: 100%,
  fill: rgb("#F3F9E8"),
  inset: (x: 14pt, y: 11pt),
  radius: 7pt,
  stroke: (left: 4pt + lime-dark),
  above: 1.2em,
  below: 1.2em,
)[
  #text(size: 8.2pt, weight: 800, fill: lime-dark, tracking: 1.4pt)[FIELD NOTE]
  #v(6pt)
  #text(size: 9.2pt, fill: ink)[#body]
]

#let bad-move(body) = block(
  width: 100%,
  fill: bad-soft,
  inset: (x: 14pt, y: 11pt),
  radius: 7pt,
  stroke: (left: 4pt + bad),
  above: 1.2em,
  below: 1.2em,
)[
  #text(size: 8.2pt, weight: 800, fill: bad, tracking: 1.4pt)[BAD MOVE]
  #v(6pt)
  #text(size: 9.2pt, fill: ink)[#body]
]

#let better-move(body) = block(
  width: 100%,
  fill: better-soft,
  inset: (x: 14pt, y: 11pt),
  radius: 7pt,
  stroke: (left: 4pt + better),
  above: 1.2em,
  below: 1.2em,
)[
  #text(size: 8.2pt, weight: 800, fill: better, tracking: 1.4pt)[BETTER MOVE]
  #v(6pt)
  #text(size: 9.2pt, fill: ink)[#body]
]

#let frame-card(body) = block(
  width: 100%,
  fill: blue-soft,
  inset: (x: 14pt, y: 11pt),
  radius: 7pt,
  stroke: (left: 4pt + navy),
  above: 1.2em,
  below: 1.2em,
)[
  #text(size: 8.2pt, weight: 800, fill: navy, tracking: 1.4pt)[FRAME]
  #v(6pt)
  #text(size: 9.2pt, fill: ink)[#body]
]

#let mission-card(body) = block(
  width: 100%,
  fill: rgb("#F3F9E8"),
  inset: (x: 14pt, y: 11pt),
  radius: 7pt,
  stroke: (left: 4pt + lime-dark),
  above: 1.2em,
  below: 1.2em,
)[
  #text(size: 8.2pt, weight: 800, fill: lime-dark, tracking: 1.4pt)[MISSION]
  #v(6pt)
  #text(size: 9.2pt, fill: ink)[#body]
]
