---
name: evaluate-wiki-quality
description: Synchronize, review, compare, and record the quality of Markdown pages in this MkDocs scientific wiki. Use whenever Codex creates, edits, moves, restores, or deletes a page under docs/, audits wiki quality, or decides whether a page is ready to publish.
---

# Evaluate Wiki Quality

Keep one current record per page in `refs/quality/documents.yaml`. Use `topic`, `scope`, current source text, body character count, and the combined number of figures, tables, display equations, and fenced code blocks to make a live comparison before the reading review.

## Required context

Read `refs/quality/README.md`, `refs/quality/rubric.yaml`, and every changed page. For a scientific article, also follow `AGENTS.md`, `refs/format.md`, and `refs/research-workflow.md`.

## Workflow

1. Before editing `docs/`, synchronize once to establish the current state.

   ```bash
   ./quality.sh sync
   ```

2. After creating, editing, moving, restoring, or deleting any Markdown page under `docs/`, synchronize again. This updates that page's topic, scope, body character count, explanatory-element count, and automatic checks, invalidates the review of changed content, archives deleted records, and restores prior history when a path returns.

3. For every added, modified, moved, or restored page, read the complete page. Use `topic`, `scope`, and current source text to choose at least two scientifically relevant documents of the same `kind`. Select by semantic subject, explanatory range, and document role.

4. Read the selected documents' current source text and metrics. The target must reach at least 80% of their average body character count and at least 80% of their average total explanatory-element count. Figures, tables, display equations, and fenced code blocks contribute to one combined count so their proportions can follow the subject. If the target falls short, add material that performs a real explanatory role for its topic, synchronize, and compare again.

5. Before scoring, list every H1–H3 heading in reading order and check it against `refs/format.md`: Korean-first wording, short noun-phrase form, consistent conceptual level among siblings, and a hierarchy that exposes the article's logic. Then score `content`, `evidence`, `explanation`, and `format` from 0 to 10 using `refs/quality/rubric.yaml`. Confirm that the research workflow already inspected the supporting passages and claim ledger. Write one concise Korean summary about the target page itself. Pass every selected comparison page to the review command; the command checks the quantitative threshold before recording the scores:

   ```bash
   ./quality.sh review docs/path/page.md \
     --reference docs/path/related-a.md \
     --reference docs/path/related-b.md \
     --content 8.4 --evidence 8.2 --explanation 8.1 --format 8.6 \
     --summary "핵심 설명은 완결되며 정량 비교 조건을 조금 더 분명히 할 수 있다."
   ```

6. If the result is `revise`, fix the named weakness and run the review again. The review command synchronizes first, so every revision is measured before it is scored. Repeat at most three times; then report that human review is needed.

7. Confirm each changed page, then build:

   ```bash
   ./quality.sh check docs/path/page.md
   ./build.sh build
   ```

For a deletion-only change, run `./quality.sh sync`; the deleted record must appear under `archived_documents`. Review any index or navigation page changed because of the deletion.

## Whole-wiki audit

Every quality command synchronizes first. Use:

```bash
./quality.sh report
./quality.sh check --all --allow-baseline
```

Treat an existing `baseline` as a migration state, not a permanent exemption. Baseline creation is closed. Any content change clears that review and requires a new `pass` review.

## Review integrity

- Choose comparison pages at review time; do not store a fixed peer set or comparison result in the registry.
- Interpret whether every added figure, table, equation, code block, or passage improves understanding of the target topic.
- Store reviews through `quality.sh review` so prior evaluations remain in `history`.
- Never mark `pass` manually; let the script apply `refs/quality/rubric.yaml`.
- Do not finish a workflow that changed `docs/` until synchronization and required reviews are recorded.
