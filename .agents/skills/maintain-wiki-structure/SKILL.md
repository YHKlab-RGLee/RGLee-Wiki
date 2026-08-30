---
name: maintain-wiki-structure
description: Maintain MkDocs navigation, page paths, titles, topic groups, indexes, and internal links in this scientific wiki. Use for adding, moving, renaming, reordering, or removing pages and navigation entries. Do not use for substantive scientific prose changes.
---

# Maintain Wiki Structure

Keep structural metadata separate from scientific content. Read `AGENTS.md`, inspect `mkdocs.yml`, and classify the requested change before editing.

## Change classes

- Navigation-only: change labels or order in `mkdocs.yml`; do not touch `docs/`.
- Presentation: change H1, description, path, index link text, or internal links without changing scientific claims.
- Scientific: stop using this skill as the primary workflow and use the relevant writing or revision skill.

## Workflow

1. Preserve the three fixed scientific domains and their order. `Research Note`, when present, is a non-scientific support section after them.
2. Keep H1, index link text, and navigation labels number-free. List order is the only ordering source.
3. For moves or renames, update only the affected nav entry, index links, internal links, and page-specific assets.
4. Run `./quality.sh sync` only when a file under `docs/` changed. It must preserve article review state for presentation-only changes.
5. For navigation-only work, run `./build.sh nav`. When a presentation file under `docs/` changed, synchronize once and run `./build.sh changed`. Then run `git diff --check` and inspect the final diff.

Do not rewrite scientific prose or refresh citations merely because a page moved or its display title changed.
