---
name: evaluate-wiki-quality
description: Synchronize, review, compare, and record the quality of Markdown pages in this MkDocs scientific wiki. Use whenever Codex creates, edits, moves, restores, or deletes a page under docs/, audits wiki quality, or decides whether a page is ready to publish.
---

# Evaluate Wiki Quality

Keep one current record per page in `refs/quality/documents.yaml`. Use `topic`, `scope`, current source text, body character count, and the combined number of figures, tables, display equations, and fenced code blocks to make a live comparison before the reading review.

Use a fast path only when no page under `docs/` changes. A navigation-order or navigation-label change edits `mkdocs.yml`, runs `./build.sh build`, and stops; it does not synchronize quality records or invalidate article reviews. Once a Markdown page changes, follow the full workflow below.

Apply quantitative comparison and checklist review only to `kind: article`. Keep `home` and `index` synchronized and automatically checked, but record them as `excluded`; do not choose comparison pages or submit an assessment for them. An article without a current checklist review is `pending`, never an implicit pass.

## Required context

Read `refs/quality/README.md`, `refs/quality/rubric.yaml`, and every changed page. For a scientific article, also follow `AGENTS.md`, `refs/format.md`, and `refs/research-workflow.md`.

## Workflow

1. Before editing `docs/`, synchronize once to establish the current state.

   ```bash
   ./quality.sh sync
   ```

2. After creating, editing, moving, restoring, or deleting any Markdown page under `docs/`, synchronize again. This updates that page's topic, scope, body character count, explanatory-element count, and automatic checks, invalidates the review of changed content, archives deleted records, and restores current-system history when a path returns.

3. For every added, modified, moved, or restored article, read the complete page. Use `topic`, `scope`, and current source text to choose at least two scientifically relevant articles. Select by semantic subject, explanatory range, and document role. For `home` and `index`, confirm only synchronization and automatic checks.

4. Read the selected documents' current source text and metrics. The target must reach at least 80% of their average body character count and at least 80% of their average total explanatory-element count. Figures, tables, display equations, and fenced code blocks contribute to one combined count so their proportions can follow the subject. If the target falls short, add material that performs a real explanatory role for its topic, synchronize, and compare again.

5. Before scoring, list every H1–H3 heading in reading order and check it against `refs/format.md`: Korean-first wording, short noun-phrase form, consistent conceptual level among siblings, and a hierarchy that exposes the article's logic. Confirm that the research workflow already inspected the supporting passages and claim ledger. Use `refs/quality/assessment-template.yaml` to record every applicable A–C criterion as `rating: 0|1|2` with concrete evidence, document locations, and a Korean reason. Do not invent a final score; the script calculates it from `refs/quality/rubric.yaml`.

6. Evaluate D1–D6 as non-scored compliance gates. Run the strict build before marking D6 pass. Record every applicable F1–F5 forced-revise condition, and answer all three critical questions: dependency chain, first likely reader blocker, and strongest case for revision. A D failure, forced-revise rule, or zero on a critical criterion produces `revise` regardless of total points.

7. Pass the assessment file and every selected comparison page to the review command. The command checks the quantitative threshold, validates that every required checklist item has evidence, calculates A–C points, and records `pass` or `revise`:

   ```bash
   ./quality.sh review docs/path/page.md \
     --reference docs/path/related-a.md \
     --reference docs/path/related-b.md \
     --assessment /tmp/page-assessment.yaml
   ```

8. If the result is `revise`, fix the named weakness and run the review again. The review command synchronizes first, so every revision is measured before it is scored. Preserve every failed attempt in history. Repeat at most three times; then report that human review is needed.

9. Confirm each changed page after recording the review:

   ```bash
   ./quality.sh check docs/path/page.md
   ```

For a deletion-only change, run `./quality.sh sync`; the deleted record must appear under `archived_documents`. Review any index or navigation page changed because of the deletion.

## Whole-wiki audit

Every quality command synchronizes first. Use:

```bash
./quality.sh report
./quality.sh check --all
```

An article remains `pending` until it receives a complete checklist review. Any content change clears that review and requires a new `pass` review.

## Review integrity

- Choose comparison pages at review time; do not store a fixed peer set or comparison result in the registry.
- Interpret whether every added figure, table, equation, code block, or passage improves understanding of the target topic.
- Never assign an impressionistic decimal score. Submit only atomic 0/1/2 ratings with evidence; let the script compute the result.
- Treat D compliance as a publication gate, never as points that can offset weak logic, evidence, or explanation.
- Store reviews through `quality.sh review` so earlier evaluations made under the current criteria remain in `history`.
- Never mark `pass` manually; let the script apply `refs/quality/rubric.yaml`.
- Do not finish a workflow that changed `docs/` until synchronization and required reviews are recorded.
