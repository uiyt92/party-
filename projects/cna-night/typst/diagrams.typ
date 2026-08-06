// =============================================================
//  ROAD TO MOTEL — 도식 모듈
//  각 도식은 순수 Typst(박스/그리드/스택)로 그린 스키매틱. RTM 레드 테마.
//  본문 마크다운의 [[DIAGRAM:key]] 토큰 위치에 render-with-diagrams가 삽입.
// =============================================================

#import "theme.typ": rtm-red, rtm-red-dk, rtm-ink, rtm-muted, rtm-line, rtm-tint
#import "@preview/cmarker:0.1.6"

#let d-green = rgb("#16A34A")
#let d-amber = rgb("#D97706")
#let d-gray  = rgb("#9AA0A6")
#let d-soft  = rgb("#F3F4F6")
#let d-soft2 = rgb("#C9CDD3")

// ---- 공통 프리미티브 ----
#let dframe(body) = block(
  width: 100%, breakable: false, fill: white, stroke: 1pt + rtm-line,
  radius: 10pt, inset: (x: 14pt, y: 14pt), above: 1.6em, below: 1.6em, body,
)
#let dtitle(t) = block(below: 11pt)[#text(size: 8.5pt, weight: 800, fill: rtm-red, tracking: 1pt)[#t]]
#let arrow-d = align(center, block(above: 4pt, below: 4pt, text(size: 12pt, fill: rtm-red, weight: 700)[↓]))
#let pill(t, col) = box(fill: col, inset: (x: 11pt, y: 6pt), radius: 20pt, text(size: 9pt, weight: 700, fill: white)[#t])
#let tag(t, col) = box(fill: col, inset: (x: 8pt, y: 4pt), radius: 4pt, text(size: 8pt, weight: 700, fill: white)[#t])
#let propbar(a, acol, b, bcol) = box(width: 100%, radius: 4pt, clip: true, stack(dir: ltr,
  rect(width: a, height: 13pt, fill: acol), rect(width: b, height: 13pt, fill: bcol)))

// ---- 1. 데이 게임 vs 나이트 게임 ----
#let d-pickup-split = dframe[
  #dtitle("데이 게임 vs 나이트 게임")
  #align(center)[#pill("같은 상대, 두 갈래", rtm-ink)]
  #arrow-d
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    box(width: 100%, fill: d-soft, radius: 8pt, inset: 10pt, stroke: (top: 2.5pt + d-gray))[
      #text(weight: 800, size: 10pt, fill: d-gray)[데이 게임 · 낮] #v(6pt)
      #text(size: 8.5pt)[목표 · 계속 만나고 싶게\ 방식 · 천천히 신뢰·호감\ 결과 · 다음 약속]
    ],
    box(width: 100%, fill: rtm-tint, radius: 8pt, inset: 10pt, stroke: (top: 2.5pt + rtm-red))[
      #text(weight: 800, size: 10pt, fill: rtm-red-dk)[나이트 게임 · 밤] #v(6pt)
      #text(size: 8.5pt)[목표 · 그 밤에 끌리게\ 방식 · 텐션·감정·몸\ 결과 · 그날 관계]
    ],
  )
]

// ---- 1b. 데이 게임 vs 나이트 게임 — 플로우 비교 ----
#let dnfnode(t, sub, bg, fg, subfg) = box(fill: bg, radius: 6pt, inset: (x: 9pt, y: 6pt),
  stack(dir: ttb, spacing: 2pt,
    text(size: 8.5pt, weight: 700, fill: fg)[#t],
    text(size: 7pt, fill: subfg)[#sub]))
#let dnfarr(col) = box(inset: (x: 5pt), text(size: 12pt, weight: 800, fill: col)[→])
#let dnfrow(label, lblcol, a, b, c, bg, fg, subfg, arrcol) = grid(
  columns: (54pt, 1fr), gutter: 8pt, align: (left + horizon, left + horizon),
  text(size: 9.5pt, weight: 800, fill: lblcol)[#label],
  grid(columns: (auto, auto, auto, auto, auto), align: horizon,
    dnfnode(a.at(0), a.at(1), bg, fg, subfg), dnfarr(arrcol),
    dnfnode(b.at(0), b.at(1), bg, fg, subfg), dnfarr(arrcol),
    dnfnode(c.at(0), c.at(1), bg, fg, subfg)))
#let d-day-night-flow = dframe[
  #dtitle("데이 게임 vs 나이트 게임 — 같은 끝, 다른 길")
  #stack(dir: ttb, spacing: 11pt,
    dnfrow("데이", d-gray,
      ("번호 따기", "로드·소개팅앱"), ("애프터 2~3번", "여러 날에 걸쳐"), ("잠자리", "최종 목표"),
      d-soft, rtm-ink, rtm-muted, d-gray),
    dnfrow("나이트", rtm-red-dk,
      ("클럽·나이트", "즉석 만남"), ("압축된 대화", "그 밤 안에"), ("잠자리", "최종 목표"),
      rtm-tint, rtm-red-dk, rtm-muted, rtm-red),
  )
  #v(9pt)
  #box(width: 100%, fill: rtm-ink, radius: 6pt, inset: (x: 10pt, y: 9pt),
    align(center, text(size: 9pt, weight: 800, fill: white)[기본 플로우는 같지만 방식이 전혀 다르다 — 낮은 여러 날, 밤은 하루에 압축]))
]

// ---- 1c. 페르소나 → 바이브 (가면 전환) ----
#let pvmask(col, label) = box(width: 56pt, stack(dir: ttb, spacing: 4pt,
  align(center, box(width: 36pt, height: 36pt,
    place(center + horizon, circle(radius: 17pt, fill: col))
      + place(center + horizon, dy: -2pt, stack(dir: ltr, spacing: 6pt,
          circle(radius: 2.2pt, fill: white), circle(radius: 2.2pt, fill: white))))),
  align(center, text(size: 8pt, weight: 700, fill: rtm-ink)[#label])))
#let pvswap = box(inset: (x: 1pt), text(size: 13pt, weight: 800, fill: rtm-muted)[↔])
#let d-persona-vibe = dframe[
  #dtitle("페르소나 — 가면을 바꿔 쓴다")
  #align(center, grid(columns: (auto, auto, auto, auto, auto), align: horizon, column-gutter: 3pt,
    pvmask(d-amber, "가벼움"), pvswap,
    pvmask(d-gray, "보통"), pvswap,
    pvmask(rtm-red, "진중함")))
  #arrow-d
  #box(width: 100%, fill: rtm-ink, radius: 6pt, inset: (x: 10pt, y: 10pt),
    align(center, text(size: 9.5pt, weight: 800, fill: white)[바이브 — 가면의 전환이 만든다]))
]

// ---- 2. 텐션 곡선 ----
#let bar(h, col) = rect(width: 15pt, height: h, fill: col, radius: (top: 2pt))
#let d-tension-curve = dframe[
  #dtitle("텐션은 올렸다 낮췄다")
  #align(center, box(height: 56pt, align(bottom, stack(dir: ltr, spacing: 9pt,
    bar(15pt, d-soft), bar(30pt, rtm-red), bar(13pt, d-soft),
    bar(41pt, rtm-red), bar(19pt, d-soft), bar(53pt, rtm-red),
  ))))
  #v(6pt)
  #align(center, text(size: 8.5pt, fill: rtm-muted)[낮춤·올림을 반복하며 전체 우상향 →])
]

// ---- 3. 좌뇌 vs 우뇌 ----
#let d-brain-model = dframe[
  #dtitle("좌뇌 vs 우뇌 대화")
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    box(width: 100%, fill: d-soft, radius: 8pt, inset: 10pt)[
      #tag("좌뇌 · 맥 끊김", d-gray) #v(7pt)
      #text(size: 9pt)["작년보단 덜 추운데?"] #v(4pt)
      #text(size: 8pt, fill: rtm-muted)[사실 정정 → 대화 끊김]
    ],
    box(width: 100%, fill: rtm-tint, radius: 8pt, inset: 10pt)[
      #tag("우뇌 · 이어짐", rtm-red) #v(7pt)
      #text(size: 9pt)["맞아 패딩 하나 사야겠어 ㅋㅋ"] #v(4pt)
      #text(size: 8pt, fill: rtm-red-dk)[감정 올라탐 → 분위기 산다]
    ],
  )
]

// ---- 4. 거울 효과 ----
#let mrow(m, w, col, dim) = grid(columns: (1fr, 26pt, 1fr),
  align: (center + horizon, center + horizon, center + horizon),
  box(width: 100%, fill: dim, radius: 8pt, inset: (x: 8pt, y: 10pt), text(size: 9pt, weight: 700, fill: col)[#m]),
  text(size: 13pt, fill: rtm-muted)[⇄],
  box(width: 100%, fill: dim, radius: 8pt, inset: (x: 8pt, y: 10pt), text(size: 9pt, weight: 700, fill: col)[#w]),
)
#let d-mirror-mask = dframe[
  #dtitle("거울 효과")
  #grid(columns: (1fr, 26pt, 1fr), align: (center, center, center),
    text(size: 8pt, fill: rtm-muted)[내 가면], [], text(size: 8pt, fill: rtm-muted)[상대 가면])
  #v(4pt)
  #stack(dir: ttb, spacing: 8pt,
    mrow("착한·바른", "단정·방어", d-gray, d-soft),
    mrow("솔직·야함", "개방·편안", rtm-red-dk, rtm-tint),
  )
  #v(6pt)
  #align(center, text(size: 8.5pt, fill: rtm-muted)[상대는 내가 쓴 가면을 따라 쓴다])
]

// ---- 5. 레벨업 곡선 ----
#let d-level-curve = dframe[
  #dtitle("레벨업 — 경험치가 쌓이면")
  #stack(dir: ttb, spacing: 10pt,
    grid(columns: (40pt, 1fr, 18pt), gutter: 8pt, align: (left + horizon, horizon, center + horizon),
      text(size: 9pt, weight: 700)[긴장], propbar(35%, d-gray, 65%, d-soft), text(size: 11pt, fill: d-gray)[↓]),
    grid(columns: (40pt, 1fr, 18pt), gutter: 8pt, align: (left + horizon, horizon, center + horizon),
      text(size: 9pt, weight: 700)[여유], propbar(82%, rtm-red, 18%, d-soft), text(size: 11pt, fill: rtm-red)[↑]),
  )
  #v(6pt)
  #align(center, text(size: 8.5pt, fill: rtm-muted)[경험치(애프터 횟수)가 쌓일수록 · 여유 = 매력])
]

// ---- 6. 실전 타임라인 ----
#let stepline(n, t, goal) = grid(columns: (20pt, 1fr), gutter: 9pt, align: (center + horizon, horizon),
  box(width: 18pt, height: 18pt, radius: 9pt, fill: rtm-red, align(center + horizon, text(size: 8pt, weight: 800, fill: white)[#n])),
  box(width: 100%, fill: d-soft, radius: 6pt, inset: (x: 10pt, y: 7pt))[#text(size: 9pt, weight: 700)[#t]#h(6pt)#text(size: 8pt, fill: rtm-muted)[· #goal]])
#let d-timeline-funnel = dframe[
  #dtitle("오늘의 전체 지도")
  #stack(dir: ttb, spacing: 5pt,
    stepline("1", "만남", "텐션 넣고 반겨주기"),
    stepline("2", "술집 이동", "상황 유리하게 해석"),
    stepline("3", "자리·초반 대화", "무난하게 풀기"),
    stepline("4", "감정·스토리", "슬픈 얘기·성적개방화"),
    stepline("5", "키스", "신호 초록불일 때"),
    stepline("6", "장소 이동", "합의 신호 확인"),
    stepline("7", "관계", "원할 때만 진행"),
  )
]

// ---- 6b. 전략적 질문 → 정보 ----
#let rqrow(q, info) = grid(columns: (1fr, 12pt, 1.1fr), gutter: 6pt, align: (left + horizon, center + horizon, left + horizon),
  box(width: 100%, fill: rtm-tint, radius: 6pt, inset: (x: 9pt, y: 7pt),
    text(size: 8.5pt, weight: 700, fill: rtm-red-dk)[#q]),
  text(size: 11pt, weight: 800, fill: rtm-red)[→],
  box(width: 100%, fill: d-soft, radius: 6pt, inset: (x: 9pt, y: 7pt),
    text(size: 8.5pt, fill: rtm-ink)[#info]))
#let d-recon-questions = dframe[
  #dtitle("전략적 질문 → 캐내는 정보")
  #stack(dir: ttb, spacing: 6pt,
    rqrow("친구랑 왔어?", "혼자냐 · 무리냐"),
    rqrow("어떤 사이야?", "누가 키맨인가 · 내 편 만들 사람"),
    rqrow("술 얼마나 마셨어?", "컨디션 확인 (취하면 다음에)"),
    rqrow("어디 살아?", "오늘 여유 있나"),
    rqrow("언제 가야 돼?", "남은 시간 · 급하면 다음에"),
  )
]

// ---- 7. IOI × FAKE IOI ----
#let quad(t, sub, col, hi) = box(width: 100%, height: 46pt, fill: if hi { rtm-tint } else { d-soft },
  radius: 6pt, stroke: if hi { 2pt + rtm-red } else { 1pt + rtm-line }, inset: 9pt)[
  #text(size: 8.5pt, weight: 800, fill: if hi { rtm-red-dk } else { rtm-muted })[#t] #v(3pt)
  #text(size: 8pt, fill: rtm-ink)[#sub]
]
#let d-ioi-mix = dframe[
  #dtitle("IOI × FAKE IOI 배합")
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    quad("말 칭찬 · 표정 무심", "★ 세련된 호감 (스윗스팟)", rtm-red, true),
    quad("말 칭찬 · 표정 반함", "뻔함 · 없어 보임", d-gray, false),
    quad("말 무심 · 표정 무심", "관심 없어 보임", d-gray, false),
    quad("말 무심 · 표정 반함", "혼란 · 애매", d-gray, false),
  )
]

// ---- 8. 대화 비율 ----
#let seg3(f, l, s) = box(width: 100%, radius: 3pt, clip: true, stack(dir: ltr,
  rect(width: f, height: 14pt, fill: d-gray), rect(width: l, height: 14pt, fill: d-soft2), rect(width: s, height: 14pt, fill: rtm-red)))
#let ratiobar(label, f, l, s) = grid(columns: (34pt, 1fr), gutter: 8pt, align: (left + horizon, horizon),
  text(size: 9pt, weight: 700)[#label], seg3(f, l, s))
#let d-talk-ratio = dframe[
  #dtitle("대화 비율 — 후반일수록 섹스↑")
  #stack(dir: ttb, spacing: 7pt,
    ratiobar("초반", 45%, 35%, 20%),
    ratiobar("중반", 30%, 30%, 40%),
    ratiobar("후반", 15%, 20%, 65%),
  )
  #v(7pt)
  #align(center, stack(dir: ltr, spacing: 14pt,
    box[#box(width: 8pt, height: 8pt, fill: d-gray, radius: 2pt)#h(4pt)#text(size: 8pt)[친구]],
    box[#box(width: 8pt, height: 8pt, fill: d-soft2, radius: 2pt)#h(4pt)#text(size: 8pt)[연애]],
    box[#box(width: 8pt, height: 8pt, fill: rtm-red, radius: 2pt)#h(4pt)#text(size: 8pt)[섹스]],
  ))
]

// ---- 9. 성적개방화 5단계 ----
#let sstep(n, say, msg) = box(width: 100%, fill: d-soft, radius: 6pt, inset: (x: 10pt, y: 7pt), stroke: (left: 3pt + rtm-red))[
  #text(size: 8.5pt, weight: 800, fill: rtm-red)[#n]#h(5pt)#text(size: 9pt, weight: 700)[#say] #v(2pt)
  #text(size: 8pt, fill: rtm-muted)[속 → #msg]
]
#let d-story-structure = dframe[
  #dtitle("성적개방화 5단계 (겉 / 속)")
  #stack(dir: ttb, spacing: 5pt,
    sstep("①", "운 띄우기", "섹스 얘기 자연스럽게 진입"),
    sstep("②", "DHV", "상대·나의 가치 세뇌"),
    sstep("③", "솔직함 미화", "'솔직함'을 가치로 어필"),
    sstep("④", "원나잇 정상화", "원나잇 = 가벼움 아님"),
    sstep("⑤", "수위 키워드 → ASD 완화", "'속궁합' 후 방어 낮춤"),
  )
]

// ---- 10. 합의 신호 판별 (핵심) ----
#let sig(name, col, action) = box(width: 100%, fill: white, radius: 8pt, stroke: 2pt + col, inset: (x: 8pt, y: 10pt))[
  #align(center)[
    #box(fill: col, inset: (x: 9pt, y: 3pt), radius: 12pt, text(size: 8.5pt, weight: 800, fill: white)[#name]) #v(6pt)
    #text(size: 8pt, fill: rtm-ink)[#action]
  ]
]
#let d-consent-flow = dframe[
  #dtitle("밀 때 · 기다릴 때 · 멈출 때")
  #align(center)[#pill("장소 이동 제안", rtm-ink)]
  #arrow-d
  #grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
    sig("초록불", d-green, "몸이 따라옴 · 눈 안 피함 → 밀어도 됨"),
    sig("노란불", d-amber, "말은 튕기나 몸은 남음 → 멈추고 스스로 오게"),
    sig("빨간불", rtm-red, "몸 뺌 · 정색 · 반복 거절 → 즉시 중단"),
  )
  #v(9pt)
  #box(width: 100%, fill: rtm-ink, radius: 6pt, inset: (x: 10pt, y: 9pt),
    align(center, text(size: 9pt, weight: 800, fill: white)[애매하면 언제나 '멈춤'이 기본값 · '밀어붙여라'는 없다]))
]

// ---- 11. 필터링 깔때기 ----
#let frow(w, t, sub, col) = align(center, box(width: w, fill: col, radius: 6pt, inset: (x: 10pt, y: 8pt))[
  #text(size: 9pt, weight: 700, fill: white)[#t]#if sub != "" [#h(6pt)#text(size: 8pt, fill: rgb("#FFDADA"))[#sub]]
])
#let d-filter-funnel = dframe[
  #dtitle("카톡에서 미리 거른다")
  #stack(dir: ttb, spacing: 4pt,
    frow(100%, "다수의 번호", "", d-gray),
    arrow-d,
    frow(72%, "카톡 필터링", "섹슈얼 코드로 반응 확인", rtm-red-dk),
    arrow-d,
    frow(46%, "애프터", "개방적 성향만", rtm-red),
  )
]

// ---- 12. 전체 지도 (인트로) — 만남→모텔 루트 + 신호등 ----
#let rmcirc(n, col) = box(width: 18pt, height: 18pt, radius: 9pt, fill: col,
  align(center + horizon, text(size: 7.5pt, weight: 800, fill: white)[#n]))
#let rmnode(n, label, col) = box(width: 34pt, stack(dir: ttb, spacing: 4pt,
  align(center, rmcirc(n, col)), align(center, text(size: 7pt, weight: 600, fill: rtm-ink)[#label])))
#let rmarr = box(height: 18pt, inset: (x: 1pt), align(horizon, text(size: 9pt, weight: 700, fill: rtm-red)[▸]))
#let rmleg(col, t, sub) = box(width: 100%, fill: white, radius: 8pt, stroke: (left: 3pt + col), inset: (x: 10pt, y: 8pt))[
  #box(width: 8pt, height: 8pt, radius: 4pt, fill: col)#h(5pt)#text(size: 9pt, weight: 800, fill: rtm-ink)[#t] #v(2pt)
  #text(size: 8pt, fill: rtm-muted)[#sub]
]
#let d-roadmap = dframe[
  #dtitle("실전 흐름 · 만남에서 관계까지")
  #align(center, stack(dir: ltr, spacing: 0pt,
    rmnode("1", "만남", rtm-ink), rmarr,
    rmnode("2", "술자리", rtm-red-dk), rmarr,
    rmnode("3", "대화", rtm-red-dk), rmarr,
    rmnode("4", "키스", rtm-red-dk), rmarr,
    rmnode("5", "이동", rtm-red-dk), rmarr,
    rmnode("6", "모텔", rtm-red),
  ))
  #v(13pt)
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    rmleg(d-green, "초록불 = 액셀", "상대가 원할 때 나아간다"),
    rmleg(rtm-red, "빨간불 = 브레이크", "거절이면 멈춘다"),
  )
]

// ---- 13. 밤의 4가지 페르소나 (03장) ----
#let pcard(name, role, warn) = box(width: 100%, height: 64pt, fill: d-soft, radius: 8pt, stroke: (top: 2.5pt + rtm-red), inset: 9pt)[
  #box(fill: rtm-red-dk, inset: (x: 8pt, y: 3pt), radius: 3pt, text(size: 8.5pt, weight: 800, fill: white)[#name]) #v(5pt)
  #text(size: 8pt, fill: rtm-ink)[#role] #v(3pt)
  #text(size: 7.5pt, fill: rtm-muted)[⚠ #warn]
]
#let d-persona4 = dframe[
  #dtitle("밤의 4가지 페르소나 (모드)")
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    pcard("플레이풀", "능글맞게 분위기 열기", "가벼움만 남으면 믿음↓"),
    pcard("카키", "기준 있고 안 휘둘림 · 네그", "무례함 ≠ 자신감"),
    pcard("오버", "과한 플러팅을 장난으로 · 페이크 호감", "짧게 쓰고 바로 회수"),
    pcard("제뉴인", "장난 뒤 진정성·안정감", "초반부터 쓰면 느끼함"),
  )
  #v(10pt)
  #align(center, box(fill: rtm-tint, radius: 20pt, inset: (x: 13pt, y: 7pt))[
    #text(size: 9pt, weight: 700, fill: rtm-red-dk)[장난 (플레이풀·오버)]#text(size: 11pt, weight: 700, fill: rtm-red)[ → ]#text(size: 9pt, weight: 700, fill: rtm-red-dk)[진정성 (제뉴인)]
  ])
]

// ---- 14. CNA NIGHT 핵심 공식 (01장) ----
#let d-core-formula = dframe[
  #dtitle("CNA NIGHT 핵심 공식")
  #stack(dir: ttb, spacing: 5pt,
    stepline("1", "상황 포착", "장소·시간대·상대·친구 읽기"),
    stepline("2", "선해소", "문제 생기기 전에 부담 낮추기"),
    stepline("3", "차별화", "뻔한 남자 프레임 밖으로"),
    stepline("4", "부담 낮추기", "허락 구걸이 아닌 여유"),
    stepline("5", "짧은 제안", "길게 끌지 않고 명확하게"),
  )
]

// ---- 15. 밤 환경 지도 (Part 2) ----
#let envcard(name, note) = box(width: 100%, fill: d-soft, radius: 8pt, stroke: (left: 3pt + rtm-red), inset: (x: 10pt, y: 8pt))[
  #text(size: 9.5pt, weight: 800, fill: rtm-ink)[#name] #v(2pt)
  #text(size: 8pt, fill: rtm-muted)[#note]
]
#let d-night-map = dframe[
  #dtitle("밤 환경 지도 — 어디서 만나느냐")
  #grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
    envcard("밤거리 · 입장 전", "짧은 첫마디 · 부담 낮춤"),
    envcard("클럽 · 라운지", "소음·경쟁 · 비언어·거리감"),
    envcard("헌팅포차", "합석 · 술자리 텐션"),
    envcard("술자리", "완급 · 대화 빌드업"),
    envcard("애프터", "번호→카톡→만남 (한 트랙)"),
    envcard("→ 관계는 합의 위에서", "밀 때/멈출 때 신호 판별"),
  )
]

// ---- 16. CNA NIGHT 루프 (05장) ----
#let d-cna-loop = dframe[
  #dtitle("CNA NIGHT 루프")
  #stack(dir: ttb, spacing: 5pt,
    stepline("1", "가치·재미 보여주기", "상황을 가볍게 비틀기"),
    stepline("2", "관심 주기", "왜 하필 이 사람인지"),
    stepline("3", "여유 보여주기", "안 맞으면 빠진다는 선택권"),
    stepline("4", "반응 확인하기", "웃음·질문·친구·몸 방향"),
    stepline("5", "다음 흐름 제안", "짧고 명확하게"),
  )
  #v(8pt)
  #align(center, box(fill: rtm-tint, radius: 20pt, inset: (x: 13pt, y: 6pt),
    text(size: 8.5pt, weight: 700, fill: rtm-red-dk)[↻ 반응을 보고 1~5를 반복한다]))
]

// ---- 17. 해소 4종 (08장) ----
#let dcard(name, desc) = box(width: 100%, height: 54pt, fill: d-soft, radius: 8pt, stroke: (top: 2.5pt + rtm-red), inset: 9pt)[
  #box(fill: rtm-red-dk, inset: (x: 8pt, y: 3pt), radius: 3pt, text(size: 8.5pt, weight: 800, fill: white)[#name]) #v(4pt)
  #text(size: 8pt, fill: rtm-ink)[#desc]
]
#let d-dissolve4 = dframe[
  #dtitle("해소 4종 — 부담을 낮추는 진정성")
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dcard("선해소", "문제 생기기 전에 미리 부담↓"),
    dcard("진정성 해소", "장난이 과해지면 온도 낮춤"),
    dcard("친구 해소", "친구 = 방해물 아닌 결정권자"),
    dcard("선택 후 불안 방지", "다음날 현타·거리감 예방"),
  )
]

// ---- 키 → 도식 매핑 ----
#let DIAGRAMS = (
  roadmap: d-roadmap,
  persona4: d-persona4,
  core_formula: d-core-formula,
  night_map: d-night-map,
  cna_loop: d-cna-loop,
  dissolve4: d-dissolve4,
  pickup_split: d-pickup-split,
  day_night_flow: d-day-night-flow,
  persona_vibe: d-persona-vibe,
  tension_curve: d-tension-curve,
  brain_model: d-brain-model,
  mirror_mask: d-mirror-mask,
  level_curve: d-level-curve,
  timeline_funnel: d-timeline-funnel,
  ioi_mix: d-ioi-mix,
  talk_ratio: d-talk-ratio,
  story_structure: d-story-structure,
  consent_flow: d-consent-flow,
  filter_funnel: d-filter-funnel,
  recon_questions: d-recon-questions,
)

// ---- 마크다운 + 도식 토큰 렌더 ----
// [[DIAGRAM:key]] 토큰 기준으로 마크다운을 쪼개 렌더하고, 사이에 도식 삽입.
#let render-with-diagrams(path) = {
  let raw = read(path)
  let chunks = raw.split(regex("\[\[DIAGRAM:[a-z0-9_]+\]\]"))
  let keys = raw.matches(regex("\[\[DIAGRAM:([a-z0-9_]+)\]\]")).map(m => m.captures.first())
  for (i, chunk) in chunks.enumerate() {
    cmarker.render(chunk)
    if i < keys.len() and keys.at(i) in DIAGRAMS {
      DIAGRAMS.at(keys.at(i))
    }
  }
}
