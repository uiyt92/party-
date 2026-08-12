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
    def assert_chapter(self, filename, minimum_chars, headings, tokens):
        chapter = (PROJECT / "manuscript" / filename).read_text(encoding="utf-8")

        self.assertGreaterEqual(len(chapter), minimum_chars)
        for heading in headings:
            self.assertIn(heading, chapter)
        for token in tokens:
            self.assertIn(token, chapter)

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
                "## 자기소개는 정보를 말하는 시간이 아니다",
            ),
            (
                "[[DIAGRAM:party_map]]",
                "[[CALLOUT:bad|",
                "[[CALLOUT:better|",
                "[[CALLOUT:mission|",
            ),
        )

    def test_environment_compares_introductions_side_by_side(self):
        chapter = (PROJECT / "manuscript" / "01-environment.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("| BAD MOVE | BETTER MOVE |", chapter)
        self.assertIn("| --- | --- |", chapter)


if __name__ == "__main__":
    unittest.main()
