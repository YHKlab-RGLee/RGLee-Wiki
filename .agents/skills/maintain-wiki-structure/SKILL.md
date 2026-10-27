---
name: maintain-wiki-structure
description: Maintain MkDocs navigation, page paths, titles, topic groups, indexes, and internal links in this scientific wiki. Use for adding, moving, renaming, reordering, or removing pages and navigation entries. Do not use for substantive scientific prose changes.
---

# Maintain Wiki Structure

Keep structural metadata separate from scientific content. Use the task-scoped context table in `AGENTS.md`, inspect affected navigation and links, and classify the requested change before editing. Do not load scientific research instructions for presentation work.

## Change classes

- Navigation-only: change labels or order in `mkdocs.yml`; do not touch `docs/`.
- Presentation: change H1, description, path, index link text, or internal links without changing scientific claims.
- Scientific: stop using this skill as the primary workflow and use the relevant writing or revision skill.

## Workflow

1. Preserve the three fixed scientific domains and their order. `Research Note`, when present, is a non-scientific support section after them.
2. Keep H1, index link text, and navigation labels number-free. List order is the only ordering source.
3. For page additions, moves, renames, or removals, update the affected nav entry and topic-group `index.md` in the same change. Keep index document lists title-only, without per-page summaries. For moves or renames, also update affected internal links and page-specific assets.
4. After confirming that title, description, order and links preserve scientific meaning, use `./quality.sh sync --non-scientific <paths>` for the completed docs changes. Pending or failed science cannot be carried forward. A changed claim in a heading or description still requires factual review.
5. For navigation-only work, run `./build.sh nav`. When a presentation file under `docs/` changed, synchronize once and run `./build.sh changed`. Then run `git diff --check` and inspect the final diff.

Do not rewrite scientific prose or refresh citations merely because a page moved or its display title changed.
