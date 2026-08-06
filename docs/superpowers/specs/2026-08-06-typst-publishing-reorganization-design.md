# Typst Publishing Project Reorganization Design

**Date:** 2026-08-06

**Status:** Approved for written-spec review

## 1. Goal

Turn the current scattered Typst publishing workspace into a reproducible, product-oriented repository. The reorganization must preserve every existing file, identify the four canonical PDF deliverables, separate source files from build artifacts and reference material, and make the next book project straightforward to start.

The four canonical PDF deliverables are:

1. `카톡의정석.pdf` - basic edition
2. `카톡의정석_심화편.pdf` - advanced adult edition
3. `카톡의정석_요약본.pdf` - free summary edition
4. `CNA_NIGHT.pdf` - CNA NIGHT course book

## 2. Current Problems

- Project sources, reference PDFs, OCR outputs, generated PDFs, previews, and historical drafts are mixed at the repository root and under `output/`.
- The workspace is currently part of an uncommitted parent Git repository rooted at `C:/Users/SuperNatural1/Code`, rather than an independent repository.
- The documented outputs `output/카톡의정석.pdf` and `output/CNA_NIGHT.pdf` are absent from their promised locations.
- `main.typ` is stale and omits the later chapters `08b`, `08c`, `10b`, and `13b`.
- `scripts/md_to_typ.py` is also stale: it uses old titles and incomplete chapter manifests, so running it can overwrite newer `build.typ` files with incomplete content.
- `output/` mixes final deliverables, web and slide assets, third-party coaching material, preview renders, and archived build files.
- `gcp-key.json` contains a Google service-account private key and is stored beside public project sources.
- Five differently named PDFs are byte-for-byte identical, so several coaching-package filenames do not describe their actual content.

## 3. Design Principles

- Organize by product first, then by responsibility within each product.
- Keep one explicitly documented typesetting source of truth per deliverable.
- Never promote an unverified build into the distribution directory.
- Preserve historical material during migration; move it to `archive/` instead of deleting it.
- Keep secrets and machine-local state outside version control.
- Use ASCII directory names for scripting and cross-platform reliability; published filenames may remain Korean.
- Make the standard workflow discoverable through one command-line entry point and concise documentation.

## 4. Target Structure

```text
.
├── README.md
├── .gitignore
├── projects/
│   ├── katalk-standard/
│   │   ├── project.json
│   │   ├── typst/
│   │   │   ├── book.typ
│   │   │   ├── advanced.typ
│   │   │   └── summary.typ
│   │   ├── manuscript/
│   │   │   ├── basic/
│   │   │   └── advanced/
│   │   └── assets/
│   └── cna-night/
│       ├── project.json
│       ├── typst/
│       │   ├── book.typ
│       │   ├── theme.typ
│       │   ├── diagrams.typ
│       │   └── persona-vibe-export.typ
│       ├── manuscript/
│       └── assets/
├── templates/
│   ├── typst/
│   │   └── book.typ
│   └── project-starter/
├── scripts/
│   ├── project.py
│   ├── ocr/
│   └── legacy/
├── tests/
│   └── test_project_cli.py
├── dist/
│   ├── pdf/
│   ├── slides/
│   ├── handouts/
│   └── packages/
├── build/
│   ├── pdf/
│   ├── rendered/
│   └── previews/
├── references/
│   ├── pdf/
│   └── ocr/
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   ├── ARTIFACT_INVENTORY.md
│   ├── NEW_PROJECT_GUIDE.md
│   ├── research/
│   └── superpowers/
├── archive/
│   ├── legacy-build/
│   ├── legacy-output/
│   ├── drafts/
│   └── ai-runs/
└── local/
    └── secrets/
```

`build/`, `local/`, `.claude/worktrees/`, large reference PDFs, and historical archives are excluded from version control. `dist/` remains tracked or explicitly distributable so the canonical PDFs can be handed off without rebuilding.

## 5. Source-of-Truth Policy

### Katalk Standard

- `projects/katalk-standard/typst/book.typ` is the typesetting source for `카톡의정석.pdf`.
- `projects/katalk-standard/typst/advanced.typ` is the typesetting source for `카톡의정석_심화편.pdf`.
- `projects/katalk-standard/typst/summary.typ` is the typesetting source for `카톡의정석_요약본.pdf`.
- Existing Markdown chapters move to `manuscript/basic/` and `manuscript/advanced/` as editorial manuscripts. They are not silently regenerated into the Typst sources by the default build.
- The stale `main.typ` and `md_to_typ.py` move to `archive/legacy-build/` and `scripts/legacy/`. This prevents accidental loss of newer typesetting content.

### CNA NIGHT

- `projects/cna-night/typst/book.typ` remains the build entry point.
- CNA NIGHT continues to read its Markdown manuscript at build time through the existing theme and diagram renderer.
- Its theme, diagram definitions, and persona-vibe exporter stay product-local because they are not shared by the Katalk books.

## 6. Artifact Classification and Migration

| Category | Destination | Examples |
|---|---|---|
| Canonical PDF | `dist/pdf/` | The four approved PDFs |
| Slides and live-course media | `dist/slides/` | PPTX and slide HTML |
| Worksheets and pre-course material | `dist/handouts/` | Workbook and pre-task HTML/PDF |
| Distribution bundles | `dist/packages/` | Valid coaching packages |
| Temporary PDFs and rendered pages | `build/` | Preview PDFs, page PNGs, generated figures |
| External source material | `references/pdf/` | `(New)폰게임.pdf`, `카톡101.pdf`, `테레사_CONTACT.pdf`, FASTER SEX source |
| OCR derivatives | `references/ocr/` | OCR Markdown and JSON |
| Historical branded outputs | `archive/legacy-output/` | `답장의기술*.pdf` and backup HTML |
| Drafts and integration work | `archive/drafts/` | `drafts/` and `_workspace/` content |
| Analysis and planning | `docs/research/` | Existing `analysis/` and `briefs/` reports |
| Local secret | `local/secrets/` | `gcp-key.json` |

No existing file is deleted during migration. The five byte-identical, differently named coaching PDFs are retained under the archive and recorded as duplicate or incorrectly packaged artifacts.

## 7. Build and Promotion Flow

```text
project manifest + Typst source + manuscript/assets
                    |
                    v
             Typst compilation
                    |
                    v
             build/pdf/<file>.pdf
                    |
          structural and visual checks
                    |
        success ----+---- failure
           |                 |
           v                 v
    copy to dist/pdf/   keep old dist file
```

Rebuilding is an integration test, not an editorial rewrite. Moving source files changes relative import, image, and manuscript paths; a successful fresh build proves that the reorganized project is reproducible. Compilation happens in `build/pdf/`, and an existing canonical file is replaced only after verification succeeds.

## 8. Project Command-Line Interface

`scripts/project.py` uses the Python standard library and exposes these commands:

- `python scripts/project.py list` - list configured deliverables and their source/output paths.
- `python scripts/project.py build <id>` - build one configured deliverable into staging, verify it, and promote it.
- `python scripts/project.py build all` - build and verify all four canonical PDFs.
- `python scripts/project.py verify` - verify the configured canonical PDFs without compiling.
- `python scripts/project.py new <slug> --title <title>` - create a new product from `templates/project-starter/` without overwriting an existing directory.

Each product has a `project.json` manifest. It declares stable deliverable IDs, Typst entry points, output filenames, and whether the source is direct Typst or Markdown-driven Typst. The CLI rejects unknown IDs, missing source files, invalid manifests, and attempts to scaffold over an existing project.

## 9. New Project Starter

The starter contains:

- `project.json` with one sample deliverable.
- `typst/book.typ` importing the shared book template with a repository-root-safe path.
- `manuscript/01-introduction.md` with a minimal chapter structure.
- `assets/.gitkeep` for project-local images.
- `README.md` with the exact build, verify, and extension workflow.

`docs/NEW_PROJECT_GUIDE.md` explains naming, source-of-truth selection, asset placement, how to add another deliverable, and the release checklist. A new project is considered ready when it appears in `list`, compiles into `build/pdf/`, passes verification, and is promoted to its configured distribution path.

## 10. Secrets and Legacy OCR

- Move `gcp-key.json` to `local/secrets/gcp-key.json`.
- Add `local/` and private-key filename patterns to `.gitignore`.
- Update the Google OCR script to accept `GOOGLE_APPLICATION_CREDENTIALS` first and use the ignored local path only as a fallback.
- Never print, copy into documentation, or commit secret values.
- Group OCR scripts under `scripts/ocr/`; group one-time integration and conversion scripts under `scripts/legacy/`.

## 11. Verification Strategy

Automated tests cover manifest loading, path containment, command selection, missing-source failures, failed-build non-promotion, successful promotion, and safe new-project scaffolding. Tests use temporary directories and a fake Typst executable so they do not alter real outputs.

The release verification for each canonical PDF is:

1. Run Typst compilation and require exit code 0.
2. Reopen the staged PDF with a PDF parser.
3. Require at least one page and non-empty extracted text from representative pages.
4. Render every page to PNG under `build/rendered/<deliverable-id>/`.
5. Inspect contact sheets for all pages and full-resolution samples from the cover, early content, middle content, and final page.
6. Confirm no clipped text, overlap, missing glyphs, black boxes, blank pages, or broken images.
7. Promote only after all checks pass.

## 12. Git Boundary and Ignore Policy

Initialize an independent Git repository at the project root so this publishing project is no longer implicitly owned by the empty parent repository. The first commit records this approved design. The implementation commit follows after migration and verification.

The ignore policy excludes:

- `build/` and temporary render files
- `local/` and credential files
- `.claude/worktrees/` and other agent-local state
- Python cache files
- large third-party reference PDFs
- historical archive content that is preserved locally but not part of the maintainable source

## 13. Success Criteria

- The repository root contains project entry documentation rather than book chapters and loose PDFs.
- Every existing file is either in an active category or preserved under `archive/`.
- The four canonical deliverables build from the reorganized paths.
- Each canonical PDF passes structural and visual verification before entering `dist/pdf/`.
- The stale generator cannot overwrite current typesetting sources through the default workflow.
- The Google service-account key is outside tracked source paths.
- A new product can be scaffolded without hand-copying the current books.
- `README.md`, `PROJECT_STRUCTURE.md`, `ARTIFACT_INVENTORY.md`, and `NEW_PROJECT_GUIDE.md` describe the resulting repository accurately.
