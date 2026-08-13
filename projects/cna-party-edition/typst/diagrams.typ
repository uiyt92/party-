// CNA Party Edition diagrams and rich Markdown token renderer.

#import "@preview/cmarker:0.1.6"
#import "theme.typ": lime, lime-dark, navy, ink, muted, line, better, blue-soft, field-note, bad-move, better-move, frame-card, mission-card

#let diagram-frame(title, body) = block(
  width: 100%,
  breakable: false,
  fill: white,
  stroke: 1pt + line,
  radius: 8pt,
  inset: (x: 13pt, y: 12pt),
  above: 1.4em,
  below: 1.4em,
)[
  #text(size: 8.5pt, weight: 800, fill: lime-dark, tracking: 1pt)[#upper(title)]
  #v(10pt)
  #body
]

#let step(number, label, note) = grid(
  columns: (22pt, 1fr),
  gutter: 8pt,
  align: (center + horizon, left + horizon),
  box(
    width: 20pt,
    height: 20pt,
    radius: 4pt,
    fill: navy,
    align(center + horizon, text(size: 8pt, weight: 800, fill: lime)[#number]),
  ),
  box(width: 100%, fill: blue-soft, radius: 5pt, inset: (x: 9pt, y: 7pt))[
    #text(size: 9pt, weight: 800, fill: navy)[#label]
    #h(5pt)
    #text(size: 8pt, fill: muted)[#note]
  ],
)

#let party-map = diagram-frame("GROUP FLOW")[
  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 7pt,
    box(width: 100%, fill: blue-soft, radius: 6pt, inset: 9pt, stroke: (top: 3pt + navy))[
      #text(size: 9pt, weight: 800, fill: navy)[현재 조]
      #v(4pt)
      #text(size: 7.8pt, fill: muted)[말의 분배 · 참여 정도]
    ],
    box(width: 100%, fill: blue-soft, radius: 6pt, inset: 9pt, stroke: (top: 3pt + better))[
      #text(size: 9pt, weight: 800, fill: navy)[다음 전환]
      #v(4pt)
      #text(size: 7.8pt, fill: muted)[교체 방향 · 새 조 구성]
    ],
    box(width: 100%, fill: blue-soft, radius: 6pt, inset: 9pt, stroke: (top: 3pt + lime-dark))[
      #text(size: 9pt, weight: 800, fill: navy)[열린 접점]
      #v(4pt)
      #text(size: 7.8pt, fill: muted)[게임 직후 · 쉬는 시간]
    ],
  )
]

#let positioning-loop = diagram-frame("POSITIONING LOOP")[
  #stack(
    dir: ttb,
    spacing: 6pt,
    step("1", "관찰", "현재 조의 말과 참여를 읽는다"),
    step("2", "기여", "필요한 연결과 편안함을 보탠다"),
    step("3", "반응", "조원들의 실제 반응을 확인한다"),
    step("4", "전환", "자리 교체와 게임 종료를 받아들인다"),
  )
]

#let rapport-ladder = diagram-frame("RAPPORT LADDER")[
  #stack(
    dir: ttb,
    spacing: 6pt,
    align(center, box(width: 58%, fill: blue-soft, radius: 5pt, inset: 7pt)[
      #align(center, text(size: 8.6pt, weight: 750, fill: navy)[현재 사실])
    ]),
    align(center, box(width: 70%, fill: blue-soft, radius: 5pt, inset: 7pt)[
      #align(center, text(size: 8.6pt, weight: 750, fill: navy)[선호])
    ]),
    align(center, box(width: 84%, fill: blue-soft, radius: 5pt, inset: 7pt)[
      #align(center, text(size: 8.6pt, weight: 750, fill: navy)[감정])
    ]),
    align(center, box(width: 100%, fill: lime, radius: 5pt, inset: 7pt)[
      #align(center, text(size: 8.6pt, weight: 800, fill: navy)[개인 경험])
    ]),
  )
]

#let influence-curve = diagram-frame("INFLUENCE CURVE")[
  #align(center, box(height: 58pt)[
    #align(bottom, stack(
      dir: ltr,
      spacing: 8pt,
      rect(width: 18pt, height: 16pt, fill: navy, radius: (top: 3pt)),
      rect(width: 18pt, height: 25pt, fill: lime, radius: (top: 3pt)),
      rect(width: 18pt, height: 22pt, fill: navy, radius: (top: 3pt)),
      rect(width: 18pt, height: 38pt, fill: lime, radius: (top: 3pt)),
      rect(width: 18pt, height: 34pt, fill: navy, radius: (top: 3pt)),
      rect(width: 18pt, height: 52pt, fill: lime, radius: (top: 3pt)),
    ))
  ])
  #v(6pt)
  #align(center, text(size: 8pt, fill: muted)[강약은 교차하고, 전체 흐름은 상승한다])
]

#let number-window = diagram-frame("NUMBER WINDOW")[
  #grid(
    columns: (1fr, 1fr),
    gutter: 7pt,
    row-gutter: 7pt,
    box(width: 100%, fill: blue-soft, radius: 6pt, inset: 9pt)[
      #text(size: 8.8pt, weight: 800, fill: navy)[상호 투자]
      #v(3pt)
      #text(size: 7.8pt, fill: muted)[서로 질문하고 반응했는가]
    ],
    box(width: 100%, fill: blue-soft, radius: 6pt, inset: 9pt)[
      #text(size: 8.8pt, weight: 800, fill: navy)[공유 맥락]
      #v(3pt)
      #text(size: 7.8pt, fill: muted)[둘만의 이야기 소재가 생겼는가]
    ],
    box(width: 100%, fill: blue-soft, radius: 6pt, inset: 9pt)[
      #text(size: 8.8pt, weight: 800, fill: navy)[다음 이유]
      #v(3pt)
      #text(size: 7.8pt, fill: muted)[다시 연락할 구체적 이유가 있는가]
    ],
    box(width: 100%, fill: lime, radius: 6pt, inset: 9pt)[
      #text(size: 8.8pt, weight: 800, fill: navy)[짧은 요청]
      #v(3pt)
      #text(size: 7.8pt, fill: ink)[설명하지 말고 간단히 제안한다]
    ],
  )
]

#let level-test = diagram-frame("LEVEL TEST")[
  #stack(
    dir: ttb,
    spacing: 5pt,
    step("1", "진입", "대화에 자연스럽게 들어간다"),
    step("2", "대화", "상호 반응을 만든다"),
    step("3", "포지션", "그룹 안의 역할을 잡는다"),
    step("4", "프레임", "분위기의 기준을 제시한다"),
    step("5", "전환", "다음 장면으로 짧게 이동한다"),
  )
]

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

#let render-rich(path) = {
  let raw = read(path)
  let token-pattern = regex("(?m)^[ \t]*\[\[(?:DIAGRAM:[a-z0-9_]+|CALLOUT:[a-z]+\|[^\r\n]*|PAGEBREAK)\]\][ \t]*$")
  let chunks = raw.split(token-pattern)
  let tokens = raw.matches(token-pattern).map(m => m.text.trim())

  for (index, chunk) in chunks.enumerate() {
    cmarker.render(chunk)

    if index < tokens.len() {
      let token = tokens.at(index)

      if token == "[[PAGEBREAK]]" {
        pagebreak(weak: true)
      } else if token.starts-with("[[DIAGRAM:") {
        let key = token.slice(10, token.len() - 2)
        if key in DIAGRAMS {
          DIAGRAMS.at(key)
        } else {
          panic("unknown diagram key: " + key)
        }
      } else {
        let payload = token.slice(10, token.len() - 2)
        let parts = payload.split("|")
        let kind = parts.first()
        let message = parts.slice(1).join("|")

        if kind in CALLOUTS {
          CALLOUTS.at(kind)(message)
        } else {
          panic("unknown callout kind: " + kind)
        }
      }
    }
  }
}
