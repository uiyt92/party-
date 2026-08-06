// CNA NIGHT — 빌드 엔트리
// 실행: python scripts/project.py build cna-night
#import "theme.typ": *
#import "diagrams.typ": render-with-diagrams

#show: book.with(
  title: "CNA NIGHT",
  subtitle: "밤의 커뮤니케이션 DNA · 매력이 즉각 전달되는 남자 (19금)",
  author: "PREDIC / SUPER NATURAL",
)

#render-with-diagrams("../manuscript/00_prologue.md")

#render-with-diagrams("../manuscript/00_notice.md")

#part-divider("PART 0", "프레임 — 밤은 다른 게임이다")
#render-with-diagrams("../manuscript/01_frame.md")

#part-divider("PART 1", "밤에서 중요한 것 — 몸·페르소나·부담")
#render-with-diagrams("../manuscript/p1_important.md")
#render-with-diagrams("../manuscript/02_state.md")
#render-with-diagrams("../manuscript/03_mask.md")

#part-divider("PART 2", "밤에서 해야 할 것 — 실전 플로우")
#render-with-diagrams("../manuscript/p2_flow.md")
#render-with-diagrams("../manuscript/04a_environments.md")
#render-with-diagrams("../manuscript/04b_situations.md")
#render-with-diagrams("../manuscript/04_flow_meet.md")

#part-divider("PART 3", "대화 & 멘트 생성 — 무슨 말을 하느냐")
#render-with-diagrams("../manuscript/05_flow_talk.md")
#render-with-diagrams("../manuscript/06_storytelling.md")

#part-divider("PART 4", "에스컬레이션 & 합의 — 밀 때와 멈출 때")
#render-with-diagrams("../manuscript/07_escalation.md")
#render-with-diagrams("../manuscript/08_consent.md")

#part-divider("PART 5", "그 이후 — 파트너·필터링·당부")
#render-with-diagrams("../manuscript/09_after.md")
