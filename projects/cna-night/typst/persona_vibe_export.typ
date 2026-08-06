// 단일 도식 SVG/PNG 내보내기용 래퍼 (persona_vibe)
// typst compile projects/cna-night/typst/persona_vibe_export.typ build/previews/cna-night/persona_vibe.svg --root .
#import "diagrams.typ": d-persona-vibe
#set page(width: 320pt, height: auto, margin: 10pt, fill: white)
#set text(font: "Pretendard", lang: "ko")
#d-persona-vibe
