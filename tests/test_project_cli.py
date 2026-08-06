import json
import tempfile
import unittest
from pathlib import Path

from scripts import project


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project_dir = self.root / "projects" / "sample"
        self.project_dir.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self, source="typst/book.typ", output="샘플.pdf"):
        payload = {
            "slug": "sample",
            "title": "샘플",
            "deliverables": [
                {"id": "sample-book", "source": source, "output": output}
            ],
        }
        path = self.project_dir / "project.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_discovers_deliverable_with_resolved_paths(self):
        (self.project_dir / "typst").mkdir()
        (self.project_dir / "typst" / "book.typ").write_text(
            "= Book", encoding="utf-8"
        )
        self.write_manifest()

        items = project.load_deliverables(self.root)

        self.assertEqual([item.id for item in items], ["sample-book"])
        self.assertEqual(
            items[0].source, (self.project_dir / "typst" / "book.typ").resolve()
        )
        self.assertEqual(
            items[0].output,
            (self.root / "dist" / "pdf" / "샘플.pdf").resolve(),
        )

    def test_rejects_source_outside_project(self):
        self.write_manifest(source="../../outside.typ")

        with self.assertRaisesRegex(project.ProjectError, "outside project"):
            project.load_deliverables(self.root)

    def test_rejects_duplicate_deliverable_ids(self):
        self.write_manifest()
        other = self.root / "projects" / "other"
        other.mkdir(parents=True)
        payload = {
            "slug": "other",
            "title": "Other",
            "deliverables": [
                {
                    "id": "sample-book",
                    "source": "book.typ",
                    "output": "other.pdf",
                }
            ],
        }
        (other / "project.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )

        with self.assertRaisesRegex(project.ProjectError, "duplicate deliverable id"):
            project.load_deliverables(self.root)


if __name__ == "__main__":
    unittest.main()
