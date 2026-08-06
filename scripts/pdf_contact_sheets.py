"""Create numbered contact sheets from rendered PDF page PNGs."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def _page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    return int(match.group(1)) if match else 0


def create_contact_sheets(
    page_directory: Path,
    output_directory: Path | None = None,
    *,
    per_sheet: int = 30,
    columns: int = 5,
    thumbnail_width: int = 180,
) -> list[Path]:
    """Create labelled sheets and return their paths."""
    pages = sorted(page_directory.glob("page-*.png"), key=_page_number)
    if not pages:
        raise ValueError(f"No page PNGs found in {page_directory}")
    if per_sheet < 1 or columns < 1 or thumbnail_width < 20:
        raise ValueError("per_sheet, columns, and thumbnail_width must be positive")

    output_directory = output_directory or page_directory
    output_directory.mkdir(parents=True, exist_ok=True)
    margin = 18
    cell_width = max(90, thumbnail_width + 24)
    cell_height = max(160, int(thumbnail_width * 1.5) + 44)
    results: list[Path] = []

    for sheet_index, start in enumerate(range(0, len(pages), per_sheet), start=1):
        chunk = pages[start : start + per_sheet]
        rows = math.ceil(len(chunk) / columns)
        canvas = Image.new(
            "RGB",
            (margin * 2 + columns * cell_width, margin * 2 + rows * cell_height),
            "#d9dde3",
        )
        draw = ImageDraw.Draw(canvas)

        for position, page_path in enumerate(chunk):
            row, column = divmod(position, columns)
            cell_x = margin + column * cell_width
            cell_y = margin + row * cell_height
            with Image.open(page_path) as source:
                page = ImageOps.exif_transpose(source).convert("RGB")
                page.thumbnail(
                    (thumbnail_width, cell_height - 34), Image.Resampling.LANCZOS
                )
            x = cell_x + (cell_width - page.width) // 2
            y = cell_y + 4
            canvas.paste(page, (x, y))
            draw.rectangle(
                (x - 1, y - 1, x + page.width, y + page.height),
                outline="#667085",
                width=1,
            )
            label = f"p. {_page_number(page_path)}"
            draw.text((cell_x + 6, cell_y + cell_height - 24), label, fill="#111827")

        output_path = output_directory / f"contact-sheet-{sheet_index:02d}.png"
        canvas.save(output_path, optimize=True)
        results.append(output_path)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_directory", type=Path)
    parser.add_argument("--output-directory", type=Path)
    parser.add_argument("--per-sheet", type=int, default=30)
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--thumbnail-width", type=int, default=180)
    args = parser.parse_args()
    sheets = create_contact_sheets(
        args.page_directory,
        args.output_directory,
        per_sheet=args.per_sheet,
        columns=args.columns,
        thumbnail_width=args.thumbnail_width,
    )
    for path in sheets:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
