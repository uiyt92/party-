# Typst Publishing Project Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the publishing workspace into product-oriented Typst projects, add a tested build/scaffold CLI, classify every existing artifact, and reproducibly rebuild and verify the four canonical PDFs.

**Architecture:** Product manifests under `projects/` declare Typst entry points and distribution filenames. A standard-library Python CLI compiles into `build/pdf/`, verifies staged PDFs with `pypdf`, and atomically promotes only successful builds into `dist/pdf/`. Existing files are moved without deletion into active, reference, build, or archive categories; a starter template and Korean documentation define the next-project workflow.

**Tech Stack:** Typst 0.14.2, Python 3.12 standard library, `pypdf`, `Pillow`, PowerShell, unittest, Git.

---

## File Structure

### Files to create

- `.gitignore` - secret, build, local, reference-PDF, archive, and tool-state exclusions.
- `README.md` - repository entry point and common commands.
- `requirements.txt` - PDF verification and contact-sheet dependencies.
- `projects/katalk-standard/project.json` - three Katalk deliverables.
- `projects/cna-night/project.json` - CNA NIGHT deliverable.
- `scripts/project.py` - list/build/verify/new command-line workflow.
- `tests/test_project_cli.py` - CLI path, build, promotion, and scaffolding tests.
- `templates/project-starter/project.json` - starter manifest.
- `templates/project-starter/typst/book.typ` - starter Typst entry point.
- `templates/project-starter/manuscript/01-introduction.md` - starter chapter.
- `templates/project-starter/assets/.gitkeep` - starter asset directory.
- `templates/project-starter/README.md` - starter-local instructions.
- `docs/PROJECT_STRUCTURE.md` - active directory and source-of-truth guide.
- `docs/ARTIFACT_INVENTORY.md` - categorized inventory and duplicate findings.
- `docs/NEW_PROJECT_GUIDE.md` - exact new-project workflow.

### Files to move and modify

- `build.typ` -> `projects/katalk-standard/typst/book.typ`; update shared-template import.
- `build_part3.typ` -> `projects/katalk-standard/typst/advanced.typ`; update shared-template import.
- `lead_magnet.typ` -> `projects/katalk-standard/typst/summary.typ`; update shared-template import.
- Root Katalk chapter Markdown -> `projects/katalk-standard/manuscript/basic/`.
- `drafts/part3/*.md` -> `projects/katalk-standard/manuscript/advanced/`.
- `CNA_NIGHT/build.typ` -> `projects/cna-night/typst/book.typ`; update manuscript paths and build comment.
- `CNA_NIGHT/theme.typ`, `diagrams.typ`, `persona_vibe_export.typ` -> `projects/cna-night/typst/`.
- `CNA_NIGHT/chapters/*.md` -> `projects/cna-night/manuscript/`.
- `CNA_NIGHT/diagrams.md` -> `projects/cna-night/README-DIAGRAMS.md`.
- `ocr_process.py` -> `scripts/ocr/ocr_process.py`; update credential/input/output paths.
- Other root OCR scripts -> `scripts/ocr/`; update reference input/output paths.
- `CLAUDE.md` - replace stale locations and output promises with the new structure.

### Files to preserve without active modification

- `main.typ` -> `archive/legacy-build/main.typ`.
- `scripts/md_to_typ.py`, `scripts/integrate_phase1.py` -> `scripts/legacy/`.
- Non-active drafts -> `archive/drafts/`.
- `_workspace/` -> `archive/ai-runs/`.
- Reference PDFs -> `references/pdf/`.
- OCR output Markdown/JSON -> `references/ocr/`.
- Old branded outputs and duplicate coaching files -> `archive/legacy-output/`.
- Preview renders -> `build/previews/`.

---

### Task 1: Establish the feature branch and repository safety boundary

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`

- [ ] **Step 1: Create and switch to the implementation branch**

Run:

```powershell
git switch -c codex/typst-project-reorganization
```

Expected: `Switched to a new branch 'codex/typst-project-reorganization'`.

- [ ] **Step 2: Add the ignore policy**

Create `.gitignore` with:

```gitignore
# Generated builds and render QA
build/

# Machine-local secrets
local/
gcp-key.json
*service-account*.json

# Tool and interpreter state
.claude/worktrees/
__pycache__/
*.py[cod]
.pytest_cache/

# External and historical material retained locally
references/pdf/*.pdf
archive/

# OS/editor files
.DS_Store
Thumbs.db
```

- [ ] **Step 3: Declare verification dependencies**

Create `requirements.txt` with:

```text
pypdf>=6.0,<7
Pillow>=11,<13
```

- [ ] **Step 4: Verify secret and build exclusions**

Run:

```powershell
git check-ignore -v gcp-key.json
git check-ignore -v build/example.pdf
git check-ignore -v references/pdf/example.pdf
```

Expected: all three paths match `.gitignore` rules.

- [ ] **Step 5: Commit the safety boundary and implementation plan**

```powershell
git add .gitignore requirements.txt docs/superpowers/plans/2026-08-06-typst-publishing-reorganization.md
git commit -m "chore: establish publishing repository boundary"
```

Expected: commit succeeds without staging `gcp-key.json`, `archive/`, or `build/`.

---

### Task 2: Test manifest discovery and safe path handling

**Files:**
- Create: `tests/test_project_cli.py`
- Create: `scripts/project.py`

- [ ] **Step 1: Write failing manifest tests**

Create `tests/test_project_cli.py` with the following initial tests:

```python
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
        (self.project_dir / "typst" / "book.typ").write_text("= Book", encoding="utf-8")
        self.write_manifest()

        items = project.load_deliverables(self.root)

        self.assertEqual([item.id for item in items], ["sample-book"])
        self.assertEqual(items[0].source, self.project_dir / "typst" / "book.typ")
        self.assertEqual(items[0].output, self.root / "dist" / "pdf" / "샘플.pdf")

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
                {"id": "sample-book", "source": "book.typ", "output": "other.pdf"}
            ],
        }
        (other / "project.json").write_text(json.dumps(payload), encoding="utf-8")

        with self.assertRaisesRegex(project.ProjectError, "duplicate deliverable id"):
            project.load_deliverables(self.root)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```powershell
python -m unittest tests.test_project_cli -v
```

Expected: FAIL because `scripts.project` does not exist.

- [ ] **Step 3: Implement manifest loading**

Create `scripts/project.py` with these definitions:

```python
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectError(RuntimeError):
    pass


@dataclass(frozen=True)
class Deliverable:
    id: str
    project_slug: str
    title: str
    source: Path
    output: Path


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def load_deliverables(root: Path = ROOT) -> list[Deliverable]:
    projects_dir = root / "projects"
    items: list[Deliverable] = []
    seen: set[str] = set()
    for manifest_path in sorted(projects_dir.glob("*/project.json")):
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            slug = str(payload["slug"])
            title = str(payload["title"])
            raw_items = payload["deliverables"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ProjectError(f"invalid manifest: {manifest_path}: {exc}") from exc
        project_dir = manifest_path.parent
        for raw in raw_items:
            item_id = str(raw["id"])
            if item_id in seen:
                raise ProjectError(f"duplicate deliverable id: {item_id}")
            source = (project_dir / str(raw["source"])).resolve()
            if not _inside(source, project_dir):
                raise ProjectError(f"source is outside project: {source}")
            output = (root / "dist" / "pdf" / str(raw["output"])).resolve()
            if not _inside(output, root / "dist" / "pdf"):
                raise ProjectError(f"output is outside dist/pdf: {output}")
            seen.add(item_id)
            items.append(Deliverable(item_id, slug, title, source, output))
    return items
```

- [ ] **Step 4: Run the tests and verify they pass**

Run:

```powershell
python -m unittest tests.test_project_cli -v
```

Expected: 3 tests pass.

- [ ] **Step 5: Commit manifest safety**

```powershell
git add scripts/project.py tests/test_project_cli.py
git commit -m "test: define safe publishing manifests"
```

---

### Task 3: Test staged builds and non-destructive promotion

**Files:**
- Modify: `tests/test_project_cli.py`
- Modify: `scripts/project.py`

- [ ] **Step 1: Add failing build tests**

Append imports and tests that mock compilation while exercising real staging and promotion:

```python
from unittest import mock


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
                {"id": "sample-book", "source": "typst/book.typ", "output": "sample.pdf"}
            ],
        }
        (project_dir.parent / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.item = project.load_deliverables(self.root)[0]

    def tearDown(self):
        self.temp.cleanup()

    @mock.patch("scripts.project.verify_pdf")
    @mock.patch("scripts.project.subprocess.run")
    def test_successful_build_promotes_verified_stage(self, run, verify):
        def compile_pdf(command, **kwargs):
            stage = Path(command[3])
            stage.parent.mkdir(parents=True, exist_ok=True)
            stage.write_bytes(b"%PDF-1.7 staged")
        run.side_effect = compile_pdf

        result = project.build_deliverable(self.item, self.root, typst="typst")

        self.assertEqual(result, self.item.output)
        self.assertEqual(self.item.output.read_bytes(), b"%PDF-1.7 staged")
        verify.assert_called_once()

    @mock.patch("scripts.project.verify_pdf", side_effect=project.ProjectError("bad pdf"))
    @mock.patch("scripts.project.subprocess.run")
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
```

- [ ] **Step 2: Run tests and verify they fail**

Run `python -m unittest tests.test_project_cli -v`.

Expected: FAIL because `verify_pdf` and `build_deliverable` are undefined.

- [ ] **Step 3: Implement verification and atomic promotion**

Append to `scripts/project.py`:

```python
def verify_pdf(path: Path) -> tuple[int, int]:
    if not path.is_file() or path.stat().st_size < 100:
        raise ProjectError(f"missing or empty PDF: {path}")
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        page_count = len(reader.pages)
        sample_indices = sorted({0, page_count // 2, page_count - 1}) if page_count else []
        extracted = "".join((reader.pages[i].extract_text() or "") for i in sample_indices)
    except Exception as exc:
        raise ProjectError(f"cannot read PDF {path}: {exc}") from exc
    if page_count < 1:
        raise ProjectError(f"PDF has no pages: {path}")
    if len(extracted.strip()) < 10:
        raise ProjectError(f"PDF has insufficient sample text: {path}")
    return page_count, len(extracted)


def build_deliverable(item: Deliverable, root: Path = ROOT, typst: str = "typst") -> Path:
    if not item.source.is_file():
        raise ProjectError(f"source does not exist: {item.source}")
    stage = root / "build" / "pdf" / item.output.name
    stage.parent.mkdir(parents=True, exist_ok=True)
    command = [typst, "compile", str(item.source), str(stage), "--root", str(root)]
    try:
        subprocess.run(command, cwd=root, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ProjectError(f"Typst build failed for {item.id}: {exc}") from exc
    verify_pdf(stage)
    item.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_target = item.output.with_suffix(item.output.suffix + ".tmp")
    shutil.copy2(stage, temporary_target)
    os.replace(temporary_target, item.output)
    return item.output
```

- [ ] **Step 4: Run all tests**

Run `python -m unittest tests.test_project_cli -v`.

Expected: 5 tests pass.

- [ ] **Step 5: Commit staged build behavior**

```powershell
git add scripts/project.py tests/test_project_cli.py
git commit -m "feat: add verified staged PDF builds"
```

---

### Task 4: Migrate active Typst products and manuscripts

**Files:**
- Create: `projects/katalk-standard/project.json`
- Create: `projects/cna-night/project.json`
- Move and modify the active source files listed in the File Structure section.

- [ ] **Step 1: Create and validate destination directories**

Run `Resolve-Path .` and confirm the result is exactly `C:\Users\SuperNatural1\Code\CODE\폰게임 강의 책`. Then create only these descendants:

```powershell
New-Item -ItemType Directory -Force projects/katalk-standard/typst, projects/katalk-standard/manuscript/basic, projects/katalk-standard/manuscript/advanced, projects/katalk-standard/assets, projects/cna-night/typst, projects/cna-night/manuscript, projects/cna-night/assets | Out-Null
```

- [ ] **Step 2: Move Katalk typesetting sources and manuscripts**

Use `Move-Item -LiteralPath` for `build.typ`, `build_part3.typ`, and `lead_magnet.typ`. Move the explicit root chapter list `01_intro.md` through `21_appendix.md`, including `08b_continue.md`, `08c_questions.md`, `10b_tone.md`, and `13b_types.md`, into `projects/katalk-standard/manuscript/basic/`. Move `drafts/part3/*.md` into `projects/katalk-standard/manuscript/advanced/` and `podcast/` into `projects/katalk-standard/podcast/`.

Expected: no Katalk chapter Markdown or active book Typst entry point remains loose at the repository root.

- [ ] **Step 3: Update Katalk shared-template imports**

Change the first line of each moved Typst entry point to:

```typst
#import "../../../templates/typst/book.typ": *
```

- [ ] **Step 4: Move CNA NIGHT and update manuscript references**

Move active CNA files into the destination paths. In `projects/cna-night/typst/book.typ`, use local imports and change every chapter argument from `"chapters/<name>.md"` to `"../manuscript/<name>.md"`. Update the build comment to:

```typst
// 실행: python scripts/project.py build cna-night
```

Update `persona-vibe-export.typ` comment to use its new path and `build/previews/cna-night/persona_vibe.svg`.

- [ ] **Step 5: Add product manifests**

Create `projects/katalk-standard/project.json`:

```json
{
  "slug": "katalk-standard",
  "title": "카톡의 정석",
  "deliverables": [
    {"id": "katalk-basic", "source": "typst/book.typ", "output": "카톡의정석.pdf"},
    {"id": "katalk-advanced", "source": "typst/advanced.typ", "output": "카톡의정석_심화편.pdf"},
    {"id": "katalk-summary", "source": "typst/summary.typ", "output": "카톡의정석_요약본.pdf"}
  ]
}
```

Create `projects/cna-night/project.json`:

```json
{
  "slug": "cna-night",
  "title": "CNA NIGHT",
  "deliverables": [
    {"id": "cna-night", "source": "typst/book.typ", "output": "CNA_NIGHT.pdf"}
  ]
}
```

- [ ] **Step 6: Verify discovery before compiling**

Run `python scripts/project.py list` after Task 6 adds the CLI commands.

Expected: exactly four IDs and four output paths under `dist/pdf/`.

---

### Task 5: Classify all historical, reference, build, and distribution artifacts

**Files:**
- Move: root references and OCR results.
- Move: `output/` contents into `dist/`, `build/`, `references/`, and `archive/`.
- Move: `analysis/`, `briefs/`, `_workspace/`, and inactive drafts.

- [ ] **Step 1: Verify the workspace boundary before bulk moves**

Resolve the repository root and every top-level source directory. Require every resolved source and destination to be below the repository root. Stop if any path resolves outside it.

- [ ] **Step 2: Move reference and research material**

Move the three root reference PDFs and `output/FASTER_SEX - 복사본.pdf` into `references/pdf/`. Move root OCR Markdown/JSON into `references/ocr/`. Move `analysis/` to `docs/research/analysis/`, `briefs/` to `docs/research/briefs/`, `output/변경이력.md` and `output/카톡의정석-review.md` to `docs/research/reviews/`.

- [ ] **Step 3: Move canonical and supporting distribution artifacts**

Move:

```text
output/1대1 코칭 자료/카톡의정석.pdf -> dist/pdf/카톡의정석.pdf
output/카톡의정석_심화편.pdf -> dist/pdf/카톡의정석_심화편.pdf
output/카톡의정석_요약본.pdf -> dist/pdf/카톡의정석_요약본.pdf
output/카톡의정석_강의슬라이드.pptx -> dist/slides/
output/답장의기술_강의슬라이드.html -> dist/slides/
output/images/ -> dist/slides/images/
output/강의스크립트.md -> dist/slides/
output/답장의기술_워크북.* -> dist/handouts/
output/답장의기술_사전과제.* -> dist/handouts/
output/어프로치_Basic_실전매뉴얼.html -> dist/packages/coaching/
output/1대1 코칭 자료/나이트 게임_노바.pdf -> dist/packages/coaching/
output/1대1 코칭 자료/어프로치_Basic_실전매뉴얼.pdf -> dist/packages/coaching/
```

- [ ] **Step 4: Preserve old and duplicate outputs**

Move old `답장의기술.pdf`, `답장의기술_심화편.pdf`, and backup/preview material to `archive/legacy-output/`. Move the four coaching files whose hashes match the FASTER SEX source into `archive/legacy-output/duplicate-coaching/`. Move `output/_archive/` preview renders to `build/previews/legacy/`, and persona-vibe PNG/SVG to `build/previews/cna-night/`.

- [ ] **Step 5: Preserve drafts and AI work without deletion**

Move remaining `drafts/` subdirectories to `archive/drafts/`, `_workspace/` to `archive/ai-runs/`, and stale `main.typ` to `archive/legacy-build/main.typ`. Move the stale converter and one-time integrator to `scripts/legacy/`.

- [ ] **Step 6: Verify no uncategorized output files remain**

Run:

```powershell
Get-ChildItem output -Recurse -Force
Get-ChildItem -File -Force | Select-Object Name
```

Expected: `output/` is empty and may be removed; root files are limited to repository configuration and entry documentation. No file-content deletion occurred.

---

### Task 6: Complete the CLI and safe new-project scaffolding

**Files:**
- Modify: `scripts/project.py`
- Modify: `tests/test_project_cli.py`
- Create: `templates/project-starter/*`

- [ ] **Step 1: Add failing CLI and scaffold tests**

Add tests for selecting `all`, unknown IDs, slug validation, successful template substitution, and refusing an existing destination. Use a temporary root and a starter containing `__SLUG__` and `__TITLE__`; assert no existing file is overwritten.

```python
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
        (starter / "project.json").write_text('{"slug":"__SLUG__","title":"__TITLE__","deliverables":[]}', encoding="utf-8")
        (starter / "typst" / "book.typ").write_text('= __TITLE__', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_scaffold_replaces_tokens(self):
        destination = project.scaffold_project("new-book", "새 책", self.root)
        self.assertEqual(destination.name, "new-book")
        self.assertIn("새 책", (destination / "typst" / "book.typ").read_text(encoding="utf-8"))

    def test_scaffold_refuses_existing_destination(self):
        (self.root / "projects" / "new-book").mkdir(parents=True)
        with self.assertRaisesRegex(project.ProjectError, "already exists"):
            project.scaffold_project("new-book", "새 책", self.root)

    def test_scaffold_rejects_unsafe_slug(self):
        with self.assertRaisesRegex(project.ProjectError, "invalid slug"):
            project.scaffold_project("../escape", "Bad", self.root)
```

- [ ] **Step 2: Run tests and verify they fail**

Run `python -m unittest tests.test_project_cli -v`.

Expected: new scaffold tests fail because `scaffold_project` is undefined.

- [ ] **Step 3: Implement scaffold and CLI dispatch**

Append these functions and a `main()` dispatcher to `scripts/project.py`:

```python
def scaffold_project(slug: str, title: str, root: Path = ROOT) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise ProjectError(f"invalid slug: {slug}")
    starter = root / "templates" / "project-starter"
    destination = root / "projects" / slug
    if destination.exists():
        raise ProjectError(f"project already exists: {destination}")
    if not starter.is_dir():
        raise ProjectError(f"starter template is missing: {starter}")
    shutil.copytree(starter, destination)
    for path in destination.rglob("*"):
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            path.write_text(text.replace("__SLUG__", slug).replace("__TITLE__", title), encoding="utf-8")
    return destination


def select_deliverables(items: list[Deliverable], requested: str) -> list[Deliverable]:
    if requested == "all":
        return items
    selected = [item for item in items if item.id == requested]
    if not selected:
        raise ProjectError(f"unknown deliverable id: {requested}")
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and manage Typst publishing projects")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    build_parser = sub.add_parser("build")
    build_parser.add_argument("deliverable")
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("deliverable", nargs="?", default="all")
    new_parser = sub.add_parser("new")
    new_parser.add_argument("slug")
    new_parser.add_argument("--title", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "new":
            print(scaffold_project(args.slug, args.title))
            return 0
        items = load_deliverables(ROOT)
        if args.command == "list":
            for item in items:
                print(f"{item.id}\t{item.source.relative_to(ROOT)}\t{item.output.relative_to(ROOT)}")
            return 0
        selected = select_deliverables(items, args.deliverable)
        for item in selected:
            if args.command == "build":
                output = build_deliverable(item)
                pages, chars = verify_pdf(output)
                print(f"built {item.id}: {output.relative_to(ROOT)} ({pages} pages, {chars} sample chars)")
            else:
                pages, chars = verify_pdf(item.output)
                print(f"verified {item.id}: {pages} pages, {chars} sample chars")
        return 0
    except ProjectError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Create the starter template**

Create `templates/project-starter/project.json`:

```json
{
  "slug": "__SLUG__",
  "title": "__TITLE__",
  "deliverables": [
    {"id": "__SLUG__-book", "source": "typst/book.typ", "output": "__TITLE__.pdf"}
  ]
}
```

Create `templates/project-starter/typst/book.typ`:

```typst
#import "../../../templates/typst/book.typ": *
#import "@preview/cmarker:0.1.6"

#show: book.with(
  title: "__TITLE__",
  subtitle: "새 Typst 교재 프로젝트",
  author: "저자명",
)

#cmarker.render(read("../manuscript/01-introduction.md"))
```

Create `templates/project-starter/manuscript/01-introduction.md`:

```markdown
# 들어가며

이 문서는 새 교재의 첫 원고입니다.

## 이 책의 목표

독자가 이 책을 읽고 얻게 될 변화를 구체적으로 작성합니다.
```

Create `templates/project-starter/README.md`:

````markdown
# __TITLE__

## Build

From the repository root:

```powershell
python scripts/project.py build __SLUG__-book
python scripts/project.py verify __SLUG__-book
```

Edit Markdown under `manuscript/`, product-local images under `assets/`, and Typst layout under `typst/`.
````

Create an empty `templates/project-starter/assets/.gitkeep`.

- [ ] **Step 5: Run the complete unit test suite**

Run `python -m unittest discover -s tests -v`.

Expected: all manifest, build, selection, and scaffold tests pass.

- [ ] **Step 6: Commit the product CLI and starter**

```powershell
git add scripts/project.py tests templates/project-starter projects
git commit -m "feat: add reproducible Typst project workflow"
```

---

### Task 7: Secure and relocate legacy OCR tools

**Files:**
- Move and modify: `scripts/ocr/ocr_process.py`
- Move and modify: `scripts/ocr/ocr_gcloud.py`
- Move and modify: `scripts/ocr/ocr_openai.py`
- Move and modify: `scripts/ocr/ocr_openai_simple.py`
- Move: `gcp-key.json` -> `local/secrets/gcp-key.json`

- [ ] **Step 1: Move the secret without reading or printing its values**

Resolve both source and destination inside the repository, create `local/secrets/`, and use `Move-Item -LiteralPath`. Confirm `git check-ignore -v local/secrets/gcp-key.json` reports the `local/` rule.

- [ ] **Step 2: Replace script-relative data assumptions**

Each OCR script defines:

```python
REPO_ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = Path(os.environ.get("KATALK101_PDF", REPO_ROOT / "references" / "pdf" / "카톡101.pdf"))
OUTPUT_DIR = Path(os.environ.get("OCR_OUTPUT_DIR", REPO_ROOT / "references" / "ocr"))
```

The Google script also defines:

```python
local_key = REPO_ROOT / "local" / "secrets" / "gcp-key.json"
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ and local_key.is_file():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(local_key)
```

No script prints credential contents.

- [ ] **Step 3: Compile-check the relocated scripts**

Run:

```powershell
python -m py_compile scripts/ocr/ocr_process.py scripts/ocr/ocr_gcloud.py scripts/ocr/ocr_openai.py scripts/ocr/ocr_openai_simple.py
```

Expected: exit code 0 and no output.

- [ ] **Step 4: Commit only scripts, never the secret**

```powershell
git add scripts/ocr
git status --short
git commit -m "chore: isolate legacy OCR inputs and credentials"
```

Expected: `local/secrets/gcp-key.json` is not staged.

---

### Task 8: Write repository, artifact, and new-project documentation

**Files:**
- Create: `README.md`
- Create: `docs/PROJECT_STRUCTURE.md`
- Create: `docs/ARTIFACT_INVENTORY.md`
- Create: `docs/NEW_PROJECT_GUIDE.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Write the root README**

Include the four canonical deliverables, prerequisites, `list`, `build all`, `verify`, and `new` commands, and direct links to the three detailed documents.

- [ ] **Step 2: Document source-of-truth and directory ownership**

`PROJECT_STRUCTURE.md` explicitly states that the three Katalk Typst files are build sources while their Markdown is editorial manuscript, and that CNA NIGHT reads its Markdown at build time. Include a tree matching the implemented layout, not the proposed layout.

- [ ] **Step 3: Write the artifact inventory from the post-migration filesystem**

For every PDF, HTML, PPTX, image tree, OCR result, and archive category, record path, classification, active/legacy/reference status, and whether it is tracked. Include the SHA-256 duplicate group and state that the four coaching names do not match their byte-identical FASTER SEX content.

- [ ] **Step 4: Write the new-project guide**

Document:

```powershell
python scripts/project.py new sample-book --title "샘플 교재"
python scripts/project.py list
python scripts/project.py build sample-book-book
python scripts/project.py verify sample-book-book
```

Explain manifest fields, Typst root rules, manuscript/assets conventions, adding multiple deliverables, and the promotion checklist.

- [ ] **Step 5: Update CLAUDE.md path promises**

Remove stale `Road_To_Motel/`, root `build.typ`, and `output/` references. Point all build commands to `scripts/project.py` and all canonical outputs to `dist/pdf/`.

- [ ] **Step 6: Validate documentation paths**

Use a PowerShell link/path audit to confirm every backtick path named in the four active docs exists or is explicitly marked as an example.

- [ ] **Step 7: Commit documentation and classified assets**

```powershell
git add README.md CLAUDE.md docs projects templates scripts dist
git commit -m "docs: document publishing products and artifacts"
```

---

### Task 9: Build and structurally verify all canonical PDFs

**Files:**
- Generate: `build/pdf/*.pdf`
- Generate/promote: `dist/pdf/카톡의정석.pdf`
- Generate/promote: `dist/pdf/카톡의정석_심화편.pdf`
- Generate/promote: `dist/pdf/카톡의정석_요약본.pdf`
- Generate/promote: `dist/pdf/CNA_NIGHT.pdf`

- [ ] **Step 1: Run the unit tests immediately before the real build**

Run `python -m unittest discover -s tests -v`.

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 2: List the configured build graph**

Run `python scripts/project.py list`.

Expected IDs: `cna-night`, `katalk-advanced`, `katalk-basic`, and `katalk-summary`, each exactly once.

- [ ] **Step 3: Build all products into staging and promote verified files**

Run `python scripts/project.py build all`.

Expected: four `built ...` lines, Typst exit code 0 for every source, and non-zero page/sample-text counts.

- [ ] **Step 4: Independently verify distribution files**

Run `python scripts/project.py verify`.

Expected: four `verified ...` lines and exit code 0.

- [ ] **Step 5: Record hashes and page counts**

Generate a Markdown table for `docs/ARTIFACT_INVENTORY.md` containing filename, byte size, SHA-256, page count, source ID, and build timestamp. Do not infer page counts from prior documentation.

---

### Task 10: Render and visually inspect every canonical PDF

**Files:**
- Generate: `build/rendered/<deliverable-id>/*.png`
- Generate: `build/rendered/<deliverable-id>/contact-sheet-*.png`

- [ ] **Step 1: Render every page**

Use `typst compile` with a PNG page-pattern output or bundled Poppler `pdftoppm`. Store each deliverable under its own `build/rendered/` directory. Require the PNG count to equal the parsed PDF page count.

- [ ] **Step 2: Create contact sheets**

Use Pillow to create readable, numbered contact sheets of no more than 30 thumbnails each. The sheets are QA intermediates and remain ignored under `build/`.

- [ ] **Step 3: Inspect all contact sheets**

Check every page for blank output, clipped blocks, overlapping text, missing glyphs, black boxes, broken diagrams, and inconsistent page geometry. Record any page needing full-resolution review.

- [ ] **Step 4: Inspect representative pages at full resolution**

For each PDF, inspect the cover, contents/early section, a middle page, every page flagged from contact sheets, and the final page. Fix only layout/path defects caused by the reorganization; do not edit manuscript content.

- [ ] **Step 5: Rebuild and repeat verification after any fix**

If a Typst path/layout fix is needed, rerun Tasks 9 and 10 for the affected deliverable. A prior render is not accepted as evidence after source changes.

---

### Task 11: Final repository verification and handoff

**Files:**
- Modify: `docs/ARTIFACT_INVENTORY.md` with final hashes and page counts.
- Modify: plan checkboxes as tasks complete.

- [ ] **Step 1: Run the complete verification suite fresh**

Run:

```powershell
python -m unittest discover -s tests -v
python scripts/project.py verify
git status --short
```

Expected: all unit tests pass; all four PDFs verify; no secret, `build/`, reference PDF, or archive file is staged.

- [ ] **Step 2: Audit requirements against the design**

Confirm every success criterion in `docs/superpowers/specs/2026-08-06-typst-publishing-reorganization-design.md` has evidence in the filesystem, commands, inventory, or render inspection.

- [ ] **Step 3: Commit final verified state**

```powershell
git add -A
git status --short
git commit -m "refactor: organize Typst publishing projects"
```

Before committing, inspect the staged list and unstage any ignored category that entered accidentally. Never use a destructive reset.

- [ ] **Step 4: Report the handoff**

Report the branch, commits, four PDF paths with fresh page counts, key commands, archived/ignored categories, duplicate finding, secret relocation, and any remaining limitation. Do not claim visual or build success without the fresh outputs from Steps 1-2.
