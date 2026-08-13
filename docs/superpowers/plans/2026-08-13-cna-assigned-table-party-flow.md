# CNA 지정석·조별 순환형 파티 흐름 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 자유 이동형 파티를 전제로 쓴 교재를 지정석·조별 순환·게임·쉬는 시간 중심의 실제 행사 흐름으로 바로잡고 네 가지 교재 장치를 한국어로 통일한다.

**Architecture:** 장별 Markdown은 콘텐츠 정본으로 유지하고, `diagrams.typ`의 두 도식을 새 행동 모델에 맞추며, `theme.typ`은 카드에 보이는 제목만 한국어로 바꾼다. 각 장의 계약을 먼저 실패하도록 갱신한 뒤 원고를 수정하고, 마지막에 제품 PDF를 다시 빌드해 인벤토리와 시각 검수 자료를 갱신한다.

**Tech Stack:** Markdown, Typst 0.14.2, Python 3.12+ `unittest`, `pypdf`, Poppler

---

## 작업 전 상태와 보존 규칙

- 작업 폴더: `C:\Users\SuperNatural1\Code\CODE\폰게임 강의 책\.worktrees\cna-party-book`
- 브랜치: `codex/cna-party-book`
- 사용자가 직접 수정한 `projects/cna-party-edition/manuscript/00-prologue.md`가 미커밋 상태다.
- 이 파일을 `checkout`, `restore`, `stash`, `reset`하지 않는다.
- 사용자가 바꾼 소제목 `## 파티에서 연애를 하기 어려운 이유`와 `파티에 처음 간 사람`이라는 방향을 유지한다.
- `기다린다..`, `뜨금한`처럼 의미가 아닌 명백한 문장부호·맞춤법 오류만 `기다린다.`, `뜨끔한`으로 바로잡는다.
- 내부 토큰 `[[CALLOUT:bad|...]]`, `[[CALLOUT:better|...]]`, `[[CALLOUT:mission|...]]`과 Typst 함수명 `bad-move`, `better-move`, `mission-card`는 공개 문구가 아니므로 바꾸지 않는다.

## File map

### Modify

- `projects/cna-party-edition/manuscript/00-prologue.md` — 지정석 파티의 첫 장면과 교재 사용법
- `projects/cna-party-edition/manuscript/01-environment.md` — 조 구성·교체 방향·게임 흐름 관찰
- `projects/cna-party-edition/manuscript/02-positioning.md` — 현재 조에서 기여하고 운영 전환을 받아들이는 모델
- `projects/cna-party-edition/manuscript/03-rapport.md` — 새 조·게임 직후에 여는 첫 대화
- `projects/cna-party-edition/manuscript/04-influence.md` — 이동 연출 없는 선택성과 긴장 조절
- `projects/cna-party-edition/manuscript/05-number-exchange.md` — 실제 번호 교환 창과 진행 복귀
- `projects/cna-party-edition/manuscript/06-checklist.md` — 지정석 행사 실행 카드와 복기표
- `projects/cna-party-edition/typst/diagrams.typ` — 조별 자리 지도와 포지셔닝 순환
- `projects/cna-party-edition/typst/theme.typ` — 세 카드의 한국어 화면 제목
- `tests/test_cna_party_project.py` — 행사 구조·한글 표기·PDF 계약
- `dist/pdf/CNA_파티의_주도권.pdf` — 갱신된 정식 배포본
- `docs/ARTIFACT_INVENTORY.md` — 새 PDF 페이지 수·바이트·SHA-256

### Preserve

- `projects/cna-party-edition/typst/book.typ` — 장 순서와 조판 구조는 바꾸지 않는다.
- `projects/cna-party-edition/project.json` — 산출물 ID와 파일명은 바꾸지 않는다.

---

### Task 1: 프롤로그와 환경 장을 지정석 파티로 전환

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Modify: `projects/cna-party-edition/manuscript/00-prologue.md`
- Modify: `projects/cna-party-edition/manuscript/01-environment.md`
- Modify: `projects/cna-party-edition/typst/diagrams.typ`

- [ ] **Step 1: 사용자 수정 상태와 기준선 실패를 기록한다**

Run:

```powershell
git diff -- projects/cna-party-edition/manuscript/00-prologue.md
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_prologue_and_environment_are_self_contained -v
```

Expected: diff에 사용자 수정 세 곳만 보이고, 기존 테스트는 옛 소제목 `## 초보자와 무성과자가 같은 곳에서 무너지는 이유`를 찾지 못해 실패한다. 이 실패는 기존 사용자 수정 때문이며 파일을 되돌리지 않는다.

- [ ] **Step 2: 지정석 오프닝 계약을 추가한다**

`test_prologue_and_environment_are_self_contained`의 프롤로그 소제목 기대값을 `## 파티에서 연애를 하기 어려운 이유`로 바꾸고, 같은 테스트 클래스에 아래 메서드를 추가한다.

```python
def test_opening_uses_assigned_groups_and_host_led_rotation(self):
    prologue = (PROJECT / "manuscript" / "00-prologue.md").read_text(
        encoding="utf-8"
    )
    environment = (PROJECT / "manuscript" / "01-environment.md").read_text(
        encoding="utf-8"
    )
    diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(encoding="utf-8")

    for expected in ("정해진 자리", "현재 조", "자리 교체", "조별 게임"):
        self.assertIn(expected, prologue + "\n" + environment)
    for expected in ("현재 조", "교체 방향", "게임 흐름"):
        self.assertIn(expected, environment)
    for expected in ("현재 조", "다음 전환", "열린 접점"):
        self.assertIn(expected, diagrams)

    for forbidden in (
        "지금 다가가도 될까?",
        "마음에 드는 사람을 찾아 곧장 걷지 말자",
        "방을 천천히 한 바퀴 바라본다",
    ):
        self.assertNotIn(forbidden, prologue + "\n" + environment)
```

`test_environment_mission_keeps_live_observation_discreet`의 본문을 아래와 같이 교체한다.

```python
def test_environment_mission_keeps_live_observation_discreet(self):
    chapter = (PROJECT / "manuscript" / "01-environment.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "휴대폰",
        "현재 조",
        "교체 방향",
        "게임 흐름",
        "머릿속",
        "파티가 끝난 뒤",
    ):
        self.assertIn(expected, chapter)
    self.assertNotIn("대화하기 전, 선택한 타깃의", chapter)
    self.assertNotIn("종이에 방의 배치와 구역만", chapter)
```

- [ ] **Step 3: 새 계약이 콘텐츠 차이로 실패하는지 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_opening_uses_assigned_groups_and_host_led_rotation tests.test_cna_party_project.CnaPartyManuscriptTests.test_environment_mission_keeps_live_observation_discreet -v
```

Expected: `정해진 자리`, `현재 조`, `자리 교체` 또는 새 도식 문구가 없어 실패한다.

- [ ] **Step 4: 프롤로그를 실제 입장 장면으로 고친다**

`00-prologue.md`에서 다음 내용을 정확히 반영한다.

- 첫 문단은 참가자가 정해진 자리에 앉고, 다른 조의 마음에 드는 사람이 보여도 곧장 찾아갈 수 없다는 장면으로 시작한다.
- `지금 다가가도 될까?` 대신 `언제 같은 조가 될까?`, `그전까지 현재 자리에서 무엇을 보여 줄까?`라는 고민을 사용한다.
- 첫 세 문단에 `현재 조에서 편안한 분위기를 만들기`, `운영자가 자리를 바꿔 주는 순간`, `조별 게임과 쉬는 시간`을 넣는다.
- `다가가는 데 시간이 오래 걸린다면`은 `새 조에서 첫 인사가 늦는다면`으로 바꾼다.
- `자리를 바꾸면 된다`는 `다른 사람에게 말할 차례를 넘기거나 다음 교체를 받아들이면 된다`로 바꾼다.
- 사용자가 바꾼 소제목과 `파티에 처음 간 사람`이라는 표현을 유지하고 명백한 `..`, `뜨금한`만 바로잡는다.

- [ ] **Step 5: 환경 장과 파티 지도를 조별 순환형으로 고친다**

`01-environment.md`와 `diagrams.typ`에 아래 내용을 반영한다.

- 첫 60~90초는 방을 한 바퀴 도는 시간이 아니라 배정된 의자, 현재 조의 말 분배, 운영자의 교체 안내와 게임 규칙을 읽는 시간으로 쓴다.
- 중앙·가장자리·동선 설명은 제거하고 `현재 조`, `주변 조`, `교체 방향`, `게임 흐름`을 설명한다.
- 관심 상대의 상태를 멀리서 단정하지 말고 같은 조나 게임에서 실제 반응을 주고받을 때 확인한다고 쓴다.
- 실전 과제는 현장에서 사람별 메모를 하지 않고, 휴대폰을 넣어 둔 채 현재 조·교체 방향·게임 흐름을 머릿속으로 관찰한 뒤 파티가 끝난 후 복기하도록 쓴다.
- `party-map`의 세 칸을 아래 문구로 바꾼다.

```typst
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
```

- [ ] **Step 6: 오프닝 계약과 전체 원고 계약을 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests -v
git diff --check
```

Expected: 모든 원고 테스트가 통과하고 공백 오류가 없다.

- [ ] **Step 7: 오프닝 전환을 커밋한다**

```powershell
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/00-prologue.md projects/cna-party-edition/manuscript/01-environment.md projects/cna-party-edition/typst/diagrams.typ
git commit -m "edit: align CNA opening with assigned group rotation"
```

---

### Task 2: 포지셔닝을 현재 조의 기여와 운영 전환으로 수정

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Modify: `projects/cna-party-edition/manuscript/02-positioning.md`
- Modify: `projects/cna-party-edition/typst/diagrams.typ`

- [ ] **Step 1: 포지셔닝 계약을 새 순환으로 바꾼다**

`test_positioning_chapter_builds_social_value`에서 기존 순환 정규식과 미션 검사를 아래 코드로 교체한다.

```python
diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(encoding="utf-8")

self.assertRegex(
    chapter,
    re.escape("사용할 순환은 **관찰 → 기여 → 반응 → 전환**이다.")
    + r"[^\n]*\n\n"
    + re.escape("[[DIAGRAM:positioning_loop]]"),
)
for context in ("현재 조", "운영자의 자리 교체", "게임 종료"):
    self.assertIn(context, chapter)
self.assertNotIn("관찰 → 공급 → 반응 → 이동", chapter)
self.assertNotIn("나 저쪽에 인사 하나만 하고 다시 볼게", chapter)

mission = re.search(r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*$", chapter)
self.assertIsNotNone(mission)
for expected in ("현재 조", "긍정적인 상호작용 세 번", "다음 전환"):
    self.assertIn(expected, mission.group(1))
```

같은 테스트에서 `positioning-loop` 도식에 `기여`, `전환`이 있고 기존 단계 `공급`, `이동`이 없는지 검사한다.

```python
positioning_loop = re.search(
    r"(?ms)^#let positioning-loop = .*?(?=^#let rapport-ladder)", diagrams
)
self.assertIsNotNone(positioning_loop)
for expected in ("관찰", "기여", "반응", "전환"):
    self.assertIn(expected, positioning_loop.group(0))
for legacy in ('"공급"', '"이동"'):
    self.assertNotIn(legacy, positioning_loop.group(0))
```

- [ ] **Step 2: 새 포지셔닝 계약의 실패를 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_positioning_chapter_builds_social_value -v
```

Expected: 옛 `공급 → 이동` 순환 때문에 실패한다.

- [ ] **Step 3: 포지셔닝 장과 도식을 수정한다**

`02-positioning.md`에서 아래 전환을 완성한다.

- 관심 상대를 보며 몸과 시선을 추적하는 장면은 유지하되, 그 사람에게 이동하는 대신 현재 조를 놓치는 문제로 설명한다.
- `나 저쪽에 인사 하나만 하고 다시 볼게` 예문과 자유 이동을 희소성으로 설명한 문단을 삭제한다.
- 기버의 세 행동은 현재 조 안에서 사람 연결, 정적 수리, 작은 편의를 제공하는 방식으로 유지한다.
- 순환을 `관찰 → 기여 → 반응 → 전환`으로 쓰고 전환은 운영자의 자리 교체 또는 게임 종료라고 정의한다.
- 서브 호스트는 새로 들어온 자유 참가자가 아니라 새 조에 합류한 사람의 참여를 돕는 역할로 쓴다.
- 거절 뒤에는 자리를 임의로 떠난다는 말 대신 질문을 멈추고 다른 조원에게 차례를 넘긴다고 쓴다.
- 마지막 실전 과제는 현재 조에서 연결·정적 수리·작은 편의로 긍정적 상호작용 세 번을 만들고 다음 전환을 편하게 받아들이도록 쓴다.

`diagrams.typ`의 `positioning-loop`를 아래 단계로 바꾼다.

```typst
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
```

- [ ] **Step 4: 포지셔닝 검사 후 커밋한다**

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_positioning_chapter_builds_social_value -v
git diff --check
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/02-positioning.md projects/cna-party-edition/typst/diagrams.typ
git commit -m "edit: adapt CNA positioning to group rotations"
```

Expected: 대상 테스트가 통과하고 커밋이 생성된다.

---

### Task 3: 라포와 영향력을 새 조·게임의 짧은 창에 맞춤

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Modify: `projects/cna-party-edition/manuscript/03-rapport.md`
- Modify: `projects/cna-party-edition/manuscript/04-influence.md`

- [ ] **Step 1: 새 조와 게임 접점 계약을 추가한다**

`CnaPartyManuscriptTests`에 아래 테스트를 추가한다.

```python
def test_rapport_and_influence_use_rotation_windows(self):
    rapport = (PROJECT / "manuscript" / "03-rapport.md").read_text(
        encoding="utf-8"
    )
    influence = (PROJECT / "manuscript" / "04-influence.md").read_text(
        encoding="utf-8"
    )

    for expected in ("새 조", "조별 게임", "게임 직후", "말할 차례"):
        self.assertIn(expected, rapport)
    for expected in ("조 전체", "자리 교체", "매달리지"):
        self.assertIn(expected, influence)
    for forbidden in (
        "답할 수 있는 거리에서 옆 공간을 비워 둔 채 시작한다",
        "나 친구들한테도 인사하고 올게요. 조금 있다가 동선 겹치면 다시 봐요",
        "필요한 동안 저는 제 일행 쪽에 있을게요",
    ):
        self.assertNotIn(forbidden, rapport + "\n" + influence)
```

- [ ] **Step 2: 새 계약이 기존 장면 때문에 실패하는지 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_rapport_and_influence_use_rotation_windows -v
```

Expected: 새 조·조별 게임 문맥이 없고 자유 이동 예문이 남아 있어 실패한다.

- [ ] **Step 3: 라포 장을 지정석의 첫 대화로 수정한다**

`03-rapport.md`에 아래 내용을 반영한다.

- 관찰 단서는 같은 조가 된 뒤 확인하며 멀리서 관심 상대를 진단하지 않는다.
- 첫 대화 전체 예시는 새 조에 앉은 직후 또는 조별 게임이 끝난 직후로 바꾼다.
- 게임에서 나온 규칙, 선택, 웃음 포인트를 첫 질문의 구체적 소재로 사용한다.
- 하이파이브나 협동 동작은 상대가 함께 손을 내밀거나 규칙상 필요한 때만 하며, 피하거나 멈추면 접촉을 만들지 않는다고 명시한다.
- 접촉을 호감 신호로 해석하거나 게임을 핑계로 반복하지 않는다고 명시한다.
- 대화 종료는 임의 이동이 아니라 다른 조원에게 말할 차례를 넘기거나 다음 자리 교체를 받아들이는 장면으로 쓴다.

- [ ] **Step 4: 영향력 장에서 떠남 연출을 제거한다**

`04-influence.md`에 아래 내용을 반영한다.

- 희소성은 다른 그룹으로 이동하는 연출이 아니라 현재 조의 한 사람을 독점하지 않고 조 전체에 고르게 참여하는 태도로 정의한다.
- `친구들한테도 인사하고 올게요`, `제 일행 쪽에 있을게요` 예문을 제거한다.
- 자리 교체가 안내되면 대화를 억지로 연장하거나 다음 조를 방해하지 않는 태도를 선택성으로 설명한다.
- 게임이나 교체를 상대에게 압박을 주는 카운트다운으로 사용하지 않는다.
- 기존 프레임 복구, 자격 부여, 명시적 거절·판단력 저하·불안에서 즉시 멈추는 안전 장치는 유지한다.

같은 테스트의 희소성 검사는 자유 이동 대신 조 안의 선택성을 확인하도록 바꾼다.

```python
for scarcity_guard in (
    "선택적으로 주의를 쓰고 한 사람을 독점하지 않을 의향",
    "바쁜 척",
    "일정을 지어내는 것",
    "벌주듯 관심을 거두는 것",
):
    self.assertIn(scarcity_guard, chapter)
self.assertNotIn("필요한 동안 저는 제 일행 쪽에 있을게요", chapter)
self.assertIn("자리 교체가 안내되면", chapter)
```

- [ ] **Step 5: 두 장의 계약과 전체 원고 검사를 통과시키고 커밋한다**

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests -v
git diff --check
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/03-rapport.md projects/cna-party-edition/manuscript/04-influence.md
git commit -m "edit: ground CNA conversations in rotation windows"
```

Expected: 모든 원고 테스트가 통과하고 두 장과 테스트만 커밋된다.

---

### Task 4: 번호 교환과 실행 카드를 실제 접점에 맞춤

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Modify: `projects/cna-party-edition/manuscript/05-number-exchange.md`
- Modify: `projects/cna-party-edition/manuscript/06-checklist.md`

- [ ] **Step 1: 번호 교환 창과 진행 복귀 계약을 작성한다**

`test_closing_chapters_end_at_number_exchange`에서 기존 이동 전제를 검사하는 부분을 아래로 바꾼다.

`number_headings`의 마지막 제목은 다음으로 바꾼다.

```python
"## 교환 뒤에는 진행으로 돌아간다",
```

```python
for exchange_window in (
    "게임 직후",
    "자리 교체 직전",
    "음료를 받는 쉬는 시간",
    "행사 종료 전",
):
    self.assertIn(exchange_window, number_chapter)

for refusal_guard in (
    "왜 안 되는지 묻지 않는다",
    "협상하지 않는다",
    "현재 진행으로 돌아간다",
    "벌주지 않는다",
):
    self.assertIn(refusal_guard, number_chapter)
self.assertIn("교환 → 마무리 한 줄 → 진행 복귀", number_chapter)
self.assertNotIn("교환 → 마무리 한 줄 → 이동", number_chapter)
self.assertNotIn("친구들한테도 인사하고 올게요", number_chapter)
```

`exit_section`을 자르는 제목도 새 제목으로 바꾼다.

```python
exit_section = number_chapter[
    number_chapter.index("## 교환 뒤에는 진행으로 돌아간다") :
]
```

끝맺음 범위 정규식은 다음으로 바꾼다.

```python
self.assertRegex(
    number_chapter,
    r"이 책의 실전 범위는 여기까지다[^\n]*번호 교환[^\n]*"
    r"현재 진행으로 돌아간다",
)
```

체크리스트 계약에는 아래 검사를 추가한다.

```python
for expected in (
    "현재 조에 기여",
    "운영자의 자리 교체",
    "게임 접촉이 상호적",
    "어느 전환에서 만났는가",
):
    self.assertIn(expected, checklist)
for legacy in (
    "방의 지도를 그리고 사회적 중심",
    "관찰 → 공급 → 반응 → 이동",
    "마무리 한 줄을 남기고 이동",
):
    self.assertNotIn(legacy, checklist)
```

같은 테스트 클래스에 책 전체의 행사 구조를 잠그는 아래 테스트를 추가한다.

```python
def test_all_chapters_follow_the_assigned_group_event_model(self):
    chapters = {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted((PROJECT / "manuscript").glob("*.md"))
    }
    expected_by_chapter = {
        "00-prologue.md": ("정해진 자리", "현재 조", "자리 교체", "조별 게임"),
        "01-environment.md": ("현재 조", "교체 방향", "게임 흐름"),
        "02-positioning.md": ("관찰 → 기여 → 반응 → 전환", "운영자의 자리 교체"),
        "03-rapport.md": ("새 조", "게임 직후", "말할 차례"),
        "04-influence.md": ("조 전체", "자리 교체", "매달리지"),
        "05-number-exchange.md": ("게임 직후", "자리 교체 직전", "쉬는 시간"),
        "06-checklist.md": ("현재 조에 기여", "게임 접촉이 상호적"),
    }
    for filename, markers in expected_by_chapter.items():
        for marker in markers:
            self.assertIn(marker, chapters[filename], f"{filename}: {marker}")

    all_text = "\n".join(chapters.values())
    for forbidden in (
        "마음에 드는 사람을 찾아 곧장 걷지 말자",
        "방을 천천히 한 바퀴 바라본다",
        "나 저쪽에 인사 하나만 하고 다시 볼게",
        "관찰 → 공급 → 반응 → 이동",
        "주요 관심 상대에게 다가가기 전에",
        "친구들한테도 인사하고 올게요",
        "교환 → 마무리 한 줄 → 이동",
    ):
        self.assertNotIn(forbidden, all_text)
```

- [ ] **Step 2: 닫는 장 계약의 실패를 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_closing_chapters_end_at_number_exchange -v
```

Expected: 실제 접점 네 곳과 진행 복귀 문구가 없어 실패한다.

- [ ] **Step 3: 번호 교환 장을 실제 창에 맞춰 수정한다**

`05-number-exchange.md`에 아래 내용을 반영한다.

- 번호 교환 창을 게임 직후, 자리 교체 직전, 음료를 받는 쉬는 시간, 행사 종료 전 자연스러운 재접점으로 명시한다.
- 단순히 가까이 앉았거나 같은 게임에서 신체 접촉이 있었다는 사실은 호감 신호가 아니라고 명시한다.
- 거절 뒤 `친구들한테도 인사하고 올게요`와 방 전체로 시선을 돌리는 연출을 삭제하고 현재 진행으로 자연스럽게 돌아간다고 쓴다.
- 번호 교환 뒤 순서를 `교환 → 마무리 한 줄 → 진행 복귀`로 바꾼다.
- 소제목 `## 먼저 떠나는 사람이 여운을 만든다`는 `## 교환 뒤에는 진행으로 돌아간다`로 바꾼다.
- 상대가 새 질문을 시작하면 이어 가도 된다는 상호성 원칙을 유지한다.
- 책의 범위는 번호 교환과 행사 마무리에서 끝내고 후속 연락 운영을 추가하지 않는다.

- [ ] **Step 4: 실행 카드와 복기표를 조별 순환형으로 수정한다**

`06-checklist.md`에 아래 내용을 반영한다.

- 첫 10분 항목을 현재 조의 참여 정도, 운영자의 자리 교체 방향, 게임 규칙 확인으로 바꾼다.
- `관찰 → 공급 → 반응 → 이동`을 `관찰 → 기여 → 반응 → 전환`으로 바꾼다.
- 게임 항목에 규칙 안의 접촉인지, 상대가 함께 참여했는지, 피하거나 멈췄을 때 즉시 그만뒀는지를 넣는다.
- 번호 교환 뒤 `이동` 대신 현재 진행으로 돌아가도록 쓴다.
- 복기표 머리글을 아래와 같이 바꾼다.

```markdown
| 만난 전환 | 현재 조에 기여한 행동 | 게임 접촉이 상호적이었는가 | 다음 실험 |
| --- | --- | --- | --- |
```

- [ ] **Step 5: 닫는 장 검사 후 커밋한다**

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyManuscriptTests.test_closing_chapters_end_at_number_exchange -v
git diff --check
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/05-number-exchange.md projects/cna-party-edition/manuscript/06-checklist.md
git commit -m "edit: use real CNA rotation windows for number exchange"
```

Expected: 대상 테스트가 통과하고 닫는 두 장과 테스트만 커밋된다.

---

### Task 5: 네 교재 장치를 한국어로 통일

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Modify: `projects/cna-party-edition/manuscript/00-prologue.md`
- Modify: `projects/cna-party-edition/manuscript/01-environment.md`
- Modify: `projects/cna-party-edition/manuscript/03-rapport.md`
- Modify: `projects/cna-party-edition/manuscript/05-number-exchange.md`
- Modify: `projects/cna-party-edition/typst/theme.typ`

- [ ] **Step 1: 한글 표기 계약을 먼저 작성한다**

기존 테스트의 공개 표기 기대값을 다음처럼 바꾼다.

```python
# introduction_rows
header_index = lines.index("| 잘못된 선택 | 좋은 선택 |")

# rapport
self.assertIn("> **대화 예시**", chapter)

# numbered examples
match = re.search(
    rf"(?m)^> \*\*대화 예시 {number}[^\n]*{re.escape(role)}\*\*$",
    number_chapter,
)

# scope guard
r"(?im)^> \*\*(?:대화 예시|예시)[^\n]*"
```

`CnaPartyTypstContractTests`에 아래 테스트를 추가한다.

```python
def test_visible_learning_labels_are_korean(self):
    sources = [
        *(PROJECT / "manuscript").glob("*.md"),
        PROJECT / "typst" / "theme.typ",
    ]
    visible_text = "\n".join(path.read_text(encoding="utf-8") for path in sources)

    for legacy in ("BAD MOVE", "BETTER MOVE", "SCRIPT", "MISSION"):
        self.assertNotIn(legacy, visible_text)
    for label in ("잘못된 선택", "좋은 선택", "대화 예시", "실전 과제"):
        self.assertIn(label, visible_text)

    theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")
    for card_label in ("잘못된 선택", "좋은 선택", "실전 과제"):
        self.assertIn(f"][{card_label}]", theme)
```

- [ ] **Step 2: 영어 공개 표기 때문에 실패하는지 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyTypstContractTests.test_visible_learning_labels_are_korean -v
```

Expected: 네 영어 표기가 원고와 테마에 남아 있어 실패한다.

- [ ] **Step 3: 원고 공개 표기를 모두 바꾼다**

아래 대응을 활성 원고에만 적용한다.

```text
BAD MOVE   -> 잘못된 선택
BETTER MOVE -> 좋은 선택
SCRIPT     -> 대화 예시
MISSION    -> 실전 과제
```

구체적으로 다음 형식을 사용한다.

```markdown
| 잘못된 선택 | 좋은 선택 |
**대화 예시**
> **대화 예시**
> **대화 예시 1 · 함께 갈 장소**
```

프롤로그의 사용법은 `**잘못된 선택**`, `**좋은 선택**`, `**대화 예시**`, `**실전 과제**`로 설명하고, `좋은 선택`이 절대적 정답이 아니라 부담을 줄이며 반응을 살피는 선택지라는 문장을 유지한다.

- [ ] **Step 4: 카드 화면 제목을 한국어로 바꾼다**

`theme.typ`에서 화면에 표시되는 세 제목만 다음처럼 바꾼다. 함수명과 색상명은 유지한다.

```typst
#text(size: 8.2pt, weight: 800, fill: bad, tracking: 0.4pt)[잘못된 선택]
#text(size: 8.2pt, weight: 800, fill: better, tracking: 0.4pt)[좋은 선택]
#text(size: 8.2pt, weight: 800, fill: lime-dark, tracking: 0.4pt)[실전 과제]
```

- [ ] **Step 5: 한글 표기와 전체 테스트를 확인하고 커밋한다**

```powershell
rg -n "BAD MOVE|BETTER MOVE|SCRIPT|MISSION" projects/cna-party-edition/manuscript projects/cna-party-edition/typst/theme.typ
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
git diff --check
git add tests/test_cna_party_project.py projects/cna-party-edition/manuscript/00-prologue.md projects/cna-party-edition/manuscript/01-environment.md projects/cna-party-edition/manuscript/03-rapport.md projects/cna-party-edition/manuscript/05-number-exchange.md projects/cna-party-edition/typst/theme.typ
git commit -m "edit: localize CNA learning labels in Korean"
```

Expected: `rg`는 결과 없이 종료하고 전체 33개 이상 테스트가 모두 통과한다.

---

### Task 6: 새 PDF를 빌드하고 인벤토리와 시각 품질을 검증

**Files:**
- Modify: `tests/test_cna_party_project.py`
- Modify: `dist/pdf/CNA_파티의_주도권.pdf`
- Modify: `docs/ARTIFACT_INVENTORY.md`
- Local-only: `build/rendered/cna-party-book/`

- [ ] **Step 1: PDF 내용 계약을 추가한다**

`test_distribution_pdf_is_release_ready`의 `all_text` 검사 뒤에 아래를 추가한다.

```python
for expected in (
    "정해진 자리",
    "자리 교체",
    "조별 게임",
    "잘못된 선택",
    "좋은 선택",
    "대화 예시",
    "실전 과제",
):
    self.assertIn(expected, all_text)
for legacy in ("BAD MOVE", "BETTER MOVE", "SCRIPT", "MISSION"):
    self.assertNotIn(legacy, all_text)
```

`test_release_docs_register_the_fifth_book_and_its_sources`의 고정 `41`쪽 문자열 검사는 실제 PDF 바이트와 일치하는 인벤토리 행 검사로 교체한다.

```python
from hashlib import sha256
from pypdf import PdfReader

pdf_path = ROOT / "dist" / "pdf" / "CNA_파티의_주도권.pdf"
inventory_row = (
    "| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` | "
    f"{len(PdfReader(pdf_path).pages)} | {pdf_path.stat().st_size:,} | "
    f"`{sha256(pdf_path.read_bytes()).hexdigest()}` |"
)
self.assertIn(inventory_row, inventory)
```

- [ ] **Step 2: 기존 배포본을 대상으로 RED를 확인한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyArtifactTests.test_distribution_pdf_is_release_ready -v
```

Expected: 기존 PDF에 새 지정석 문구 또는 한글 카드 제목이 없어 실패한다.

- [ ] **Step 3: CNA 책만 다시 빌드하고 전체 산출물을 검증한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/project.py build cna-party-book
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/project.py verify all
```

Expected: `cna-party-book` 빌드가 성공하고 정식 PDF 다섯 종이 모두 검증된다. CNA PDF는 35~45쪽이다.

- [ ] **Step 4: 새 PDF의 인벤토리 값을 계산해 기록한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "from pathlib import Path; import hashlib; from pypdf import PdfReader; p=Path(r'dist/pdf/CNA_파티의_주도권.pdf'); print('| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` |', len(PdfReader(p).pages), '|', f'{p.stat().st_size:,}', '|', f'`{hashlib.sha256(p.read_bytes()).hexdigest()}`', '|')"
```

Expected: 완성된 Markdown 인벤토리 행 한 줄이 출력된다. `docs/ARTIFACT_INVENTORY.md`의 기존 `cna-party-book` 행을 출력된 한 줄로 정확히 교체한다.

- [ ] **Step 5: 전체 PDF를 렌더링하고 대표 페이지를 확인한다**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'build\rendered\cna-party-book' | Out-Null
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe' -r 150 -png 'dist\pdf\CNA_파티의_주도권.pdf' 'build\rendered\cna-party-book\page'
```

각 PNG를 연락 시트 또는 `view_image`로 확인한다. 반드시 다음 페이지 유형을 포함한다.

- 프롤로그의 지정석 첫 장면
- `GROUP FLOW` 도식
- `POSITIONING LOOP` 도식
- `잘못된 선택`과 `좋은 선택` 카드
- `대화 예시`가 있는 라포와 번호 교환 페이지
- `실전 과제` 카드
- 게임 접촉과 번호 교환 창을 설명하는 페이지
- 마지막 실행 카드와 복기표

검수 기준은 빈 페이지, 잘림, 겹침, 카드 분리, 한글 글리프 깨짐, 영어 표기 잔존이 모두 0건이다.

- [ ] **Step 6: 최종 회귀 검사를 새로 실행한다**

Run:

```powershell
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
& 'C:\Users\SuperNatural1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/project.py verify all
git diff --check
git status --short
```

Expected: 전체 테스트와 다섯 PDF 검증이 통과한다. 상태에는 이번 작업의 테스트·PDF·인벤토리 변경만 남고 임시 PNG는 Git 추적 대상이 아니다.

- [ ] **Step 7: 배포본을 커밋한다**

```powershell
git add tests/test_cna_party_project.py dist/pdf/CNA_파티의_주도권.pdf docs/ARTIFACT_INVENTORY.md
git commit -m "build: publish assigned-table CNA party edition"
```

커밋 뒤 `git status --short`가 비어 있어야 한다.
