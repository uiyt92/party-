import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        project_dir = self.root / "projects" / "sample" / "typst"
        project_dir.mkdir(parents=True)
        (project_dir / "book.typ").write_text("= Book", encoding="utf-8")
        manifest = {
            "slug": "sample",
            "title": "Sample",
            "deliverables": [
                {
                    "id": "sample-book",
                    "source": "typst/book.typ",
                    "output": "sample.pdf",
                }
            ],
        }
        (project_dir.parent / "project.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        self.item = project.load_deliverables(self.root)[0]

    def tearDown(self):
        self.temp.cleanup()

    @mock.patch("scripts.project.verify_pdf", create=True)
    @mock.patch("subprocess.run")
    def test_successful_build_promotes_verified_stage(self, run, verify):
        def compile_pdf(command, **kwargs):
            stage = Path(command[3])
            stage.parent.mkdir(parents=True, exist_ok=True)
            stage.write_bytes(b"%PDF-1.7 staged")

        run.side_effect = compile_pdf

        result = project.build_deliverable(
            self.item, self.root, typst="typst"
        )

        self.assertEqual(result, self.item.output)
        self.assertEqual(self.item.output.read_bytes(), b"%PDF-1.7 staged")
        verify.assert_called_once()

    @mock.patch(
        "scripts.project.verify_pdf",
        side_effect=project.ProjectError("bad pdf"),
        create=True,
    )
    @mock.patch("subprocess.run")
    def test_failed_verification_keeps_existing_distribution(self, run, verify):
        self.item.output.parent.mkdir(parents=True)
        self.item.output.write_bytes(b"old-good-pdf")

        def compile_pdf(command, **kwargs):
            stage = Path(command[3])
            stage.parent.mkdir(parents=True, exist_ok=True)
            stage.write_bytes(b"bad-stage")

        run.side_effect = compile_pdf

        with self.assertRaisesRegex(project.ProjectError, "bad pdf"):
            project.build_deliverable(self.item, self.root, typst="typst")

        self.assertEqual(self.item.output.read_bytes(), b"old-good-pdf")


if __name__ == "__main__":
    unittest.main()
