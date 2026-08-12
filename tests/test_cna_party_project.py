import json
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


if __name__ == "__main__":
    unittest.main()
