import json
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
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


class SelectionTests(unittest.TestCase):
    def setUp(self):
        source = Path("source.typ")
        output = Path("output.pdf")
        self.items = [
            project.Deliverable("one", "sample", "Sample", source, output),
            project.Deliverable("two", "sample", "Sample", source, output),
        ]

    def test_select_all_returns_every_item(self):
        self.assertEqual(project.select_deliverables(self.items, "all"), self.items)

    def test_unknown_id_is_rejected(self):
        with self.assertRaisesRegex(project.ProjectError, "unknown deliverable id"):
            project.select_deliverables(self.items, "missing")


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        starter = self.root / "templates" / "project-starter"
        (starter / "typst").mkdir(parents=True)
        (starter / "project.json").write_text(
            '{"slug":"__SLUG__","title":"__TITLE__","deliverables":[]}',
            encoding="utf-8",
        )
        (starter / "typst" / "book.typ").write_text(
            "= __TITLE__", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_scaffold_replaces_tokens(self):
        destination = project.scaffold_project("new-book", "새 책", self.root)

        self.assertEqual(destination.name, "new-book")
        self.assertIn(
            "새 책",
            (destination / "typst" / "book.typ").read_text(encoding="utf-8"),
        )

    def test_scaffold_refuses_existing_destination(self):
        (self.root / "projects" / "new-book").mkdir(parents=True)

        with self.assertRaisesRegex(project.ProjectError, "already exists"):
            project.scaffold_project("new-book", "새 책", self.root)

    def test_scaffold_rejects_unsafe_slug(self):
        with self.assertRaisesRegex(project.ProjectError, "invalid slug"):
            project.scaffold_project("../escape", "Bad", self.root)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        product = self.root / "projects" / "sample"
        (product / "typst").mkdir(parents=True)
        (product / "typst" / "book.typ").write_text("= Book", encoding="utf-8")
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
        (product / "project.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_list_prints_configured_deliverable(self):
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            result = project.main(["list"], root=self.root)

        self.assertEqual(result, 0)
        self.assertIn("sample-book", stdout.getvalue())
        self.assertIn("dist", stdout.getvalue())

    def test_unknown_build_id_returns_error(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            result = project.main(["build", "missing"], root=self.root)

        self.assertEqual(result, 1)
        self.assertIn("unknown deliverable id", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
