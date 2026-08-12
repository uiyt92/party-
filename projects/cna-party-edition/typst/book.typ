// CNA Party Edition — 빌드 엔트리
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
#[
  #set text(size: 8.8pt)
  #set par(leading: 1.18em, spacing: 0.25em)
  #render-rich("../manuscript/06-checklist.md")
]
