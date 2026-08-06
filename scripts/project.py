"""Build, verify, and scaffold Typst publishing projects."""

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
    """Raised when a project manifest or operation is unsafe or invalid."""


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
    """Load and validate all manifests below ``projects/``."""
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
            try:
                item_id = str(raw["id"])
                raw_source = str(raw["source"])
                raw_output = str(raw["output"])
            except (KeyError, TypeError) as exc:
                raise ProjectError(
                    f"invalid deliverable in {manifest_path}: {exc}"
                ) from exc
            if item_id in seen:
                raise ProjectError(f"duplicate deliverable id: {item_id}")

            source = (project_dir / raw_source).resolve()
            if not _inside(source, project_dir):
                raise ProjectError(f"source is outside project: {source}")

            output_root = root / "dist" / "pdf"
            output = (output_root / raw_output).resolve()
            if not _inside(output, output_root):
                raise ProjectError(f"output is outside dist/pdf: {output}")

            seen.add(item_id)
            items.append(Deliverable(item_id, slug, title, source, output))
    return items


def verify_pdf(path: Path) -> tuple[int, int]:
    """Require a readable, non-empty PDF with representative text."""
    if not path.is_file() or path.stat().st_size < 100:
        raise ProjectError(f"missing or empty PDF: {path}")
    try:
        from pypdf import PdfReader

        reader = PdfReader(path)
        page_count = len(reader.pages)
        sample_indices = (
            sorted({0, page_count // 2, page_count - 1}) if page_count else []
        )
        extracted = "".join(
            (reader.pages[index].extract_text() or "") for index in sample_indices
        )
    except Exception as exc:
        raise ProjectError(f"cannot read PDF {path}: {exc}") from exc
    if page_count < 1:
        raise ProjectError(f"PDF has no pages: {path}")
    if len(extracted.strip()) < 10:
        raise ProjectError(f"PDF has insufficient sample text: {path}")
    return page_count, len(extracted)


def build_deliverable(
    item: Deliverable, root: Path = ROOT, typst: str = "typst"
) -> Path:
    """Compile to staging, verify, then atomically promote a PDF."""
    if not item.source.is_file():
        raise ProjectError(f"source does not exist: {item.source}")
    stage = root / "build" / "pdf" / item.output.name
    stage.parent.mkdir(parents=True, exist_ok=True)
    command = [
        typst,
        "compile",
        str(item.source),
        str(stage),
        "--root",
        str(root),
    ]
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


def scaffold_project(slug: str, title: str, root: Path = ROOT) -> Path:
    """Create a product from the repository starter without overwriting."""
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
            path.write_text(
                text.replace("__SLUG__", slug).replace("__TITLE__", title),
                encoding="utf-8",
            )
    return destination


def select_deliverables(
    items: list[Deliverable], requested: str
) -> list[Deliverable]:
    """Select one deliverable or all configured deliverables."""
    if requested == "all":
        return items
    selected = [item for item in items if item.id == requested]
    if not selected:
        raise ProjectError(f"unknown deliverable id: {requested}")
    return selected


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(
        description="Build and manage Typst publishing projects"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("deliverable")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("deliverable", nargs="?", default="all")

    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("slug")
    new_parser.add_argument("--title", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "new":
            print(scaffold_project(args.slug, args.title, root))
            return 0

        items = load_deliverables(root)
        if args.command == "list":
            for item in items:
                print(
                    f"{item.id}\t{item.source.relative_to(root.resolve())}"
                    f"\t{item.output.relative_to(root.resolve())}"
                )
            return 0

        selected = select_deliverables(items, args.deliverable)
        for item in selected:
            if args.command == "build":
                output = build_deliverable(item, root)
                pages, chars = verify_pdf(output)
                print(
                    f"built {item.id}: {output.relative_to(root.resolve())} "
                    f"({pages} pages, {chars} sample chars)"
                )
            else:
                pages, chars = verify_pdf(item.output)
                print(f"verified {item.id}: {pages} pages, {chars} sample chars")
        return 0
    except ProjectError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
