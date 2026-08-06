"""Build, verify, and scaffold Typst publishing projects."""

from __future__ import annotations

import json
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
