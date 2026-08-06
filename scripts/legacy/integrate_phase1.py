# -*- coding: utf-8 -*-
"""Phase 1 통합: 신규장 생성 + 사례/상황 병합 + 상호참조 +1 시프트."""
import re
from pathlib import Path

ROOT = Path(r"C:/Users/SuperNatural1/Code/CODE/폰게임 강의 책")
DRAFT = ROOT / "drafts" / "phase1"

def rd(p): return Path(p).read_text(encoding="utf-8")
def wr(p, t): Path(p).write_text(t, encoding="utf-8"); print("  쓰기:", Path(p).name)

REF = re.compile(r"\s*\([^)]*(?:장|참조)[^)]*\)")  # 챕터 번호 괄호 참조 제거용

def strip_refs_on(line):
    if ("**포인트**" in line) or ("참조" in line) or line.strip().startswith("> 주의"):
        return REF.sub("", line)
    return line

# ── 1. 신규장 08b_continue.md ──────────────────────────────────────
src = rd(DRAFT / "00_continue_chapter.md")
src = src.replace(
    "## 사례 1. 차가운 단답에서 약속 직전까지 — 7턴 실전 대화",
    "## 실전 대화 — 차가운 단답에서 약속 직전까지 (7턴)",
)
src = "\n".join(strip_refs_on(l) for l in src.split("\n"))
wr(ROOT / "08b_continue.md", src)

# ── 2. 사례 병합 (cases_1..5 → 20_cases.md, 핵심 박스 앞) ──────────
def load_cases():
    parts = []
    for i in range(1, 6):
        t = rd(DRAFT / f"cases_{i}.md")
        out = []
        for l in t.split("\n"):
            if re.match(r"^---+\s*$", l):   # 사례 간 구분선 제거(기존 20장과 통일)
                continue
            out.append(strip_refs_on(l))
        parts.append("\n".join(out).strip())
    return "\n\n".join(parts)

cases_new = load_cases()
cases_md = rd(ROOT / "20_cases.md")
lines = cases_md.split("\n")
idx = next(i for i, l in enumerate(lines) if l.startswith("> **핵심**"))
# 핵심 박스 앞 빈 줄 위치까지 거슬러
insert_at = idx
while insert_at > 0 and lines[insert_at - 1].strip() == "":
    insert_at -= 1
new_lines = lines[:insert_at] + ["", cases_new, ""] + lines[insert_at:]
cases_md = "\n".join(new_lines)

# 기존 사례 1~10 참조 +1 시프트 (high→low, 신규 사례엔 참조 없음)
for old, new in [("19장", "20장"), ("17장", "18장"), ("14장", "15장"),
                 ("13장", "14장"), ("9장", "10장")]:
    cases_md = cases_md.replace(old, new)
wr(ROOT / "20_cases.md", cases_md)

# ── 3. 상황 병합 (sits_1..3 → 15_situation.md, 핵심 박스 앞) ───────
def extract_sits(path):
    blocks, cur = [], None
    for l in rd(path).split("\n"):
        if l.startswith("## "):
            h = l[3:].strip()
            if h.startswith("사례") or "자가검증" in h:
                cur = None
            else:
                cur = [l]; blocks.append(cur)
        elif l.startswith("# "):
            cur = None
        elif cur is not None:
            cur.append(l)
    out = []
    for b in blocks:
        for l in b:
            if re.match(r"^---+\s*$", l):
                continue
            out.append(strip_refs_on(l))
        out.append("")
    return "\n".join(out).strip()

sits_new = "\n\n".join(extract_sits(DRAFT / f"sits_{i}.md") for i in (1, 2, 3))
sit_md = rd(ROOT / "15_situation.md")
slines = sit_md.split("\n")
sidx = next(i for i, l in enumerate(slines) if l.startswith("> **핵심**"))
ins = sidx
while ins > 0 and slines[ins - 1].strip() == "":
    ins -= 1
sit_md = "\n".join(slines[:ins] + ["", sits_new, ""] + slines[ins:])
wr(ROOT / "15_situation.md", sit_md)

# ── 4. 16_mistakes 참조 시프트 ────────────────────────────────────
m = rd(ROOT / "16_mistakes.md")
m = m.replace("(9장 참고)", "(10장 참고)").replace("(19장에서 다룬다)", "(20장에서 다룬다)")
wr(ROOT / "16_mistakes.md", m)

# ── 5. 21_appendix 인덱스 시프트 + 신규장 행 추가 ─────────────────
a = rd(ROOT / "21_appendix.md")
appx = [
    ("| 읽씹·안읽씹당했다 | 8장 읽씹 대응 |",
     "| 읽씹·안읽씹당했다 | 8장 읽씹 대응 |\n| 답장은 받는데 그 다음이 막막하다 | 9장 답장을 받았다면 |"),
    ("9장 대화가 끊겼을 때", "10장 대화가 끊겼을 때"),
    ("10장 사진으로 대화", "11장 사진으로 대화"),
    ("11·12장 표현·화술", "12·13장 표현·화술"),
    ("13장 호감 신호", "14장 호감 신호"),
    ("14장 말 놓기", "15장 말 놓기"),
    ("15장 상황별 대응", "16장 상황별 대응"),
    ("16장 단계별 실수", "17장 단계별 실수"),
    ("17장 죽은 번호 살리기", "18장 죽은 번호 살리기"),
    ("18장 전화·보이스톡", "19장 전화·보이스톡"),
    ("19장 만남으로", "20장 만남으로"),
]
for old, new in appx:
    a = a.replace(old, new)
wr(ROOT / "21_appendix.md", a)

print("통합 완료.")
