# CNA 프롤로그 자연스러운 한국어 윤문 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `00-prologue.md`만 친근한 구어체와 담백한 교재 문체의 중간 톤으로 다시 써서 번역투를 없앤다.

**Architecture:** 장 제목, 세 개의 소제목, 레벨 테스트, FIELD NOTE와 교재 장치 설명은 그대로 유지한다. 실제 파티 장면과 구체적인 행동을 중심으로 문장을 다시 쓰고, 기존 Typst 조립 경로로 PDF를 재빌드해 프롤로그의 페이지 흐름을 확인한다.

**Tech Stack:** Markdown, Typst 0.14.x, Python `unittest`, 프로젝트 빌드·검증 스크립트

---

## File map

- Modify: `projects/cna-party-edition/manuscript/00-prologue.md` — 프롤로그 본문 정본
- Test unchanged: `tests/test_cna_party_project.py` — 제목, 최소 분량, 토큰과 최종 PDF 계약

### Task 1: 프롤로그 전면 윤문

**Files:**
- Modify: `projects/cna-party-edition/manuscript/00-prologue.md`
- Test: `tests/test_cna_party_project.py`

- [ ] **Step 1: 수정 전 원고 계약 검사를 실행한다**

Run:

```powershell
& 'C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyProjectTest.test_prologue_and_environment_are_self_contained -v
```

Expected: 기존 원고에서 `OK`.

- [ ] **Step 2: 프롤로그를 아래 원고로 교체한다**

```markdown
# 파티는 말보다 먼저 시작된다

파티에 들어서면 눈이 먼저 바빠진다. 누가 왔는지, 어디가 가장 활기찬지 훑다가 마음에 드는 사람이 보이면 시선이 그쪽에 멈춘다. 그때부터 머릿속에서는 혼자 회의가 시작된다. 지금 다가가도 될까? 첫마디는 뭐라고 하지? 조금 더 기다리는 게 낫지 않을까? 아직 인사 한 번 하지 않았는데 벌써 그 사람에게만 신경을 다 써 버린다.

파티가 익숙한 사람도 쉽게 놓치는 게 있다. 이 사람은 여기저기 자연스럽게 끼어들고 농담도 곧잘 한다. 밤새 많은 사람과 얘기했으니 잘 보냈다고 생각한다. 그런데 다음 날 떠올려 보면 정작 기억에 남는 대화가 없다. 상대가 편해졌는지, 대화를 더 이어 가고 싶어 했는지는 살피지 않은 채 자기가 말할 차례만 계속 만들었기 때문이다.

한쪽은 한 사람만 보느라 방 전체를 놓치고, 다른 쪽은 말하는 재미에 빠져 눈앞의 사람을 놓친다. 출발점은 달라도 필요한 연습은 같다. 먼저 주변을 보고, 가볍게 말을 건 뒤, 돌아오는 반응에 맞춰 다음 행동을 고르는 것이다. 이 책에서는 바로 그 연습을 한다. 낯선 자리에 들어가는 일이 아직 버겁더라도 괜찮다. 처음부터 능숙할 필요는 없다. 무엇을 볼지 알고 있으면 다음 행동은 훨씬 고르기 쉬워진다.

## 초보자와 무성과자가 같은 곳에서 무너지는 이유

초보자는 완벽한 순간이 오기를 기다린다. 누군가 잠깐 시선을 돌리기만 해도 자신을 싫어한다고 짐작하고, 준비한 문장이 생각나지 않으면 아예 움직이지 않는다. 상대의 반응을 직접 확인하기도 전에 머릿속에서 거절부터 당하는 셈이다.

파티에 자주 가지만 별다른 성과가 없는 사람은 반대로 쉴 새 없이 움직인다. 목소리를 키우고, 자기 이야기를 길게 하고, 반응이 약하면 더 센 농담을 꺼낸다. 문제는 행동량이 아니다. 눈앞의 사람이 웃고 있는지, 대화를 이어 가고 싶은지, 잠깐 쉬고 싶은지를 보지 않는 데 있다. 초보자와 경험자의 공통점은 사람보다 자기 머릿속 시나리오에 더 집중한다는 것이다.

자신의 습관부터 가볍게 확인해 보자. 들어가자마자 한 사람을 정해 두는가? 아는 사람 곁을 좀처럼 떠나지 못하는가? 잠깐 조용해지면 급하게 아무 말이나 꺼내는가? 상대의 반응이 식었는데도 하던 방식을 계속 밀어붙이는가? 하나라도 뜨끔한 항목이 있다면 그게 먼저 연습할 부분이다.

[[DIAGRAM:level_test]]

결과가 몇 단계인지는 그다지 중요하지 않다. 지금 무엇부터 해 보면 좋을지 고르면 된다. 주변을 잘 못 본다면 공간을 둘러보는 연습부터, 다가가는 데 시간이 오래 걸린다면 짧은 인사부터 시작하자. 혼자 말을 많이 하는 편이라면 상대의 말 속도와 표정을 한 번 더 보는 것으로도 충분하다.

## 파티는 동적 포지셔닝 게임이다

파티 분위기는 계속 바뀐다. 새 사람이 들어오면 시선이 한쪽으로 쏠리고, 누군가 던진 농담 하나에 어색함이 풀린다. 조용히 둘이 나누는 이야기에 주변 목소리가 낮아질 때도 있다. 여기서 말하는 포지셔닝은 거창한 기술이 아니다. 그때그때 자리에 필요한 역할을 알아보고 자연스럽게 맡는 것에 가깝다.

어떤 자리에는 먼저 인사를 건네는 사람이 필요하다. 말이 적은 사람이 어색하게 서 있다면 대화에 슬쩍 끼워 주는 사람이 반갑다. 이미 분위기가 한껏 오른 무리에서는 더 크게 말하기보다 잘 들어 주는 편이 낫고, 모두가 할 말을 찾지 못할 때는 짧은 질문 하나가 숨통을 틔워 준다. 결국 중요한 것은 대단한 첫마디가 아니라, 지금 이 자리에 무엇이 필요한지 알아차리는 눈이다.

[[CALLOUT:field|파티가 끝난 뒤 사람들은 정확한 대사보다, 당신과 있을 때 편했는지 즐거웠는지를 기억한다.]]

모두에게 좋은 인상을 남기려고 애쓸 필요는 없다. 애초에 마음대로 할 수 있는 일도 아니다. 대신 주변을 보고, 부담 없는 행동 하나를 해 보고, 상대의 반응을 살피자. 잘 맞으면 조금 더 이어 가고, 어색하면 속도를 늦추거나 자리를 바꾸면 된다. 이렇게 몇 번 직접 확인해 보면 자신감은 억지로 끌어올리지 않아도 따라온다.

## 이 책을 사용하는 법

이 책에는 네 가지 표시가 반복해서 나온다. **BAD MOVE**에서는 사람들이 흔히 하는 실수와 그 뒤에 벌어지는 일을 보여 준다. 잘못을 따지기 위해서가 아니라, 나도 모르게 반복하는 습관을 알아차리기 위한 부분이다. **BETTER MOVE**에는 같은 상황에서 부담을 덜 주면서 반응을 확인할 수 있는 방법을 담았다. 언제나 통하는 정답이라기보다 다음번에 한 번 써 볼 선택지라고 생각하면 된다.

**SCRIPT**는 통째로 외우는 대본이 아니다. 어느 정도 길이로, 얼마나 가볍게 말하면 되는지 보여 주는 예시다. 자기 말투에 맞게 바꾸되, 상대가 불편해하거나 선을 그으면 바로 멈춘다. **MISSION**은 읽은 내용을 현장에서 작은 행동으로 옮기는 과제다. 성공했는지를 따지기보다 실제로 해 봤는지를 기록하자. 짧은 시도를 여러 번 해 보는 편이 한 번의 화려한 성공보다 훨씬 많이 남는다.

한 장을 읽을 때 욕심내지 말고 딱 한 가지 행동만 고르자. 파티에서 직접 해 본 뒤, 집에 돌아와 무엇을 봤고 상대가 어떻게 반응했는지 두세 줄만 적으면 된다. 상대가 편한지, 대화를 더 이어 가고 싶은지 먼저 보고, 불편해하거나 거절하면 그 자리에서 멈춘다. 이 원칙만 지켜도 경험은 쌓이고 다음 파티는 조금 덜 낯설어진다. 이제 멋진 첫마디를 찾기 전에, 방부터 살펴보자.
```

- [ ] **Step 3: 원고 계약과 전체 테스트를 실행한다**

Run:

```powershell
& 'C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe' -m unittest tests.test_cna_party_project.CnaPartyProjectTest.test_prologue_and_environment_are_self_contained -v
& 'C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe' -m unittest discover -s tests -v
```

Expected: 프롤로그 검사를 포함한 전체 테스트가 `OK`.

- [ ] **Step 4: 책을 재빌드하고 제품 검증을 실행한다**

Run:

```powershell
& 'C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe' scripts/project.py build cna-party-book
& 'C:\Program Files\PostgreSQL\17\pgAdmin 4\python\python.exe' scripts/project.py verify cna-party-book
```

Expected: 빌드와 검증이 성공하고 PDF가 30~45쪽 범위에 남는다.

- [ ] **Step 5: 변경 범위와 문장을 확인한다**

Run:

```powershell
git diff --check
git diff --name-only HEAD
```

Expected: 구현 변경 파일은 `projects/cna-party-edition/manuscript/00-prologue.md` 하나이며 공백 오류가 없다.

- [ ] **Step 6: 윤문 결과를 커밋한다**

```powershell
git add projects/cna-party-edition/manuscript/00-prologue.md
git commit -m "edit: rewrite CNA party prologue in natural Korean"
```
