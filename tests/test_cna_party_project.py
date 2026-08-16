import json
import re
import unittest
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "cna-party-edition"


class CnaPartyManifestTests(unittest.TestCase):
    def test_manifest_registers_stable_deliverable(self):
        payload = json.loads((PROJECT / "project.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["slug"], "cna-party-edition")
        self.assertEqual(payload["title"], "파티의 주도권")
        self.assertEqual(
            payload["deliverables"],
            [
                {
                    "id": "cna-party-book",
                    "source": "typst/book.typ",
                    "output": "CNA_파티의_주도권.pdf",
                }
            ],
        )


class CnaPartyTypstContractTests(unittest.TestCase):
    def test_diagram_renderer_supports_required_visuals_and_cards(self):
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(encoding="utf-8")

        top_level_names = set(re.findall(r"(?m)^#let ([\w-]+)", diagrams))
        self.assertEqual(
            top_level_names,
            {
                "diagram-frame",
                "step",
                "party-map",
                "positioning-loop",
                "rapport-ladder",
                "influence-curve",
                "number-window",
                "level-test",
                "DIAGRAMS",
                "CALLOUTS",
                "render-rich",
            },
        )

        def map_keys(name):
            match = re.search(
                rf"(?ms)^#let {name} = \(\s*(.*?)^\)",
                diagrams,
            )
            self.assertIsNotNone(match, f"missing {name} map")
            return set(
                re.findall(
                    r"(?m)^\s*([a-z][a-z0-9_]*):\s*[^\n,]+,\s*$",
                    match.group(1),
                )
            )

        self.assertEqual(
            map_keys("DIAGRAMS"),
            {
                "party_map",
                "positioning_loop",
                "rapport_ladder",
                "influence_curve",
                "number_window",
                "level_test",
            },
        )
        self.assertEqual(
            map_keys("CALLOUTS"),
            {"field", "bad", "better", "frame", "mission"},
        )
        self.assertIn("#let render-rich(path)", diagrams)
        self.assertIn('panic("unknown diagram key: " + key)', diagrams)
        self.assertIn('panic("unknown callout kind: " + kind)', diagrams)

    def test_book_and_theme_expose_required_contract(self):
        book = (PROJECT / "typst" / "book.typ").read_text(encoding="utf-8")
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")

        for expected in (
            "파티의 주도권",
            "첫 대화부터 번호 교환까지",
            "PREDIC / SUPER NATURAL",
            "render-rich",
        ):
            self.assertIn(expected, book)

        for expected in (
            "#let book(",
            "#let part-divider(",
            "#let field-note(",
            "#let bad-move(",
            "#let better-move(",
            "#let frame-card(",
            "#let mission-card(",
        ):
            self.assertIn(expected, theme)

    def test_theme_exposes_only_the_supported_public_api(self):
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")
        top_level_names = set(re.findall(r"(?m)^#let ([\w-]+)", theme))

        self.assertEqual(
            top_level_names,
            {
                "lime",
                "lime-dark",
                "navy",
                "ink",
                "muted",
                "line",
                "paper",
                "bad",
                "bad-soft",
                "better",
                "better-soft",
                "blue-soft",
                "book",
                "part-divider",
                "field-note",
                "bad-move",
                "better-move",
                "frame-card",
                "mission-card",
            },
        )

    def test_cards_and_long_titles_have_stable_page_boundaries(self):
        book = (PROJECT / "typst" / "book.typ").read_text(encoding="utf-8")
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")

        self.assertEqual(theme.count("breakable: false"), 5)
        for title in (
            "들어가기 전에 이미 승부는 #linebreak() 시작된다",
            "참가자가 아니라 분위기의 #linebreak() 공급자가 되어라",
            "호감과 긴장감을 #linebreak() 의도적으로 설계하라",
        ):
            self.assertIn(title, book)
        self.assertIn(
            "[호감과 긴장감을 #linebreak() 의도적으로 설계하라]", theme
        )

    def test_body_paragraphs_keep_readable_rhythm(self):
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")

        self.assertIn(
            "size: 10.2pt,\n    fill: ink,\n    lang: \"ko\",\n    hyphenate: false,\n    tracking: 0.04pt,",
            theme,
        )
        self.assertIn(
            "set par(justify: true, leading: 0.74em, spacing: 1.28em)", theme
        )

    def test_numbered_dialogue_quotes_stay_atomic(self):
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")
        quote_renderer = re.search(
            r"(?ms)^  show quote\.where\(block: true\):.*?(?=^  show table)", theme
        )

        self.assertIsNotNone(quote_renderer)
        self.assertIn("let is-numbered-dialogue", quote_renderer.group(0))
        self.assertIn("breakable: not is-numbered-dialogue", quote_renderer.group(0))

    def test_chapter_end_missions_keep_their_context(self):
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(
            encoding="utf-8"
        )

        self.assertIn("KEEP_WITH_NEXT_START", diagrams)
        self.assertIn("KEEP_WITH_NEXT_END", diagrams)
        self.assertIn("render-kept-pair", diagrams)
        self.assertIn("block(breakable: false)", diagrams)
        self.assertIn("render-token-stream", diagrams)

        number_chapter = (
            PROJECT / "manuscript" / "05-number-exchange.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(number_chapter.count("[[KEEP_WITH_NEXT_START]]"), 1)
        self.assertEqual(number_chapter.count("[[KEEP_WITH_NEXT_END]]"), 1)
        kept_tail = re.search(
            r"(?m)^\[\[KEEP_WITH_NEXT_START\]\]\s*\n"
            r"([^\n]+)\n\n"
            r"(\[\[CALLOUT:mission\|[^\n]+\]\])\s*\n"
            r"\[\[KEEP_WITH_NEXT_END\]\]\s*$",
            number_chapter,
        )
        self.assertIsNotNone(kept_tail)
        self.assertLess(len(kept_tail.group(1)), 500)

    def test_level_test_uses_the_host_led_transition_model(self):
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(
            encoding="utf-8"
        )
        level_test = re.search(
            r"(?ms)^#let level-test = .*?(?=^#let DIAGRAMS)", diagrams
        )

        self.assertIsNotNone(level_test)
        self.assertIn("운영자의 안내에 맞춰 전환한다", level_test.group(0))
        self.assertNotIn("다음 장면으로 짧게 이동한다", level_test.group(0))


class CnaPartyManuscriptTests(unittest.TestCase):
    DIAGRAM_KEYS = {
        "party_map",
        "positioning_loop",
        "rapport_ladder",
        "influence_curve",
        "number_window",
        "level_test",
    }
    CALLOUT_KINDS = {"field", "bad", "better", "frame", "mission"}

    def assert_chapter(self, filename, minimum_chars, headings, tokens):
        chapter = (PROJECT / "manuscript" / filename).read_text(encoding="utf-8")

        self.assertGreaterEqual(len(chapter), minimum_chars)
        for heading in headings:
            self.assertIn(heading, chapter)
        for token in tokens:
            self.assertIn(token, chapter)

    def assert_valid_markers(self, text):
        marker_pattern = re.compile(
            r"(?:\[\[DIAGRAM:([a-z][a-z0-9_]*)\]\]|"
            r"\[\[CALLOUT:([a-z][a-z0-9_]*)\|([^\[\]\r\n]+)\]\]|"
            r"(\[\[PAGEBREAK\]\])|"
            r"\[\[(KEEP_WITH_NEXT_(?:START|END))\]\])"
        )
        marker_lines = [
            line for line in text.splitlines() if "[[" in line or "]]" in line
        ]

        self.assertTrue(marker_lines)
        for line in marker_lines:
            self.assertEqual(line, line.strip())
            match = marker_pattern.fullmatch(line)
            self.assertIsNotNone(match, f"invalid manuscript marker: {line}")
            diagram_key, callout_kind, _, pagebreak, keep_marker = match.groups()
            if pagebreak or keep_marker:
                continue
            if diagram_key:
                self.assertIn(diagram_key, self.DIAGRAM_KEYS)
            else:
                self.assertIn(callout_kind, self.CALLOUT_KINDS)

    def introduction_rows(self, text):
        lines = text.splitlines()
        header_index = lines.index("| 잘못된 선택 | 좋은 선택 |")
        self.assertEqual(lines[header_index + 1], "| --- | --- |")

        rows = []
        for line in lines[header_index + 2 :]:
            if not line.startswith("|"):
                break
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            self.assertEqual(len(cells), 2)
            rows.append(cells)
        return rows

    def test_prologue_and_environment_are_self_contained(self):
        self.assert_chapter(
            "00-prologue.md",
            1600,
            (
                "# 파티는 말보다 먼저 시작된다",
                "## 파티에서 연애를 하기 어려운 이유",
                "## 파티는 동적 포지셔닝 게임이다",
                "## 이 책을 사용하는 법",
            ),
            ("[[DIAGRAM:level_test]]", "[[CALLOUT:field|"),
        )
        self.assert_chapter(
            "01-environment.md",
            3200,
            (
                "# 공간을 먼저 읽어라",
                "## 자리 배치를 답답하게 느끼지 말자",
                "## 경쟁자를 분석하는 기준",
                "## 내가 마음에 드는 사람의 상태를 읽는 법",
                "## 외모는 입장권일 뿐이다",
                "## 자기소개는 정보를 말하는 시간이 아니다",
            ),
            (
                "[[DIAGRAM:party_map]]",
                "[[CALLOUT:bad|",
                "[[CALLOUT:better|",
                "[[CALLOUT:mission|",
            ),
        )

    def test_opening_uses_assigned_groups_and_host_led_rotation(self):
        prologue = (PROJECT / "manuscript" / "00-prologue.md").read_text(
            encoding="utf-8"
        )
        environment = (PROJECT / "manuscript" / "01-environment.md").read_text(
            encoding="utf-8"
        )
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(encoding="utf-8")

        for expected in (
            "정해진 자리",
            "현재 조",
            "자리 교체",
            "조별 게임",
            "여러 사람이 정해진 방향으로 자리를 옮기고",
            "함께 앉는 조합이 바뀐다",
            "다른 조원에게 말할 차례",
            "현재 조의 흐름부터 읽어 보자",
        ):
            self.assertIn(expected, prologue)
        for expected in (
            "현재 조",
            "교체 방향",
            "게임 흐름",
            "자리 배치를 장애물로 생각하지 말자",
            "보통 파티에서는 게임을 자기 조끼리만 시키지 않는다",
            "다른 테이블과 교류할 수 있는 시간",
            "가까운 조에 마음에 드는 사람이 있다면",
            "살짝 눈을 맞추는 것",
            "여러 사람이 정해진 순서대로 자리를 옮기며",
            "테이블 조합이 바뀐다",
        ):
            self.assertIn(expected, environment)
        for forbidden in (
            "## 자리 배치는 대화보다 솔직하다",
            "처음에는 세 개의 렌즈만 쓴다",
            "둘째는 **다음 전환**이다",
            "파티는 사회적 지능",
            "이 지도는 통제 계획이 아니다",
        ):
            self.assertNotIn(forbidden, environment)
        for expected in ("현재 조", "다음 전환", "열린 접점"):
            self.assertIn(expected, diagrams)

        for forbidden in (
            "지금 다가가도 될까?",
            "마음에 드는 사람을 찾아 곧장 걷지 말자",
            "방을 천천히 한 바퀴 바라본다",
        ):
            self.assertNotIn(forbidden, prologue + "\n" + environment)
        for forbidden in (
            "쉴 새 없이 움직인다",
            "아는 사람 곁을 좀처럼 떠나지 못하는가",
            "방부터 살펴보자",
            "조가 통째로 바뀌고",
            "조 전체가 이동하고",
        ):
            self.assertNotIn(forbidden, prologue)

    def test_positioning_chapter_builds_social_value(self):
        headings = [
            "# 분위기를 공급하는 사람이 되어라",
            "## 특정성에서 빠져나오기",
            "## 기버는 착한 사람이 아니라 주도하는 사람이다",
            "## 셀프 어뮤즈",
            "## 서브 호스트 프레임",
            "## 거절을 사회적 굳은살로 바꾸기",
        ]
        self.assert_chapter(
            "02-positioning.md",
            3500,
            headings,
            ["[[DIAGRAM:positioning_loop]]", "[[CALLOUT:frame|", "[[CALLOUT:mission|"],
        )

        chapter = (PROJECT / "manuscript" / "02-positioning.md").read_text(
            encoding="utf-8"
        )
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(encoding="utf-8")
        heading_positions = [chapter.index(heading) for heading in headings]
        self.assertEqual(heading_positions, sorted(heading_positions))

        for expected in (
            "사람들은 당신이 자신을 소개하기 전부터 무의식적으로 이 차이를 읽는다",
            "목표는 인기 있는 사람인 척하는 것이 아니다",
            "유창한 말솜씨",
            "주변 사람을 즐겁게 만드는 사람",
            "잘생긴 사람",
            "주위 사람들을 챙겨 주고 편안하게 해 주는 사람",
            "같이 있으면 긴장이 낮아지고 말하기 쉬워진다는 신호",
        ):
            self.assertIn(expected, chapter)

        self.assertIn(
            "이 책에서 ‘특정성’은 한 사람을 유일한 기회처럼 여기면서 "
            "관심과 행동이 그 사람에게 고정되는 상태를 뜻한다.",
            chapter,
        )
        self.assertIn(
            "[[CALLOUT:frame|당신의 위치는 스스로 주장해서 생기지 않는다. "
            "다른 사람들의 반응이 반복해서 당신을 중심으로 가리킬 때 생긴다.]]",
            chapter,
        )
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

        positioning_loop = re.search(
            r"(?ms)^#let positioning-loop = .*?(?=^#let rapport-ladder)", diagrams
        )
        self.assertIsNotNone(positioning_loop)
        for expected in ("관찰", "기여", "반응", "전환"):
            self.assertIn(expected, positioning_loop.group(0))
        for legacy in ('"공급"', '"이동"'):
            self.assertNotIn(legacy, positioning_loop.group(0))

        for expected in (
            "서로 모르는 두 사람을 연결한다",
            "어색한 정적을 수리한다",
            "상황에 맞는 작은 편의를 제공한다",
            "사람들을 편안하게 해 주라고 했다",
            "그 자리를 주도하는 것은 명백히 피곤한 일이다",
            "그 피곤한 일을 먼저 감당하는 사람이 조의 기준을 만든다",
            "어색함을 낮추고 말할 차례를 만들어 주는 사람",
            "사람들이 다시 기대는 중심",
            "사람들이 기대한다는 것은 호감을 사는 행동 중 하나다",
            "말을 꺼내도 안전하다",
            "작은 안심이 반복되면서 방향을 잡는다",
            "외모, 말솜씨, 농담도 호감으로 번역된다",
            "아래에 나와 있는 세 가지 행동만 하더라도 충분히 그런 존재가 될 수 있다",
            "서비스 스태프로 포지셔닝된다",
            "명확한 거절이나 불편한 표정은 더 좋은 기술을 시도하라는 신호가 아니라 "
            "멈추라는 신호다",
        ):
            self.assertIn(expected, chapter)
        self.assertNotIn("미세 행동", chapter)

        giver_start = chapter.index("## 기버는")
        giver_end = chapter.index("## 셀프 어뮤즈")
        giver = chapter[giver_start:giver_end]
        subhost_start = chapter.index("## 서브 호스트 프레임")
        subhost_end = chapter.index("## 거절을")
        subhost = chapter[subhost_start:subhost_end]
        refusal_start = chapter.index("## 거절을")
        refusal = chapter[refusal_start:]

        self.assertIn("소개한 뒤 말을 줄이고 둘의 대화를 듣는다", giver)
        self_amuse_start = chapter.index("## 셀프 어뮤즈")
        self_amuse_end = chapter.index("## 서브 호스트 프레임")
        self_amuse = chapter[self_amuse_start:self_amuse_end]
        for expected in (
            "게임 생각보다 진심으로 하게 되네요",
            "누군가 웃으며 내 말을 받아주면, 한마디 더 던진다",
            "반응이 약하면 미소 짓고 다른 주제로 넘어간다",
            "내 기분을 남의 반응에 맡기지 않고",
            "내 재미를 남에게 강제로 먹이지도 않는 것이다",
            "혼자서도 즐겁고 편안한 사람은 반응을 구걸하지 않는다",
            "지금 웃겨야 해",
            "사람들의 반응에 눈치를 살핀다",
            "호응이 없더라도 자신의 리듬을 잃지 않는 것이다",
        ):
            self.assertIn(expected, self_amuse)
        for forbidden in (
            "이 테이블만 유난히 디저트 전략회의 분위기네요",
            "박수의 크기",
            "눈이 사람들의 승인을 확인하고",
        ):
            self.assertNotIn(forbidden, self_amuse)
        for expected in (
            "말이 적던 사람이 참여했는가",
            "말할 차례가 고르게 돌았는가",
            "개입을 멈춘 뒤에도 대화가 편하게 이어졌는가",
            "말할 차례를 넘긴 뒤에도",
        ):
            self.assertIn(expected, subhost)
        self.assertIn("질문이나 개입을 멈추고", refusal)
        self.assertIn("다른 조원에게 말할 차례를 넘긴다", refusal)
        for expected in (
            "합석을 제안했는데 “저희끼리 이야기 중이에요”라는 말을 들을 수 있고",
            "“아, 편하게 이야기하세요”라고 말한 뒤",
        ):
            self.assertIn(expected, refusal)
        for old_wording in (
            "소개를 제안했는데",
            "저희끼리 얘기 중이에요",
            "편하게 얘기하세요",
        ):
            self.assertNotIn(old_wording, refusal)
        self.assertIn(
            "아무리 내가 좋은 마음으로 사람들에게 말을 걸고, 분위기를 바꿔 보려고 해도 "
            "모두에게 환영받지는 못한다",
            refusal,
        )
        self.assertNotIn("모든 개입이 환영받지는 않는다", refusal)
        for expected in (
            "파티 경험은 많지만 별다른 성과가 없는 사람",
            "오래 말한 것이 곧 좋은 흐름은 아니다",
            "진행자가 자리 교체를 안내하거나",
            "게임이 끝나 다음 순서로 넘어가야 하는데도",
            "어색하게 붙잡지 않고 자연스럽게 마무리했는지",
        ):
            self.assertIn(expected, refusal)
        for confusing_term in ("운영자 주도 전환", "전환을 편안하게 맞았는가"):
            self.assertNotIn(confusing_term, refusal)

        for forbidden in (
            "한 걸음 물러나",
            "몸을 반걸음 뒤로",
            "한발 물러난 뒤",
            "자리를 비운다",
            "다음 자리로 이동",
            "저쪽에 다녀온다",
            "사회적 증거",
            "더 오래 기억된다",
        ):
            self.assertNotIn(forbidden, chapter)

        mission = re.search(r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*$", chapter)
        self.assertIsNotNone(mission)
        for expected in ("현재 조", "긍정적인 상호작용 세 번", "다음 전환"):
            self.assertIn(expected, mission.group(1))

    def test_rapport_chapter_turns_observation_into_conversation(self):
        headings = [
            "# 상대의 주파수 안으로 들어가라",
            "## 말을 걸기 전과 후에 볼 것",
            "## 페이싱은 흉내가 아니다",
            "## 감정에서 경험까지 내려가는 네 층",
            "## 스몰토크는 역추적이다",
            "## 5감을 6감으로 바꾸는 법",
            "## 첫 대화 전체 예시",
        ]
        self.assert_chapter(
            "03-rapport.md",
            4800,
            headings,
            [
                "[[DIAGRAM:rapport_ladder]]",
                "[[CALLOUT:bad|",
                "[[CALLOUT:better|",
                "[[CALLOUT:mission|",
            ],
        )

        chapter = (PROJECT / "manuscript" / "03-rapport.md").read_text(
            encoding="utf-8"
        )
        diagrams = (PROJECT / "typst" / "diagrams.typ").read_text(
            encoding="utf-8"
        )
        heading_positions = [chapter.index(heading) for heading in headings]
        self.assertEqual(heading_positions, sorted(heading_positions))

        rapport_ladder = re.search(
            r"(?ms)^#let rapport-ladder = .*?(?=^#let influence-curve)",
            diagrams,
        )
        self.assertIsNotNone(rapport_ladder)
        self.assertEqual(
            re.findall(r"fill: navy\)\[([^\]]+)\]", rapport_ladder.group(0)),
            ["현재 사실", "선호", "감정", "개인 경험"],
        )

        self.assertRegex(
            chapter,
            re.escape(
                "네 층은 **현재 사실 → 선호 → 감정 → 개인 경험** 순서로 내려간다."
            )
            + r"[^\n]*\n\n"
            + re.escape("[[DIAGRAM:rapport_ladder]]"),
        )
        for cue in (
            "말을 걸기 전에는 목소리와 시선만 본다",
            "여러 사람이 함께 듣는 열린 대화",
            "조 전체에 먼저 말을 건다",
            "말을 건 뒤에는 첫 반응을 본다",
            "말을 보태거나 질문을 돌려주면",
            "짧게 대답한 뒤 시선이 돌아가면",
            "눈이 마주쳤다고 호감이 있다는 뜻은 아니다",
            "아까 게임 이야기예요?",
            "편하게 이야기하세요",
            "목소리와 시선 확인 → 첫 반응 확인 → 감정 단서 추적 → 짧은 자기 공개",
        ):
            self.assertIn(cue, chapter)
        for overcomplicated_cue in (
            "반응 지연",
            "호흡",
            "여섯 단서",
            "몸이 대화 쪽으로 열려 있는가",
            "세 가지 중 두 가지",
            "두 가지 이상이 닫혀",
            "## 말보다 먼저 상태를 읽는다",
            "세 단서 관찰",
        ):
            self.assertNotIn(overcomplicated_cue, chapter)
        for state in ("고에너지", "조심스러운 상태", "피곤한 상태", "사회적으로 포화된 상태"):
            self.assertIn(state, chapter)
        for warning in ("동작을 기계적으로 따라 하는 것", "페이싱이 아니다", "조종당하는 느낌"):
            self.assertIn(warning, chapter)

        bad = re.search(r"\[\[CALLOUT:bad\|([^\n]+)\]\]", chapter)
        better = re.search(r"\[\[CALLOUT:better\|([^\n]+)\]\]", chapter)
        self.assertIsNotNone(bad)
        self.assertIsNotNone(better)
        for expected in ("사실", "연속 질문", "면접"):
            self.assertIn(expected, bad.group(1))
        for expected in ("감정 단서 하나", "따라간", "내 이야기"):
            self.assertIn(expected, better.group(1))

        for example in ("빛의 예", "음악의 예", "밀도의 예"):
            self.assertIn(example, chapter)
        self.assertIn("> **대화 예시**", chapter)
        for beat in ("[첫 반응 확인]", "[페이싱]", "[감정 질문]", "[자기 공개]", "[종료]"):
            self.assertIn(f"> **{beat}**", chapter)
        emotional_question = re.search(
            r"> \*\*\[감정 질문\]\*\* (?P<annotation>[^\n]+)\n>\n"
            r"> 나: “(?P<question>[^”]+)”",
            chapter,
        )
        self.assertIsNotNone(emotional_question)
        for expected in ("상태 단서", "지금의 기분"):
            self.assertIn(expected, emotional_question.group("annotation"))
        for expected in ("지친", "숨통이 트인"):
            self.assertIn(expected, emotional_question.group("question"))
        self.assertIn("반응이 낮을 때의 종료 분기", chapter)
        self.assertIn("설득해서 뒤집지 않는다", chapter)

        mission = re.search(r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*$", chapter)
        self.assertIsNotNone(mission)
        for expected in ("말을 걸기 전에", "목소리와 시선", "조 전체", "첫 반응"):
            self.assertIn(expected, mission.group(1))
        self.assertNotIn("관찰 세 가지", mission.group(1))
        self.assertNotIn("[[PAGEBREAK]]", chapter)

    def test_rapport_and_influence_use_rotation_windows(self):
        rapport = (PROJECT / "manuscript" / "03-rapport.md").read_text(
            encoding="utf-8"
        )
        influence = (PROJECT / "manuscript" / "04-influence.md").read_text(
            encoding="utf-8"
        )

        for expected in ("새 조", "조별 게임", "게임 직후"):
            self.assertIn(expected, rapport)
        for expected in ("조 전체", "자리 교체", "매달리지"):
            self.assertIn(expected, influence)
        for boundary in (
            "게임 규칙 안에서 상대도 손을 내밀거나 분명히 함께 동작할 때만",
            "규칙상 동작이어도 상대가 참여하지 않으면 생략한다",
            "몸을 피하거나 멈추면",
            "호감의 증거",
            "접촉을 반복하지 않는다",
            "멀리서",
            "상태를 단정하지 않는다",
            "다음 자리 교체",
            "다른 조원이 말을 시작하면 질문을 멈추고 조 전체의 흐름으로 돌아가 듣는다",
            "더 묻지 않고 다른 조원의 이야기를 듣는다",
        ):
            self.assertIn(boundary, rapport)
        self.assertLess(rapport.index("저는 지연이에요"), rapport.index("지연 씨"))
        self.assertIn("압박을 주는 카운트다운으로 사용하지 않는다", influence)
        self.assertIn("다음 게임도 같은 조가 된다면", influence)
        for forbidden in (
            "답할 수 있는 거리에서 옆 공간을 비워 둔 채 시작한다",
            "나 친구들한테도 인사하고 올게요. 조금 있다가 동선 겹치면 다시 봐요",
            "필요한 동안 저는 제 일행 쪽에 있을게요",
            "규칙이 요구하거나",
            "말할 차례를 넘길게요",
            "말할 차례를 넘겼",
            "다른 조원에게 말할 차례가 오면 그 흐름을 넘기고",
            "다음 조별 게임에서도",
        ):
            self.assertNotIn(forbidden, rapport + "\n" + influence)

    def test_influence_chapter_keeps_strategy_and_boundaries_together(self):
        headings = [
            "# 호감과 긴장감을 의도적으로 설계하라",
            "## 희소성은 바쁜 척이 아니다",
            "## 프레임을 먼저 제시하는 사람이 해석을 만든다",
            "## 자격 부여",
            "## 가벼움 뒤에 반전을 배치하라",
            "## 미래 투사는 약속이 아니라 장면이다",
            "## 긴장감을 회수하는 법",
        ]
        self.assert_chapter(
            "04-influence.md",
            4800,
            headings,
            [
                "[[DIAGRAM:influence_curve]]",
                "[[CALLOUT:frame|",
                "[[CALLOUT:bad|",
                "[[CALLOUT:better|",
                "[[CALLOUT:mission|",
            ],
        )

        chapter = (PROJECT / "manuscript" / "04-influence.md").read_text(
            encoding="utf-8"
        )
        heading_positions = [chapter.index(heading) for heading in headings]
        self.assertEqual(heading_positions, sorted(heading_positions))

        exact_frame = (
            "[[CALLOUT:frame|호감은 많이 주는 사람이 이기는 게임이 아니다. 상대가 "
            "당신의 관심을 얻기 위해 조금씩 투자하게 만드는 구조가 중요하다.]]"
        )
        self.assertEqual(chapter.count(exact_frame), 1)
        for lever in ("해석", "주의", "투자", "타이밍"):
            self.assertIn(lever, chapter)

        for scarcity_guard in (
            "선택적으로 주의를 쓰고 한 사람을 독점하지 않을 의향",
            "바쁜 척",
            "일정을 지어내는 것",
            "벌주듯 관심을 거두는 것",
        ):
            self.assertIn(scarcity_guard, chapter)
        for qualification_guard in ("외모 칭찬", "태도·선택·기준"):
            self.assertIn(qualification_guard, chapter)

        self.assertRegex(
            chapter,
            re.escape("영향력은 **통제된 상승 리듬**으로 만든다.")
            + r"[^\n]*\n\n"
            + re.escape("[[DIAGRAM:influence_curve]]"),
        )
        self.assertEqual(chapter.count("[[PAGEBREAK]]"), 1)

        sequence = (
            "장난스러운 관찰",
            "기준/프레임",
            "자격 질문",
            "획득한 인정",
            "반전",
            "함께하는 장면",
        )
        sequence_positions = [chapter.index(beat) for beat in sequence]
        self.assertEqual(sequence_positions, sorted(sequence_positions))
        practical_beats = [
            f"> **{number}. {beat}**"
            for number, beat in enumerate(sequence, start=1)
        ]
        practical_positions = [chapter.index(beat) for beat in practical_beats]
        self.assertEqual(practical_positions, sorted(practical_positions))

        self.assertIn("계속 도전하면 경멸로 들리고 안전감이 낮아진다", chapter)
        self.assertIn("인정만 계속하면 긴장감이 사라진다", chapter)
        self.assertNotIn("검증만 계속하면", chapter)
        self.assertIn("동의를 만들어 내는 장치가 아니다", chapter)
        self.assertIn("다른 사람의 선택을 무효로 하거나", chapter)

        repair_steps = (
            "갑자기 평가받는 기분인데요?",
            "제가 방금 사람을 평가하는 틀을 씌웠네요. 그 말은 거둘게요.",
            "누가 어색해 보이면 제가 뭐라도 정리하면서 말을 걸 계기를 만드는 편이에요.",
            "> **3. 자격 질문**",
            "얼마나 지켜본 뒤 말을 거는 편이에요?",
            "조금 기다려 봐요.",
        )
        repair_positions = [chapter.index(step) for step in repair_steps]
        self.assertEqual(repair_positions, sorted(repair_positions))
        self.assertNotIn("정정권은 드릴게요", chapter)

        for explanation in (
            "첫 프레임 시도는 상대를 불편하게 했다",
            "화자는 이를 즉시 인정하고 거두었다",
            "배려와 경계의 주제는 상대가 자발적으로 다시 열고 나서야 이어 갔다",
        ):
            self.assertIn(explanation, chapter)
        self.assertNotIn(
            "프레임은 대화를 ‘배려를 보는 시간’으로 바꿨다", chapter
        )

        self.assertNotIn("필요한 동안 저는 제 일행 쪽에 있을게요", chapter)
        self.assertIn("자리 교체가 안내되면", chapter)
        self.assertNotIn("잠깐 인사하고 와도 괜찮아요", chapter)

        hard_boundary = (
            "상대의 판단력이 흐려진 상태, 명시적인 거절, 눈에 보이는 불안이나 고통 중 "
            "하나라도 확인되면 모든 기술은 즉시 끝난다."
        )
        self.assertEqual(chapter.count(hard_boundary), 1)

        mission = re.search(r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*$", chapter)
        self.assertIsNotNone(mission)
        for expected in ("자격 질문 하나", "침묵", "밀어붙이지"):
            self.assertIn(expected, mission.group(1))

    def test_closing_chapters_end_at_number_exchange(self):
        number_headings = [
            "# 고점에서 번호를 교환하라",
            "## 번호보다 먼저 명분을 만든다",
            "## 교환 창이 열렸다는 신호",
            "## 짧게 제안하고 설명하지 않는다",
            "## 거절을 처리하는 가장 좋은 방식",
            "## 교환 뒤에는 진행으로 돌아간다",
        ]
        checklist_headings = [
            "# 다음 파티를 위한 실행 카드",
            "## 입장 전",
            "## 첫 10분",
            "## 첫 대화",
            "### 영향 설계",
            "### 게임 안에서 확인할 것",
            "## 번호 교환",
            "## 집에 돌아온 뒤 복기",
        ]
        self.assert_chapter(
            "05-number-exchange.md",
            2600,
            number_headings,
            [
                "[[DIAGRAM:number_window]]",
                "[[CALLOUT:bad|",
                "[[CALLOUT:better|",
                "[[CALLOUT:mission|",
            ],
        )
        self.assert_chapter(
            "06-checklist.md",
            1200,
            checklist_headings,
            ["[[DIAGRAM:level_test]]", "[[CALLOUT:field|"],
        )

        number_chapter = (PROJECT / "manuscript" / "05-number-exchange.md").read_text(
            encoding="utf-8"
        )
        checklist = (PROJECT / "manuscript" / "06-checklist.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            [number_chapter.index(heading) for heading in number_headings],
            sorted(number_chapter.index(heading) for heading in number_headings),
        )
        self.assertEqual(
            [checklist.index(heading) for heading in checklist_headings],
            sorted(checklist.index(heading) for heading in checklist_headings),
        )
        for stage_heading in ("### 영향 설계", "### 게임 안에서 확인할 것"):
            heading_line = re.search(
                rf"(?m)^{re.escape(stage_heading)}\s*$", checklist
            )
            self.assertIsNotNone(heading_line, stage_heading)
            next_list = checklist.find("- [ ]", heading_line.end())
            next_heading = checklist.find("\n##", heading_line.end())
            self.assertGreater(next_list, heading_line.end(), stage_heading)
            self.assertTrue(
                next_heading == -1 or next_list < next_heading, stage_heading
            )

        self.assertRegex(
            number_chapter,
            r"세 조건은[^\n]*상호 투자[^\n]*공유 맥락[^\n]*"
            r"다음 단계의 이유[^\n]*\n\n"
            + re.escape("[[DIAGRAM:number_window]]"),
        )
        for signal_heading in ("### 초록 신호", "### 애매한 신호"):
            self.assertIn(signal_heading, number_chapter)
        for green_signal in (
            "질문을 돌려준다",
            "조 전체의 이야기가 한 차례 오간 뒤",
            "게임 차례가 끝난 뒤",
            "공유한 소재",
        ):
            self.assertIn(green_signal, number_chapter)
        for ambiguous_signal in ("예의상 웃음", "가까이 서 있음", "시선이 자주 마주침"):
            self.assertIn(ambiguous_signal, number_chapter)
        self.assertIn("어떤 신호도 동의를 보장하지 않는다", number_chapter)

        script_roles = (
            "함께 갈 장소",
            "공유한 관심사",
            "장난의 다음 편",
            "맥락이 분명할 때의 직접 제안",
            "초보자를 위한 부드러운 제안",
        )
        script_labels = []
        for number, role in enumerate(script_roles, start=1):
            match = re.search(
                rf"(?m)^> \*\*대화 예시 {number}[^\n]*{re.escape(role)}\*\*$",
                number_chapter,
            )
            self.assertIsNotNone(match, role)
            script_labels.append(match.start())
        self.assertEqual(
            script_labels,
            sorted(script_labels),
        )

        bad = re.search(r"\[\[CALLOUT:bad\|([^\n]+)\]\]", number_chapter)
        better = re.search(r"\[\[CALLOUT:better\|([^\n]+)\]\]", number_chapter)
        self.assertIsNotNone(bad)
        self.assertIsNotNone(better)
        for failure in ("장황하게 설명", "애원", "거절 뒤 협상"):
            self.assertIn(failure, bad.group(1))
        for improvement in ("한 문장", "선택권", "멈춘다"):
            self.assertIn(improvement, better.group(1))

        for exchange_window in (
            "게임 직후",
            "자리 교체 직전",
            "음료를 받는 쉬는 시간",
            "행사 종료 전",
        ):
            self.assertIn(exchange_window, number_chapter)
        self.assertIn(
            "전환은 만나는 조합을 바꾸며, 같은 사람을 다시 만날 수도 있고 아닐 수도 있다",
            number_chapter,
        )
        for guaranteed_or_free_movement_signal in (
            "운영자가 만든 전환 안에서 다시 만난다",
            "누군가 끼어들어도",
            "몸을 돌려 떠날 수 있는 순간에도",
        ):
            self.assertNotIn(guaranteed_or_free_movement_signal, number_chapter)
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
        self.assertIn("번호가 위로 상품이 된다", number_chapter)

        exit_section = number_chapter[
            number_chapter.index("## 교환 뒤에는 진행으로 돌아간다") :
        ]
        for mutual_exit_guard in (
            "상대가 새 질문이나 주제를 꺼내면 그대로 이어가도 좋다",
            "벌주는 행동",
            "기계적인 퇴장",
            "철수 전술",
        ):
            self.assertIn(mutual_exit_guard, exit_section)
        self.assertNotIn("상대가 먼저 새 질문을 꺼내면 짧게 답", number_chapter)
        self.assertIn(
            "나: “알겠어요. 말해 줘서 고마워요.”",
            number_chapter,
        )
        self.assertNotIn("남은 시간 즐겁게 보내요", number_chapter)
        self.assertIn(
            "상대가 새 질문이나 주제를 꺼내면 그대로 이어가도 좋다",
            exit_section,
        )
        self.assertNotIn("진짜 새로운 질문", exit_section)

        self.assertRegex(
            number_chapter,
            r"이 책의 실전 범위는 여기까지다[^\n]*번호 교환[^\n]*"
            r"현재 진행으로 돌아간다",
        )
        self.assertIn(
            "이 카드는 연락처를 교환하고 현장을 정리하는 데서 멈춘다.",
            checklist,
        )
        operational_follow_up = (
            r"(?im)^> \*\*(?:대화 예시|예시)[^\n]*"
            r"(?:카카오톡|카톡|DM|디엠|후속 연락|데이트|성적 에스컬레이션)",
            r"(?im)^- \[ \][^\n]*"
            r"(?:카카오톡|카톡|DM|디엠|후속 연락|데이트|만남 일정|스킨십)",
            r"(?:카카오톡|카톡|DM|디엠)[^\n]{0,50}"
            r"(?:보내라|보낸다|보내세요|작성하라|써라)",
            r"(?:데이트|만남)[^\n]{0,30}(?:일정|시간|장소)[^\n]{0,30}"
            r"(?:정하라|정한다|잡아라|잡는다|제안하라)",
            r"(?:연락|메시지)[^\n]{0,30}(?:주기|간격|몇 시간|다음 날)"
            r"[^\n]{0,30}(?:하라|한다|보내라|보낸다)",
            r"(?:성적 에스컬레이션|스킨십)[^\n]{0,40}"
            r"(?:시도하라|시도한다|진행하라|진행한다|단계)",
        )
        closing_text = number_chapter + "\n" + checklist
        for pattern in operational_follow_up:
            self.assertNotRegex(closing_text, pattern)

        mission = re.search(
            r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*"
            r"\[\[KEEP_WITH_NEXT_END\]\]\s*$",
            number_chapter,
        )
        self.assertIsNotNone(mission)
        for expected in ("이어갈 이유를 한 문장", "말한 뒤에만", "번호 교환"):
            self.assertIn(expected, mission.group(1))

        for section_index, heading in enumerate(checklist_headings[1:], start=1):
            start = checklist.index(heading) + len(heading)
            if section_index + 1 < len(checklist_headings):
                end = checklist.index(checklist_headings[section_index + 1])
            else:
                end = len(checklist)
            self.assertIn("- [ ]", checklist[start:end], heading)

        for required_item in (
            "복장",
            "현재 조에 기여",
            "운영자의 자리 교체",
            "게임 접촉이 상호적",
            "어느 전환에서 만났는가",
            "상태 단서",
            "페이싱",
            "감정 단서",
            "자기 공개",
            "기준",
            "자격 부여",
            "반전",
            "긴장 해제",
            "상호 투자",
            "공유 맥락",
            "다음 이유",
            "짧게 요청",
        ):
            self.assertIn(required_item, checklist)
        self.assertIn("| 복기 항목 | 기록 |", checklist)
        for debrief_row in (
            "| 만난 전환 | 자리 교체 뒤 새 조에 합류했을 때 |",
            "| 현재 조에 기여한 행동 | 게임 규칙을 확인하고 말이 끊긴 사람에게 질문 하나를 건넸다 |",
            "| 게임 접촉이 상호적이었는가 | 해당 없음 — 이 장면에서는 접촉하지 않았다 |",
            "| 다음 실험 | 다음에도 이름을 먼저 기억해 부르기 |",
        ):
            self.assertIn(debrief_row, checklist)
        self.assertNotIn(
            "| 만난 전환 | 현재 조에 기여한 행동 | 게임 접촉이 상호적이었는가 | 다음 실험 |",
            checklist,
        )
        self.assertIn("해당 없음 — 이 장면에서는 접촉하지 않았다", checklist)
        for old_phrase in (
            "방의 지도를 그리고 사회적 중심",
            "관찰 → 공급 → 반응 → 이동",
            "마무리 한 줄을 남기고 이동한다",
        ):
            self.assertNotIn(old_phrase, checklist)

        game_section = checklist[
            checklist.index("### 게임 안에서 확인할 것") : checklist.index("## 번호 교환")
        ]
        for contact_guard in (
            "상대도 손을 내밀거나 분명히 함께 동작할 때만",
            "상대가 참여하지 않으면 접촉을 생략한다",
        ):
            self.assertIn(contact_guard, game_section)
        for absence_of_refusal_basis in (
            "멈추라는 신호도 없었다",
            "거절하지 않으면",
            "피하지 않으면",
        ):
            self.assertNotIn(absence_of_refusal_basis, checklist)

        level_positions = []
        for number, level in enumerate(
            ("진입", "대화", "포지션", "프레임", "전환"), start=1
        ):
            match = re.search(
                rf"(?m)^- \[ \] \*\*레벨 {number}[^\n]*{level}\*\*", checklist
            )
            self.assertIsNotNone(match, level)
            level_positions.append(match.start())
        self.assertEqual(
            level_positions,
            sorted(level_positions),
        )
        self.assertEqual(
            checklist.count(
                "[[CALLOUT:field|한 번의 번호보다 중요한 것은 다음 파티에서도 "
                "반복할 수 있는 행동을 남기는 것이다.]]"
            ),
            1,
        )
        self.assertIn("체크가 가장 많이 비는", checklist)
        self.assertNotIn("동그라미가 가장 많이 비는", checklist)

    def test_visible_learning_labels_are_korean(self):
        manuscript = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PROJECT / "manuscript").glob("*.md"))
        )
        prologue = (PROJECT / "manuscript" / "00-prologue.md").read_text(
            encoding="utf-8"
        )
        theme = (PROJECT / "typst" / "theme.typ").read_text(encoding="utf-8")

        for legacy_label in ("BAD MOVE", "BETTER MOVE", "SCRIPT", "MISSION"):
            self.assertNotIn(legacy_label, manuscript)
            self.assertNotIn(legacy_label, theme)

        for visible_label in ("잘못된 선택", "좋은 선택", "대화 예시", "실전 과제"):
            self.assertIn(visible_label, manuscript)
            self.assertIn(f"**{visible_label}**", prologue)

        for natural_explanation in (
            "말을 어느 정도 길이로, 얼마나 가볍게 건네면 되는지 보여 주는 참고 문장이다",
            "읽은 내용을 현장에서 작은 행동으로 옮겨 보는 부분이다",
        ):
            self.assertIn(natural_explanation, prologue)
        for repetitive_explanation in ("보여 주는 예시다", "옮기는 과제다"):
            self.assertNotIn(repetitive_explanation, prologue)

        card_headings = {
            "bad-move": "잘못된 선택",
            "better-move": "좋은 선택",
            "mission-card": "실전 과제",
        }
        for function_name, visible_label in card_headings.items():
            card = re.search(
                rf"(?ms)^#let {re.escape(function_name)}\(body\).*?(?=^#let |\Z)",
                theme,
            )
            self.assertIsNotNone(card, function_name)
            self.assertIn(f"tracking: 0.4pt)[{visible_label}]", card.group(0))

    def test_all_chapters_follow_the_assigned_group_event_model(self):
        chapters = {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted((PROJECT / "manuscript").glob("*.md"))
        }
        expected_by_chapter = {
            "00-prologue.md": ("정해진 자리", "현재 조", "자리 교체", "조별 게임"),
            "01-environment.md": ("현재 조", "교체 방향", "게임 흐름"),
            "02-positioning.md": ("관찰 → 기여 → 반응 → 전환", "운영자의 자리 교체"),
            "03-rapport.md": ("새 조", "게임 직후", "조 전체의 흐름"),
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

    def test_environment_compares_introductions_side_by_side(self):
        chapter = (PROJECT / "manuscript" / "01-environment.md").read_text(
            encoding="utf-8"
        )

        for expected in (
            "파티에서 사람들을 친해지게 만들기 위해 자주 쓰는 주제가 자기소개다",
            "자기소개에서 정보만 말하면 어떻게 될까",
            "사람은 정보보다 감정이 붙은 장면을 더 오래 기억한다",
            "직업과 취미는 재료이고, 기억에 남는 것은 그 재료에 붙은 감정이다",
            "이런 식으로 이야기한다고 해서 내가 원하는 사람과 잘된다는 보장은 없다",
            "기억에 오래 남을수록 유리하다",
            "자리 교체나 쉬는 시간, 다음 게임에서 다시 말을 걸 명분이 생긴다",
            "결국 어떻게 될지는 모른다",
        ):
            self.assertIn(expected, chapter)

        rows = self.introduction_rows(chapter)
        self.assertEqual(len(rows), 4)
        for bad_move, better_move in rows:
            self.assertGreaterEqual(len(bad_move.strip(' "')), 8)
            self.assertGreaterEqual(len(better_move.strip(' "')), 12)
            self.assertGreater(len(better_move), len(bad_move))

    def test_manuscript_markers_are_closed_standalone_and_known(self):
        for chapter_path in sorted((PROJECT / "manuscript").glob("*.md")):
            with self.subTest(chapter=chapter_path.name):
                self.assert_valid_markers(chapter_path.read_text(encoding="utf-8"))

        malformed_samples = (
            "[[DIAGRAM:party_map]",
            "intro [[DIAGRAM:party_map]]",
            "[[DIAGRAM:unknown]]",
            "[[CALLOUT:unknown|message]]",
            "[[CALLOUT:bad|broken ] message]]",
        )
        for sample in malformed_samples:
            with self.subTest(sample=sample), self.assertRaises(AssertionError):
                self.assert_valid_markers(sample)

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
        mission_match = re.search(r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*$", chapter)
        self.assertIsNotNone(mission_match)
        mission_body = mission_match.group(1)
        for expected in ("자기 행동", "어느 전환", "상대 반응"):
            self.assertIn(expected, mission_body)
        self.assertNotIn("사람별 기록", mission_body)

        for expected in (
            "진행자가 알린 쉬는 시간이나 자리 교체 중 우연히 다시 마주치면",
            "어디론가 가는 중이면 붙잡지 않고 보내 준다",
            "특성 전이",
            "말수가 적은 사람은 차분하고 진중한 사람으로",
            "활달하고 분위기를 풀어 주는 사람으로",
            "남을 깎아내리는 말은 그 사람보다 말한 사람의 인상을 먼저 낮춘다",
            "파티에 가면 마음에 드는 사람이 한 명쯤은 있기 마련이다",
            "다른 기회를 없애는 것뿐만 아니라, 내 상태에도 영향을 준다",
            "같은 조가 되거나 게임을 함께하거나 쉬는 시간에 직접 이야기하기 전까지는",
            "그저 한 참가자로 생각하는 편이 좋다",
            "첫 번째로 볼 것은 대화에 참여하는 방식이다",
            "일단 편안함을 주는 것이 먼저다",
            "외모는 현실적으로 상대를 판단할 때 가장 먼저 보이는 도구다",
            "성격, 예의, 배려, 친절함",
            "본인이 꾸밀 수 있는 만큼 꾸미는 것도 중요하다",
            "외모가 전부는 아니라는 말이다",
        ):
            self.assertIn(expected, chapter)
        self.assertNotIn("## 타깃의 상태를 읽는 법", chapter)
        self.assertNotIn("타깃의 상태를 진단", chapter)
        self.assertNotIn("쉬는 시간에는 이미 나눈 대화를 자연스럽게 다시 마주쳤을 때만", chapter)
        self.assertNotIn("상대가 이동 중이면 보내 준다", chapter)
        self.assertNotIn("접점은 충분히 생긴다", chapter)
        self.assertNotIn("음료나 화장실을 다녀온 뒤에도 상대가 대화를 이어 가는지 확인", chapter)


class CnaPartyArtifactTests(unittest.TestCase):
    def test_distribution_pdf_is_release_ready(self):
        from pypdf import PdfReader

        path = ROOT / "dist" / "pdf" / "CNA_파티의_주도권.pdf"
        self.assertTrue(path.is_file())
        reader = PdfReader(str(path))
        self.assertGreaterEqual(len(reader.pages), 35)
        self.assertLessEqual(len(reader.pages), 45)
        cover_text = reader.pages[0].extract_text() or ""
        self.assertIn("파티의 주도권", cover_text)
        self.assertIn("CNA", cover_text)
        all_text = "".join(page.extract_text() or "" for page in reader.pages)
        self.assertGreaterEqual(len(all_text), 15000)
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


class CnaPartyDocumentationTests(unittest.TestCase):
    def test_release_docs_register_the_fifth_book_and_its_sources(self):
        from pypdf import PdfReader

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        inventory = (ROOT / "docs" / "ARTIFACT_INVENTORY.md").read_text(
            encoding="utf-8"
        )
        structure = (ROOT / "docs" / "PROJECT_STRUCTURE.md").read_text(
            encoding="utf-8"
        )
        guide = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

        release_row = (
            "| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` | "
            "`projects/cna-party-edition/typst/book.typ` |"
        )
        self.assertIn(release_row, readme)
        pdf_path = ROOT / "dist" / "pdf" / "CNA_파티의_주도권.pdf"
        inventory_row = (
            "| `cna-party-book` | `dist/pdf/CNA_파티의_주도권.pdf` | "
            f"{len(PdfReader(pdf_path).pages)} | {pdf_path.stat().st_size:,} | "
            f"`{sha256(pdf_path.read_bytes()).hexdigest()}` |"
        )
        self.assertIn(inventory_row, inventory)
        self.assertIn("### CNA Party Edition", structure)
        self.assertIn("정식 교재 PDF 다섯 종", structure)
        for document in (readme, inventory, structure, guide):
            self.assertIn("projects/cna-party-edition/manuscript/", document)
        self.assertIn("정식 배포 PDF는 `dist/pdf/`의 다섯 파일", guide)
        self.assertIn("`cna-party-book`", guide)

        for workflow_doc in (readme, guide):
            self.assertIn("python scripts/project.py build cna-party-book", workflow_doc)
            self.assertIn("python scripts/project.py verify all", workflow_doc)
            self.assertIn("의도적으로", workflow_doc)
            self.assertIn("build all", workflow_doc)
        for policy in (
            "현재 커밋된 배포 바이트",
            "생성 메타데이터와 타임스탬프",
            "같아도 SHA-256이 달라질 수 있다",
            "페이지 수, 바이트, SHA-256",
            "같은 변경에서 이 목록도 갱신",
            "python scripts/project.py build cna-party-book",
            "python scripts/project.py verify all",
        ):
            self.assertIn(policy, inventory)


if __name__ == "__main__":
    unittest.main()
