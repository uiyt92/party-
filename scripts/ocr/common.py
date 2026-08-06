"""Shared path configuration for legacy OCR tools."""

from __future__ import annotations

import os
from collections.abc import Mapping, MutableMapping
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_ocr_paths(
    root: Path = REPO_ROOT,
    environment: Mapping[str, str] = os.environ,
) -> tuple[Path, Path]:
    """Resolve the classified OCR input and output locations."""
    pdf_path = Path(
        environment.get(
            "KATALK101_PDF", str(root / "references" / "pdf" / "카톡101.pdf")
        )
    )
    output_dir = Path(
        environment.get("OCR_OUTPUT_DIR", str(root / "references" / "ocr"))
    )
    return pdf_path, output_dir


def configure_google_credentials(
    root: Path = REPO_ROOT,
    environment: MutableMapping[str, str] = os.environ,
) -> Path | None:
    """Use explicit credentials first, otherwise the ignored local key."""
    configured = environment.get("GOOGLE_APPLICATION_CREDENTIALS")
    if configured:
        return Path(configured)

    local_key = root / "local" / "secrets" / "gcp-key.json"
    if local_key.is_file():
        environment["GOOGLE_APPLICATION_CREDENTIALS"] = str(local_key)
        return local_key
    return None
