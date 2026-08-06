// =============================================================
//  폰게임 초보 탈출 가이드 — Typst 클린 화이트 템플릿
//  제목: Noto Serif KR (명조) / 본문: Pretendard (고딕)
// =============================================================

// ---- 컬러 토큰 ----
#let accent      = rgb("#2563eb")   // 강조 블루 (CTA, 숫자, 링크)
#let accent-dark = rgb("#1e3a8a")   // 네이비 (소제목)
#let ink         = rgb("#1a1a1a")   // 본문
#let muted       = rgb("#6b7280")   // 보조 텍스트
#let tint        = rgb("#f1f5f9")   // 강조 박스 / 상대 말풍선 배경
#let line-col    = rgb("#e5e7eb")   // 구분선
#let danger      = rgb("#dc2626")   // 경고 (BAD, 묻힘 강조)
#let amber       = rgb("#d97706")   // 분기 (안 읽음/주의)

// ---- 본문 문서 래퍼 ----
#let book(title: "", subtitle: "", author: "", body) = {
  set document(title: title, author: author)
  set text(font: "Pretendard", size: 10.5pt, fill: ink, lang: "ko")
  set par(justify: true, leading: 1.2em, spacing: 1.45em)

  // ===== 표지 =====
  set page(paper: "a5", margin: (x: 2.2cm, y: 2.4cm))
  page(numbering: none)[
    #set par(justify: false, leading: 0.5em)
    #v(1fr)
    #align(center)[
      #text(font: "Noto Serif KR", size: 26pt, weight: 700, fill: ink, tracking: -0.5pt)[#title]
      #v(18pt)
      #line(length: 42%, stroke: 1pt + line-col)
      #v(14pt)
      #text(size: 11pt, fill: muted)[#subtitle]
    ]
    #v(1fr)
    #align(center, text(size: 9pt, fill: muted)[#author])
  ]

  // ===== 목차 =====
  page(numbering: none)[
    #text(font: "Noto Serif KR", size: 20pt, weight: 700, fill: ink)[목차]
    #v(8pt)
    #line(length: 36pt, stroke: 2.5pt + accent)
    #v(20pt)
    #show outline.entry: it => {
      set text(size: 11pt, fill: ink)
      v(6pt)
      it
    }
    #outline(title: none, depth: 1)
  ]

  // ===== 본문 페이지 =====
  set page(
    paper: "a5",
    margin: (x: 2.0cm, top: 2.2cm, bottom: 1.8cm),
    numbering: "— 1 —",
    number-align: center,
    footer-descent: 1.0em,
  )

  // 섹션 제목 (h1) — 큰 번호 느낌의 명조 헤딩
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    block(above: 0em, below: 0.8em)[
      #text(font: "Noto Serif KR", size: 21pt, weight: 800, fill: ink)[#it.body]
      #v(5pt)
      #line(length: 36pt, stroke: 2.5pt + accent)
    ]
  }
  // 소제목 (h2) — 네이비 고딕
  show heading.where(level: 2): it => block(above: 1.3em, below: 0.5em)[
    #text(font: "Pretendard", size: 13pt, weight: 700, fill: accent-dark)[#it.body]
  ]
  // 강조 인용
  set text(hyphenate: false)
  body
}

// ---- 파트 구분 페이지 ----
#let part-divider(label, title) = {
  pagebreak(weak: true)
  page(numbering: none)[
    #v(1fr)
    #align(center)[
      #block(fill: accent, inset: (x: 14pt, y: 6pt), radius: 4pt)[
        #text(size: 11pt, weight: 700, fill: white, tracking: 2pt)[#label]
      ]
      #v(16pt)
      #text(font: "Noto Serif KR", size: 26pt, weight: 800, fill: ink)[#title]
    ]
    #v(1fr)
  ]
}

// ---- 강조 박스 (핵심 메시지) ----
#let callout(body) = block(
  width: 100%,
  breakable: false,
  fill: tint,
  inset: (x: 16pt, y: 12pt),
  radius: 8pt,
  stroke: (left: 3pt + accent),
  above: 0.9em,
  below: 0.9em,
  body,
)

// ---- 심리 근거 박스 ----
#let psych = rgb("#7c3aed")
#let psych-box(body) = block(
  width: 100%,
  breakable: false,
  fill: rgb("#f5f3ff"),
  inset: (x: 14pt, y: 12pt),
  radius: 8pt,
  stroke: (left: 3pt + psych),
  above: 0.9em,
  below: 0.9em,
)[
  #text(size: 9pt, weight: 700, fill: psych)[💡 왜 통할까]
  #v(4pt)
  #body
]

// ---- 카톡 말풍선 ----
// 위치: her=왼쪽(흰색) / me=오른쪽(카톡 옐로우). 단, 말풍선 안 텍스트는 둘 다 왼쪽 정렬.
#let kakao-yellow = rgb("#fee500")
#let bubble(msg, mine: false) = {
  let bg = if mine { kakao-yellow } else { white }
  let fg = ink
  let bdr = if mine { none } else { 0.5pt + rgb("#d5dde5") }
  let b = box(
    fill: bg,
    stroke: bdr,
    inset: (x: 13pt, y: 9pt),
    radius: 14pt,
    {
      set par(justify: false)
      text(size: 10pt, fill: fg)[#msg]
    },
  )
  // me는 h(1fr)로 오른쪽 끝까지 밀어 붙인다 (텍스트는 박스 안에서 좌측 정렬 유지)
  block(below: 6pt, width: 100%, breakable: false, if mine { [#h(1fr)#b] } else { b })
}
#let her(msg) = bubble(msg, mine: false)
#let me(msg)  = bubble(msg, mine: true)

// 대화 컨테이너 (카톡 대화방 톤)
#let chat(label: none, body) = block(
  width: 100%,
  fill: rgb("#dce6f0"),
  stroke: 1pt + rgb("#c3d2e0"),
  radius: 12pt,
  inset: (x: 14pt, y: 12pt),
  above: 0.9em,
  below: 0.9em,
)[
  #if label != none [
    #text(size: 8.5pt, weight: 700, fill: muted)[#label]
    #v(8pt)
  ]
  #body
]

// ---- 체크리스트 항목 ----
#let check(item) = grid(
  columns: (16pt, 1fr),
  gutter: 8pt,
  align: (horizon, horizon),
  box(width: 13pt, height: 13pt, radius: 3pt, stroke: 1.5pt + accent),
  text(size: 10pt)[#item],
)

// ---- 카톡함 플러드 도식 (똑같은 첫 톡이 묻히는 모습) ----
#let inbox-flood(title: "○○님의 카톡함", rows: ()) = block(
  width: 100%,
  breakable: false,
  fill: tint,
  stroke: 1pt + line-col,
  radius: 12pt,
  inset: 12pt,
  above: 0.8em,
  below: 0.8em,
)[
  #text(size: 8.5pt, weight: 700, fill: muted)[#title]
  #v(10pt)
  #for r in rows {
    grid(
      columns: (50pt, 1fr),
      gutter: 8pt,
      align: (left + horizon, left + horizon),
      text(size: 8.5pt, weight: if r.mine { 700 } else { 400 }, fill: if r.mine { danger } else { muted })[#r.sender],
      block(
        fill: white,
        stroke: (1pt + if r.mine { danger } else { line-col }),
        radius: 8pt,
        inset: (x: 10pt, y: 6pt),
      )[
        #text(size: 9pt, fill: ink)[#r.msg]
        #if r.mine [ #text(size: 8pt, fill: danger)[  ← 똑같다]]
      ],
    )
    v(5pt)
  }
]

// ---- BAD / GOOD 비교 카드 (좌우) ----
#let vs(bad: [], good: []) = block(breakable: false, grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  block(width: 100%, fill: rgb("#fef2f2"), stroke: (left: 3pt + danger), radius: 8pt, inset: 12pt)[
    #text(size: 8.5pt, weight: 700, fill: danger)[BAD] #v(6pt) #bad
  ],
  block(width: 100%, fill: rgb("#eff6ff"), stroke: (left: 3pt + accent), radius: 8pt, inset: 12pt)[
    #text(size: 8.5pt, weight: 700, fill: accent)[GOOD] #v(6pt) #good
  ],
))

// ---- 단계 흐름 다이어그램 (가로) ----
#let stage(label) = box(
  fill: tint,
  inset: (x: 9pt, y: 11pt),
  radius: 8pt,
  align(center, text(size: 8pt, weight: 600, fill: accent-dark)[#label]),
)
#let arrow = text(size: 11pt, fill: accent, weight: 700)[ → ]
#let flow(..steps) = {
  let items = steps.pos()
  let row = ()
  for (i, s) in items.enumerate() {
    row.push(stage(s))
    if i < items.len() - 1 { row.push(arrow) }
  }
  align(center, block(breakable: false, above: 1em, below: 1em, stack(dir: ltr, spacing: 2pt, ..row)))
}

// ---- 로드맵 (여러 단계 그룹: 1부/2부) ----
#let roadmap(phases) = block(
  width: 100%,
  breakable: false,
  fill: tint,
  radius: 12pt,
  inset: (x: 12pt, y: 14pt),
  above: 1.0em,
  below: 1.0em,
)[
  #for ph in phases {
    block(above: 0.6em, below: 0.2em)[
      #text(size: 9.5pt, weight: 700, fill: accent)[#ph.label]
    ]
    flow(..ph.steps)
  }
]

// ---- 단계형 세로 흐름 (악순환·갈림길 등) ----
#let steps-vert(..items) = {
  let list = items.pos()
  block(breakable: false, above: 0.8em, below: 0.8em, stack(dir: ttb, spacing: 6pt,
    ..list.map(s => box(
      width: 100%,
      fill: white,
      stroke: 1pt + line-col,
      radius: 8pt,
      inset: (x: 12pt, y: 8pt),
      text(size: 9.5pt, fill: ink)[#s],
    ))
  ))
}

// ---- 전체 흐름 여정 맵 (세로 + 3갈래 분기) ----
#let _jbox(label, fill: tint, fg: ink, strk: true) = box(
  fill: fill, inset: (x: 14pt, y: 8pt), radius: 8pt,
  stroke: if strk { 1pt + line-col } else { none },
  text(size: 10.5pt, weight: 700, fill: fg)[#label],
)
#let _jdown = text(size: 13pt, fill: accent, weight: 700)[↓]
#let _jbranch(name, action, col) = stack(dir: ttb, spacing: 5pt,
  box(width: 100%, fill: rgb("f8fafc"), stroke: 1pt + col, radius: 8pt, inset: (x: 7pt, y: 8pt),
    align(center, text(size: 9pt, weight: 700, fill: col)[#name])),
  align(center, text(size: 10pt, fill: muted)[↓]),
  align(center, text(size: 8.5pt, fill: muted)[#action]),
)
#let journey = align(center, block(breakable: false, above: 1em, below: 1em, stack(dir: ttb, spacing: 7pt,
  _jbox("번호 받음"),
  _jdown,
  _jbox("첫 톡 보냄"),
  _jdown,
  grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,
    _jbranch("답장 옴", "바로 대화", accent),
    _jbranch("안 읽음 (잠수)", "며칠 뒤 다시", amber),
    _jbranch("읽씹", "새 화제로", danger),
  ),
  _jdown,
  _jbox("대화 운영", fill: accent-dark, fg: white, strk: false),
  _jdown,
  _jbox("만남", fill: accent, fg: white, strk: false),
)))

// ---- 읽씹 3분류 분기 ----
#let read-branch = align(center, block(breakable: false, above: 0.9em, below: 0.9em,
  grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,
    _jbranch("처음부터 읽씹", "며칠 뒤 처음처럼", danger),
    _jbranch("연락 중 끊김", "새 얘기로 리셋", amber),
    _jbranch("자주 씹힘", "만남으로 전환", accent),
  )))
