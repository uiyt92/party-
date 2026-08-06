#import "../../../templates/typst/book.typ": *
#import "@preview/cmarker:0.1.6"

#show: book.with(
  title: "__TITLE__",
  subtitle: "새 Typst 교재 프로젝트",
  author: "저자명",
)

#cmarker.render(read("../manuscript/01-introduction.md"))
