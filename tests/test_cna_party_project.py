import json
import re
import unittest
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
            r"\[\[CALLOUT:([a-z][a-z0-9_]*)\|([^\[\]\r\n]+)\]\])"
        )
        marker_lines = [
            line for line in text.splitlines() if "[[" in line or "]]" in line
        ]

        self.assertTrue(marker_lines)
        for line in marker_lines:
            self.assertEqual(line, line.strip())
            match = marker_pattern.fullmatch(line)
            self.assertIsNotNone(match, f"invalid manuscript marker: {line}")
            diagram_key, callout_kind, _ = match.groups()
            if diagram_key:
                self.assertIn(diagram_key, self.DIAGRAM_KEYS)
            else:
                self.assertIn(callout_kind, self.CALLOUT_KINDS)

    def introduction_rows(self, text):
        lines = text.splitlines()
        header_index = lines.index("| BAD MOVE | BETTER MOVE |")
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
                "## 초보자와 무성과자가 같은 곳에서 무너지는 이유",
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
                "## 자리 배치는 대화보다 솔직하다",
                "## 경쟁자를 분석하는 기준",
                "## 타깃의 상태를 읽는 법",
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
        heading_positions = [chapter.index(heading) for heading in headings]
        self.assertEqual(heading_positions, sorted(heading_positions))

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
            re.escape("사용할 순환은 **관찰 → 공급 → 반응 → 이동**이다.")
            + r"[^\n]*\n\n"
            + re.escape("[[DIAGRAM:positioning_loop]]"),
        )

        for expected in (
            "서로 모르는 두 사람을 연결한다",
            "어색한 정적을 수리한다",
            "상황에 맞는 작은 편의를 제공한다",
            "서비스 스태프로 포지셔닝된다",
            "명확한 거절이나 불편한 표정은 더 좋은 기술을 시도하라는 신호가 아니라 "
            "멈추라는 신호다",
        ):
            self.assertIn(expected, chapter)

        mission = re.search(r"\[\[CALLOUT:mission\|([^\n]+)\]\]\s*$", chapter)
        self.assertIsNotNone(mission)
        self.assertIn("주요 관심 상대에게 다가가기 전에", mission.group(1))
        self.assertIn("긍정적인 상호작용 세 번", mission.group(1))

    def test_rapport_chapter_turns_observation_into_conversation(self):
        headings = [
            "# 상대의 주파수 안으로 들어가라",
            "## 말보다 먼저 상태를 읽는다",
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
        for cue in ("몸의 방향", "반응 지연", "호흡", "목소리 크기", "눈", "친구를 확인"):
            self.assertIn(cue, chapter)
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
        self.assertIn("> **SCRIPT**", chapter)
        for beat in ("[상태 읽기]", "[페이싱]", "[감정 질문]", "[자기 공개]", "[종료]"):
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
        self.assertIn("개인적인 질문을 하기 전에", mission.group(1))
        self.assertIn("관찰 세 가지", mission.group(1))

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
            "선택적으로 주의를 쓰고 실제로 떠날 의향",
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

        self.assertIn("필요한 동안 저는 제 일행 쪽에 있을게요", chapter)
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

    def test_environment_compares_introductions_side_by_side(self):
        chapter = (PROJECT / "manuscript" / "01-environment.md").read_text(
            encoding="utf-8"
        )

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

        for expected in ("휴대폰", "종이에", "구역만", "머릿속", "파티가 끝난 뒤"):
            self.assertIn(expected, chapter)
        self.assertNotIn("대화하기 전, 선택한 타깃의", chapter)


if __name__ == "__main__":
    unittest.main()
